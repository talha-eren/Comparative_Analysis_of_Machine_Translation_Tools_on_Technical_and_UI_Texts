#!/usr/bin/env python3
"""
MaCoCu TR-EN Korpus İndirme ve Filtreleme Scripti

Bu script MaCoCu Türkçe-İngilizce korpusunu indirir ve
teknik/yazılım içeriklerini filtreler.

Kullanım:
    python scripts/download_macocu.py
"""

import os
import sys
import json
import re
import requests
from pathlib import Path
from tqdm import tqdm

# Proje kök dizini
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw" / "macocu"

# MaCoCu dataset URL'leri
MACOCU_URLS = {
    "sentence_txt": "https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1816/MaCoCu-tr-en.sent.txt.gz",
    "sentence_tmx": "https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1816/MaCoCu-tr-en.sent.tmx.gz"
}

# Teknik/yazılım terimleri (filtreleme için)
TECHNICAL_KEYWORDS = [
    # Programlama
    'software', 'program', 'code', 'function', 'variable', 'algorithm',
    'debug', 'compile', 'execute', 'runtime', 'syntax', 'library',
    
    # Web/Mobil
    'website', 'application', 'app', 'interface', 'browser', 'server',
    'client', 'database', 'api', 'endpoint', 'request', 'response',
    
    # Teknoloji
    'computer', 'system', 'network', 'internet', 'data', 'file',
    'download', 'upload', 'install', 'configuration', 'settings',
    
    # Yazılım Geliştirme
    'developer', 'development', 'framework', 'platform', 'version',
    'update', 'upgrade', 'release', 'deployment', 'repository',
    
    # UI/UX
    'button', 'menu', 'click', 'select', 'input', 'output',
    'display', 'screen', 'window', 'dialog', 'notification',
    
    # Veri/Güvenlik
    'password', 'username', 'login', 'logout', 'authentication',
    'authorization', 'encryption', 'security', 'privacy',
    
    # Türkçe teknik terimler
    'yazılım', 'program', 'uygulama', 'sistem', 'veri', 'dosya',
    'indirme', 'yükleme', 'kurulum', 'ayarlar', 'güncelleme'
]

def download_file(url, output_path):
    """
    Dosyayı indir (progress bar ile)
    
    Args:
        url: İndirme URL'i
        output_path: Çıktı dosya yolu
    """
    print(f"\nİndiriliyor: {url}")
    print(f"Hedef: {output_path}")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as f, tqdm(
            desc=output_path.name,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
        
        print(f"✓ İndirme tamamlandı: {output_path.stat().st_size / 1024 / 1024:.1f} MB")
        return True
        
    except Exception as e:
        print(f"✗ İndirme hatası: {e}")
        return False

def extract_gz(gz_file, output_file):
    """
    .gz dosyasını çıkar
    
    Args:
        gz_file: Sıkıştırılmış dosya
        output_file: Çıktı dosyası
    """
    import gzip
    
    print(f"\nÇıkarılıyor: {gz_file}")
    
    try:
        with gzip.open(gz_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                f_out.write(f_in.read())
        
        print(f"✓ Çıkarma tamamlandı: {output_file.stat().st_size / 1024 / 1024:.1f} MB")
        return True
        
    except Exception as e:
        print(f"✗ Çıkarma hatası: {e}")
        return False

def is_technical_text(text):
    """
    Metnin teknik içerik içerip içermediğini kontrol et
    
    Args:
        text: Kontrol edilecek metin
    
    Returns:
        Boolean
    """
    text_lower = text.lower()
    
    # En az 2 teknik terim içermeli
    keyword_count = sum(1 for keyword in TECHNICAL_KEYWORDS if keyword in text_lower)
    
    return keyword_count >= 2

def filter_technical_content(input_file, output_file, max_segments=10000):
    """
    Korpustan teknik içerikleri filtrele
    
    Args:
        input_file: Giriş dosyası (TXT format)
        output_file: Çıkış dosyası (JSON)
        max_segments: Maksimum segment sayısı
    """
    print(f"\nFiltreleniyor: {input_file}")
    print(f"Hedef: {max_segments} teknik segment")
    
    segments = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"Toplam satır: {len(lines)}")
        
        for idx, line in enumerate(tqdm(lines, desc="Filtreleme"), 1):
            if len(segments) >= max_segments:
                break
            
            line = line.strip()
            if not line:
                continue
            
            # İlk satır başlık satırı ise atla
            if idx == 1 and ('src_text' in line or 'source' in line):
                continue
            
            # Format: source_text \t target_text \t score
            parts = line.split('\t')
            
            if len(parts) >= 2:
                source_text = parts[0].strip()
                target_text = parts[1].strip()
                
                # Kalite skoru varsa al
                try:
                    quality_score = float(parts[2]) if len(parts) >= 3 else 1.0
                except (ValueError, IndexError):
                    quality_score = 1.0
                
                # Filtreleme kriterleri
                if (source_text and target_text and 
                    len(source_text) > 10 and len(source_text) < 500 and
                    quality_score > 0.8 and
                    is_technical_text(source_text)):
                    
                    segment = {
                        "id": f"macocu_{idx:06d}",
                        "source_text": source_text,
                        "target_text": target_text,
                        "category": "technical",
                        "subcategory": "general_technical",
                        "source_lang": "en",
                        "target_lang": "tr",
                        "length": len(source_text),
                        "source": "macocu",
                        "metadata": {
                            "quality_score": quality_score,
                            "has_placeholder": any(c in source_text for c in ['%', '{', '}', '<', '>']),
                            "word_count": len(source_text.split())
                        }
                    }
                    segments.append(segment)
        
        # JSON'a kaydet
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(segments, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ {len(segments)} teknik segment filtrelendi")
        print(f"✓ Kaydedildi: {output_file}")
        
        # İstatistikler
        print(f"\nİstatistikler:")
        print(f"  - Toplam segment: {len(segments)}")
        print(f"  - Ortalama uzunluk: {sum(s['length'] for s in segments) / len(segments):.1f} karakter")
        print(f"  - Ortalama kalite: {sum(s['metadata']['quality_score'] for s in segments) / len(segments):.3f}")
        print(f"  - Placeholder içeren: {sum(1 for s in segments if s['metadata']['has_placeholder'])}")
        
        return True
        
    except Exception as e:
        print(f"✗ Filtreleme hatası: {e}")
        return False

def main():
    """Ana fonksiyon"""
    print("="*60)
    print("MaCoCu TR-EN Korpus İndirme ve Filtreleme")
    print("="*60)
    
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    # Not: MaCoCu dataset'i çok büyük (1.6M segment, ~2GB)
    # Manuel indirme öneriliyor
    
    print("\n⚠ MaCoCu dataset'i çok büyük (1.6M segment, ~2GB)")
    print("\nManuel indirme önerilir:")
    print("  1. Şu linke gidin: https://www.clarin.si/repository/xmlui/handle/11356/1816")
    print("  2. 'MaCoCu-tr-en.sent.txt.gz' dosyasını indirin")
    print(f"  3. {DATA_RAW_DIR} klasörüne koyun")
    print("  4. Bu scripti tekrar çalıştırın")
    
    # Dosya var mı kontrol et
    gz_file = DATA_RAW_DIR / "MaCoCu-tr-en.sent.txt.gz"
    txt_file = DATA_RAW_DIR / "MaCoCu-tr-en.sent.txt"
    json_file = DATA_RAW_DIR / "macocu_technical.json"
    
    if json_file.exists():
        print(f"\n✓ Filtrelenmiş dataset zaten mevcut: {json_file}")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            segments = json.load(f)
        print(f"  - {len(segments)} segment")
        return
    
    if gz_file.exists():
        print(f"\n✓ Sıkıştırılmış dosya bulundu: {gz_file}")
        
        if not txt_file.exists():
            extract_gz(gz_file, txt_file)
        
        if txt_file.exists():
            filter_technical_content(txt_file, json_file, max_segments=10000)
        
    elif txt_file.exists():
        print(f"\n✓ TXT dosya bulundu: {txt_file}")
        filter_technical_content(txt_file, json_file, max_segments=10000)
        
    else:
        print("\n✗ MaCoCu dataset dosyası bulunamadı")
        print("\nOtomatik indirme denemesi...")
        
        # Otomatik indirme dene (uzun sürebilir)
        if download_file(MACOCU_URLS["sentence_txt"], gz_file):
            extract_gz(gz_file, txt_file)
            filter_technical_content(txt_file, json_file, max_segments=10000)
        else:
            print("\n✗ Otomatik indirme başarısız")
            print("Lütfen manuel olarak indirin")

if __name__ == "__main__":
    main()

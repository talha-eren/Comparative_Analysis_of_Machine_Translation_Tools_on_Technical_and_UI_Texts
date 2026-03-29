#!/usr/bin/env python3
"""
OPUS Dataset İndirme Scripti

Bu script OPUS korpusundan GNOME, KDE ve Mozilla-I10n dataset'lerini
İngilizce-Türkçe dil çifti için indirir.

Kullanım:
    python scripts/download_opus.py
"""

import os
import sys
import json
from pathlib import Path
from tqdm import tqdm
import subprocess

# Proje kök dizinini bul
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"

# OPUS dataset'leri
OPUS_DATASETS = [
    {
        "name": "GNOME",
        "description": "GNOME masaüstü dokümantasyonu",
        "category": "technical",
        "url": "https://opus.nlpl.eu/GNOME.php"
    },
    {
        "name": "KDE4",
        "description": "KDE sistem mesajları ve dokümantasyon",
        "category": "technical",
        "url": "https://opus.nlpl.eu/KDE4.php"
    },
    {
        "name": "Mozilla",
        "description": "Mozilla Firefox UI string'leri",
        "category": "ui",
        "url": "https://opus.nlpl.eu/Mozilla.php"
    }
]

def check_opustools_installed():
    """OpusTools'un kurulu olup olmadığını kontrol et"""
    try:
        result = subprocess.run(['opus_read', '--help'], 
                              capture_output=True, 
                              text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_opustools():
    """OpusTools'u kur"""
    print("OpusTools kurulu değil. Kuruluyor...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'opustools'], 
                      check=True)
        print("✓ OpusTools başarıyla kuruldu")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ OpusTools kurulumu başarısız: {e}")
        return False

def download_opus_corpus(corpus_name, source_lang='en', target_lang='tr', max_sentences=10000):
    """
    OPUS korpusundan veri indir
    
    Args:
        corpus_name: Korpus adı (GNOME, KDE4, Mozilla)
        source_lang: Kaynak dil kodu
        target_lang: Hedef dil kodu
        max_sentences: Maksimum cümle sayısı
    """
    output_dir = DATA_RAW_DIR / corpus_name.lower()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{corpus_name.lower()}_en_tr.txt"
    
    print(f"\n{'='*60}")
    print(f"İndiriliyor: {corpus_name}")
    print(f"Dil çifti: {source_lang} → {target_lang}")
    print(f"Çıktı: {output_file}")
    print(f"{'='*60}\n")
    
    try:
        # opus_read komutu ile indir
        cmd = [
            'opus_read',
            '-d', corpus_name,
            '-s', source_lang,
            '-t', target_lang,
            '-w', str(output_file),
            '-wm', 'moses',
            '-ln', str(max_sentences)
        ]
        
        print(f"Komut: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True,
                              timeout=600)
        
        if result.returncode == 0:
            print(f"✓ {corpus_name} başarıyla indirildi")
            
            # İndirilen dosyayı JSON formatına dönüştür
            convert_moses_to_json(output_file, corpus_name)
            
            return True
        else:
            print(f"✗ {corpus_name} indirme hatası:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ {corpus_name} indirme zaman aşımı (10 dakika)")
        return False
    except Exception as e:
        print(f"✗ {corpus_name} indirme hatası: {e}")
        return False

def convert_moses_to_json(moses_file, corpus_name):
    """
    Moses formatındaki dosyayı JSON formatına dönüştür
    
    Moses format: Her satırda kaynak ve hedef metin tab ile ayrılmış
    """
    json_file = moses_file.parent / f"{corpus_name.lower()}_en_tr.json"
    
    print(f"JSON'a dönüştürülüyor: {json_file}")
    
    try:
        segments = []
        
        if not moses_file.exists():
            print(f"✗ Dosya bulunamadı: {moses_file}")
            return
        
        with open(moses_file, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('\t')
                if len(parts) >= 2:
                    source_text = parts[0].strip()
                    target_text = parts[1].strip()
                    
                    if source_text and target_text:
                        segment = {
                            "id": f"{corpus_name.lower()}_{idx:06d}",
                            "source_text": source_text,
                            "target_text": target_text,
                            "category": "technical" if corpus_name in ["GNOME", "KDE4"] else "ui",
                            "subcategory": "documentation" if corpus_name in ["GNOME", "KDE4"] else "ui_string",
                            "source_lang": "en",
                            "target_lang": "tr",
                            "length": len(source_text),
                            "source": corpus_name.lower(),
                            "metadata": {
                                "corpus": corpus_name,
                                "has_placeholder": any(c in source_text for c in ['%', '{', '}', '<', '>']),
                                "word_count": len(source_text.split())
                            }
                        }
                        segments.append(segment)
        
        # JSON dosyasına yaz
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(segments, f, ensure_ascii=False, indent=2)
        
        print(f"✓ {len(segments)} segment JSON'a dönüştürüldü")
        
        # İstatistikleri göster
        print(f"\nİstatistikler:")
        print(f"  - Toplam segment: {len(segments)}")
        print(f"  - Ortalama uzunluk: {sum(s['length'] for s in segments) / len(segments):.1f} karakter")
        print(f"  - Placeholder içeren: {sum(1 for s in segments if s['metadata']['has_placeholder'])}")
        
    except Exception as e:
        print(f"✗ JSON dönüşüm hatası: {e}")

def main():
    """Ana fonksiyon"""
    print("="*60)
    print("OPUS Dataset İndirme Scripti")
    print("="*60)
    
    # OpusTools kontrolü
    if not check_opustools_installed():
        print("\n[!] OpusTools kurulu degil!")
        if not install_opustools():
            print("\n[X] OpusTools kurulamadi. Lutfen manuel olarak kurun:")
            print("  pip install opustools")
            sys.exit(1)
    else:
        print("[OK] OpusTools kurulu\n")
    
    # Data dizinini oluştur
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    # Her korpusu indir
    results = {}
    for dataset in OPUS_DATASETS:
        success = download_opus_corpus(
            corpus_name=dataset["name"],
            source_lang='en',
            target_lang='tr',
            max_sentences=10000
        )
        results[dataset["name"]] = success
    
    # Özet
    print("\n" + "="*60)
    print("İndirme Özeti")
    print("="*60)
    
    for corpus_name, success in results.items():
        status = "✓ Başarılı" if success else "✗ Başarısız"
        print(f"{corpus_name}: {status}")
    
    successful = sum(1 for s in results.values() if s)
    print(f"\nToplam: {successful}/{len(results)} dataset başarıyla indirildi")
    
    if successful > 0:
        print(f"\nİndirilen dosyalar: {DATA_RAW_DIR}")
        print("\nSonraki adım:")
        print("  python scripts/process_datasets.py")

if __name__ == "__main__":
    main()

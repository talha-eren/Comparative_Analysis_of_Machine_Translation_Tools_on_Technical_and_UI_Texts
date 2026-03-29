#!/usr/bin/env python3
"""
OPUS Dataset Alternatif Indirme Scripti

OPUS API kullanarak dataset'leri indirir.
"""

import os
import sys
import json
import requests
from pathlib import Path
from tqdm import tqdm
import gzip
import io

# Proje kök dizinini bul
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"

# OPUS API endpoint'leri
OPUS_API = "https://opus.nlpl.eu/opusapi/"

# Dataset konfigürasyonu
DATASETS = {
    "GNOME": {
        "corpus": "GNOME",
        "version": "v1",
        "src": "en",
        "trg": "tr",
        "max_segments": 5000
    },
    "KDE4": {
        "corpus": "KDE4",
        "version": "v2",
        "src": "en",
        "trg": "tr",
        "max_segments": 5000
    },
    "Mozilla": {
        "corpus": "Mozilla-I10n",
        "version": "v1",
        "src": "en",
        "trg": "tr",
        "max_segments": 5000
    }
}

def download_opus_corpus(corpus_name, config):
    """
    OPUS API kullanarak korpus indir
    """
    output_dir = DATA_RAW_DIR / corpus_name.lower()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{corpus_name.lower()}_en_tr.json"
    
    print(f"\n{'='*60}")
    print(f"Indiriliyor: {corpus_name}")
    print(f"Dil cifti: {config['src']} -> {config['trg']}")
    print(f"Cikti: {output_file}")
    print(f"{'='*60}\n")
    
    try:
        # OPUS API'den download URL'i al
        api_url = f"{OPUS_API}?corpus={config['corpus']}&source={config['src']}&target={config['trg']}&version={config['version']}&preprocessing=moses"
        
        print(f"API sorgusu: {api_url}")
        
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Download URL'i bul
        if 'corpora' not in data or len(data['corpora']) == 0:
            print(f"[X] {corpus_name} icin veri bulunamadi")
            return False
        
        corpus_info = data['corpora'][0]
        
        # Moses format dosyasını indir
        if 'url' in corpus_info:
            download_url = corpus_info['url']
        else:
            print(f"[X] {corpus_name} icin download URL bulunamadi")
            return False
        
        print(f"Indiriliyor: {download_url}")
        
        # Dosyayi indir
        download_response = requests.get(download_url, stream=True, timeout=120)
        download_response.raise_for_status()
        
        total_size = int(download_response.headers.get('content-length', 0))
        
        # Gzip formatinda indir ve coz
        content = b""
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Indirme") as pbar:
            for chunk in download_response.iter_content(chunk_size=8192):
                if chunk:
                    content += chunk
                    pbar.update(len(chunk))
        
        # Gzip coz
        print("Dosya cozuluyor...")
        try:
            decompressed = gzip.decompress(content)
            text_content = decompressed.decode('utf-8')
        except:
            # Gzip degil, direkt text
            text_content = content.decode('utf-8')
        
        # Moses formatini JSON'a cevir
        segments = convert_moses_to_json(text_content, corpus_name, config['max_segments'])
        
        # JSON olarak kaydet
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(segments, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] {len(segments)} segment kaydedildi: {output_file}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"[X] {corpus_name} indirme hatasi: {e}")
        return False
    except Exception as e:
        print(f"[X] {corpus_name} beklenmeyen hata: {e}")
        return False

def convert_moses_to_json(text_content, corpus_name, max_segments):
    """
    Moses formatindaki metni JSON'a cevir
    """
    segments = []
    lines = text_content.strip().split('\n')
    
    # Moses format: source ve target ayri satirlarda
    # Veya tab-separated format
    
    for idx, line in enumerate(lines[:max_segments * 2]):  # Her segment 2 satir
        line = line.strip()
        if not line:
            continue
        
        # Tab-separated format
        if '\t' in line:
            parts = line.split('\t')
            if len(parts) >= 2:
                source_text = parts[0].strip()
                target_text = parts[1].strip()
                
                if source_text and target_text:
                    # Kategori belirle
                    category = determine_category(source_text)
                    
                    segment = {
                        "id": f"{corpus_name.lower()}_{len(segments)+1:06d}",
                        "source_text": source_text,
                        "target_text": target_text,
                        "category": category,
                        "subcategory": "ui_strings",
                        "source_lang": "en",
                        "target_lang": "tr",
                        "source": corpus_name,
                        "metadata": {
                            "length": len(source_text),
                            "has_placeholders": has_placeholders(source_text)
                        }
                    }
                    segments.append(segment)
                    
                    if len(segments) >= max_segments:
                        break
    
    return segments

def determine_category(text):
    """
    Metin kategorisini belirle
    """
    text_lower = text.lower()
    
    # Error mesajlari
    error_keywords = ['error', 'exception', 'failed', 'warning', 'invalid', 'cannot', 'unable']
    if any(keyword in text_lower for keyword in error_keywords):
        return 'error'
    
    # UI strings (kisa, basit)
    if len(text) < 50 and any(char in text for char in [':', '...', '_']):
        return 'ui'
    
    # Teknik dokümantasyon (uzun, aciklayici)
    return 'technical'

def has_placeholders(text):
    """
    Metinde placeholder var mi kontrol et
    """
    placeholder_patterns = ['%s', '%d', '{', '}', '<', '>', '$', '{{', '}}']
    return any(pattern in text for pattern in placeholder_patterns)

def main():
    print("="*60)
    print("OPUS Dataset Indirme Scripti (Alternatif)")
    print("="*60)
    
    # Dizinleri olustur
    for dataset_name in DATASETS.keys():
        output_dir = DATA_RAW_DIR / dataset_name.lower()
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Her dataset'i indir
    results = {}
    for dataset_name, config in DATASETS.items():
        success = download_opus_corpus(dataset_name, config)
        results[dataset_name] = success
    
    # Ozet
    print("\n" + "="*60)
    print("Indirme Ozeti")
    print("="*60)
    
    for dataset_name, success in results.items():
        status = "[OK] Basarili" if success else "[X] Basarisiz"
        print(f"{dataset_name}: {status}")
    
    successful = sum(1 for s in results.values() if s)
    print(f"\nToplam: {successful}/{len(results)} dataset basariyla indirildi")
    
    if successful == 0:
        print("\n[!] Hicbir dataset indirilemedi!")
        print("Manuel indirme icin: https://opus.nlpl.eu/")
        sys.exit(1)

if __name__ == "__main__":
    main()

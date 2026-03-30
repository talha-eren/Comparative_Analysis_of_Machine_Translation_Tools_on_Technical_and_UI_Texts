#!/usr/bin/env python3
"""
Dataset İşleme ve Birleştirme Scripti

Bu script tüm indirilen dataset'leri birleştirir, temizler ve
train/test split yapar.

Kullanım:
    python scripts/process_datasets.py
"""

import os
import sys
import json
import random
import csv
import re
from pathlib import Path
from collections import Counter
import pandas as pd

# Proje kök dizini
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def clean_text(text):
    """Metni normalize et"""
    if text is None:
        return ""
    text = str(text).strip()
    text = " ".join(text.split())
    return text


def has_placeholder(text):
    """UI tarzı placeholder pattern'lerini tespit et"""
    patterns = [
        r"\b\d+[A-Za-z]\b",       # 1S, 2d
        r"\{[^}]+\}",             # {name}
        r"%[sd]",                   # %s, %d
        r"\bname\b",              # name
        r"\buri\b",               # uri
    ]
    t = (text or "").lower()
    return any(re.search(p, t) for p in patterns)


def categorize_en_saf_text(source_text):
    """en_saf string'lerini ui/error olarak ayir"""
    t = (source_text or "").lower()
    error_markers = [
        "error", "warning", "failed", "cannot", "can't", "not found",
        "unsupported", "denied", "invalid", "blocked", "disabled",
    ]
    if any(marker in t for marker in error_markers):
        return "error", "error_strings"
    return "ui", "ui_strings"


def load_semicolon_csv(file_path):
    """Noktalı virgül ayrımlı CSV yükle"""
    rows = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                normalized = {}
                for key, value in row.items():
                    clean_key = (key or "").strip().lstrip("\ufeff")
                    normalized[clean_key] = value
                rows.append(normalized)
        print(f"✓ {file_path.name}: {len(rows)} satır")
    except Exception as e:
        print(f"✗ {file_path.name} yüklenemedi: {e}")
    return rows


def build_segments_from_en_saf(rows):
    """en_saf_kelimeler.csv -> proje segment şeması"""
    segments = []
    for idx, row in enumerate(rows, 1):
        source = clean_text(row.get("source_string", ""))
        target = clean_text(row.get("target_string", ""))
        if not source or not target:
            continue

        category, subcategory = categorize_en_saf_text(source)
        segments.append({
            "id": f"ensaf_{idx:06d}",
            "source_text": source,
            "target_text": target,
            "category": category,
            "subcategory": subcategory,
            "source_lang": "en",
            "target_lang": "tr",
            "source": "en_saf",
            "metadata": {
                "length": len(source),
                "has_placeholders": has_placeholder(source),
                "word_count": len(source.split()),
            },
            "length": len(source),
        })
    print(f"✓ en_saf segment'e dönüştürüldü: {len(segments)}")
    return segments


def build_segments_from_ms_terms(rows):
    """microsoft_terms_en_tr.csv -> proje segment şeması"""
    segments = []
    for idx, row in enumerate(rows, 1):
        source = clean_text(row.get("English_Term", ""))
        target = clean_text(row.get("Turkish_Term", ""))
        definition = clean_text(row.get("Definition", ""))
        if not source or not target:
            continue

        segments.append({
            "id": f"mterms_{idx:06d}",
            "source_text": source,
            "target_text": target,
            "category": "technical",
            "subcategory": "terminology",
            "source_lang": "en",
            "target_lang": "tr",
            "source": "microsoft_terms",
            "metadata": {
                "length": len(source),
                "has_placeholders": has_placeholder(source),
                "word_count": len(source.split()),
                "has_definition": bool(definition),
            },
            "length": len(source),
        })
    print(f"✓ microsoft terms segment'e dönüştürüldü: {len(segments)}")
    return segments


def build_terminology_glossary(rows):
    """English_Term -> en sık Turkish_Term map'i üret"""
    term_counts = {}
    for row in rows:
        en = clean_text(row.get("English_Term", "")).lower()
        tr = clean_text(row.get("Turkish_Term", ""))
        if not en or not tr:
            continue
        term_counts.setdefault(en, Counter())
        term_counts[en][tr] += 1

    glossary = {}
    for en, tr_counter in term_counts.items():
        glossary[en] = tr_counter.most_common(1)[0][0]
    return glossary

def load_json_dataset(file_path):
    """JSON dataset'i yükle"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ {file_path.name}: {len(data)} segment")
        return data
    except Exception as e:
        print(f"✗ {file_path.name} yüklenemedi: {e}")
        return []

def collect_all_datasets():
    """Tüm dataset'leri topla"""
    print("="*60)
    print("Dataset'ler Toplanıyor")
    print("="*60)
    
    all_segments = []
    
    # OPUS dataset'leri
    opus_datasets = [
        DATA_RAW_DIR / "gnome" / "gnome_en_tr.json",
        DATA_RAW_DIR / "kde4" / "kde4_en_tr.json",
        DATA_RAW_DIR / "mozilla" / "mozilla_en_tr.json"
    ]
    
    for dataset_path in opus_datasets:
        if dataset_path.exists():
            segments = load_json_dataset(dataset_path)
            all_segments.extend(segments)
    
    # GitHub dataset
    github_path = DATA_RAW_DIR / "github" / "github_i18n.json"
    if github_path.exists():
        segments = load_json_dataset(github_path)
        all_segments.extend(segments)
    
    # MaCoCu dataset
    macocu_path = DATA_RAW_DIR / "macocu" / "macocu_technical.json"
    if macocu_path.exists():
        segments = load_json_dataset(macocu_path)
        all_segments.extend(segments)

    # Kullanıcıdan gelen ek CSV dataset'leri (opsiyonel)
    en_saf_path = PROJECT_ROOT / "en_saf_kelimeler.csv"
    if en_saf_path.exists():
        rows = load_semicolon_csv(en_saf_path)
        all_segments.extend(build_segments_from_en_saf(rows))

    ms_terms_path = PROJECT_ROOT / "microsoft_terms_en_tr.csv"
    if ms_terms_path.exists():
        rows = load_semicolon_csv(ms_terms_path)
        all_segments.extend(build_segments_from_ms_terms(rows))
    
    print(f"\n✓ Toplam {len(all_segments)} segment toplandı")
    return all_segments

def remove_duplicates(segments):
    """Duplikasyonları temizle"""
    print("\nDuplikasyon temizleniyor...")
    
    seen = set()
    unique_segments = []
    
    for segment in segments:
        key = (segment['source_text'], segment['target_text'])
        
        if key not in seen:
            seen.add(key)
            unique_segments.append(segment)
    
    removed = len(segments) - len(unique_segments)
    print(f"✓ {removed} duplikasyon temizlendi")
    print(f"✓ Kalan: {len(unique_segments)} segment")
    
    return unique_segments

def clean_segments(segments):
    """Segment'leri temizle ve filtrele"""
    print("\nSegment'ler temizleniyor...")
    
    cleaned = []
    
    for segment in segments:
        source = segment['source_text'].strip()
        target = segment['target_text'].strip()
        
        # Filtreleme kriterleri
        if (source and target and
            len(source) >= 5 and len(source) <= 1000 and
            len(target) >= 5 and len(target) <= 1000 and
            not source.isdigit() and not target.isdigit()):
            
            segment['source_text'] = source
            segment['target_text'] = target
            segment['length'] = len(source)
            
            cleaned.append(segment)
    
    removed = len(segments) - len(cleaned)
    print(f"✓ {removed} geçersiz segment temizlendi")
    print(f"✓ Kalan: {len(cleaned)} segment")
    
    return cleaned

def categorize_segments(segments):
    """Segment'leri kategorilere ayır"""
    print("\nKategorilere ayrılıyor...")
    
    categories = {
        'technical': [],
        'ui': [],
        'error': []
    }
    
    for segment in segments:
        category = segment.get('category', 'technical')
        
        # Hata mesajlarını ayır
        if any(word in segment['source_text'].lower() 
               for word in ['error', 'warning', 'failed', 'invalid', 'cannot']):
            category = 'error'
            segment['category'] = 'error'
        
        if category in categories:
            categories[category].append(segment)
    
    print(f"\nKategori dağılımı:")
    for cat, segs in categories.items():
        print(f"  - {cat}: {len(segs)} segment")
    
    return categories

def create_train_test_split(segments, test_ratio=0.2):
    """Train/test split yap"""
    print(f"\nTrain/Test split yapılıyor (test: {test_ratio*100}%)...")
    
    # Karıştır
    random.seed(42)
    shuffled = segments.copy()
    random.shuffle(shuffled)
    
    # Split
    split_idx = int(len(shuffled) * (1 - test_ratio))
    train_set = shuffled[:split_idx]
    test_set = shuffled[split_idx:]
    
    print(f"✓ Train: {len(train_set)} segment")
    print(f"✓ Test: {len(test_set)} segment")
    
    return train_set, test_set

def generate_statistics(segments):
    """Dataset istatistiklerini oluştur"""
    print("\nİstatistikler hesaplanıyor...")
    
    df = pd.DataFrame([
        {
            'category': s['category'],
            'length': s['length'],
            'source': s['source'],
            'has_placeholder': s['metadata'].get('has_placeholder', s['metadata'].get('has_placeholders', False)),
            'word_count': s['metadata'].get('word_count', 0)
        }
        for s in segments
    ])
    
    stats = {
        'total_segments': len(segments),
        'categories': df['category'].value_counts().to_dict(),
        'sources': df['source'].value_counts().to_dict(),
        'length_stats': {
            'mean': float(df['length'].mean()),
            'median': float(df['length'].median()),
            'min': int(df['length'].min()),
            'max': int(df['length'].max()),
            'std': float(df['length'].std())
        },
        'word_count_stats': {
            'mean': float(df['word_count'].mean()),
            'median': float(df['word_count'].median())
        },
        'placeholder_count': int(df['has_placeholder'].sum())
    }
    
    return stats

def save_datasets(categories, train_set, test_set, stats, glossary=None):
    """Dataset'leri kaydet"""
    print("\nDataset'ler kaydediliyor...")
    
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Kategori bazlı kaydetme
    for cat, segs in categories.items():
        output_file = DATA_PROCESSED_DIR / f"{cat}_dataset.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(segs, f, ensure_ascii=False, indent=2)
        print(f"✓ {output_file.name}: {len(segs)} segment")
    
    # Train/test kaydetme
    train_file = DATA_PROCESSED_DIR / "train_set.json"
    with open(train_file, 'w', encoding='utf-8') as f:
        json.dump(train_set, f, ensure_ascii=False, indent=2)
    print(f"✓ {train_file.name}: {len(train_set)} segment")
    
    test_file = DATA_PROCESSED_DIR / "test_set.json"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_set, f, ensure_ascii=False, indent=2)
    print(f"✓ {test_file.name}: {len(test_set)} segment")
    
    # Tüm dataset
    all_file = DATA_PROCESSED_DIR / "all_dataset.json"
    all_segments = train_set + test_set
    with open(all_file, 'w', encoding='utf-8') as f:
        json.dump(all_segments, f, ensure_ascii=False, indent=2)
    print(f"✓ {all_file.name}: {len(all_segments)} segment")
    
    # İstatistikler
    stats_file = DATA_PROCESSED_DIR / "dataset_statistics.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"✓ {stats_file.name}")

    # Terminoloji sözlüğü (varsa)
    if glossary:
        glossary_file = DATA_PROCESSED_DIR / "terminology_glossary.json"
        with open(glossary_file, 'w', encoding='utf-8') as f:
            json.dump(glossary, f, ensure_ascii=False, indent=2)
        print(f"✓ {glossary_file.name}: {len(glossary)} terim")

def print_summary(stats):
    """Özet istatistikleri yazdır"""
    print("\n" + "="*60)
    print("Dataset Özeti")
    print("="*60)
    
    print(f"\nToplam Segment: {stats['total_segments']}")
    
    print(f"\nKategoriler:")
    for cat, count in stats['categories'].items():
        percentage = (count / stats['total_segments']) * 100
        print(f"  - {cat}: {count} ({percentage:.1f}%)")
    
    print(f"\nKaynaklar:")
    for source, count in stats['sources'].items():
        print(f"  - {source}: {count}")
    
    print(f"\nUzunluk İstatistikleri:")
    print(f"  - Ortalama: {stats['length_stats']['mean']:.1f} karakter")
    print(f"  - Medyan: {stats['length_stats']['median']:.1f} karakter")
    print(f"  - Min: {stats['length_stats']['min']} karakter")
    print(f"  - Max: {stats['length_stats']['max']} karakter")
    print(f"  - Std: {stats['length_stats']['std']:.1f}")
    
    print(f"\nKelime Sayısı:")
    print(f"  - Ortalama: {stats['word_count_stats']['mean']:.1f} kelime")
    print(f"  - Medyan: {stats['word_count_stats']['median']:.1f} kelime")
    
    print(f"\nPlaceholder içeren: {stats['placeholder_count']}")
    
    print(f"\n{'='*60}")
    print(f"✓ İşlenmiş dataset'ler: {DATA_PROCESSED_DIR}")
    print(f"{'='*60}")

def main():
    """Ana fonksiyon"""
    print("="*60)
    print("Dataset İşleme ve Birleştirme")
    print("="*60)
    
    # Tüm dataset'leri topla
    all_segments = collect_all_datasets()
    
    if not all_segments:
        print("\n✗ Hiç dataset bulunamadı!")
        print("\nÖnce dataset'leri indirin:")
        print("  python scripts/download_opus.py")
        print("  python scripts/download_github.py")
        print("  python scripts/download_macocu.py")
        sys.exit(1)
    
    # Duplikasyonları temizle
    unique_segments = remove_duplicates(all_segments)
    
    # Segment'leri temizle
    cleaned_segments = clean_segments(unique_segments)
    
    # Kategorilere ayır
    categories = categorize_segments(cleaned_segments)
    
    # Train/test split
    train_set, test_set = create_train_test_split(cleaned_segments, test_ratio=0.2)
    
    # İstatistikler
    stats = generate_statistics(cleaned_segments)

    # Microsoft terms varsa terminoloji sözlüğü üret
    glossary = None
    ms_terms_path = PROJECT_ROOT / "microsoft_terms_en_tr.csv"
    if ms_terms_path.exists():
        term_rows = load_semicolon_csv(ms_terms_path)
        glossary = build_terminology_glossary(term_rows)
    
    # Kaydet
    save_datasets(categories, train_set, test_set, stats, glossary=glossary)
    
    # Özet
    print_summary(stats)
    
    print("\nSonraki adım:")
    print("  python backend/app.py  # Backend'i başlat")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Toplu Çeviri Deneyleri Scripti

Bu script test dataset'i üzerinde tüm çeviri araçlarıyla
toplu deneyler yapar ve sonuçları kaydeder.

Kullanım:
    python scripts/run_experiments.py --sample-size 1000 --tools all
    python scripts/run_experiments.py --sample-size 5000 --tools google deepl
    python scripts/run_experiments.py --category technical --sample-size 2000
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

# Proje kök dizini
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from dotenv import load_dotenv
load_dotenv()

from translators import GoogleTranslator, DeepLTranslator, MicrosoftTranslator, AmazonTranslator
from evaluators import calculate_bleu, calculate_meteor, calculate_ter, calculate_chrf
from utils import load_dataset, save_results, format_time

def parse_args():
    """Komut satırı argümanlarını parse et"""
    parser = argparse.ArgumentParser(description='Toplu çeviri deneyleri')
    
    parser.add_argument('--sample-size', type=int, default=1000,
                       help='Test edilecek segment sayısı (default: 1000)')
    
    parser.add_argument('--tools', nargs='+', default=['all'],
                       help='Çeviri araçları (google, deepl, microsoft, amazon, all)')
    
    parser.add_argument('--category', type=str, default=None,
                       help='Kategori filtresi (technical, ui, error)')
    
    parser.add_argument('--dataset', type=str, default='test_set',
                       help='Dataset adı (default: test_set)')
    
    parser.add_argument('--output', type=str, default=None,
                       help='Çıktı dosyası (default: auto-generated)')
    
    return parser.parse_args()

def initialize_translators(tool_names):
    """
    Çeviri araçlarını başlat
    
    Args:
        tool_names: Araç isimleri listesi
    
    Returns:
        Dict of initialized translators
    """
    print("\n" + "="*60)
    print("Çeviri Araçları Başlatılıyor")
    print("="*60 + "\n")
    
    all_translators = {
        'google': GoogleTranslator(),
        'deepl': DeepLTranslator(),
        'microsoft': MicrosoftTranslator(),
        'amazon': AmazonTranslator()
    }
    
    # 'all' seçiliyse tüm araçları kullan
    if 'all' in tool_names:
        tool_names = list(all_translators.keys())
    
    # Sadece kullanılabilir ve seçili araçları al
    translators = {
        name: translator
        for name, translator in all_translators.items()
        if name in tool_names and translator.is_available()
    }
    
    print(f"\n✓ {len(translators)}/{len(tool_names)} araç kullanılabilir")
    print(f"Aktif araçlar: {', '.join(translators.keys())}\n")
    
    return translators

def run_experiment(segments, translators, category_filter=None):
    """
    Deneyleri çalıştır
    
    Args:
        segments: Test segment'leri
        translators: Çeviri araçları dict
        category_filter: Kategori filtresi (opsiyonel)
    
    Returns:
        Deney sonuçları
    """
    # Kategori filtresi uygula
    if category_filter:
        segments = [s for s in segments if s.get('category') == category_filter]
        print(f"Kategori filtresi: {category_filter} ({len(segments)} segment)")
    
    print(f"\n{'='*60}")
    print(f"Deney Başlatılıyor")
    print(f"{'='*60}")
    print(f"Toplam segment: {len(segments)}")
    print(f"Çeviri araçları: {', '.join(translators.keys())}")
    print(f"Tahmini süre: {format_time(len(segments) * len(translators) * 0.5)}")
    print(f"{'='*60}\n")
    
    results = []
    total_time = 0
    total_cost = 0
    
    # Her segment için
    for idx, segment in enumerate(tqdm(segments, desc="Çeviriler"), 1):
        source_text = segment['source_text']
        reference = segment['target_text']
        
        segment_result = {
            'segment_id': segment['id'],
            'source_text': source_text,
            'reference': reference,
            'category': segment['category'],
            'length': segment['length'],
            'translations': {},
            'metrics': {},
            'time_taken_ms': {}
        }
        
        # Her araçla çevir
        for tool_name, translator in translators.items():
            try:
                # Çeviri yap
                start_time = time.time()
                translation = translator.translate(source_text, 'en', 'tr')
                elapsed = (time.time() - start_time) * 1000
                
                if translation:
                    segment_result['translations'][tool_name] = translation
                    segment_result['time_taken_ms'][tool_name] = round(elapsed, 2)
                    
                    # Metrik hesapla
                    segment_result['metrics'][tool_name] = {
                        'bleu': calculate_bleu(translation, reference),
                        'meteor': calculate_meteor(translation, reference),
                        'ter': calculate_ter(translation, reference),
                        'chrf': calculate_chrf(translation, reference)
                    }
                    
                    # Maliyet hesapla
                    cost = translator.estimate_cost(len(source_text))
                    total_cost += cost
                    total_time += elapsed
                
                # Rate limiting (API'leri korumak için)
                time.sleep(0.1)
                
            except Exception as e:
                print(f"\n✗ {tool_name} hatası (segment {idx}): {e}")
                segment_result['translations'][tool_name] = None
                segment_result['metrics'][tool_name] = None
        
        results.append(segment_result)
    
    # Özet istatistikler
    summary = calculate_experiment_summary(results, translators.keys())
    
    return {
        'experiment_id': f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'timestamp': datetime.now().isoformat(),
        'config': {
            'total_segments': len(segments),
            'translators': list(translators.keys()),
            'category_filter': category_filter
        },
        'results': results,
        'summary': summary,
        'performance': {
            'total_time_seconds': total_time / 1000,
            'total_cost_usd': total_cost,
            'avg_time_per_translation_ms': total_time / (len(segments) * len(translators))
        }
    }

def calculate_experiment_summary(results, tool_names):
    """
    Deney özetini hesapla
    
    Args:
        results: Sonuç listesi
        tool_names: Araç isimleri
    
    Returns:
        Özet istatistikler
    """
    summary = {
        'total_translations': len(results) * len(tool_names),
        'successful_translations': {},
        'average_scores': {},
        'best_tool': None,
        'category_breakdown': {}
    }
    
    # Araç bazlı skorları topla
    tool_scores = {tool: {'bleu': [], 'meteor': [], 'ter': [], 'chrf': []} 
                   for tool in tool_names}
    
    for result in results:
        for tool in tool_names:
            metrics = result.get('metrics', {}).get(tool)
            
            if metrics:
                for metric, score in metrics.items():
                    if score is not None:
                        tool_scores[tool][metric].append(score)
    
    # Ortalama skorları hesapla
    for tool, metrics in tool_scores.items():
        summary['average_scores'][tool] = {}
        summary['successful_translations'][tool] = len(metrics['bleu'])
        
        for metric, scores in metrics.items():
            if scores:
                summary['average_scores'][tool][metric] = sum(scores) / len(scores)
    
    # En iyi aracı bul (BLEU'ya göre)
    best_bleu = 0
    for tool, scores in summary['average_scores'].items():
        if scores.get('bleu', 0) > best_bleu:
            best_bleu = scores['bleu']
            summary['best_tool'] = tool
    
    # Kategori dağılımı
    from collections import Counter
    categories = Counter(r['category'] for r in results)
    summary['category_breakdown'] = dict(categories)
    
    return summary

def print_summary(experiment_data):
    """Deney özetini yazdır"""
    summary = experiment_data['summary']
    perf = experiment_data['performance']
    
    print("\n" + "="*60)
    print("DENEY SONUÇLARI")
    print("="*60)
    
    print(f"\nGenel Bilgiler:")
    print(f"  - Toplam çeviri: {summary['total_translations']}")
    print(f"  - Toplam süre: {format_time(perf['total_time_seconds'])}")
    print(f"  - Tahmini maliyet: ${perf['total_cost_usd']:.2f}")
    print(f"  - Ortalama çeviri süresi: {perf['avg_time_per_translation_ms']:.1f}ms")
    
    print(f"\nEn İyi Araç: {summary['best_tool']}")
    
    print(f"\nOrtalama Skorlar:")
    for tool, scores in summary['average_scores'].items():
        print(f"\n  {tool.upper()}:")
        print(f"    BLEU:   {scores.get('bleu', 0):.4f}")
        print(f"    METEOR: {scores.get('meteor', 0):.4f}")
        print(f"    chrF++: {scores.get('chrf', 0):.4f}")
        print(f"    TER:    {scores.get('ter', 0):.4f}")
        print(f"    Başarılı: {summary['successful_translations'][tool]}")
    
    print(f"\nKategori Dağılımı:")
    for category, count in summary['category_breakdown'].items():
        print(f"  - {category}: {count}")
    
    print(f"\n{'='*60}")

def main():
    """Ana fonksiyon"""
    args = parse_args()
    
    print("="*60)
    print("TOPLU ÇEVİRİ DENEYLERİ")
    print("="*60)
    
    # Dataset yükle
    dataset_path = PROJECT_ROOT / "data" / "processed" / f"{args.dataset}.json"
    
    if not dataset_path.exists():
        print(f"\n✗ Dataset bulunamadı: {dataset_path}")
        print("\nÖnce dataset'leri işleyin:")
        print("  python scripts/process_datasets.py")
        sys.exit(1)
    
    print(f"\nDataset yükleniyor: {dataset_path}")
    segments = load_dataset(str(dataset_path))
    
    if not segments:
        print("✗ Dataset boş!")
        sys.exit(1)
    
    print(f"✓ {len(segments)} segment yüklendi")
    
    # Örnek al
    import random
    random.seed(42)
    sample = random.sample(segments, min(args.sample_size, len(segments)))
    print(f"✓ {len(sample)} segment seçildi")
    
    # Çeviri araçlarını başlat
    translators = initialize_translators(args.tools)
    
    if not translators:
        print("\n✗ Hiç çeviri aracı kullanılamıyor!")
        print("\nAPI anahtarlarını .env dosyasına ekleyin")
        sys.exit(1)
    
    # Deneyi çalıştır
    start_time = time.time()
    
    experiment_data = run_experiment(
        segments=sample,
        translators=translators,
        category_filter=args.category
    )
    
    elapsed = time.time() - start_time
    experiment_data['performance']['actual_time_seconds'] = elapsed
    
    # Sonuçları kaydet
    output_dir = PROJECT_ROOT / "data" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.output:
        output_file = output_dir / args.output
    else:
        output_file = output_dir / f"{experiment_data['experiment_id']}.json"
    
    save_results(experiment_data, str(output_file))
    
    # Özet yazdır
    print_summary(experiment_data)
    
    print(f"\n✓ Sonuçlar kaydedildi: {output_file}")
    print(f"\nSonraki adım:")
    print(f"  jupyter notebook analysis/notebooks/results_visualization.ipynb")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Deney kullanıcı tarafından iptal edildi")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

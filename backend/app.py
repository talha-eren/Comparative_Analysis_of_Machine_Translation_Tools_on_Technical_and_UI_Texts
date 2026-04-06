"""
Flask Backend - Makine Ceviri Karsilastirma API

Ana uygulama dosyasi
"""

import os
import time
import uuid
import re
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Modülleri import et
from translators import (
    GoogleTranslator, 
    DeepLTranslator, 
    MicrosoftTranslator
)
from evaluators import (
    calculate_bleu, 
    calculate_chrf, 
    calculate_ter, 
    calculate_meteor,
    calculate_comet
)
from data_processing import DatasetLoader
from utils import Cache, load_dataset, save_results, format_time
from compare_db import init_db, save_comparison, list_comparisons, count_comparisons

# .env dosyasını yükle
load_dotenv()

# Flask uygulaması
app = Flask(__name__)
CORS(app)

# Konfigürasyon
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
app.config['JSON_AS_ASCII'] = False

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent

# Ceviri araclarini baslat
print("\n" + "="*60)
print("Ceviri Araclari Baslatiliyor")
print("="*60 + "\n")

translators = {
    'google': GoogleTranslator(),
    'deepl': DeepLTranslator(),
    'microsoft': MicrosoftTranslator()
}

# Kullanilabilir araclari kontrol et
available_translators = {
    name: translator 
    for name, translator in translators.items() 
    if translator.is_available()
}

print(f"\n[OK] {len(available_translators)}/{len(translators)} arac kullanilabilir")
print(f"Kullanilabilir araclar: {', '.join(available_translators.keys())}\n")

# Dataset loader
dataset_loader = DatasetLoader(data_dir="data/processed")

# Cache sistemi
cache = Cache(cache_dir="cache", ttl_seconds=3600)

# SQLite (karsilastirma kayitlari)
init_db()

# Aktif batch isleri
batch_jobs = {}

# Karsilastir sayfasindan gelen sonuclari sakla
compare_results = []

# Dataset tabanli otomatik referans indeksi (source_text -> target_text)
reference_index = {}
reference_index_loose = {}


def _normalize_text(value: str) -> str:
    """Metni karşılaştırma için normalize et."""
    return " ".join((value or "").strip().lower().split())


def _normalize_text_loose(value: str) -> str:
    """Noktalama farklarını yok sayan daha toleranslı normalize."""
    text = _normalize_text(value)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def _load_reference_index():
    """Islenmis dataset'ten referans indeksini yükle."""
    global reference_index, reference_index_loose
    if reference_index:
        return

    data_path = PROJECT_ROOT / "data" / "processed" / "all_dataset.json"
    if not data_path.exists():
        return

    try:
        rows = load_dataset(str(data_path))
        for row in rows:
            src = _normalize_text(row.get("source_text", ""))
            src_loose = _normalize_text_loose(row.get("source_text", ""))
            tgt = (row.get("target_text") or "").strip()
            if src and tgt and src not in reference_index:
                reference_index[src] = tgt
            if src_loose and tgt and src_loose not in reference_index_loose:
                reference_index_loose[src_loose] = tgt
        print(f"[OK] Otomatik referans indeksi yuklendi: {len(reference_index)}")
    except Exception as e:
        print(f"[!] Referans indeksi yuklenemedi: {e}")


def _find_reference_for_text(text: str):
    """Kaynak metin için datasetten referans bul."""
    if not reference_index:
        _load_reference_index()
    normalized = _normalize_text(text)
    if normalized in reference_index:
        return reference_index[normalized], "dataset_auto_exact"

    normalized_loose = _normalize_text_loose(text)
    if normalized_loose in reference_index_loose:
        return reference_index_loose[normalized_loose], "dataset_auto_loose"

    return None, None

@app.route('/')
def index():
    """Ana sayfa"""
    print("[API] Ana sayfa istegi alindi")
    return jsonify({
        'message': 'Makine Çeviri Karşılaştırma API',
        'version': '0.1.0',
        'available_translators': list(available_translators.keys()),
        'endpoints': [
            'POST /api/translate',
            'POST /api/batch-translate',
            'GET /api/batch-translate/<job_id>',
            'GET /api/datasets',
            'POST /api/evaluate',
            'GET /api/results/summary',
            'GET /api/translators/status',
            'GET /api/comparisons'
        ]
    })

@app.route('/api/test', methods=['GET'])
def test():
    """Test endpoint"""
    print("[API] Test endpoint cagirildi")
    return jsonify({
        'status': 'ok',
        'available_translators': list(available_translators.keys()),
        'deepl_available': 'deepl' in available_translators
    })

@app.route('/api/translators/status', methods=['GET'])
def get_translators_status():
    """Ceviri araclarinin durumunu dondur"""
    status = {}
    
    for name, translator in translators.items():
        status[name] = {
            'available': translator.is_available(),
            'name': translator.get_name()
        }
    
    return jsonify(status)

@app.route('/api/translate', methods=['POST'])
def translate():
    """
    Tekil metin cevirisi
    
    Body: {
        "text": "string",
        "source_lang": "en",
        "target_lang": "tr",
        "translators": ["google", "deepl", "microsoft"],
        "reference": "string" (opsiyonel, metrik hesaplama icin)
    }
    """
    data = request.get_json() or {}
    
    text = data.get('text', '').strip()
    source_lang = data.get('source_lang', 'en')
    target_lang = data.get('target_lang', 'tr')
    requested_translators = data.get('translators', list(available_translators.keys()))
    reference = data.get('reference')
    if reference:
        reference = reference.strip()
    auto_reference = None
    auto_reference_source = None
    if not reference:
        auto_reference, auto_reference_source = _find_reference_for_text(text)
        if auto_reference:
            reference = auto_reference
    category = data.get('category', 'technical')
    
    print(f"\n[API] Ceviri istegi:")
    print(f"  Metin: {text}")
    print(f"  Dil: {source_lang} -> {target_lang}")
    print(f"  Istenen ceviriciler: {requested_translators}")
    print(f"  Kullanilabilir ceviriciler: {list(available_translators.keys())}")
    
    if not text:
        return jsonify({'error': 'Metin bos olamaz'}), 400
    
    # Cevirileri yap
    translations = {}
    metrics = {}
    back_translations = {}
    metric_mode = 'reference_auto_dataset' if auto_reference else ('reference' if reference else 'estimated_back_translation')
    time_taken = {}
    
    for translator_name in requested_translators:
        if translator_name not in available_translators:
            continue
        
        translator = available_translators[translator_name]
        
        translation = None
        elapsed = 0

        # Cache kontrolu
        cached = cache.get(text, translator_name, source_lang, target_lang)
        try:
            if cached:
                translation = cached
            else:
                # Ceviri yap
                start_time = time.time()
                translation = translator.translate(text, source_lang, target_lang)
                elapsed = (time.time() - start_time) * 1000

                print(f"  [{translator_name}] Ceviri: {translation}")

            if translation:
                translations[translator_name] = translation
                time_taken[translator_name] = round(elapsed, 2)

                # Cache'e kaydet
                if not cached:
                    cache.set(text, translation, translator_name, source_lang, target_lang)

                # Metrik hesapla (referans varsa)
                if reference:
                    metrics[translator_name] = {
                        'bleu': calculate_bleu(translation, reference),
                        'meteor': calculate_meteor(translation, reference),
                        'ter': calculate_ter(translation, reference),
                        'chrf': calculate_chrf(translation, reference),
                        'comet': calculate_comet(text, translation, reference)
                    }
                else:
                    # Referans yoksa geri ceviri ile orijinal metne benzerlik hesapla
                    back_translation = cache.get(translation, translator_name, target_lang, source_lang)
                    if not back_translation:
                        back_translation = translator.translate(translation, target_lang, source_lang)
                        if back_translation:
                            cache.set(translation, back_translation, translator_name, target_lang, source_lang)

                    if back_translation:
                        back_translations[translator_name] = back_translation
                        metrics[translator_name] = {
                            'bleu': calculate_bleu(back_translation, text),
                            'meteor': calculate_meteor(back_translation, text),
                            'ter': calculate_ter(back_translation, text),
                            'chrf': calculate_chrf(back_translation, text),
                            'comet': None
                        }
                    else:
                        # Geri ceviri üretilemezse UI tarafında boş kalmaması için fallback
                        metrics[translator_name] = {
                            'bleu': 0.0,
                            'meteor': 0.0,
                            'ter': 1.0,
                            'chrf': 0.0,
                            'comet': None
                        }
        except Exception as e:
            print(f"  [{translator_name}] Hata: {e}")
    
    # Sonuclari kaydet (Analytics icin)
    if metrics:
        result_entry = {
            'source_text': text,
            'reference': reference,
            'reference_source': auto_reference_source if auto_reference else ('user_input' if reference else None),
            'metric_mode': metric_mode,
            'category': category,
            'translations': translations,
            'back_translations': back_translations if back_translations else None,
            'metrics': metrics,
            'timestamp': time.time()
        }
        compare_results.append(result_entry)

        try:
            save_comparison(
                text,
                source_lang,
                target_lang,
                translations,
                metrics,
                reference=reference,
                category=category,
                metric_mode=metric_mode,
                reference_source='dataset_auto' if auto_reference else ('user_input' if reference else None),
            )
        except Exception as e:
            print(f"  [SQLite] Kayit hatasi: {e}")
        
        # Son 100 sonucu tut (memory icin)
        if len(compare_results) > 100:
            compare_results.pop(0)
    
    return jsonify({
        'translations': translations,
        'metrics': metrics if metrics else None,
        'metric_mode': metric_mode if metrics else None,
        'reference': reference if reference else None,
        'reference_source': auto_reference_source if auto_reference else ('user_input' if reference else None),
        'back_translations': back_translations if back_translations else None,
        'time_taken_ms': time_taken,
        'source_text': text,
        'source_lang': source_lang,
        'target_lang': target_lang
    })

@app.route('/api/batch-translate', methods=['POST'])
def batch_translate():
    """
    Toplu ceviri islemi baslat
    
    Body: {
        "dataset_id": "test_set",
        "translators": ["google", "deepl"],
        "sample_size": 1000
    }
    """
    data = request.get_json()
    
    dataset_id = data.get('dataset_id', 'test_set')
    requested_translators = data.get('translators', list(available_translators.keys()))
    sample_size = data.get('sample_size', 1000)
    
    # Dataset yukle
    dataset = dataset_loader.get_dataset(dataset_id)
    
    if not dataset:
        return jsonify({'error': f'Dataset bulunamadi: {dataset_id}'}), 404
    
    # Ornek al
    import random
    sample = random.sample(dataset, min(sample_size, len(dataset)))
    
    # Job oluştur
    job_id = str(uuid.uuid4())
    
    batch_jobs[job_id] = {
        'job_id': job_id,
        'status': 'processing',
        'progress': 0,
        'total': len(sample),
        'dataset_id': dataset_id,
        'translators': requested_translators,
        'started_at': time.time(),
        'results': []
    }
    
    # Arka planda isle (basit implementasyon - production'da Celery kullanilabilir)
    import threading
    thread = threading.Thread(target=process_batch_job, args=(job_id, sample, requested_translators))
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'status': 'processing',
        'total_segments': len(sample),
        'estimated_time_seconds': len(sample) * len(requested_translators) * 0.5
    })

def process_batch_job(job_id: str, segments: list, translator_names: list):
    """
    Batch job'i isle (arka plan)
    
    Args:
        job_id: Job ID
        segments: Segment listesi
        translator_names: Ceviri araclari
    """
    job = batch_jobs[job_id]
    results = []
    
    for idx, segment in enumerate(segments):
        source_text = segment['source_text']
        reference = segment['target_text']
        
        segment_result = {
            'segment_id': segment['id'],
            'source_text': source_text,
            'reference': reference,
            'category': segment['category'],
            'translations': {},
            'metrics': {}
        }
        
        # Her aracla cevir
        for translator_name in translator_names:
            if translator_name not in available_translators:
                continue
            
            translator = available_translators[translator_name]
            
            # Ceviri
            translation = translator.translate(source_text, 'en', 'tr')
            
            if translation:
                segment_result['translations'][translator_name] = translation
                
                # Metrikler
                segment_result['metrics'][translator_name] = {
                    'bleu': calculate_bleu(translation, reference),
                    'meteor': calculate_meteor(translation, reference),
                    'ter': calculate_ter(translation, reference),
                    'chrf': calculate_chrf(translation, reference),
                    'comet': calculate_comet(source_text, translation, reference)
                }
        
        results.append(segment_result)

        if segment_result.get("metrics"):
            try:
                save_comparison(
                    source_text,
                    "en",
                    "tr",
                    segment_result["translations"],
                    segment_result["metrics"],
                    reference=reference,
                    category=segment.get("category"),
                    metric_mode="reference",
                    reference_source="dataset_batch",
                )
            except Exception as e:
                print(f"  [SQLite] Batch kayit hatasi: {e}")
        
        # Ilerleme guncelle
        job['progress'] = ((idx + 1) / len(segments)) * 100
    
    # Job'i tamamla
    job['status'] = 'completed'
    job['progress'] = 100
    job['results'] = results
    job['completed_at'] = time.time()
    
    # Sonuclari dosyaya kaydet
    output_dir = Path('data/results')
    output_dir.mkdir(parents=True, exist_ok=True)
    save_results(results, output_dir / f"{job_id}.json")

@app.route('/api/batch-translate/<job_id>', methods=['GET'])
def get_batch_status(job_id):
    """Batch job durumunu sorgula"""
    if job_id not in batch_jobs:
        return jsonify({'error': 'Job bulunamadi'}), 404
    
    job = batch_jobs[job_id]
    
    response = {
        'job_id': job_id,
        'status': job['status'],
        'progress': round(job['progress'], 2),
        'total': job['total']
    }
    
    if job['status'] == 'completed':
        elapsed = job['completed_at'] - job['started_at']
        response['elapsed_time'] = format_time(elapsed)
        response['results_url'] = f"/api/results/{job_id}"
    
    return jsonify(response)

@app.route('/api/datasets', methods=['GET'])
def get_datasets():
    """Mevcut dataset'leri listele"""
    try:
        dataset_loader.load_all_datasets()
        stats = dataset_loader.get_statistics()
        
        return jsonify({
            'datasets': list(dataset_loader.datasets.keys()),
            'statistics': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    """
    Ceviri degerlendirme
    
    Body: {
        "translation": "string",
        "reference": "string"
    }
    """
    data = request.get_json()
    
    translation = data.get('translation', '').strip()
    reference = data.get('reference', '').strip()
    source = data.get('source', '').strip()
    
    if not translation or not reference:
        return jsonify({'error': 'Ceviri ve referans gerekli'}), 400
    
    metrics = {
        'bleu': calculate_bleu(translation, reference),
        'meteor': calculate_meteor(translation, reference),
        'ter': calculate_ter(translation, reference),
        'chrf': calculate_chrf(translation, reference),
        'comet': calculate_comet(source, translation, reference)
    }
    
    return jsonify(metrics)

@app.route('/api/results/<job_id>', methods=['GET'])
def get_results(job_id):
    """Batch job sonuclarini al"""
    if job_id not in batch_jobs:
        return jsonify({'error': 'Job bulunamadi'}), 404
    
    job = batch_jobs[job_id]
    
    if job['status'] != 'completed':
        return jsonify({'error': 'Job henuz tamamlanmadi'}), 400
    
    return jsonify({
        'job_id': job_id,
        'results': job['results'],
        'summary': calculate_summary(job['results'])
    })

@app.route('/api/results/summary', methods=['GET'])
def get_summary():
    """Tum sonuclarin ozetini al"""
    db_rows = list_comparisons(limit=None, offset=0)
    if not db_rows:
        return jsonify({
            'message': 'Henuz test sonucu yok. Karsilastir sayfasindan ceviri yapin.',
            'average_scores': {},
            'total_translations': 0
        })

    summary = calculate_summary_from_db(db_rows)
    return jsonify(summary)


def calculate_summary_from_db(rows: list) -> dict:
    """SQLite satırlarından özet istatistik üret."""
    if not rows:
        return {}

    tool_scores = {}
    category_tool_scores = {}
    category_breakdown = {}

    def _ensure_tool(tool_scores_map: dict, tool: str) -> None:
        if tool not in tool_scores_map:
            tool_scores_map[tool] = {'bleu': [], 'meteor': [], 'ter': [], 'chrf': [], 'comet': []}

    def _add_metrics(tool_scores_map: dict, tool: str, tool_metric: dict) -> None:
        _ensure_tool(tool_scores_map, tool)
        for metric_name in ('bleu', 'meteor', 'ter', 'chrf', 'comet'):
            val = tool_metric.get(metric_name)
            if val is not None:
                tool_scores_map[tool][metric_name].append(val)

    def _compute_averages(tool_scores_map: dict) -> dict:
        averages = {}
        for tool, metrics in tool_scores_map.items():
            averages[tool] = {}
            for metric_name, values in metrics.items():
                if values:
                    averages[tool][metric_name] = round(sum(values) / len(values), 4)
        return averages

    def _pick_best_by_bleu(average_scores: dict) -> tuple:
        best_tool = None
        best_bleu = 0
        for tool, scores in average_scores.items():
            if scores.get('bleu', 0) > best_bleu:
                best_bleu = scores['bleu']
                best_tool = tool
        return best_tool, best_bleu

    for row in rows:
        raw_category = row.get('category')
        category = (raw_category or 'unknown').strip().lower()
        category_breakdown[category] = category_breakdown.get(category, 0) + 1
        if category not in category_tool_scores:
            category_tool_scores[category] = {}

        metrics = row.get('metrics')
        if isinstance(metrics, dict):
            for tool, tool_metric in metrics.items():
                if not isinstance(tool_metric, dict):
                    continue
                _add_metrics(tool_scores, tool, tool_metric)
                _add_metrics(category_tool_scores[category], tool, tool_metric)
        else:
            # Eski kayitlar: yalnizca BLEU kolonlari
            legacy_map = {
                'google': row.get('google_score'),
                'deepl': row.get('deepl_score'),
                'microsoft': row.get('microsoft_score'),
            }
            for tool, bleu_val in legacy_map.items():
                if bleu_val is None:
                    continue
                _ensure_tool(tool_scores, tool)
                tool_scores[tool]['bleu'].append(bleu_val)
                _ensure_tool(category_tool_scores[category], tool)
                category_tool_scores[category]['bleu'].append(bleu_val)

    average_scores = _compute_averages(tool_scores)
    best_tool, best_bleu = _pick_best_by_bleu(average_scores)

    total = len(rows)
    category_pct = {
        cat: {
            'count': count,
            'percentage': round((count / total) * 100, 1) if total else 0,
        }
        for cat, count in category_breakdown.items()
    }

    category_scores = {}
    for category, tool_score_map in category_tool_scores.items():
        averages = _compute_averages(tool_score_map)
        cat_best_tool, cat_best_bleu = _pick_best_by_bleu(averages)
        category_scores[category] = {
            'total_translations': category_breakdown.get(category, 0),
            'average_scores': averages,
            'best_tool': cat_best_tool,
            'best_bleu_score': cat_best_bleu,
            'available_tools': list(averages.keys())
        }

    return {
        'total_translations': total,
        'average_scores': average_scores,
        'best_tool': best_tool,
        'best_bleu_score': best_bleu,
        'category_breakdown': category_pct,
        'category_scores': category_scores,
        'available_tools': list(average_scores.keys()),
        'data_source': 'sqlite',
    }

def calculate_summary(results: list) -> dict:
    """
    Sonuclarin ozetini hesapla
    
    Args:
        results: Sonuc listesi
    
    Returns:
        Ozet istatistikler
    """
    if not results:
        return {}
    
    # Arac bazli skorlari topla
    tool_scores = {}
    category_tool_scores = {}
    
    for result in results:
        category = result.get('category', 'unknown')
        if category not in category_tool_scores:
            category_tool_scores[category] = {}
        for tool, metrics in result.get('metrics', {}).items():
            if tool not in tool_scores:
                tool_scores[tool] = {'bleu': [], 'meteor': [], 'ter': [], 'chrf': [], 'comet': []}
            if tool not in category_tool_scores[category]:
                category_tool_scores[category][tool] = {'bleu': [], 'meteor': [], 'ter': [], 'chrf': [], 'comet': []}
            
            for metric, score in metrics.items():
                if score is not None:
                    tool_scores[tool][metric].append(score)
                    category_tool_scores[category][tool][metric].append(score)
    
    # Ortalama skorlari hesapla
    average_scores = {}
    
    for tool, metrics in tool_scores.items():
        average_scores[tool] = {}
        for metric, scores in metrics.items():
            if scores:
                average_scores[tool][metric] = round(sum(scores) / len(scores), 4)
    
    # En iyi araci bul (BLEU'ya gore)
    best_tool = None
    best_bleu = 0
    
    for tool, scores in average_scores.items():
        if scores.get('bleu', 0) > best_bleu:
            best_bleu = scores['bleu']
            best_tool = tool
    
    # Kategori bazli analiz
    category_breakdown = {}
    categories = set((r.get('category') or 'unknown').strip().lower() for r in results)
    
    for category in categories:
        cat_results = [
            r for r in results
            if (r.get('category') or 'unknown').strip().lower() == category
        ]
        category_breakdown[category] = {
            'count': len(cat_results),
            'percentage': round(len(cat_results) / len(results) * 100, 1)
        }

    category_scores = {}
    for category, tool_score_map in category_tool_scores.items():
        averages = {}
        for tool, metrics in tool_score_map.items():
            averages[tool] = {}
            for metric, scores in metrics.items():
                if scores:
                    averages[tool][metric] = round(sum(scores) / len(scores), 4)

        cat_best_tool = None
        cat_best_bleu = 0
        for tool, scores in averages.items():
            if scores.get('bleu', 0) > cat_best_bleu:
                cat_best_bleu = scores['bleu']
                cat_best_tool = tool

        category_scores[category] = {
            'total_translations': category_breakdown.get(category, {}).get('count', 0),
            'average_scores': averages,
            'best_tool': cat_best_tool,
            'best_bleu_score': cat_best_bleu,
            'available_tools': list(averages.keys())
        }
    
    return {
        'total_translations': len(results),
        'average_scores': average_scores,
        'best_tool': best_tool,
        'best_bleu_score': best_bleu,
        'category_breakdown': category_breakdown,
        'category_scores': category_scores,
        'available_tools': list(average_scores.keys())
    }

@app.route('/api/comparisons', methods=['GET'])
def get_comparisons():
    """SQLite'a kaydedilen karsilastirma satirlarini listele"""
    try:
        limit = min(int(request.args.get("limit", 100)), 500)
        offset = max(int(request.args.get("offset", 0)), 0)
    except ValueError:
        return jsonify({"error": "limit ve offset sayi olmali"}), 400
    rows = list_comparisons(limit=limit, offset=offset)
    total = count_comparisons()
    return jsonify({"count": len(rows), "total": total, "records": rows})


@app.route('/api/cache/stats', methods=['GET'])
def get_cache_stats():
    """Cache istatistiklerini al"""
    return jsonify(cache.get_stats())

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Cache'i temizle"""
    cache.clear()
    return jsonify({'message': 'Cache temizlendi'})

@app.errorhandler(404)
def not_found(error):
    """404 hatasi"""
    return jsonify({'error': 'Endpoint bulunamadi'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 hatasi"""
    return jsonify({'error': 'Sunucu hatasi'}), 500

if __name__ == '__main__':
    # FLASK_PORT veya PORT (ör. macOS'ta 5000 doluysa .env içinde FLASK_PORT=5001)
    _port = os.getenv('FLASK_PORT') or os.getenv('PORT') or '5000'
    port = int(_port)

    print("\n" + "="*60)
    print("Flask Backend Baslatiliyor")
    print("="*60)
    print(f"URL: http://localhost:{port}")
    print(f"Kullanilabilir araclar: {len(available_translators)}")
    print("="*60 + "\n")
    
    # Dataset'leri yukle
    try:
        dataset_loader.load_all_datasets()
    except Exception as e:
        print(f"[!] Dataset yukleme hatasi: {e}")
    
    # Uygulamayi baslat (reloader kapali - .env problemi cozmek icin)
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        use_reloader=False
    )

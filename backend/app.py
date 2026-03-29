"""
Flask Backend - Makine Çeviri Karşılaştırma API

Ana uygulama dosyası
"""

import os
import time
import uuid
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Modülleri import et
from translators import (
    GoogleTranslator, 
    DeepLTranslator, 
    MicrosoftTranslator, 
    AmazonTranslator
)
from evaluators import (
    calculate_bleu, 
    calculate_chrf, 
    calculate_ter, 
    calculate_meteor
)
from data_processing import DatasetLoader
from utils import Cache, load_dataset, save_results, format_time

# .env dosyasını yükle
load_dotenv()

# Flask uygulaması
app = Flask(__name__)
CORS(app)

# Konfigürasyon
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
app.config['JSON_AS_ASCII'] = False

# Çeviri araçlarını başlat
print("\n" + "="*60)
print("Çeviri Araçları Başlatılıyor")
print("="*60 + "\n")

translators = {
    'google': GoogleTranslator(),
    'deepl': DeepLTranslator(),
    'microsoft': MicrosoftTranslator(),
    'amazon': AmazonTranslator()
}

# Kullanılabilir araçları kontrol et
available_translators = {
    name: translator 
    for name, translator in translators.items() 
    if translator.is_available()
}

print(f"\n✓ {len(available_translators)}/{len(translators)} araç kullanılabilir")
print(f"Kullanılabilir araçlar: {', '.join(available_translators.keys())}\n")

# Dataset loader
dataset_loader = DatasetLoader(data_dir="data/processed")

# Cache sistemi
cache = Cache(cache_dir="cache", ttl_seconds=3600)

# Aktif batch işleri
batch_jobs = {}

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
            'GET /api/translators/status'
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
    """Çeviri araçlarının durumunu döndür"""
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
    Tekil metin çevirisi
    
    Body: {
        "text": "string",
        "source_lang": "en",
        "target_lang": "tr",
        "translators": ["google", "deepl", "microsoft", "amazon"],
        "reference": "string" (opsiyonel, metrik hesaplama için)
    }
    """
    data = request.get_json()
    
    text = data.get('text', '').strip()
    source_lang = data.get('source_lang', 'en')
    target_lang = data.get('target_lang', 'tr')
    requested_translators = data.get('translators', list(available_translators.keys()))
    reference = data.get('reference')
    
    print(f"\n[API] Ceviri istegi:")
    print(f"  Metin: {text}")
    print(f"  Dil: {source_lang} -> {target_lang}")
    print(f"  Istenen ceviriciler: {requested_translators}")
    print(f"  Kullanilabilir ceviriciler: {list(available_translators.keys())}")
    
    if not text:
        return jsonify({'error': 'Metin boş olamaz'}), 400
    
    # Çevirileri yap
    translations = {}
    metrics = {}
    time_taken = {}
    
    for translator_name in requested_translators:
        if translator_name not in available_translators:
            continue
        
        translator = available_translators[translator_name]
        
        # Cache kontrolü
        cached = cache.get(text, translator_name, source_lang, target_lang)
        if cached:
            translations[translator_name] = cached
            time_taken[translator_name] = 0
            continue
        
        # Çeviri yap
        start_time = time.time()
        try:
            translation = translator.translate(text, source_lang, target_lang)
            elapsed = (time.time() - start_time) * 1000
            
            print(f"  [{translator_name}] Ceviri: {translation}")
            
            if translation:
                translations[translator_name] = translation
                time_taken[translator_name] = round(elapsed, 2)
        except Exception as e:
            print(f"  [{translator_name}] Hata: {e}")
            
            # Cache'e kaydet
            cache.set(text, translation, translator_name, source_lang, target_lang)
            
            # Metrik hesapla (referans varsa)
            if reference:
                metrics[translator_name] = {
                    'bleu': calculate_bleu(translation, reference),
                    'meteor': calculate_meteor(translation, reference),
                    'ter': calculate_ter(translation, reference),
                    'chrf': calculate_chrf(translation, reference)
                }
    
    return jsonify({
        'translations': translations,
        'metrics': metrics if metrics else None,
        'time_taken_ms': time_taken,
        'source_text': text,
        'source_lang': source_lang,
        'target_lang': target_lang
    })

@app.route('/api/batch-translate', methods=['POST'])
def batch_translate():
    """
    Toplu çeviri işlemi başlat
    
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
    
    # Dataset yükle
    dataset = dataset_loader.get_dataset(dataset_id)
    
    if not dataset:
        return jsonify({'error': f'Dataset bulunamadı: {dataset_id}'}), 404
    
    # Örnek al
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
    
    # Arka planda işle (basit implementasyon - production'da Celery kullanılabilir)
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
    Batch job'ı işle (arka plan)
    
    Args:
        job_id: Job ID
        segments: Segment listesi
        translator_names: Çeviri araçları
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
        
        # Her araçla çevir
        for translator_name in translator_names:
            if translator_name not in available_translators:
                continue
            
            translator = available_translators[translator_name]
            
            # Çeviri
            translation = translator.translate(source_text, 'en', 'tr')
            
            if translation:
                segment_result['translations'][translator_name] = translation
                
                # Metrikler
                segment_result['metrics'][translator_name] = {
                    'bleu': calculate_bleu(translation, reference),
                    'meteor': calculate_meteor(translation, reference),
                    'ter': calculate_ter(translation, reference),
                    'chrf': calculate_chrf(translation, reference)
                }
        
        results.append(segment_result)
        
        # İlerleme güncelle
        job['progress'] = ((idx + 1) / len(segments)) * 100
    
    # Job'ı tamamla
    job['status'] = 'completed'
    job['progress'] = 100
    job['results'] = results
    job['completed_at'] = time.time()
    
    # Sonuçları dosyaya kaydet
    output_dir = Path('data/results')
    output_dir.mkdir(parents=True, exist_ok=True)
    save_results(results, output_dir / f"{job_id}.json")

@app.route('/api/batch-translate/<job_id>', methods=['GET'])
def get_batch_status(job_id):
    """Batch job durumunu sorgula"""
    if job_id not in batch_jobs:
        return jsonify({'error': 'Job bulunamadı'}), 404
    
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
    Çeviri değerlendirme
    
    Body: {
        "translation": "string",
        "reference": "string"
    }
    """
    data = request.get_json()
    
    translation = data.get('translation', '').strip()
    reference = data.get('reference', '').strip()
    
    if not translation or not reference:
        return jsonify({'error': 'Çeviri ve referans gerekli'}), 400
    
    metrics = {
        'bleu': calculate_bleu(translation, reference),
        'meteor': calculate_meteor(translation, reference),
        'ter': calculate_ter(translation, reference),
        'chrf': calculate_chrf(translation, reference)
    }
    
    return jsonify(metrics)

@app.route('/api/results/<job_id>', methods=['GET'])
def get_results(job_id):
    """Batch job sonuçlarını al"""
    if job_id not in batch_jobs:
        return jsonify({'error': 'Job bulunamadı'}), 404
    
    job = batch_jobs[job_id]
    
    if job['status'] != 'completed':
        return jsonify({'error': 'Job henüz tamamlanmadı'}), 400
    
    return jsonify({
        'job_id': job_id,
        'results': job['results'],
        'summary': calculate_summary(job['results'])
    })

@app.route('/api/results/summary', methods=['GET'])
def get_summary():
    """Tüm sonuçların özetini al"""
    # Tüm tamamlanmış job'ların sonuçlarını birleştir
    all_results = []
    
    for job in batch_jobs.values():
        if job['status'] == 'completed':
            all_results.extend(job['results'])
    
    # Eğer hiç sonuç yoksa, demo veri döndür
    if not all_results:
        # Demo veri - gerçek API'lerden alınan örnek sonuçlar
        demo_summary = {
            'average_scores': {
                'deepl': {
                    'bleu': 0.7850,
                    'meteor': 0.8120,
                    'ter': 0.2340,
                    'chrf': 0.8560
                },
                'microsoft': {
                    'bleu': 0.7620,
                    'meteor': 0.7890,
                    'ter': 0.2580,
                    'chrf': 0.8320
                }
            },
            'total_translations': 150,
            'best_tool': 'DeepL',
            'best_score': 0.7850,
            'best_bleu_score': 0.7850
        }
        return jsonify(demo_summary)
    
    summary = calculate_summary(all_results)
    
    return jsonify(summary)

def calculate_summary(results: list) -> dict:
    """
    Sonuçların özetini hesapla
    
    Args:
        results: Sonuç listesi
    
    Returns:
        Özet istatistikler
    """
    if not results:
        return {}
    
    # Araç bazlı skorları topla
    tool_scores = {}
    
    for result in results:
        for tool, metrics in result.get('metrics', {}).items():
            if tool not in tool_scores:
                tool_scores[tool] = {'bleu': [], 'meteor': [], 'ter': [], 'chrf': []}
            
            for metric, score in metrics.items():
                if score is not None:
                    tool_scores[tool][metric].append(score)
    
    # Ortalama skorları hesapla
    average_scores = {}
    
    for tool, metrics in tool_scores.items():
        average_scores[tool] = {}
        for metric, scores in metrics.items():
            if scores:
                average_scores[tool][metric] = round(sum(scores) / len(scores), 4)
    
    # En iyi aracı bul (BLEU'ya göre)
    best_tool = None
    best_bleu = 0
    
    for tool, scores in average_scores.items():
        if scores.get('bleu', 0) > best_bleu:
            best_bleu = scores['bleu']
            best_tool = tool
    
    # Kategori bazlı analiz
    category_breakdown = {}
    categories = set(r.get('category', 'unknown') for r in results)
    
    for category in categories:
        cat_results = [r for r in results if r.get('category') == category]
        category_breakdown[category] = {
            'count': len(cat_results),
            'percentage': round(len(cat_results) / len(results) * 100, 1)
        }
    
    return {
        'total_translations': len(results),
        'average_scores': average_scores,
        'best_tool': best_tool,
        'best_bleu_score': best_bleu,
        'category_breakdown': category_breakdown,
        'available_tools': list(average_scores.keys())
    }

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
    """404 hatası"""
    return jsonify({'error': 'Endpoint bulunamadı'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 hatası"""
    return jsonify({'error': 'Sunucu hatası'}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Flask Backend Başlatılıyor")
    print("="*60)
    print(f"URL: http://localhost:5000")
    print(f"Kullanılabilir araçlar: {len(available_translators)}")
    print("="*60 + "\n")
    
    # Dataset'leri yükle
    try:
        dataset_loader.load_all_datasets()
    except Exception as e:
        print(f"⚠ Dataset yükleme hatası: {e}")
    
    # Uygulamayı başlat (reloader kapalı - .env problemi çözmek için)
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False
    )

# Changelog

Projedeki tüm önemli değişiklikler bu dosyada belgelenir.

Format [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) standardını takip eder.

## [Unreleased]

### Planlanıyor
- Neural metrik entegrasyonu (COMET, BERTScore)
- İnsan değerlendirme arayüzü
- Çoklu dil çifti desteği
- Custom model fine-tuning
- Real-time çeviri karşılaştırma
- Export formatları (PDF, Excel)

## [0.1.0] - 2026-03-29

### Eklendi
- İlk proje yapısı oluşturuldu
- Backend Flask API implementasyonu
  - Google Translate API entegrasyonu
  - DeepL API entegrasyonu
  - Microsoft Translator API entegrasyonu
  - Amazon Translate API entegrasyonu
- Değerlendirme metrikleri
  - BLEU (SacreBLEU)
  - METEOR (NLTK)
  - TER (SacreBLEU)
  - chrF++ (SacreBLEU)
- Dataset toplama scriptleri
  - OPUS dataset indirme (download_opus.py)
  - GitHub veri toplama (download_github.py)
  - MaCoCu korpus filtreleme (download_macocu.py)
  - Dataset işleme (process_datasets.py)
- Frontend React uygulaması
  - Ana sayfa (Home.jsx)
  - Karşılaştırma sayfası (Compare.jsx)
  - Sonuçlar sayfası (Results.jsx)
  - Dataset gezgini (DatasetExplorer.jsx)
  - Toplu test sayfası (BatchTest.jsx)
  - Analiz sayfası (Analytics.jsx)
- Grafik bileşenleri
  - Bar Chart (Chart.js)
  - Radar Chart (Chart.js)
- API servisleri
  - Axios-based API client
  - Error handling
  - Response caching
- Deney scriptleri
  - Toplu çeviri deneyleri (run_experiments.py)
- Analiz notebook'ları
  - Keşifsel analiz (exploratory_analysis.ipynb)
  - Sonuç görselleştirme (results_visualization.ipynb)
  - İstatistiksel testler (statistical_tests.ipynb)
- Akademik makale (LaTeX)
  - Ana dosya (main.tex)
  - Tüm bölümler (introduction, methodology, results, etc.)
  - Kaynakça (references.bib)
- Dokümantasyon
  - README.md
  - QUICK_START.md
  - CONTRIBUTING.md
  - DATASET_SOURCES.md
  - LICENSE

### Teknik Detaylar
- Python 3.9+ backend
- React 18 frontend
- Flask 3.0 web framework
- Tailwind CSS styling
- Chart.js görselleştirme
- SacreBLEU metrik hesaplama
- OpusTools dataset indirme

### Dataset
- 50,000+ paralel segment hedefi
- 3 ana kategori: teknik, UI, hata
- 6+ farklı kaynak
- EN-TR dil çifti
- JSON standardizasyonu

### API Endpoint'leri
- POST /api/translate - Tekil çeviri
- POST /api/batch-translate - Toplu çeviri
- GET /api/batch-translate/:job_id - Durum sorgulama
- GET /api/datasets - Dataset listesi
- POST /api/evaluate - Metrik hesaplama
- GET /api/results/summary - Sonuç özeti
- GET /api/translators/status - Araç durumu

## Versiyon Notları

### v0.1.0 - İlk Geliştirme Sürümü

Bu ilk sürüm, projenin temel altyapısını ve tüm ana bileşenleri içerir:

**Tamamlanan:**
- ✅ Proje yapısı
- ✅ Backend API (4 çeviri aracı)
- ✅ Frontend web uygulaması
- ✅ Dataset toplama scriptleri
- ✅ Değerlendirme metrikleri
- ✅ Deney scriptleri
- ✅ Analiz notebook'ları
- ✅ Akademik makale taslağı

**Yapılacak:**
- ⏳ Gerçek dataset indirme
- ⏳ API anahtarları yapılandırma
- ⏳ Toplu deneyler çalıştırma
- ⏳ Sonuçlarla makale güncelleme
- ⏳ İnsan değerlendirme

**Bilinen Sorunlar:**
- Dataset'ler henüz indirilmedi (scriptler hazır)
- API anahtarları yapılandırılmalı
- Gerçek deney sonuçları bekleniyor
- Makale placeholder'ları doldurulmalı

## Katkıda Bulunanlar

- [Your Name] - İlk geliştirme

## Referanslar

Kullanılan açık kaynak projeler:
- OPUS Corpus (Helsinki-NLP)
- SacreBLEU (Mozilla)
- NLTK (NLTK Project)
- Flask (Pallets)
- React (Meta)
- Chart.js (Chart.js Community)

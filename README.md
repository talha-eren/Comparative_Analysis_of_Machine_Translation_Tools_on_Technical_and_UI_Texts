# Teknik ve UI Metinlerinde Makine Çeviri Araçlarının Karşılaştırmalı Analizi

## Proje Hakkında

Bu proje, yazılım lokalizasyonunda kullanılan makine çeviri araçlarının (Google Translate, DeepL, Microsoft Translator, Amazon Translate) performansını teknik dokümantasyon ve UI metinleri üzerinde karşılaştırmaktadır.

### Amaçlar

- Farklı makine çeviri araçlarının İngilizce-Türkçe çeviri kalitesini ölçmek
- Teknik dokümantasyon ve UI metinlerinde performans farklarını analiz etmek
- Yazılım geliştiriciler için pratik araç seçim önerileri sunmak
- Türkçe odaklı yazılım çeviri dataset'i oluşturmak
- Akademik makale yayınlamak

## Özellikler

- **Çoklu Araç Karşılaştırması**: 4 farklı çeviri aracını aynı anda test edin
- **Kapsamlı Dataset**: 50,000+ segment teknik ve UI metni
- **Otomatik Değerlendirme**: BLEU, METEOR, TER, chrF++ metrikleri
- **İnteraktif Web Arayüzü**: Canlı çeviri karşılaştırma ve analiz dashboard
- **Toplu Test**: Dataset'ler üzerinde otomatik deneyler
- **Görselleştirme**: Detaylı grafikler ve karşılaştırma tabloları
- **Export**: Sonuçları CSV, JSON, PDF formatında indirin

## Dataset Kaynakları

### Teknik Dokümantasyon Dataset'leri

1. **OPUS GNOME Corpus** (~10,000 segment)
   - Kaynak: https://opus.nlpl.eu/GNOME.php
   - İçerik: GNOME masaüstü dokümantasyonu
   - Dil: EN-TR paralel

2. **OPUS KDE Corpus** (~8,000 segment)
   - Kaynak: https://opus.nlpl.eu/KDE4.php
   - İçerik: KDE sistem dokümantasyonu

3. **SAP Software Documentation** (~4,000 segment)
   - Kaynak: https://github.com/SAP/software-documentation-data-set-for-machine-translation
   - İçerik: SAP yazılım dokümantasyonu
   - Lisans: CC BY-NC 4.0

4. **GitHub Türk Projeleri** (~3,000 segment)
   - README.md dosyaları
   - API dokümantasyonları

### UI String Dataset'leri

1. **Mozilla Firefox i18n** (~6,000 segment)
   - Kaynak: https://opus.nlpl.eu/Mozilla-I10n.php
   - İçerik: Firefox tarayıcısı UI metinleri
   - Lisans: Mozilla Public License 2.0

2. **Common UI Translations** (~4,000 segment)
   - Kaynak: https://github.com/deviro/common-ui-translations
   - İçerik: Yaygın UI string'leri (buton, form, hata mesajları)
   - Format: JSON

3. **GitHub i18n Dosyaları** (~5,000 segment)
   - Popüler Türk projelerinin i18n dosyaları

### Türkçe-İngilizce Paralel Korpus

1. **MaCoCu TR-EN Corpus** (~10,000 segment - filtrelenmiş)
   - Kaynak: https://www.clarin.si/repository/xmlui/handle/11356/1816
   - İçerik: 1.6M segment'ten teknik içerik filtrelemesi
   - Boyut: 89M kelime

**Toplam Dataset: ~50,000 segment**

## Teknoloji Stack

### Backend
- **Framework**: Flask 3.0
- **Dil**: Python 3.9+
- **Çeviri API'leri**: 
  - Google Cloud Translation API
  - DeepL API
  - Microsoft Azure Translator
  - Amazon Translate
- **Değerlendirme**: SacreBLEU, NLTK
- **Veri İşleme**: Pandas, OpusTools

### Frontend
- **Framework**: React 18
- **Dil**: JavaScript/JSX
- **Styling**: Tailwind CSS
- **Grafik**: Chart.js, Recharts
- **HTTP Client**: Axios
- **Routing**: React Router

### Analiz
- **Notebook**: Jupyter
- **Görselleştirme**: Matplotlib, Seaborn
- **İstatistik**: SciPy, NumPy

## Kurulum

### Gereksinimler

- Python 3.9 veya üzeri
- Node.js 18 veya üzeri
- npm veya yarn
- Git

### Backend Kurulumu

```bash
# Virtual environment oluştur
cd backend
python -m venv venv

# Virtual environment'ı aktifleştir
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# NLTK verilerini indir
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"

# Çevre değişkenlerini ayarla
cp .env.example .env
# .env dosyasını düzenleyip API anahtarlarınızı ekleyin

# Flask uygulamasını çalıştır
python app.py
```

Backend http://localhost:5000 adresinde çalışacaktır.

### Frontend Kurulumu

```bash
# Frontend klasörüne git
cd frontend

# Bağımlılıkları yükle
npm install

# Geliştirme sunucusunu başlat
npm run dev
```

Frontend http://localhost:5173 adresinde çalışacaktır.

## API Anahtarları

Projeyi çalıştırmak için aşağıdaki API anahtarlarına ihtiyacınız var:

### 1. Google Cloud Translation API
- Google Cloud Console'a gidin: https://console.cloud.google.com
- Yeni proje oluşturun
- Cloud Translation API'yi etkinleştirin
- Service account oluşturup JSON key indirin
- `.env` dosyasına ekleyin

### 2. DeepL API
- DeepL hesabı oluşturun: https://www.deepl.com/pro-api
- API key alın (Free tier: 500,000 karakter/ay)
- `.env` dosyasına ekleyin

### 3. Microsoft Azure Translator
- Azure hesabı oluşturun: https://azure.microsoft.com
- Translator resource oluşturun
- Key ve region bilgilerini alın
- `.env` dosyasına ekleyin

### 4. Amazon Translate
- AWS hesabı oluşturun: https://aws.amazon.com
- IAM user oluşturup Translate yetkisi verin
- Access key ve secret key alın
- `.env` dosyasına ekleyin

## Kullanım

### 1. Canlı Çeviri Karşılaştırma

1. Ana sayfadan "Karşılaştır" sayfasına gidin
2. Çevirmek istediğiniz metni girin
3. Kaynak ve hedef dili seçin (EN → TR)
4. Metin tipini seçin (Teknik/UI/Hata Mesajı)
5. Çeviri araçlarını seçin (tümü veya belirli araçlar)
6. "Çevir" butonuna tıklayın
7. Sonuçları yan yana görüntüleyin ve metrik skorlarını inceleyin

### 2. Toplu Test

1. "Toplu Test" sayfasına gidin
2. Test etmek istediğiniz dataset'i seçin
3. Çeviri araçlarını seçin
4. Örnek sayısını belirleyin (1,000 - 10,000)
5. "Testi Başlat" butonuna tıklayın
6. İlerlemeyi takip edin
7. Test tamamlandığında sonuçları indirin

### 3. Sonuç Analizi

1. "Sonuçlar" sayfasına gidin
2. Genel istatistikleri inceleyin
3. Grafikleri ve tabloları görüntüleyin
4. Filtreleme ve sıralama yapın
5. Sonuçları export edin

### 4. Dataset Gezgini

1. "Dataset" sayfasına gidin
2. Mevcut dataset'leri görüntüleyin
3. Filtreleme ve arama yapın
4. Örnek metinleri inceleyin

## Dataset İndirme

Dataset'leri indirmek için scriptleri kullanın:

```bash
# OPUS dataset'lerini indir
python scripts/download_opus.py

# GitHub'dan veri topla
python scripts/download_github.py

# MaCoCu korpusunu indir ve filtrele
python scripts/download_macocu.py

# Tüm dataset'leri işle ve birleştir
python scripts/process_datasets.py
```

## Deneyler

Toplu çeviri deneyleri yapmak için:

```bash
# 10,000 segment üzerinde tüm araçlarla test
python scripts/run_experiments.py --sample-size 10000 --tools all

# Sadece belirli araçlarla test
python scripts/run_experiments.py --sample-size 5000 --tools google deepl

# Sadece teknik dokümantasyon kategorisi
python scripts/run_experiments.py --category technical --sample-size 5000
```

## Analiz

Jupyter notebook'larla sonuçları analiz edin:

```bash
# Jupyter'i başlat
cd analysis/notebooks
jupyter notebook

# Notebook'ları açın:
# - exploratory_analysis.ipynb: Dataset istatistikleri
# - results_visualization.ipynb: Grafik ve görselleştirmeler
# - statistical_tests.ipynb: İstatistiksel testler
```

## Proje Yapısı

```
Comparative_Analysis_of_Machine_Translation_Tools/
├── data/
│   ├── raw/                      # Ham dataset'ler
│   ├── processed/                # İşlenmiş veriler
│   └── results/                  # Çeviri sonuçları
├── backend/
│   ├── app.py                    # Flask ana uygulama
│   ├── requirements.txt          # Python bağımlılıkları
│   ├── translators/              # Çeviri API wrapper'ları
│   ├── evaluators/               # Metrik hesaplama
│   ├── data_processing/          # Veri işleme
│   └── utils/                    # Yardımcı fonksiyonlar
├── frontend/
│   ├── src/
│   │   ├── components/           # React bileşenleri
│   │   ├── pages/                # Sayfalar
│   │   └── services/             # API servisleri
│   ├── package.json              # Node bağımlılıkları
│   └── tailwind.config.js        # Tailwind config
├── scripts/
│   ├── download_opus.py          # OPUS dataset indirme
│   ├── download_github.py        # GitHub veri toplama
│   ├── download_macocu.py        # MaCoCu indirme
│   ├── process_datasets.py       # Veri işleme
│   └── run_experiments.py        # Toplu deneyler
├── analysis/
│   └── notebooks/                # Jupyter notebook'lar
├── paper/
│   ├── main.tex                  # LaTeX ana dosya
│   ├── sections/                 # Makale bölümleri
│   ├── figures/                  # Figürler
│   └── references.bib            # Kaynakça
├── .env.example                  # API anahtarları şablonu
├── .gitignore                    # Git ignore
└── README.md                     # Bu dosya
```

## API Endpoint'leri

### POST /api/translate
Tekil metin çevirisi

**Request:**
```json
{
  "text": "Click here to continue",
  "source_lang": "en",
  "target_lang": "tr",
  "translators": ["google", "deepl", "microsoft", "amazon"]
}
```

**Response:**
```json
{
  "translations": {
    "google": "Devam etmek için buraya tıklayın",
    "deepl": "Devam etmek için buraya tıklayın",
    "microsoft": "Devam etmek için buraya tıklayın",
    "amazon": "Devam etmek için buraya tıklayın"
  },
  "metrics": {
    "google": {"bleu": 0.85, "meteor": 0.78, "ter": 0.15, "chrf": 0.82},
    "deepl": {"bleu": 0.88, "meteor": 0.81, "ter": 0.12, "chrf": 0.85},
    "microsoft": {"bleu": 0.82, "meteor": 0.76, "ter": 0.18, "chrf": 0.80},
    "amazon": {"bleu": 0.80, "meteor": 0.75, "ter": 0.20, "chrf": 0.78}
  },
  "time_taken": {
    "google": 120,
    "deepl": 150,
    "microsoft": 110,
    "amazon": 130
  }
}
```

### POST /api/batch-translate
Toplu çeviri işlemi başlatma

**Request:**
```json
{
  "dataset_id": "technical_docs",
  "translators": ["google", "deepl"],
  "sample_size": 1000
}
```

**Response:**
```json
{
  "job_id": "job_123456",
  "status": "processing",
  "estimated_time_seconds": 1200
}
```

### GET /api/batch-translate/:job_id
Toplu çeviri durumu sorgulama

**Response:**
```json
{
  "job_id": "job_123456",
  "status": "completed",
  "progress": 100,
  "results_url": "/api/results/job_123456"
}
```

### GET /api/datasets
Mevcut dataset'leri listeleme

**Response:**
```json
{
  "technical": [
    {
      "id": "gnome_docs",
      "name": "GNOME Documentation",
      "segments": 10000,
      "source": "OPUS"
    }
  ],
  "ui": [
    {
      "id": "mozilla_ui",
      "name": "Mozilla Firefox UI Strings",
      "segments": 6000,
      "source": "Mozilla-I10n"
    }
  ],
  "stats": {
    "total_segments": 50000,
    "categories": 3
  }
}
```

### POST /api/evaluate
Çeviri değerlendirme

**Request:**
```json
{
  "translation": "Devam etmek için buraya tıklayın",
  "reference": "Devam etmek için buraya tıklayın"
}
```

**Response:**
```json
{
  "bleu": 1.0,
  "meteor": 1.0,
  "ter": 0.0,
  "chrf": 1.0
}
```

### GET /api/results/summary
Genel sonuç özeti

**Response:**
```json
{
  "total_translations": 10000,
  "average_scores": {
    "google": {"bleu": 0.75, "meteor": 0.70},
    "deepl": {"bleu": 0.80, "meteor": 0.75},
    "microsoft": {"bleu": 0.73, "meteor": 0.68},
    "amazon": {"bleu": 0.72, "meteor": 0.67}
  },
  "best_tool": "deepl",
  "category_breakdown": {
    "technical": {...},
    "ui": {...}
  }
}
```

## Değerlendirme Metrikleri

### BLEU (Bilingual Evaluation Understudy)
- N-gram overlap tabanlı metrik
- 0-1 arası skor (1 = mükemmel)
- En yaygın kullanılan metrik

### METEOR (Metric for Evaluation of Translation with Explicit Ordering)
- Eş anlamlı kelime desteği
- Recall odaklı
- BLEU'ya göre daha esnek

### TER (Translation Error Rate)
- Düzenleme mesafesi tabanlı
- Düşük skor = daha iyi (0 = mükemmel)
- İnsan düzenlemelerini simüle eder

### chrF++ (Character n-gram F-score)
- Karakter seviyesi benzerlik
- Morfolojik zengin diller için uygun
- Türkçe için özellikle yararlı

## Karşılaştırılan Araçlar

### Google Translate
- **Avantajlar**: Ücretsiz tier, 100+ dil, hızlı
- **Dezavantajlar**: Bazen literal çeviri
- **Maliyet**: $20/1M karakter (free tier: 500K/ay)

### DeepL
- **Avantajlar**: Yüksek kalite, doğal çeviri
- **Dezavantajlar**: Daha az dil desteği, ücretli
- **Maliyet**: $25/1M karakter (free tier: 500K/ay)

### Microsoft Translator
- **Avantajlar**: Azure entegrasyonu, özel terminoloji
- **Dezavantajlar**: Kurulum karmaşık
- **Maliyet**: $10/1M karakter (free tier: 2M/ay)

### Amazon Translate
- **Avantajlar**: AWS entegrasyonu, ölçeklenebilir
- **Dezavantajlar**: Daha az popüler
- **Maliyet**: $15/1M karakter (free tier: 2M/ay)

## Beklenen Sonuçlar

### Hipotezler

1. **DeepL** genel çeviri kalitesinde en yüksek BLEU skorunu alacak
2. **Google Translate** hız ve maliyet açısından en avantajlı olacak
3. **Microsoft Translator** teknik terminolojide tutarlı olacak
4. **UI string'leri** teknik dokümantasyondan daha düşük skor alacak (bağlam eksikliği)
5. Kısa metinler (UI) uzun metinlerden (teknik) daha zor çevrilecek

### Araştırma Soruları

- **RQ1**: Hangi makine çeviri aracı teknik dokümantasyon çevirisinde en iyi performansı gösterir?
- **RQ2**: UI string çevirisinde araçlar arasında anlamlı performans farkı var mı?
- **RQ3**: Metin uzunluğu çeviri kalitesini nasıl etkiler?
- **RQ4**: Teknik terminoloji hangi araç tarafından daha tutarlı çevrilir?
- **RQ5**: Placeholder ve özel karakterler hangi araç tarafından daha iyi korunur?
- **RQ6**: Maliyet-kalite dengesi açısından hangi araç daha avantajlı?

## Katkıda Bulunma

Bu açık kaynak bir projedir. Katkılarınızı bekliyoruz!

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## İletişim

Sorularınız için issue açabilirsiniz.

## Teşekkürler

Bu proje aşağıdaki açık kaynak projeleri ve dataset'leri kullanmaktadır:

- OPUS Corpus (Helsinki-NLP)
- Mozilla Firefox Localization
- SAP Software Documentation Dataset
- Salesforce Localization Dataset
- Common UI Translations
- MaCoCu Turkish-English Corpus
- SacreBLEU
- NLTK

## Referanslar

### Dataset'ler
- OPUS: https://opus.nlpl.eu/
- SAP Dataset: https://github.com/SAP/software-documentation-data-set-for-machine-translation
- Salesforce Dataset: https://github.com/salesforce/localization-xml-mt
- Mozilla L10n: https://github.com/mozilla-l10n/firefox-l10n-source
- Common UI: https://github.com/deviro/common-ui-translations
- MaCoCu: https://www.clarin.si/repository/xmlui/handle/11356/1816

### Araçlar
- SacreBLEU: https://github.com/mozilla/sacreBLEU
- OpusTools: https://github.com/Helsinki-NLP/OpusTools
- NLTK: https://www.nltk.org/

### Makaleler
- Papineni et al. (2002): BLEU: a method for automatic evaluation of machine translation
- Banerjee & Lavie (2005): METEOR: An Automatic Metric for MT Evaluation
- Snover et al. (2006): A Study of Translation Edit Rate

## Durum

- ✅ Proje yapısı oluşturuldu
- ⏳ Dataset'ler indiriliyor
- ⏳ Backend geliştiriliyor
- ⏳ Frontend geliştiriliyor
- ⏳ Deneyler yapılıyor
- ⏳ Makale yazılıyor

## Versiyon

v0.1.0 - İlk geliştirme versiyonu

# Hızlı Başlangıç Rehberi

Bu rehber projeyi hızlıca çalıştırmanız için adım adım talimatlar içerir.

## Ön Gereksinimler

- Python 3.9 veya üzeri
- Node.js 18 veya üzeri
- Git

## Adım 1: Projeyi Klonlayın

```bash
git clone <repository-url>
cd Comparative_Analysis_of_Machine_Translation_Tools_on_Technical_and_UI_Texts
```

## Adım 2: Backend Kurulumu

### 2.1 Virtual Environment Oluşturun

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 2.2 Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 2.3 NLTK Verilerini İndirin

```bash
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```

### 2.4 API Anahtarlarını Ayarlayın

1. `.env.example` dosyasını `.env` olarak kopyalayın:
```bash
cp .env.example .env
```

2. `.env` dosyasını düzenleyin ve API anahtarlarınızı ekleyin:

```env
# Google Cloud Translation
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json

# DeepL
DEEPL_API_KEY=your_deepl_api_key

# Microsoft Azure
AZURE_TRANSLATOR_KEY=your_azure_key
AZURE_TRANSLATOR_REGION=your_region

# Amazon AWS
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
```

**Not:** En az bir API anahtarı gereklidir. Ücretsiz tier'lar:
- Google: 500K karakter/ay
- DeepL: 500K karakter/ay
- Microsoft: 2M karakter/ay
- Amazon: 2M karakter/ay (12 ay)

## Adım 3: Dataset'leri İndirin

### 3.1 OPUS Dataset'leri

```bash
python scripts/download_opus.py
```

Bu script şunları indirir:
- GNOME dokümantasyonu (~10K segment)
- KDE sistem mesajları (~8K segment)
- Mozilla Firefox UI strings (~6K segment)

**Süre:** 10-30 dakika (internet hızına bağlı)

### 3.2 GitHub Veri Toplama (Opsiyonel)

```bash
python scripts/download_github.py
```

**Not:** GitHub token olmadan rate limit düşüktür. Token için:
1. https://github.com/settings/tokens adresine gidin
2. "Generate new token" → "classic"
3. `repo` yetkisi verin
4. Token'ı `.env` dosyasına ekleyin: `GITHUB_TOKEN=your_token`

### 3.3 MaCoCu Korpusu (Opsiyonel)

```bash
python scripts/download_macocu.py
```

**Not:** Bu çok büyük bir dataset (~2GB). Manuel indirme önerilir:
1. https://www.clarin.si/repository/xmlui/handle/11356/1816
2. `MaCoCu-tr-en.sent.txt.gz` dosyasını indirin
3. `data/raw/macocu/` klasörüne koyun
4. Scripti tekrar çalıştırın

### 3.4 Dataset'leri İşleyin

```bash
python scripts/process_datasets.py
```

Bu script:
- Tüm dataset'leri birleştirir
- Duplikasyonları temizler
- Kategorilere ayırır (technical, ui, error)
- Train/test split yapar (%80/%20)
- İstatistikleri hesaplar

**Çıktı:** `data/processed/` klasöründe JSON dosyaları

## Adım 4: Backend'i Başlatın

```bash
cd backend
python app.py
```

Backend http://localhost:5000 adresinde çalışacaktır.

**Test edin:**
```bash
curl http://localhost:5000/
```

## Adım 5: Frontend Kurulumu

Yeni bir terminal açın:

```bash
cd frontend
npm install
```

**Süre:** 2-5 dakika

## Adım 6: Frontend'i Başlatın

```bash
npm run dev
```

Frontend http://localhost:5173 adresinde çalışacaktır.

Tarayıcınızda açın: http://localhost:5173

## Adım 7: İlk Çeviriyi Yapın

1. "Karşılaştır" sayfasına gidin
2. Örnek metin girin veya "Örnek Yükle" butonuna tıklayın
3. Çeviri araçlarını seçin
4. "Çevir" butonuna tıklayın
5. Sonuçları görüntüleyin

## Adım 8: Toplu Test (Opsiyonel)

1. "Toplu Test" sayfasına gidin
2. Dataset seçin (örn: test_set)
3. Araçları seçin
4. Örnek sayısı belirleyin (başlangıç için 100-500 önerilir)
5. "Testi Başlat" butonuna tıklayın
6. İlerlemeyi takip edin

**Not:** İlk test küçük bir örnekle yapın (100-500 segment) çünkü:
- API maliyeti oluşur
- Zaman alır (~1-5 dakika)

## Sorun Giderme

### Backend Başlamıyor

**Hata:** `ModuleNotFoundError`
**Çözüm:** Virtual environment'ı aktifleştirin ve bağımlılıkları yükleyin

**Hata:** `API key not found`
**Çözüm:** `.env` dosyasını kontrol edin, en az bir API anahtarı ekleyin

### Frontend Başlamıyor

**Hata:** `Cannot find module`
**Çözüm:** `npm install` komutunu tekrar çalıştırın

**Hata:** `Port 5173 already in use`
**Çözüm:** Portu değiştirin veya çalışan uygulamayı kapatın

### Dataset İndirme Hataları

**Hata:** `OpusTools not found`
**Çözüm:** 
```bash
pip install opustools
```

**Hata:** `Connection timeout`
**Çözüm:** İnternet bağlantınızı kontrol edin, tekrar deneyin

### API Hataları

**Hata:** `401 Unauthorized`
**Çözüm:** API anahtarlarınızı kontrol edin

**Hata:** `429 Too Many Requests`
**Çözüm:** Rate limit aşıldı, birkaç dakika bekleyin

## Minimum Çalışma Konfigürasyonu

Sadece test etmek istiyorsanız:

1. **Sadece Google Translate** kullanın (ücretsiz tier)
2. **Küçük dataset** ile başlayın (1,000 segment)
3. **Manuel veri** ekleyin (kendi metinleriniz)

```bash
# Minimum setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install flask flask-cors python-dotenv requests google-cloud-translate sacrebleu nltk

# .env dosyasına sadece Google credentials ekleyin
# Backend'i başlatın
python app.py
```

## Sonraki Adımlar

1. **Dataset'leri keşfedin:** "Dataset" sayfasından mevcut verileri inceleyin
2. **Çeviriler yapın:** "Karşılaştır" sayfasından farklı metinler test edin
3. **Toplu test çalıştırın:** Daha büyük örneklerle deneyler yapın
4. **Sonuçları analiz edin:** Jupyter notebook'larla detaylı analiz
5. **Makaleyi tamamlayın:** Gerçek sonuçlarla LaTeX dosyasını güncelleyin

## Yardım

Sorun yaşarsanız:
1. README.md dosyasını okuyun
2. GitHub Issues açın
3. Dokümantasyonu kontrol edin

## Hızlı Komutlar

```bash
# Backend başlat
cd backend && python app.py

# Frontend başlat
cd frontend && npm run dev

# Dataset indir
python scripts/download_opus.py

# Dataset işle
python scripts/process_datasets.py

# Deney çalıştır
python scripts/run_experiments.py --sample-size 1000 --tools google deepl

# Jupyter başlat
cd analysis/notebooks && jupyter notebook
```

## Başarılı Kurulum Kontrolü

Eğer şunları görüyorsanız kurulum başarılı:

✓ Backend: http://localhost:5000 açılıyor
✓ Frontend: http://localhost:5173 açılıyor
✓ En az 1 çeviri aracı "Aktif" görünüyor
✓ Dataset'ler yüklendi mesajı görünüyor

Başarılar!

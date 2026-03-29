# Kurulum Rehberi

## Adım Adım Kurulum

### 1. Sistem Gereksinimleri

#### Yazılım Gereksinimleri
- Python 3.9 veya üzeri
- Node.js 18 veya üzeri
- npm veya yarn
- Git
- 5GB boş disk alanı

#### İşletim Sistemi
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+)

### 2. Python Sanal Ortam Kurulumu

#### Windows
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Linux/Mac
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 3. Python Bağımlılıkları

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Kurulum süresi:** 5-10 dakika

**Kurulacak paketler:**
- Flask 3.0.0 - Web framework
- google-cloud-translate 3.12.0 - Google API
- deepl 1.16.0 - DeepL API
- azure-ai-translation-text 1.0.0 - Microsoft API
- boto3 1.28.0 - Amazon API
- sacrebleu 2.6.0 - Metrikler
- nltk 3.8.1 - METEOR metriği
- pandas 2.1.0 - Veri işleme
- Ve daha fazlası...

### 4. NLTK Veri İndirme

```bash
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```

### 5. API Anahtarları Yapılandırma

#### 5.1 .env Dosyası Oluşturma

```bash
cp .env.example .env
```

`.env` dosyasını bir metin editörü ile açın.

#### 5.2 Google Cloud Translation API

**Adımlar:**
1. https://console.cloud.google.com adresine gidin
2. Yeni proje oluşturun veya mevcut projeyi seçin
3. "APIs & Services" → "Enable APIs and Services"
4. "Cloud Translation API" arayın ve etkinleştirin
5. "Credentials" → "Create Credentials" → "Service Account"
6. Service account oluşturun
7. "Keys" → "Add Key" → "Create new key" → JSON
8. İndirilen JSON dosyasını projeye koyun
9. `.env` dosyasına ekleyin:

```env
GOOGLE_APPLICATION_CREDENTIALS=path/to/your-credentials.json
```

**Ücretsiz Tier:** 500,000 karakter/ay

#### 5.3 DeepL API

**Adımlar:**
1. https://www.deepl.com/pro-api adresine gidin
2. Hesap oluşturun (ücretsiz tier mevcut)
3. API key alın
4. `.env` dosyasına ekleyin:

```env
DEEPL_API_KEY=your-deepl-api-key-here
```

**Ücretsiz Tier:** 500,000 karakter/ay

#### 5.4 Microsoft Azure Translator

**Adımlar:**
1. https://azure.microsoft.com adresine gidin
2. Azure hesabı oluşturun (kredi kartı gerekli, ama ücretsiz tier var)
3. "Create a resource" → "Translator"
4. Resource oluşturun
5. "Keys and Endpoint" bölümünden bilgileri alın
6. `.env` dosyasına ekleyin:

```env
AZURE_TRANSLATOR_KEY=your-azure-key
AZURE_TRANSLATOR_REGION=your-region
AZURE_TRANSLATOR_ENDPOINT=https://api.cognitive.microsofttranslator.com
```

**Ücretsiz Tier:** 2M karakter/ay

#### 5.5 Amazon Translate

**Adımlar:**
1. https://aws.amazon.com adresine gidin
2. AWS hesabı oluşturun
3. IAM → Users → Add user
4. "Programmatic access" seçin
5. "TranslateFullAccess" yetkisi verin
6. Access key ve secret key'i kaydedin
7. `.env` dosyasına ekleyin:

```env
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
```

**Ücretsiz Tier:** 2M karakter/ay (12 ay)

### 6. Frontend Kurulumu

```bash
cd frontend
npm install
```

**Kurulum süresi:** 2-5 dakika

**Kurulacak paketler:**
- React 18.2.0
- React Router 6.20.0
- Axios 1.6.0
- Chart.js 4.4.0
- Tailwind CSS 3.4.0
- Vite 5.0.8

### 7. Dataset İndirme

#### Minimum Kurulum (Test için)

Sadece test etmek istiyorsanız, küçük bir örnek dataset oluşturun:

```bash
# Örnek dataset oluştur
mkdir -p data/processed
```

`data/processed/test_set.json` dosyasını oluşturun:

```json
[
  {
    "id": "test_001",
    "source_text": "Click here to continue",
    "target_text": "Devam etmek için buraya tıklayın",
    "category": "ui",
    "source_lang": "en",
    "target_lang": "tr",
    "length": 22,
    "source": "manual"
  }
]
```

#### Tam Kurulum

```bash
# OPUS dataset'leri indir (önerilen)
python scripts/download_opus.py

# GitHub veri topla (opsiyonel)
python scripts/download_github.py

# MaCoCu korpusu (opsiyonel, büyük)
python scripts/download_macocu.py

# Tüm dataset'leri işle
python scripts/process_datasets.py
```

**Süre:** 1-3 saat (internet hızına bağlı)

### 8. Uygulamayı Başlatma

#### Backend

Terminal 1:
```bash
cd backend
python app.py
```

Çıktı:
```
============================================================
Çeviri Araçları Başlatılıyor
============================================================

✓ Google Translate hazır
✓ DeepL hazır
✓ Microsoft Translator hazır
✓ Amazon Translate hazır

✓ 4/4 araç kullanılabilir
Kullanılabilir araçlar: google, deepl, microsoft, amazon

============================================================
Flask Backend Başlatılıyor
============================================================
URL: http://localhost:5000
Kullanılabilir araçlar: 4
============================================================

 * Running on http://0.0.0.0:5000
```

#### Frontend

Terminal 2:
```bash
cd frontend
npm run dev
```

Çıktı:
```
  VITE v5.0.8  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 9. İlk Test

1. Tarayıcınızda http://localhost:5173 açın
2. "Karşılaştır" sayfasına gidin
3. Örnek metin girin: "The function returns a promise"
4. "Örnek Yükle" butonunu kullanabilirsiniz
5. Çeviri araçlarını seçin (en az birini)
6. "Çevir" butonuna tıklayın
7. Sonuçları görüntüleyin

### 10. Doğrulama

#### Backend Testi
```bash
curl http://localhost:5000/
curl http://localhost:5000/api/translators/status
```

Başarılı yanıt:
```json
{
  "google": {"available": true, "name": "Google Translate"},
  "deepl": {"available": true, "name": "DeepL"},
  ...
}
```

#### Frontend Testi
Tarayıcıda http://localhost:5173 açıldığında ana sayfa görünmelidir.

---

## Sorun Giderme

### Backend Sorunları

#### "ModuleNotFoundError: No module named 'flask'"
**Çözüm:**
```bash
# Virtual environment aktif mi kontrol edin
# Windows: (venv) prompt'ta görünmeli
# Tekrar yükleyin:
pip install -r requirements.txt
```

#### "GOOGLE_APPLICATION_CREDENTIALS not set"
**Çözüm:**
- `.env` dosyasını oluşturdunuz mu?
- Credentials path doğru mu?
- Dosya var mı?

#### "No module named 'google.cloud'"
**Çözüm:**
```bash
pip install google-cloud-translate
```

### Frontend Sorunları

#### "Cannot find module 'react'"
**Çözüm:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### "Port 5173 is already in use"
**Çözüm:**
```bash
# Portu değiştirin
npm run dev -- --port 3000
```

### Dataset Sorunları

#### "OpusTools not found"
**Çözüm:**
```bash
pip install opustools
```

#### "Dataset file not found"
**Çözüm:**
- Dataset'leri indirdiniz mi?
- `python scripts/download_opus.py` çalıştırın
- Veya manuel örnek dataset oluşturun

### API Sorunları

#### "401 Unauthorized"
**Çözüm:**
- API anahtarları doğru mu?
- `.env` dosyası backend klasöründe mi?
- API servisleri aktif mi?

#### "429 Too Many Requests"
**Çözüm:**
- Rate limit aşıldı
- 1-5 dakika bekleyin
- Free tier limitlerini kontrol edin

---

## Minimum Çalışma Konfigürasyonu

Sadece test amaçlı, minimum kurulum:

### Backend (Sadece Google Translate)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install flask flask-cors python-dotenv requests google-cloud-translate sacrebleu nltk
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```

`.env` dosyası:
```env
GOOGLE_APPLICATION_CREDENTIALS=your-credentials.json
FLASK_SECRET_KEY=test-secret-key
```

Manuel test dataset (`data/processed/test_set.json`):
```json
[
  {
    "id": "test_001",
    "source_text": "Click here to save",
    "target_text": "Kaydetmek için buraya tıklayın",
    "category": "ui",
    "source_lang": "en",
    "target_lang": "tr",
    "length": 19,
    "source": "manual",
    "metadata": {}
  }
]
```

### Frontend (Basit)

```bash
cd frontend
npm install react react-dom react-router-dom axios
npm run dev
```

---

## Başarılı Kurulum Kontrol Listesi

- [ ] Python 3.9+ kurulu
- [ ] Node.js 18+ kurulu
- [ ] Virtual environment oluşturuldu
- [ ] Python bağımlılıkları yüklendi
- [ ] NLTK verileri indirildi
- [ ] `.env` dosyası oluşturuldu
- [ ] En az 1 API anahtarı yapılandırıldı
- [ ] Frontend bağımlılıkları yüklendi
- [ ] Backend başlatıldı (http://localhost:5000)
- [ ] Frontend başlatıldı (http://localhost:5173)
- [ ] API status endpoint çalışıyor
- [ ] En az 1 araç "available: true"
- [ ] İlk çeviri testi başarılı

---

## Sonraki Adımlar

1. ✅ Kurulum tamamlandı
2. 🔄 Dataset'leri indirin
3. 🔄 İlk testleri yapın
4. 🔄 Toplu deneyler çalıştırın
5. 🔄 Sonuçları analiz edin
6. 🔄 Makaleyi tamamlayın

---

## Yardım ve Destek

- **Dokümantasyon**: README.md, QUICK_START.md
- **API Dokümantasyonu**: README.md "API Endpoint'leri" bölümü
- **Dataset Bilgisi**: DATASET_SOURCES.md
- **Katkı**: CONTRIBUTING.md
- **Sorunlar**: GitHub Issues

---

## Başarılar!

Kurulum tamamlandıktan sonra, kapsamlı bir makine çeviri karşılaştırma sisteminiz olacak. İyi çalışmalar!

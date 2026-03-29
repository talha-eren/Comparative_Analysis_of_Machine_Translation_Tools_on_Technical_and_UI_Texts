# Ücretsiz API Anahtarları Nasıl Alınır?

## Hızlı Başlangıç - Sadece DeepL ile Test

En hızlı yol: Sadece DeepL API ile başlayın (5 dakika)

### DeepL API (ÜCRETSİZ - En Kolay)

1. **Kayıt olun:**
   - https://www.deepl.com/pro-api?cta=header-pro-api adresine gidin
   - "Sign up for free" tıklayın
   - Email ve şifre ile kayıt olun

2. **API Key alın:**
   - Email'inizi onaylayın
   - Giriş yapın
   - Account > API Keys bölümüne gidin
   - API Key'inizi kopyalayın (örn: `abc123def-456g-789h-ijk0-lmnopqrstuv:fx`)

3. **.env dosyasını güncelleyin:**
   ```
   DEEPL_API_KEY=abc123def-456g-789h-ijk0-lmnopqrstuv:fx
   ```

4. **Backend'i yeniden başlatın**

✅ **Ücretsiz Limit:** 500,000 karakter/ay  
✅ **Kredi kartı:** Gerekli DEĞİL  
✅ **Kurulum süresi:** 5 dakika

---

## Tüm API'ler için Detaylı Rehber

### 1. Google Cloud Translation

**Ücretsiz:** $300 kredi (90 gün) + 500K karakter/ay

**Adımlar:**
1. https://console.cloud.google.com
2. Yeni proje oluştur
3. "Cloud Translation API" etkinleştir
4. Service Account oluştur
5. JSON key indir
6. `.env` dosyasına ekle:
   ```
   GOOGLE_CLOUD_PROJECT_ID=proje-adi
   GOOGLE_APPLICATION_CREDENTIALS=./google-key.json
   ```

**Video Rehber:** https://www.youtube.com/results?search_query=google+cloud+translation+api+setup

---

### 2. Microsoft Azure Translator

**Ücretsiz:** 2 milyon karakter/ay

**Adımlar:**
1. https://portal.azure.com
2. "Create a resource" > "Translator"
3. Pricing tier: **F0 (Free)**
4. Keys and Endpoint'ten key al
5. `.env` dosyasına ekle:
   ```
   AZURE_TRANSLATOR_KEY=your-key-here
   AZURE_TRANSLATOR_REGION=westeurope
   ```

**Not:** Kredi kartı gerekli ama ücretlendirilmez

---

### 3. Amazon Translate

**Ücretsiz:** 2 milyon karakter/ay (12 ay)

**Adımlar:**
1. https://aws.amazon.com
2. IAM > Users > Add user
3. Programmatic access seç
4. TranslateFullAccess izni ver
5. Access Key kaydet
6. `.env` dosyasına ekle:
   ```
   AWS_ACCESS_KEY_ID=AKIA...
   AWS_SECRET_ACCESS_KEY=wJal...
   AWS_REGION=us-east-1
   ```

**Not:** Kredi kartı gerekli

---

## Önerilen Sıra

1. **İlk test için:** Sadece DeepL (5 dk, kredi kartı yok)
2. **Karşılaştırma için:** Microsoft ekle (10 dk, kredi kartı gerekli ama ücretsiz)
3. **Tam analiz için:** Google ve Amazon ekle

---

## Hızlı Komutlar

```powershell
# API'leri test et
.\backend\venv\Scripts\Activate.ps1
python scripts/test_apis.py

# Backend'i başlat
python backend/app.py

# Frontend'i başlat (başka terminal)
cd frontend
npm run dev
```

---

## Yardım

Sorun yaşarsanız:
- `API_SETUP_GUIDE.md` dosyasına bakın (detaylı rehber)
- Backend log'larını kontrol edin
- API provider'ın dokümantasyonuna bakın

**Önemli:** API anahtarlarını asla Git'e commit etmeyin! `.env` dosyası `.gitignore`'da zaten var.

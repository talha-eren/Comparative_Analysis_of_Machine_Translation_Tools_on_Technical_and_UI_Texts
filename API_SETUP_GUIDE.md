# API Kurulum Rehberi

Bu rehber, tüm çeviri API'lerini nasıl kuracağınızı adım adım açıklar.

## 1. Google Cloud Translation API

### Ücretsiz Kredi
- Yeni kullanıcılar için **$300 ücretsiz kredi** (90 gün)
- Aylık ilk 500,000 karakter ücretsiz

### Kurulum Adımları

1. **Google Cloud Console'a gidin:**
   - https://console.cloud.google.com

2. **Yeni proje oluşturun:**
   - Sol üstteki proje seçiciden "New Project"
   - Proje adı: `mt-comparison` (veya istediğiniz ad)
   - "Create" tıklayın

3. **Translation API'yi etkinleştirin:**
   - Arama çubuğuna "Cloud Translation API" yazın
   - "Enable" butonuna tıklayın

4. **Service Account oluşturun:**
   - Sol menüden "IAM & Admin" > "Service Accounts"
   - "Create Service Account" tıklayın
   - Ad: `translator-service`
   - Role: "Cloud Translation API User"
   - "Done" tıklayın

5. **JSON Key indirin:**
   - Oluşturduğunuz service account'a tıklayın
   - "Keys" sekmesine gidin
   - "Add Key" > "Create new key" > "JSON"
   - İndirilen dosyayı projenizin kök dizinine koyun

6. **.env dosyasını güncelleyin:**
   ```
   GOOGLE_CLOUD_PROJECT_ID=mt-comparison
   GOOGLE_APPLICATION_CREDENTIALS=./google-credentials.json
   ```

---

## 2. DeepL API (Zaten Çalışıyor!)

### Mevcut Durum
✅ DeepL API anahtarınız geçerli ve çalışıyor!

### Ücretsiz Plan
- Aylık 500,000 karakter ücretsiz
- Kayıt: https://www.deepl.com/pro-api

### Kontrol
`.env` dosyanızda `DEEPL_API_KEY` zaten ayarlanmış.

---

## 3. Microsoft Azure Translator

### Ücretsiz Katman
- Aylık **2 milyon karakter ücretsiz**
- Kredi kartı gerekli (ama ücretlendirilmez)

### Kurulum Adımları

1. **Azure Portal'a gidin:**
   - https://portal.azure.com
   - Microsoft hesabıyla giriş yapın

2. **Translator kaynağı oluşturun:**
   - "Create a resource" tıklayın
   - "Translator" aratın ve seçin
   - "Create" tıklayın

3. **Ayarları yapın:**
   - Subscription: Ücretsiz deneme seçin
   - Resource group: Yeni oluşturun (örn: `mt-resources`)
   - Region: `West Europe` veya `East US`
   - Name: `mt-translator`
   - Pricing tier: **Free F0** (aylık 2M karakter)
   - "Review + create" > "Create"

4. **Key ve Endpoint alın:**
   - Kaynak oluşturulduktan sonra "Go to resource"
   - Sol menüden "Keys and Endpoint"
   - KEY 1 ve LOCATION/REGION değerlerini kopyalayın

5. **.env dosyasını güncelleyin:**
   ```
   AZURE_TRANSLATOR_KEY=your_key_1_here
   AZURE_TRANSLATOR_REGION=westeurope
   AZURE_TRANSLATOR_ENDPOINT=https://api.cognitive.microsofttranslator.com
   ```

---

## 4. Amazon Translate (AWS)

### Ücretsiz Katman
- İlk 12 ay **aylık 2 milyon karakter ücretsiz**
- Kredi kartı gerekli

### Kurulum Adımları

1. **AWS Console'a gidin:**
   - https://aws.amazon.com
   - "Create an AWS Account" veya giriş yapın

2. **IAM User oluşturun:**
   - Services > IAM
   - "Users" > "Add users"
   - Username: `mt-translator-user`
   - Access type: "Programmatic access" ✓
   - "Next: Permissions"

3. **İzinleri ayarlayın:**
   - "Attach existing policies directly"
   - `TranslateFullAccess` politikasını seçin
   - "Next" > "Create user"

4. **Access Key'leri kaydedin:**
   - User oluşturulduktan sonra **Access Key ID** ve **Secret Access Key** gösterilir
   - ⚠️ Bu bilgileri bir yere kaydedin (bir daha gösterilmez!)

5. **.env dosyasını güncelleyin:**
   ```
   AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
   AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   AWS_REGION=us-east-1
   ```

---

## Hızlı Test

API anahtarlarını ekledikten sonra:

1. **Backend'i yeniden başlatın:**
   ```powershell
   # Eski process'i durdurun (Ctrl+C)
   .\backend\venv\Scripts\Activate.ps1
   python backend/app.py
   ```

2. **Frontend'i açın:**
   - http://localhost:5173
   - "Compare" sayfasına gidin
   - Bir metin girin ve çevirin

3. **API durumunu kontrol edin:**
   - Ana sayfada hangi API'lerin aktif olduğunu görebilirsiniz

---

## Maliyet Tahminleri

Bu proje için tahmini maliyetler:

| API | Ücretsiz Limit | 10K Segment Maliyeti | 50K Segment Maliyeti |
|-----|----------------|----------------------|----------------------|
| Google | 500K/ay | $0 | ~$10 |
| DeepL | 500K/ay | $0 | ~$25 |
| Microsoft | 2M/ay | $0 | $0 |
| Amazon | 2M/ay (12 ay) | $0 | $0 |

**Toplam:** Ücretsiz limitler içinde kalırsanız **$0**

---

## Sorun Giderme

### Google: "Credentials dosyası bulunamadı"
- JSON key dosyasının yolunu kontrol edin
- Dosya adını `.env`'de doğru yazdığınızdan emin olun

### Microsoft: "401 Unauthorized"
- Key'in doğru kopyalandığını kontrol edin
- Region'ın doğru olduğundan emin olun

### Amazon: "Invalid security token"
- Access Key ID ve Secret Key'i kontrol edin
- IAM user'ın TranslateFullAccess iznine sahip olduğundan emin olun

### DeepL: "403 Forbidden"
- API key'in geçerli olduğunu kontrol edin
- Ücretsiz limitinizi aşmadığınızdan emin olun

---

## Şu Anda Çalışan

✅ **Backend:** http://localhost:5000  
✅ **Frontend:** http://localhost:5173  
✅ **Dataset:** 6,116 segment (MaCoCu + örnekler)  
✅ **DeepL:** Aktif ve çalışıyor!

Diğer API'leri ekledikten sonra tüm özellikler kullanılabilir olacak.

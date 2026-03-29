# Katkıda Bulunma Rehberi

Bu projeye katkıda bulunmak istediğiniz için teşekkürler! Bu rehber, katkı sürecini kolaylaştırmak için hazırlanmıştır.

## Katkı Türleri

### 1. Dataset Katkıları
- Yeni paralel metin çiftleri ekleme
- Mevcut dataset'leri iyileştirme
- Yeni dil çiftleri ekleme
- Kalite kontrol ve hata düzeltme

### 2. Kod Katkıları
- Yeni özellikler ekleme
- Bug düzeltmeleri
- Performans iyileştirmeleri
- Dokümantasyon güncellemeleri

### 3. Çeviri API'leri
- Yeni çeviri araçları entegrasyonu
- Mevcut API wrapper'larını iyileştirme
- Hata yönetimi geliştirme

### 4. Değerlendirme Metrikleri
- Yeni metrik implementasyonları
- Metrik hesaplama optimizasyonu
- Neural metrik entegrasyonu (COMET, BERTScore)

### 5. Frontend İyileştirmeleri
- UI/UX geliştirmeleri
- Yeni görselleştirmeler
- Responsive tasarım iyileştirmeleri
- Erişilebilirlik (a11y) iyileştirmeleri

## Başlamadan Önce

1. **Issue Açın**: Büyük değişiklikler için önce issue açın ve tartışın
2. **Mevcut Issue'ları Kontrol Edin**: Belki birisi zaten üzerinde çalışıyordur
3. **Dokümantasyonu Okuyun**: README.md ve kod yorumlarını inceleyin

## Geliştirme Süreci

### 1. Fork ve Clone

```bash
# Fork edin (GitHub'da)
# Sonra klonlayın
git clone https://github.com/YOUR_USERNAME/Comparative_Analysis_of_Machine_Translation_Tools.git
cd Comparative_Analysis_of_Machine_Translation_Tools

# Upstream ekleyin
git remote add upstream https://github.com/ORIGINAL_OWNER/Comparative_Analysis_of_Machine_Translation_Tools.git
```

### 2. Branch Oluşturun

```bash
# Feature branch
git checkout -b feature/amazing-feature

# Bug fix branch
git checkout -b fix/bug-description

# Dataset branch
git checkout -b data/new-dataset
```

### 3. Değişikliklerinizi Yapın

#### Kod Standartları

**Python:**
- PEP 8 stil rehberini takip edin
- Docstring'ler ekleyin (Google style)
- Type hint'ler kullanın
- Black formatter kullanın: `black .`

**JavaScript/React:**
- ESLint kurallarını takip edin
- Functional component'ler kullanın
- PropTypes veya TypeScript kullanın
- Anlamlı değişken isimleri

#### Commit Mesajları

```bash
# Format
<type>: <kısa açıklama>

<detaylı açıklama (opsiyonel)>

# Tipler
feat: Yeni özellik
fix: Bug düzeltme
docs: Dokümantasyon
style: Formatting, noktalı virgül vb.
refactor: Kod iyileştirme
test: Test ekleme
data: Dataset ekleme/güncelleme
chore: Build, dependency güncellemeleri

# Örnekler
feat: add DeepL API integration
fix: correct BLEU calculation for empty strings
docs: update API endpoint documentation
data: add 5000 segments from Mozilla i18n
```

### 4. Test Edin

**Backend Test:**
```bash
cd backend
pytest
# veya manuel test
python app.py
# Test endpoint'leri curl ile
```

**Frontend Test:**
```bash
cd frontend
npm run lint
npm run build
# Manuel test: npm run dev
```

### 5. Commit ve Push

```bash
git add .
git commit -m "feat: add amazing feature"
git push origin feature/amazing-feature
```

### 6. Pull Request Açın

1. GitHub'da repository'nize gidin
2. "Pull Request" butonuna tıklayın
3. Değişikliklerinizi açıklayın:
   - Ne yaptınız?
   - Neden yaptınız?
   - Nasıl test ettiniz?
4. Screenshot ekleyin (UI değişiklikleri için)
5. "Create Pull Request"

## Pull Request Şablonu

```markdown
## Açıklama
[Değişikliğin kısa açıklaması]

## Motivasyon ve Bağlam
[Neden bu değişiklik gerekli?]

## Değişiklik Tipi
- [ ] Bug fix
- [ ] Yeni özellik
- [ ] Breaking change
- [ ] Dokümantasyon güncellemesi
- [ ] Dataset ekleme

## Test Edildi mi?
- [ ] Evet, manuel test
- [ ] Evet, otomatik test
- [ ] Hayır

## Test Adımları
1. [Adım 1]
2. [Adım 2]
3. [Adım 3]

## Checklist
- [ ] Kod PEP 8 / ESLint standartlarına uygun
- [ ] Docstring/comment'ler eklendi
- [ ] Test edildi
- [ ] Dokümantasyon güncellendi (gerekirse)
- [ ] CHANGELOG.md güncellendi (gerekirse)

## Screenshot (UI değişiklikleri için)
[Ekran görüntüsü]
```

## Özel Katkı Alanları

### Dataset Katkısı

Yeni dataset eklemek için:

1. `data/raw/your_dataset/` klasörü oluşturun
2. JSON formatında veri ekleyin:
```json
[
  {
    "id": "unique_id",
    "source_text": "English text",
    "target_text": "Türkçe metin",
    "category": "technical|ui|error",
    "source_lang": "en",
    "target_lang": "tr",
    "source": "dataset_name"
  }
]
```
3. `scripts/process_datasets.py` dosyasını güncelleyin
4. Pull request açın

### Yeni Çeviri Aracı Ekleme

1. `backend/translators/new_tool_translator.py` oluşturun
2. `BaseTranslator` sınıfından türetin
3. `translate()` ve `batch_translate()` metodlarını implement edin
4. `backend/translators/__init__.py` dosyasına ekleyin
5. `backend/app.py` dosyasında initialize edin
6. Frontend'de araç seçeneklerine ekleyin

### Yeni Metrik Ekleme

1. `backend/evaluators/new_metric.py` oluşturun
2. Metrik hesaplama fonksiyonunu yazın
3. `backend/evaluators/__init__.py` dosyasına ekleyin
4. API endpoint'lerinde kullanın
5. Frontend'de görselleştirin

## Kod İnceleme Süreci

Pull request'iniz:
1. Otomatik kontroller geçmelidir (lint, test)
2. En az 1 maintainer tarafından incelenecektir
3. Değişiklik istekleri yapılabilir
4. Onaylandıktan sonra merge edilecektir

## Davranış Kuralları

- Saygılı ve yapıcı olun
- Farklı görüşlere açık olun
- Yardımcı olmaya çalışın
- Profesyonel iletişim kurun

## İletişim

- **Issues**: Sorular ve öneriler için
- **Discussions**: Genel tartışmalar için
- **Email**: [Maintainer email]

## Lisans

Katkılarınız MIT lisansı altında yayınlanacaktır.

## Teşekkürler

Her katkı, büyük veya küçük, değerlidir. Zaman ayırdığınız için teşekkürler!

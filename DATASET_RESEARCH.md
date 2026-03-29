# Dataset Araştırması: Teknik ve UI Metinleri Çeviri Analizi

## 📊 Bulunan Dataset Kaynakları

### 1. Profesyonel Yazılım Dokümantasyon Dataset'leri

#### SAP Software Documentation Dataset
- **Kaynak**: https://github.com/SAP/software-documentation-data-set-for-machine-translation
- **İçerik**: SAP yazılım dokümantasyonundan paralel değerlendirme dataset'i
- **Dil Çiftleri**: İngilizce → Hindi, Endonezce, Malayca, Tayca
- **Boyut**: Her dil çifti için ~4,000 segment
- **Format**: XML yapılı, doküman yapısı anotasyonlu
- **Lisans**: Creative Commons CC BY-NC 4.0
- **Özellikler**: 
  - Profesyonel çeviriler
  - Doküman sınırları metadata
  - Paragraf bilgisi
  - Metin tipleri (başlıklar, tablo elemanları)

#### Salesforce Localization Dataset
- **Kaynak**: https://github.com/salesforce/localization-xml-mt
- **İçerik**: Kurumsal yazılım platformu dokümantasyonu
- **Dil Çiftleri**: İngilizce → 16 dil
- **Boyut**: Her dil çifti için ~100,000 metin segmenti
- **Format**: XML yapılı paralel metin
- **Özellikler**:
  - Profesyonel çeviriler
  - Yapısal dokümantasyon korunmuş
  - Kurumsal yazılım terminolojisi

### 2. Açık Kaynak Yazılım Yerelleştirme Dataset'leri

#### OPUS Corpus - Yazılım Yerelleştirme
- **Kaynak**: https://opus.nlpl.eu/
- **İçerik**: Açık kaynak yazılım çevirileri
- **Mevcut Korpuslar**:
  - **GNOME**: GNOME masaüstü ortamı yerelleştirme dosyaları
  - **KDE**: KDE sistem mesajları (450 MB)
  - **KDEdoc**: KDE kullanım kılavuzu korpusu (77 MB)
  - **Mozilla-I10n**: Mozilla ürünleri yerelleştirme verileri
- **Dil Sayısı**: 100+ dil
- **Format**: TMX, TXT, Moses format
- **Erişim**: OpusTools (Python), OPUS-API

#### Mozilla Firefox Localization
- **Kaynak**: https://github.com/mozilla-l10n/firefox-l10n-source
- **İçerik**: Firefox tarayıcısı UI string'leri (en-US kaynak)
- **Paralel Korpus**: https://opus.nlpl.eu/Mozilla-I10n/corpus/version/Mozilla-I10n
  - 197 dil
  - 18,856 bitexts
  - 28.73M token
  - 3.22M cümle
- **Format**: .properties dosyaları
- **Lisans**: Mozilla Public License 2.0

#### Common UI Translations
- **Kaynak**: https://github.com/deviro/common-ui-translations
- **İçerik**: 4,000+ yaygın UI çeviri string'i
- **Dil Sayısı**: 35 dil
- **Format**: JSON
- **Kategoriler**:
  - Butonlar (Save, Cancel, Delete, vb.)
  - Formlar (Email, Password, Submit, vb.)
  - Navigasyon (Home, Settings, Profile, vb.)
  - Hata mesajları
  - Durum mesajları
  - Yaygın UI elemanları

#### i18n Info/Warning/Error Strings
- **Kaynak**: https://github.com/gnrlbzik/iwe-i18n-strings
- **İçerik**: Bilgi, uyarı ve hata mesajları koleksiyonu
- **Lisans**: MIT

### 3. Türkçe-İngilizce Özel Kaynaklar

#### MaCoCu Turkish-English Corpus
- **Kaynak**: https://elrc-share.eu/repository/browse/turkish-english-parallel-corpus-macocu-tr-en-20/
- **İçerik**: .tr ve .cy domainlerinden toplanmış paralel korpus
- **Boyut**: 
  - 1,646,739 giriş
  - 89,231,511 kelime
  - 584,752 metin
- **Format**: 
  - Cümle seviyesi TXT
  - Cümle seviyesi TMX (XML)
  - Doküman seviyesi TXT
- **Metadata**: Kalite skorları, benzerlik skorları, çeviri yönü
- **Araçlar**: Bitextor (hizalama), BicleanerAI (temizleme)
- **Not**: Genel web içeriği, özellikle yazılım odaklı değil

#### Turkish Parallel Corpora Collection
- **Kaynak**: https://github.com/maidis/turkish-parallel-corpora
- **İçerik**: Çeşitli Türkçe paralel korpus koleksiyonu

### 4. Büyük Ölçekli Genel Dataset'ler

#### DocHPLT (2025)
- **İçerik**: Doküman seviyesi çeviri dataset'i
- **Boyut**: 124M hizalanmış doküman çifti, 50 dil
- **Toplam**: 4.26 milyar cümle
- **Özellik**: Doküman bütünlüğü korunmuş

#### OPUS-100
- **İçerik**: İngilizce merkezli çok dilli korpus
- **Dil Sayısı**: 100 dil
- **Boyut**: ~55M cümle çifti
- **Format**: Train/dev/test split'li

## 🎯 Projeniz İçin Önerilen Strateji

### Hibrit Dataset Yaklaşımı

Projeniz için **üç kategoride** dataset oluşturmanızı öneriyorum:

#### Kategori 1: Teknik Dokümantasyon Metinleri
**Kaynaklar**:
1. SAP Software Documentation Dataset (temel olarak)
2. Salesforce Localization Dataset
3. OPUS GNOME/KDE dokümantasyon korpusu
4. Stack Overflow teknik açıklamaları (StaQC dataset)

**Örnek Metin Tipleri**:
- API dokümantasyonu
- Kullanım kılavuzları
- Teknik özellik açıklamaları
- Kod yorumları
- README dosyaları

#### Kategori 2: UI String'leri ve Mesajları
**Kaynaklar**:
1. Mozilla Firefox localization files (OPUS Mozilla-I10n)
2. Common UI Translations (4,000+ string)
3. GNOME/KDE UI mesajları
4. GitHub'dan popüler projelerin i18n dosyaları

**Örnek Metin Tipleri**:
- Buton etiketleri (Save, Cancel, Delete)
- Form alanları (Username, Password, Email)
- Hata mesajları (Invalid input, Connection failed)
- Bildirimler (Success, Warning, Error)
- Menü öğeleri
- Tooltip'ler

#### Kategori 3: Türkçe-İngilizce Özel Dataset (Oluşturulacak)
**Yöntem**: GitHub'dan popüler Türk yazılım projelerinin i18n dosyalarını toplama

**Hedef Projeler**:
- Türk şirketlerinin açık kaynak projeleri
- Türkçe lokalizasyonu olan uluslararası projeler
- Türk geliştiricilerin popüler GitHub repoları

## 🔧 Değerlendirme Metrikleri

### Otomatik Metrikler (Python Kütüphaneleri)

1. **SacreBLEU** (v2.6.0+)
   - BLEU skoru
   - chrF, chrF++
   - TER (Translation Error Rate)
   - Kurulum: `pip install sacrebleu`

2. **NLTK**
   - METEOR skoru
   - Kurulum: `pip install nltk`

3. **Ek Metrikler**:
   - COMET (neural metric)
   - BERTScore (semantic similarity)

### Manuel Değerlendirme
- Fluency (akıcılık)
- Adequacy (yeterlilik)
- Terminology consistency (terminoloji tutarlılığı)

## 📦 Dataset İndirme ve Hazırlama Adımları

### Adım 1: Hazır Dataset'leri İndirme
```bash
# OPUS araçlarını kurma
pip install opustools

# Mozilla korpusunu indirme
opus_read -d Mozilla-I10n -s en -t tr -w mozilla_en_tr.txt

# GNOME korpusunu indirme
opus_read -d GNOME -s en -t tr -w gnome_en_tr.txt
```

### Adım 2: GitHub'dan Veri Toplama
- GitHub API ile popüler projelerin i18n dosyalarını arama
- `.json`, `.po`, `.properties` formatlarını çekme
- Paralel metin çiftleri oluşturma

### Adım 3: Veri Temizleme ve Normalizasyon
- Duplikasyon temizleme
- Format standardizasyonu
- Kalite filtreleme

## 🎨 Çeviri Araçları Karşılaştırması

### Test Edilecek Araçlar

1. **Google Translate API**
   - En yaygın kullanılan
   - 100+ dil desteği
   - Neural MT

2. **DeepL API**
   - Yüksek kalite
   - Daha az dil desteği
   - Avrupa dilleri için güçlü

3. **Microsoft Translator**
   - Azure entegrasyonu
   - Özel terminoloji desteği
   - 100+ dil

4. **Amazon Translate**
   - AWS entegrasyonu
   - Özel terminoloji
   - Gerçek zamanlı çeviri

5. **OpenAI GPT (opsiyonel)**
   - Context-aware çeviri
   - Açıklama ile çeviri

## 📈 Beklenen Analiz Sonuçları

### Karşılaştırma Kriterleri
1. **Doğruluk**: BLEU, METEOR, TER skorları
2. **Terminoloji Tutarlılığı**: Teknik terimlerin doğru çevirisi
3. **Bağlam Anlama**: UI string'lerinde bağlam korunması
4. **Hız**: Çeviri süresi
5. **Maliyet**: API fiyatlandırması
6. **Özel Karakter İşleme**: Kod snippet'leri, değişkenler, placeholder'lar

### Hipotezler
- DeepL genel metinlerde daha iyi performans gösterebilir
- Google Translate daha geniş dil desteği sunar
- Microsoft Translator kurumsal terminolojide güçlü olabilir
- UI string'leri kısa ve bağlam-bağımlı olduğu için zorlayıcıdır

## 📝 Makale Yapısı Önerisi

### Abstract
- Problem tanımı
- Metodoloji özeti
- Ana bulgular

### 1. Introduction
- Makine çevirisinin yazılım lokalizasyonundaki önemi
- Teknik metin vs UI metin farklılıkları
- Araştırma soruları

### 2. Related Work
- Makine çeviri araçları literatürü
- Teknik metin çevirisi çalışmaları
- Değerlendirme metrikleri

### 3. Methodology
- Dataset oluşturma/toplama
- Çeviri araçları seçimi
- Değerlendirme metrikleri
- Deney tasarımı

### 4. Dataset Description
- Teknik dokümantasyon korpusu
- UI string korpusu
- İstatistikler ve özellikler

### 5. Experiments and Results
- Otomatik metrik sonuçları
- Manuel değerlendirme
- Karşılaştırmalı analiz
- Hata analizi

### 6. Discussion
- Bulguların yorumlanması
- Araçların güçlü/zayıf yönleri
- Pratik öneriler

### 7. Conclusion
- Özet bulgular
- Gelecek çalışmalar

## 🚀 Uygulama Sırası

1. ✅ Dataset araştırması (TAMAMLANDI)
2. ⏭️ Proje yapısı oluşturma
3. ⏭️ Dataset indirme ve hazırlama scriptleri
4. ⏭️ Backend API geliştirme (çeviri entegrasyonları)
5. ⏭️ Frontend web arayüzü
6. ⏭️ Metrik hesaplama modülü
7. ⏭️ Deneyler ve veri toplama
8. ⏭️ Sonuç analizi ve görselleştirme
9. ⏭️ Makale yazımı

## 💡 Önerilen Dataset Kombinasyonu

### Minimum Viable Dataset (Hızlı Başlangıç)
- **Teknik**: SAP dataset (4K segment) + OPUS GNOME (10K segment)
- **UI**: Mozilla Firefox strings (5K segment) + Common UI Translations (4K segment)
- **Toplam**: ~23,000 segment

### Kapsamlı Dataset (Daha Güçlü Analiz)
- **Teknik**: SAP + Salesforce + OPUS (GNOME/KDE/Mozilla) + GitHub scraping
- **UI**: Mozilla + Common UI + GitHub i18n files + Kendi topladığınız
- **Toplam**: 100,000+ segment

### Türkçe-İngilizce Özel
- MaCoCu korpusundan teknik içerik filtreleme
- GitHub Türk projelerinden i18n dosyaları
- Türkçe yazılım dokümantasyonları

## 🔍 Veri Toplama Araçları

### Otomatik Toplama İçin Gerekli Araçlar
1. **OpusTools**: OPUS korpuslarını indirme
2. **GitHub API**: i18n dosyalarını arama ve indirme
3. **BeautifulSoup/Scrapy**: Web scraping (gerekirse)
4. **Pandas**: Veri işleme ve temizleme

### Veri Formatları
- JSON (modern web uygulamaları)
- PO/POT (gettext - Linux/GNOME/KDE)
- XLIFF (XML Localization Interchange File Format)
- Properties (Java/Firefox)
- TMX (Translation Memory eXchange)

## ⚠️ Dikkat Edilmesi Gerekenler

1. **Lisans Uyumluluğu**: Tüm dataset'lerin lisanslarını kontrol edin
2. **Veri Kalitesi**: Profesyonel çeviriler > makine çevirileri
3. **Domain Spesifikliği**: Genel korpus yerine yazılım odaklı içerik
4. **Dil Çifti**: Türkçe-İngilizce için özel kaynak gerekebilir
5. **Boyut Dengesi**: Teknik vs UI metinleri dengeli olmalı

## 📊 Beklenen Dataset İstatistikleri

| Kategori | Segment Sayısı | Ortalama Uzunluk | Kaynak |
|----------|----------------|------------------|---------|
| Teknik Dok | 20,000-50,000 | 50-200 karakter | SAP, Salesforce, OPUS |
| UI Strings | 10,000-30,000 | 10-50 karakter | Mozilla, Common UI |
| Hata Mesajları | 2,000-5,000 | 20-80 karakter | GitHub, i18n files |
| **TOPLAM** | **32,000-85,000** | - | - |

## 🎯 Sonraki Adım

Dataset'leri indirip işlemek için Python scriptleri yazalım ve proje yapısını kuralım.

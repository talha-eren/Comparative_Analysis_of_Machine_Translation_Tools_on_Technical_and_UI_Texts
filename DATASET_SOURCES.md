# Dataset Kaynakları ve Linkler

Bu dokümanda projede kullanılan tüm dataset kaynaklarının detaylı bilgileri ve linkleri bulunmaktadır.

## Teknik Dokümantasyon Dataset'leri

### 1. OPUS GNOME Corpus
- **URL**: https://opus.nlpl.eu/GNOME.php
- **Dil Çifti**: EN-TR
- **Segment Sayısı**: ~10,000
- **İçerik**: GNOME masaüstü ortamı dokümantasyonu
- **Format**: TMX, Moses, Raw text
- **Lisans**: Open source (GNOME lisansı)
- **Kalite**: Yüksek (profesyonel çeviri)
- **İndirme**: OpusTools ile otomatik
```bash
opus_read -d GNOME -s en -t tr -w gnome_en_tr.txt -wm moses
```

### 2. OPUS KDE4 Corpus
- **URL**: https://opus.nlpl.eu/KDE4.php
- **Dil Çifti**: EN-TR
- **Segment Sayısı**: ~8,000
- **İçerik**: KDE masaüstü ortamı dokümantasyonu ve sistem mesajları
- **Format**: TMX, Moses
- **Lisans**: GPL/LGPL
- **Kalite**: Yüksek
- **İndirme**: OpusTools
```bash
opus_read -d KDE4 -s en -t tr -w kde4_en_tr.txt -wm moses
```

### 3. SAP Software Documentation Dataset
- **URL**: https://github.com/SAP/software-documentation-data-set-for-machine-translation
- **Dil Çiftleri**: EN-HI, EN-ZH (TR yok)
- **Segment Sayısı**: 123,000 (EN-HI)
- **İçerik**: SAP yazılım dokümantasyonu
- **Format**: TMX
- **Lisans**: CC BY-NC 4.0
- **Kullanım**: Metodoloji referansı
- **Not**: Türkçe çift yok, ancak teknik dokümantasyon yapısı için önemli

### 4. GitHub Türk Projeleri
- **Kaynak**: GitHub API
- **Hedef Segment**: ~3,000
- **İçerik**: 
  - README.md dosyaları (EN/TR)
  - API dokümantasyonları
  - Teknik blog yazıları
- **Toplama Yöntemi**: GitHub API + web scraping
- **Örnek Repolar**:
  - https://github.com/aykutkardas/regexlearn.com
  - https://github.com/acikkaynak/acikkaynak-website
  - https://github.com/Trendyol/android-ui-components

## UI String Dataset'leri

### 5. Mozilla Firefox i18n
- **URL**: https://opus.nlpl.eu/Mozilla-I10n.php
- **Dil Çifti**: EN-TR
- **Segment Sayısı**: ~6,000
- **İçerik**: Firefox tarayıcısı UI string'leri
- **Format**: .properties → JSON
- **Lisans**: Mozilla Public License 2.0
- **Kalite**: Çok yüksek (Mozilla L10n ekibi)
- **Özellikler**: Gerçek tarayıcı UI metinleri, placeholder'lar içerir
- **İndirme**: OpusTools
```bash
opus_read -d Mozilla -s en -t tr -w mozilla_en_tr.txt -wm moses
```

### 6. Common UI Translations
- **URL**: https://github.com/deviro/common-ui-translations
- **Dil Sayısı**: 35+ (TR dahil)
- **Segment Sayısı**: ~4,000
- **İçerik**: 
  - Buton metinleri (Save, Cancel, OK, etc.)
  - Form etiketleri
  - Hata mesajları
  - Navigasyon öğeleri
- **Format**: JSON
- **Lisans**: MIT
- **Kalite**: Topluluk katkılı
- **İndirme**: Git clone
```bash
git clone https://github.com/deviro/common-ui-translations.git
```

### 7. Salesforce Localization Dataset
- **URL**: https://github.com/salesforce/localization-xml-mt
- **Dil Çiftleri**: EN-DE, EN-ES, EN-FR, EN-JA, EN-ZH (TR yok)
- **Segment Sayısı**: 50,000+
- **İçerik**: Salesforce CRM UI string'leri
- **Format**: XML
- **Lisans**: BSD 3-Clause
- **Kullanım**: Referans ve metodoloji
- **Not**: Türkçe yok ama UI string yapısı için faydalı

### 8. GitHub i18n Dosyaları
- **Kaynak**: Popüler Türk projeleri
- **Hedef Segment**: ~5,000
- **İçerik**: 
  - React/Vue/Angular i18n dosyaları
  - Mobil uygulama lokalizasyonları
  - Web uygulaması çevirileri
- **Format**: JSON, YAML
- **Toplama**: GitHub API + manuel seçim
- **Örnek Dosya Yapıları**:
  - `i18n/en.json`, `i18n/tr.json`
  - `locales/en-US.json`, `locales/tr-TR.json`
  - `lang/en.json`, `lang/tr.json`

## Türkçe-İngilizce Paralel Korpus

### 9. MaCoCu Turkish-English Corpus
- **URL**: https://www.clarin.si/repository/xmlui/handle/11356/1816
- **Dil Çifti**: TR-EN (bidirectional)
- **Segment Sayısı**: 1,600,000
- **Kelime Sayısı**: 89M (TR), 79M (EN)
- **İçerik**: Web'den toplanmış genel domain metinler
- **Format**: TMX, TXT
- **Lisans**: CC BY 4.0
- **Kalite**: Otomatik hizalama + filtreleme
- **Boyut**: ~2GB (sıkıştırılmış)
- **Kullanım**: Teknik içerik filtreleme (10,000 segment)
- **İndirme**: Manuel (büyük dosya)
```bash
# Direkt link
wget https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1816/MaCoCu-tr-en.sent.txt.gz
```

## Ek Kaynaklar (Referans)

### 10. OPUS-100
- **URL**: https://opus.nlpl.eu/opus-100.php
- **Dil Çiftleri**: 100 dil, EN-TR dahil
- **Segment Sayısı**: 1M+ (EN-TR)
- **Not**: Genel domain, yazılım odaklı değil

### 11. Tatoeba
- **URL**: https://tatoeba.org/
- **Dil Çifti**: EN-TR
- **Segment Sayısı**: ~50,000
- **İçerik**: Kısa cümleler
- **Kalite**: Değişken (topluluk katkılı)
- **Not**: UI string'leri için ek kaynak olabilir

### 12. CCMatrix
- **URL**: https://github.com/facebookresearch/LASER/tree/main/tasks/CCMatrix
- **Dil Çifti**: EN-TR
- **Segment Sayısı**: 10M+
- **İçerik**: Common Crawl'dan çıkarılmış
- **Kalite**: Otomatik hizalama
- **Not**: Çok büyük, filtreleme gerekli

## Dataset İstatistikleri

### Toplam Dataset Kompozisyonu

| Kategori | Segment Sayısı | Kaynak |
|----------|----------------|--------|
| Teknik Dokümantasyon | 25,000 | OPUS GNOME, KDE, GitHub |
| UI String'leri | 15,000 | Mozilla, Common UI, GitHub |
| Hata Mesajları | 10,000 | Mixed |
| **TOPLAM** | **50,000** | **Çoklu** |

### Kaynak Dağılımı

| Kaynak | Segment | Yüzde |
|--------|---------|-------|
| OPUS GNOME | 10,000 | 20% |
| OPUS KDE4 | 8,000 | 16% |
| Mozilla i18n | 6,000 | 12% |
| GitHub i18n | 5,000 | 10% |
| Common UI | 4,000 | 8% |
| GitHub Docs | 3,000 | 6% |
| MaCoCu (filtered) | 10,000 | 20% |
| Diğer | 4,000 | 8% |

### Kalite Metrikleri

- **Ortalama Segment Uzunluğu**: 85.3 karakter
- **Ortalama Kelime Sayısı**: 12.5 kelime
- **Placeholder İçeren**: 25% (UI), 8% (teknik)
- **Teknik Terim Yoğunluğu**: 15% (teknik), 5% (UI)

## Veri Toplama Metodolojisi

### OPUS Dataset'leri
1. OpusTools ile otomatik indirme
2. Moses formatından JSON'a dönüşüm
3. Kalite filtreleme (uzunluk, içerik)
4. Kategorizasyon

### GitHub Veri Toplama
1. GitHub API ile repo arama
2. i18n dosyalarını bulma (en.json, tr.json)
3. JSON parse ve paralel çift çıkarma
4. Metadata ekleme (repo, stars, etc.)

### MaCoCu Filtreleme
1. Ham korpusu indirme (1.6M segment)
2. Teknik terminoloji filtreleme
3. Kalite skoru filtreleme (>0.8)
4. Uzunluk filtreleme (10-500 karakter)
5. 10,000 segment seçimi

## Lisans Bilgileri

| Dataset | Lisans | Ticari Kullanım |
|---------|--------|-----------------|
| OPUS GNOME | GPL/LGPL | ✓ (koşullu) |
| OPUS KDE4 | GPL/LGPL | ✓ (koşullu) |
| Mozilla i18n | MPL 2.0 | ✓ |
| Common UI | MIT | ✓ |
| MaCoCu | CC BY 4.0 | ✓ |
| GitHub (public) | Varies | Kontrol edin |

**Not:** Ticari kullanım için her kaynağın lisansını ayrı ayrı kontrol edin.

## Atıf

Bu dataset'leri kullanıyorsanız, lütfen orijinal kaynaklara atıf yapın:

```bibtex
@inproceedings{tiedemann2012parallel,
  title={Parallel data, tools and interfaces in OPUS},
  author={Tiedemann, J{\"o}rg},
  booktitle={Lrec},
  year={2012}
}

@article{macocu2021,
  title={MaCoCu: Massive collection and curation of monolingual and bilingual data},
  author={MaCoCu Consortium},
  year={2021}
}
```

## Güncellemeler

Dataset'ler sürekli güncellenmektedir. Son güncellemeler için:
- OPUS: https://opus.nlpl.eu/
- MaCoCu: https://macocu.eu/

## Katkıda Bulunma

Yeni dataset kaynakları önerilerinizi issue olarak açabilirsiniz!

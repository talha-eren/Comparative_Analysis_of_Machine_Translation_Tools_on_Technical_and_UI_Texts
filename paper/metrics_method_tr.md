# Değerlendirme Metrikleri ve Hesaplama Süreci

Bu çalışmada çeviri kalitesi dört metrikle ölçülmüştür: BLEU, METEOR, chrF++ ve TER. Tüm metriklerden önce ortak bir normalizasyon uygulanmıştır.

## 1) Ortak Ön İşleme (Normalization)

Her hipotez ve referans metin şu sırayla normalize edilmiştir:

1. Unicode NFKD dönüşümü
2. Diakritik (aksan) kaldırma
3. Büyük-küçük harf duyarsızlaştırma (casefold)
4. Noktalama karakterlerini temizleme
5. Çoklu boşlukları tek boşluğa indirme

Matematiksel gösterim:

$$
\tilde{x} = \mathrm{Normalize}(x)
$$

## 2) BLEU (SacreBLEU)

BLEU metriği SacreBLEU ile hesaplanmıştır.

- Kısa metinler için (minimum token sayısı <= 6) sentence-level BLEU
- Diğerlerinde corpus-level BLEU
- Sonuç 0-100 aralığından 0-1 aralığına dönüştürülmüştür

Formül:

$$
\mathrm{BLEU} = \mathrm{BP} \cdot \exp\left(\sum_{n=1}^{N} w_n \log p_n\right)
$$

Burada:

- $p_n$: n-gram precision
- $w_n$: n-gram ağırlıkları, $\sum w_n = 1$
- BP: brevity penalty

## 3) METEOR (NLTK)

METEOR, NLTK meteor_score ile normalize edilmiş tokenlar üzerinden hesaplanmıştır.

Formül:

$$
\mathrm{METEOR} = (1 - \mathrm{Penalty}) \cdot F_{\alpha}
$$

$$
F_{\alpha} = \frac{PR}{\alpha P + (1-\alpha)R}
$$

Burada:

- $P$: precision
- $R$: recall
- Penalty: parçalanma cezası

## 4) chrF++ (SacreBLEU)

chrF++ karakter düzeyinde F-skor yaklaşımıdır (chrF++ varyantında kelime bilgisi de kullanılır). Sonuç 0-100'den 0-1'e ölçeklenmiştir.

Genel form:

$$
\mathrm{chrF}_{\beta} = \frac{(1+\beta^2)PR}{\beta^2P + R}
$$

## 5) TER (SacreBLEU)

TER, çeviriyi referansa dönüştürmek için gereken edit işlemlerinin referans kelime sayısına oranıdır. Sonuç 0-100'den 0-1'e çevrilmiştir.

Formül:

$$
\mathrm{TER} = \frac{\#\mathrm{edits}}{\#\mathrm{reference\ words}}
$$

Not: TER'de düşük değer daha iyidir.

## 6) Birleşik Doğruluk Skoru

Arayüzde tekil doğruluk yüzdesi şu şekilde hesaplanmıştır:

$$
\mathrm{Accuracy} = 100 \times \frac{\mathrm{BLEU} + \mathrm{METEOR} + \mathrm{chrF} + (1 - \mathrm{TER})}{4}
$$

Burada TER terslenerek diğer metriklerle aynı yönde yorumlanmıştır.

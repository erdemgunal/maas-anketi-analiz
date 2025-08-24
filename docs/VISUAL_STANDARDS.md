# 🎨 Görselleştirme Standartları

## 📊 Genel Görselleştirme Kuralları

### 🎯 Temel Prensipler
- **Okunabilirlik**: Grafikler LaTeX raporunda küçültüldüğünde bile okunabilir olmalı
- **Tutarlılık**: Tüm grafikler aynı stil ve format kullanmalı
- **Profesyonellik**: Yayın kalitesinde görünüm
- **Erişilebilirlik**: Renk körü dostu tasarım

### 📏 Boyut ve Çözünürlük
- **Grafik Boyutu**: 12x8 inç (30.48x20.32 cm)
- **Çözünürlük**: 300 DPI
- **Format**: PNG (şeffaflık desteği için)
- **Aspect Ratio**: 1.5:1 (yatay format)

## 🔤 Tipografi Standartları

### 📝 Font Ayarları
- **Ana Font**: Arial veya Helvetica
- **Alternatif**: DejaVu Sans (Linux sistemler için)
- **Matematiksel Semboller**: LaTeX math mode uyumlu

### 📏 Font Boyutları (LaTeX için optimize edilmiş)
- **Ana Başlık**: 20pt (görsel başlığı)
- **Alt Başlık**: 18pt (eksen başlıkları)
- **Eksen Etiketleri**: 16pt (x, y eksen etiketleri)
- **Legend**: 16pt (açıklama metni)
- **Grafik İçi Yazılar**: 16pt (değerler, etiketler)
- **Tick Labels**: 14pt (eksen değerleri)
- **Annotation**: 16pt (grafik üzerindeki notlar)

### 🎨 Font Stilleri
- **Başlıklar**: Bold (kalın)
- **Eksen Etiketleri**: Regular
- **Legend**: Regular
- **Değerler**: Regular
- **Önemli Notlar**: Bold

## 🎨 Renk Paleti

### 🌈 Ana Renk Paleti (Viridis)
- **Birincil**: #440154 (koyu mor)
- **İkincil**: #31688E (mavi)
- **Üçüncül**: #35B779 (yeşil)
- **Dördüncül**: #FDE725 (sarı)

### 🎯 Kategorik Renkler
- **React Kullanıcıları**: #440154 (koyu mor)
- **Non-React Kullanıcıları**: #35B779 (yeşil)
- **Erkek**: #31688E (mavi)
- **Kadın**: #FDE725 (sarı)
- **Remote**: #440154 (koyu mor)
- **Office**: #31688E (mavi)
- **Hybrid**: #35B779 (yeşil)

### ⚠️ Renk Körü Dostu Alternatifler
- **Protanopia**: #E69F00, #56B4E9, #009E73, #F0E442
- **Deuteranopia**: #E69F00, #56B4E9, #009E73, #F0E442
- **Tritanopia**: #E69F00, #56B4E9, #009E73, #F0E442

## 📊 Grafik Türleri ve Standartları

### 📈 Histogram ve Yoğunluk Eğrisi
- **Bar Rengi**: #440154 (koyu mor)
- **Yoğunluk Eğrisi**: #FDE725 (sarı), kalınlık 2pt
- **Grid**: Açık gri (#E5E5E5)
- **Bin Sayısı**: 30-50 arası

### 📦 Box Plot
- **Box Rengi**: #31688E (mavi)
- **Whisker Rengi**: #440154 (koyu mor)
- **Outlier Rengi**: #FDE725 (sarı)
- **Median Çizgisi**: Beyaz, kalınlık 2pt

### 🎻 Violin Plot
- **Violin Rengi**: #35B779 (yeşil)
- **Box Rengi**: #440154 (koyu mor)
- **Median Nokta**: Beyaz, boyut 8pt

### 📊 Scatter Plot
- **Nokta Rengi**: #31688E (mavi)
- **Nokta Boyutu**: 20pt
- **Transparanlık**: 0.6 (alpha)
- **Trend Çizgisi**: #FDE725 (sarı), kalınlık 3pt

### 🔥 Heatmap
- **Renk Haritası**: Viridis
- **Grid Çizgileri**: Beyaz, kalınlık 0.5pt
- **Değer Yazıları**: Siyah, 14pt

### 🥧 Pie Chart
- **Renk Paleti**: Viridis
- **Etiket Rengi**: Siyah
- **Etiket Boyutu**: 16pt
- **Yüzde Gösterimi**: 14pt

## 📋 Grafik Başlıkları ve Etiketler

### 📝 Başlık Formatı
- **Format**: "1. Maaş Dağılımı (Histogram ve Yoğunluk Eğrisi)"
- **Stil**: Bold, 20pt
- **Hizalama**: Merkez
- **Renk**: Siyah (#000000)

### 📏 Eksen Etiketleri
- **Format**: "Aylık Ortalama Net Maaş (bin TL)"
- **Stil**: Regular, 16pt
- **Renk**: Siyah (#000000)
- **Hizalama**: Merkez
- **Anlaşılırlık**: İstatistiksel terimler yerine günlük dil kullanın
  - "Frekans" → "Geliştirici Sayısı" veya "Katılımcı Sayısı"
  - "Yoğunluk" → "Oran" veya "Dağılım"
  - "Ortalama" → "Ortalama Maaş"

### 📊 Legend (Açıklama)
- **Pozisyon**: Sağ üst köşe
- **Font Boyutu**: 16pt
- **Renk**: Siyah (#000000)
- **Arka Plan**: Beyaz, %90 transparanlık

### 📝 Grafik Açıklamaları
- **"Bu Ne Anlama Geliyor?" Bölümü**: Her grafiğin altında kısa açıklama
- **İstatistiksel Kavramlar**: Basit dilde açıklama
  - **Box Plot**: "Kutu ortasındaki çizgi ortalama maaşı, kutunun üst ve alt sınırları %75 ve %25'lik dilimleri gösterir"
  - **Violin Plot**: "Şeklin genişliği o maaş aralığındaki geliştirici sayısını gösterir"
  - **Histogram**: "Her sütun o maaş aralığındaki geliştirici sayısını gösterir"
- **Ana Bulgular**: Grafikteki en önemli 2-3 bulgu vurgulanmalı

## 🔧 Teknik Ayarlar

### 📐 Matplotlib Ayarları
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Temel ayarlar
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# Font ayarları
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 16
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 16

# Renk paleti
sns.set_palette("viridis")
```

### 🎨 Seaborn Ayarları
```python
# Renk paleti
sns.set_palette("viridis")

# Stil ayarları
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.2)
```

## 📄 LaTeX Entegrasyonu

### 🔧 LaTeX Grafik Ayarları
```latex
\usepackage{graphicx}
\graphicspath{{../outputs/figures/}}

% Grafik boyutlandırma
\includegraphics[width=0.9\textwidth]{figure_name.png}
```

### 📏 LaTeX Grafik Boyutlandırma
- **Tam Sayfa**: `\textwidth`
- **Yarım Sayfa**: `0.5\textwidth`
- **Üçte İki**: `0.67\textwidth`
- **Özel Boyut**: `0.8\textwidth`

## 🚀 En İyi Uygulamalar

### 📊 Grafik Tasarımı
1. **Basitlik**: Gereksiz detayları kaldırın
2. **Netlik**: Her elemanın amacı açık olsun
3. **Tutarlılık**: Tüm grafikler aynı stili kullansın
4. **Okunabilirlik**: LaTeX'te küçültüldüğünde bile okunabilir olsun

### 🎨 Renk Kullanımı
1. **Anlamlı Renkler**: Renkler veri anlamını desteklesin
2. **Kontrast**: Arka plan ile yeterli kontrast olsun
3. **Erişilebilirlik**: Renk körü dostu paletler kullanın
4. **Tutarlılık**: Aynı kategoriler için aynı renkleri kullanın

### 📝 Metin ve Etiketler
1. **Açıklayıcı Başlıklar**: Grafik ne gösteriyor açık olsun
2. **Birim Belirtme**: Tüm sayısal değerler için birim ekleyin
3. **Kaynak Gösterimi**: Veri kaynağını belirtin
4. **Tarih Bilgisi**: Analiz tarihini ekleyin

---

*Bu standartlar, grafiklerin LaTeX raporunda optimal görünmesi için tasarlanmıştır.*
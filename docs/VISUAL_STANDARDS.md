# 🎨 GÖRSEL STANDARTLARI (VISUAL STANDARDS)

## Renk Paleti

### Ana Renkler
```python
PRIMARY_COLORS = {
    'blue': '#2E86AB',      # Ana mavi - güven ve profesyonellik
    'orange': '#F24236',    # Turuncu - enerji ve dikkat çekici
    'green': '#A23B72',     # Yeşil - büyüme ve pozitif trend
    'purple': '#F18F01',    # Mor - yaratıcılık ve inovasyon
    'gray': '#C73E1D'       # Gri - denge ve stabilite
}
```

### Renk Kullanım Kuralları
- **Mavi**: Ana veri serileri, güvenilir metrikler
- **Turuncu**: Vurgu, önemli noktalar, uyarılar
- **Yeşil**: Pozitif trendler, başarı metrikleri
- **Mor**: Kategorik veriler, farklı gruplar
- **Gri**: Arka plan, yardımcı bilgiler

### Gradient Renkler
```python
GRADIENT_COLORS = {
    'blue_gradient': ['#E3F2FD', '#2E86AB'],
    'green_gradient': ['#E8F5E8', '#A23B72'],
    'orange_gradient': ['#FFF3E0', '#F24236']
}
```

## Font ve Boyut

### Font Ayarları
```python
FONT_SETTINGS = {
    'title_size': 16,        # Ana başlık boyutu
    'subtitle_size': 14,     # Alt başlık boyutu
    'label_size': 12,        # Eksen etiketleri
    'tick_size': 10,         # Eksen değerleri
    'legend_size': 11,       # Açıklama metni
    'annotation_size': 9,    # Açıklama notları
    'dpi': 300,              # Çözünürlük
    'figure_size': (12, 8)   # Grafik boyutu (inch)
}
```

### Font Ailesi
- **Ana Font**: Arial (sans-serif)
- **Alternatif**: Helvetica, sans-serif
- **Matematiksel**: Times New Roman (formüller için)

## Grafik Türleri ve Standartları

### Histogram ve Dağılım Grafikleri
```python
HISTOGRAM_STYLE = {
    'bins': 20,              # Varsayılan bin sayısı
    'alpha': 0.7,            # Şeffaflık
    'edgecolor': 'black',    # Kenar rengi
    'linewidth': 0.5         # Kenar kalınlığı
}
```

### Scatter Plot (Dağılım Grafikleri)
```python
SCATTER_STYLE = {
    'alpha': 0.6,            # Şeffaflık
    's': 50,                 # Nokta boyutu
    'edgecolors': 'white',   # Kenar rengi
    'linewidth': 0.5         # Kenar kalınlığı
}
```

### Bar Chart (Çubuk Grafikleri)
```python
BAR_STYLE = {
    'alpha': 0.8,            # Şeffaflık
    'edgecolor': 'black',    # Kenar rengi
    'linewidth': 0.5,        # Kenar kalınlığı
    'width': 0.8             # Çubuk genişliği
}
```

### Box Plot (Kutu Grafikleri)
```python
BOX_STYLE = {
    'patch_artist': True,    # Dolgu rengi
    'medianprops': {'color': 'red', 'linewidth': 2},
    'whiskerprops': {'color': 'black', 'linewidth': 1},
    'capprops': {'color': 'black', 'linewidth': 1}
}
```

## Layout ve Düzen

### Grafik Düzeni
```python
LAYOUT_SETTINGS = {
    'figsize': (12, 8),      # Grafik boyutu
    'dpi': 300,              # Çözünürlük
    'facecolor': 'white',    # Arka plan rengi
    'edgecolor': 'black',    # Kenar rengi
    'linewidth': 1           # Kenar kalınlığı
}
```

### Eksen Ayarları
```python
AXIS_SETTINGS = {
    'grid': True,            # Izgara çizgileri
    'grid_alpha': 0.3,       # Izgara şeffaflığı
    'spines': ['top', 'right'],  # Gizlenecek eksenler
    'tick_params': {'direction': 'out', 'length': 6}
}
```

### Başlık ve Etiketler
```python
TITLE_SETTINGS = {
    'fontsize': 16,          # Başlık boyutu
    'fontweight': 'bold',    # Kalın yazı
    'pad': 20,               # Üst boşluk
    'loc': 'center'          # Hizalama
}
```

## Özel Grafik Türleri

### Heatmap (Isı Haritası)
```python
HEATMAP_STYLE = {
    'cmap': 'Blues',         # Renk haritası
    'annot': True,           # Değer gösterimi
    'fmt': '.2f',            # Sayı formatı
    'cbar_kws': {'shrink': 0.8}
}
```

### Word Cloud (Kelime Bulutu)
```python
WORDCLOUD_STYLE = {
    'background_color': 'white',
    'max_words': 100,
    'width': 800,
    'height': 400,
    'colormap': 'viridis'
}
```

### Correlation Matrix (Korelasyon Matrisi)
```python
CORRELATION_STYLE = {
    'cmap': 'RdBu_r',        # Kırmızı-mavi renk haritası
    'center': 0,             # Merkez değeri
    'square': True,          # Kare format
    'annot': True            # Değer gösterimi
}
```

## Kalite Kontrol

### Çözünürlük Standartları
- **Minimum DPI**: 300 (publication quality)
- **Format**: PNG (kayıpsız sıkıştırma)
- **Boyut**: 12x8 inch (standart)
- **Renk Modu**: RGB

### Erişilebilirlik
- **Renk Körlüğü**: Renk körü dostu paletler
- **Kontrast**: Yeterli kontrast oranı
- **Font Boyutu**: Minimum 10pt
- **Açıklama**: Her grafik için açıklama

### Tutarlılık Kontrolü
- **Renk Paleti**: Tüm grafiklerde aynı renkler
- **Font**: Tutarlı font kullanımı
- **Boyut**: Standart grafik boyutları
- **Stil**: Tutarlı stil uygulaması

## Örnek Grafik Kodu

### Standart Grafik Template
```python
def create_standard_plot(title, xlabel, ylabel, figsize=(12, 8)):
    """
    Standart grafik oluşturma fonksiyonu
    """
    plt.figure(figsize=figsize, dpi=300, facecolor='white')
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt.gca()

# Kullanım örneği
ax = create_standard_plot(
    title="Maaş Dağılımı",
    xlabel="Maaş (Bin TL)",
    ylabel="Frekans"
)
```

### Renk Paleti Uygulaması
```python
def apply_color_palette(ax, color_type='primary'):
    """
    Renk paleti uygulama fonksiyonu
    """
    if color_type == 'primary':
        colors = list(PRIMARY_COLORS.values())
    elif color_type == 'gradient':
        colors = GRADIENT_COLORS['blue_gradient']
    
    for i, patch in enumerate(ax.patches):
        patch.set_facecolor(colors[i % len(colors)])
        patch.set_alpha(0.8)
        patch.set_edgecolor('black')
        patch.set_linewidth(0.5)
```

## Export Ayarları

### PNG Export
```python
EXPORT_SETTINGS = {
    'dpi': 300,
    'bbox_inches': 'tight',
    'pad_inches': 0.1,
    'facecolor': 'white',
    'edgecolor': 'none'
}

# Kullanım
plt.savefig('output.png', **EXPORT_SETTINGS)
```

### PDF Export
```python
PDF_SETTINGS = {
    'format': 'pdf',
    'bbox_inches': 'tight',
    'pad_inches': 0.1
}

# Kullanım
plt.savefig('output.pdf', **PDF_SETTINGS)
```

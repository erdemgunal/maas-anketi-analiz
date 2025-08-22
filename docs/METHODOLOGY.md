# 🔬 METODOLOJI (METHODOLOGY)

## İstatistiksel Testler

### Hipotez Testleri
```python
# 1. Independent t-test: React vs non-React maaş karşılaştırması
H0: μ_react = μ_non_react
H1: μ_react ≠ μ_non_react

# 2. One-way ANOVA: Lokasyon bazlı maaş farkları
H0: μ_turkey = μ_europe = μ_other
H1: En az bir grup farklı

# 3. Chi-square test: Cinsiyet vs teknoloji tercihi bağımsızlığı
H0: Cinsiyet ve teknoloji tercihi bağımsız
H1: Cinsiyet ve teknoloji tercihi bağımlı

# 4. Pearson correlation: Deneyim vs maaş ilişkisi
H0: ρ = 0 (Korelasyon yok)
H1: ρ ≠ 0 (Korelasyon var)

# 5. One-way ANOVA: Saat bazlı maaş farkları
H0: μ_saat0 = μ_saat1 = ... = μ_saat23
H1: En az bir saat grubu farklı

# 6. Chi-square test: Saat vs rol/seviye/demografik özellik bağımsızlığı
H0: Saat ve rol/seviye/demografik özellik bağımsız
H1: Saat ve rol/seviye/demografik özellik bağımlı

### Güven Aralıkları
- **Confidence Level**: 95% (α = 0.05)
- **Effect Size**: Cohen's d, eta-squared
- **Power Analysis**: Minimum sample size hesaplaması

## Veri İşleme Adımları

### 1. Data Cleaning
- **Maaş Normalizasyonu**: "61-70" → 65 (aralık ortalaması)
- **Teknoloji Ayrıştırma**: "React, Redux" → ayrı dummy variables
- **Timestamp Dönüşümü**: Timestamp sütunundan (örn: "8/20/2025 12:31:15") sadece saat bilgisini (0-23 arası) ayrıştırarak yeni bir Anket_Saati sütunu oluşturulacak
- **Kategorik Kodlama**: Label encoding ve one-hot encoding
- **Missing Values**: Imputation stratejileri

### 2. Feature Engineering
- **Skill Dummy Variables**: Her teknoloji için binary column
- **Experience Numeric**: String deneyim → sayısal değer
- **Interaction Terms**: Teknoloji × deneyim kombinasyonları
- **Polynomial Features**: Non-linear ilişkiler için

### 3. Outlier Detection
- **IQR Method**: Q1 - 1.5*IQR, Q3 + 1.5*IQR
- **Z-Score**: |z| > 3 olan değerler
- **Isolation Forest**: Statistical outlier detection

### 4. Normalization
- **PPP-adjusted**: Satın alma gücü paritesi
- **Standard Scaling**: Z-score normalization
- **Min-Max Scaling**: [0,1] aralığına çevirme

## İstatistiksel Güç Analizi

### Sample Size Calculation
```python
# Minimum sample size hesaplaması
# Effect size = 0.3 (medium effect)
# Power = 0.8
# Alpha = 0.05

# T-test için: n = 64 per group
# ANOVA için: n = 52 per group
# Correlation için: n = 84 total
```

### Effect Size Interpretation
- **Cohen's d**: 0.2 (small), 0.5 (medium), 0.8 (large)
- **Eta-squared**: 0.01 (small), 0.06 (medium), 0.14 (large)
- **R²**: 0.02 (small), 0.13 (medium), 0.26 (large)

## Veri Kalitesi Kontrolü

### Data Quality Metrics
- **Completeness**: Eksik veri oranı
- **Consistency**: Tutarlılık kontrolü
- **Accuracy**: Doğruluk kontrolü
- **Timeliness**: Güncellik

### Validation Steps
1. **Data Profiling**: Temel istatistikler
2. **Distribution Analysis**: Normal dağılım kontrolü
3. **Correlation Analysis**: Multicollinearity tespiti
4. **Outlier Analysis**: Anomali tespiti

## Raporlama Standartları

### İstatistiksel Raporlama
- **APA Format**: Statistical reporting standards
- **Effect Sizes**: Her test için effect size
- **Confidence Intervals**: %95 güven aralıkları
- **P-values**: Exact p-values (p < 0.001)

### Görselleştirme Standartları
- **Chart Types**: Uygun grafik türü seçimi
- **Color Schemes**: Tutarlı renk paleti
- **Data Labels**: Açık ve anlaşılır etiketler
- **Interactive Elements**: Kullanıcı etkileşimi

### Anlaşılırlık Standartları
- **Eksen Etiketleri**: İstatistiksel terimler yerine günlük dil kullanımı
  - "Frekans" → "Geliştirici Sayısı"
  - "Yoğunluk" → "Oran"
  - "Ortalama" → "Ortalama Maaş"
- **Grafik Açıklamaları**: Her grafiğin altında "Bu Ne Anlama Geliyor?" bölümü
- **İstatistiksel Terimler**: Basit dilde açıklama
  - p-değeri: "Sonucun güvenilirliği"
  - Korelasyon: "İlişki gücü"
  - Standart sapma: "Değerlerin dağılımı"

## Analiz Süreci

### 1. Keşifsel Veri Analizi (EDA)
- **Descriptive Statistics**: Temel istatistikler
- **Distribution Plots**: Dağılım görselleştirmeleri
- **Correlation Matrix**: Korelasyon analizi
- **Missing Data Analysis**: Eksik veri analizi

### 2. İstatistiksel Testler
- **Parametric Tests**: Normal dağılım varsayımı
- **Non-parametric Tests**: Dağılım varsayımı yok
- **Post-hoc Analysis**: Çoklu karşılaştırmalar
- **Effect Size Calculation**: Etki büyüklüğü

### 3. Saat Bazlı Analiz Metodolojisi
- **Saat Bazlı Maaş Analizi**:
  - Her bir Anket_Saati için ortalama maaş ve standart sapma hesaplanacak
  - Saatler arasında ortalama maaşlarda anlamlı bir fark olup olmadığını belirlemek için ANOVA testi kullanılacak
  - p-değerleri, etki büyüklükleri (eta-squared) ve %95 güven aralıkları raporlanacak
- **Saat Bazlı Rol, Seviye ve Demografik Analizler**:
  - Anket_Saati'ne göre rol, kariyer seviyesi ve demografik özelliklerin dağılımları incelenecek
  - Bu dağılımlar arasında istatistiksel olarak anlamlı farklılıklar olup olmadığını belirlemek için Chi-square testi uygulanacak
  - p-değerleri ve etki büyüklükleri raporlanacak

### 3. Görselleştirme ve Raporlama
- **Dashboard Creation**: İnteraktif dashboard
- **Report Generation**: Detaylı raporlar
- **Presentation Preparation**: Sunum materyalleri
- **Insight Documentation**: İçgörü dokümantasyonu

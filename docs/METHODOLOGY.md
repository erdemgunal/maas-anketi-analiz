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

# 3. One-way ANOVA: Şirket lokasyonu bazlı maaş farkları
H0: μ_yurtdisi_tr_hub = μ_avrupa = μ_turkiye_merkez = μ_diger
H1: En az bir grup farklı

# 4. Two-way ANOVA: Şirket lokasyonu × Çalışma şekli etkileşimi
H0: Lokasyon ve çalışma şekli arasında etkileşim yok
H1: Lokasyon ve çalışma şekli arasında etkileşim var

# 5. Chi-square test: Cinsiyet vs teknoloji tercihi bağımsızlığı
H0: Cinsiyet ve teknoloji tercihi bağımsız
H1: Cinsiyet ve teknoloji tercihi bağımlı

# 6. Pearson correlation: Deneyim vs maaş ilişkisi
H0: ρ = 0 (Korelasyon yok)
H1: ρ ≠ 0 (Korelasyon var)

# 7. One-way ANOVA: Saat bazlı maaş farkları
H0: μ_saat0 = μ_saat1 = ... = μ_saat23
H1: En az bir saat grubu farklı

# 8. Chi-square test: Saat vs rol/seviye/demografik özellik bağımsızlığı
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
- **Şirket Lokasyonu Standardizasyonu**: Farklı yazım şekillerini standart kategorilere dönüştürme

### 2. Feature Engineering
- **Skill Dummy Variables**: Her teknoloji için binary column
- **Experience Numeric**: String deneyim → sayısal değer
- **Interaction Terms**: Teknoloji × deneyim kombinasyonları
- **Polynomial Features**: Non-linear ilişkiler için
- **Lokasyon Kategorileri**: Şirket lokasyonunu standart kategorilere dönüştürme
- **Çalışma Şekli × Lokasyon**: İki faktörün kombinasyonu

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
# Two-way ANOVA için: n = 45 per cell
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

### 4. Şirket Lokasyonu Analiz Metodolojisi
- **Lokasyon Bazlı Maaş Analizi**:
  - Her şirket lokasyonu kategorisi için ortalama maaş ve standart sapma hesaplanacak
  - Lokasyonlar arasında anlamlı maaş farkları olup olmadığını belirlemek için ANOVA testi kullanılacak
  - Post-hoc testler ile hangi lokasyonlar arasında fark olduğu belirlenecek
- **Lokasyon × Çalışma Şekli Etkileşimi**:
  - İki faktörün birlikte maaş üzerindeki etkisi analiz edilecek
  - Two-way ANOVA ile etkileşim etkisi test edilecek

### 5. Görselleştirme ve Raporlama
- **Dashboard Creation**: İnteraktif dashboard
- **Report Generation**: Detaylı raporlar
- **Presentation Preparation**: Sunum materyalleri
- **Insight Documentation**: İçgörü dokümantasyonu

## Sınırlılıklar ve Kısıtlamalar

### Veri Kalitesi Sınırlılıkları
- **Eksik Veriler**: Bazı katılımcılardan eksik bilgi toplanması
- **Yanlış Yanıtlar**: Anket sırasında yanlış bilgi verilmesi
- **Örneklem Temsiliyeti**: Belirli gruplardan yetersiz veri toplanması

### Metodolojik Sınırlılıklar
- **Cross-sectional Design**: Zaman içindeki değişimleri yakalayamama
- **Self-reported Data**: Katılımcıların kendi bildirdiği veriler
- **Selection Bias**: Gönüllü katılım nedeniyle oluşan yanlılık

### Coğrafi Analiz Sınırlılıkları
- **Fiziksel İkametgah Çıkarımındaki Sınırlılık**: `Şirket lokasyon` ve `Çalışma şekli` kombinasyonları analiz edilirken, özellikle `Yurtdışı TR hub` veya `Avrupa` lokasyonlu ve `Remote` çalışan kişilerin **fiziksel ikametgahının kesin olarak belirlenemediği** ve bunun coğrafi analizlerin önemli bir sınırlılığı olduğu
- **Şirket Lokasyonu Standardizasyonu**: Farklı yazım şekilleri ve kategorilerin standartlaştırılmasındaki zorluklar
- **Remote Çalışanların Gerçek Lokasyonu**: Remote çalışanların şirket lokasyonu ile ikametgahı arasındaki farklılıkların analiz edilememesi
- **Coğrafi Arbitraj Analizi**: Farklı lokasyonlardaki maaş farklılıklarından yararlanma stratejilerinin tam olarak ölçülememesi

### İstatistiksel Sınırlılıklar
- **Multiple Testing**: Çoklu test yapılması nedeniyle Type I error riski
- **Effect Size**: Küçük etki büyüklüklerinin pratik anlamlılığı
- **Generalizability**: Sonuçların genellenebilirliği

### Zaman Bazlı Sınırlılıklar
- **Veri Toplama Zamanı**: Anketin belirli bir dönemde toplanması
- **Piyasa Değişkenliği**: Maaş verilerinin zaman içindeki değişkenliği
- **Trend Analizi**: Uzun vadeli trendlerin yakalanamaması

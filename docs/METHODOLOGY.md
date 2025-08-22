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
```

### Güven Aralıkları
- **Confidence Level**: 95% (α = 0.05)
- **Effect Size**: Cohen's d, eta-squared
- **Power Analysis**: Minimum sample size hesaplaması

## Machine Learning Models

### Regresyon Modelleri
```python
# 1. Linear Regression (baseline)
from sklearn.linear_model import LinearRegression
# Baseline model olarak kullanılacak

# 2. Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor
# Non-linear ilişkileri yakalama

# 3. XGBoost Regressor
import xgboost as xgb
# Gradient boosting ile performans optimizasyonu

# 4. Feature importance analysis
# Her model için feature importance hesaplama
```

### Clustering
```python
# 1. K-means clustering (Developer personas)
from sklearn.cluster import KMeans
# Elbow method ile optimal k değeri

# 2. Hierarchical clustering (Stack combinations)
from sklearn.cluster import AgglomerativeClustering
# Dendrogram ile görselleştirme
```

### Model Değerlendirme
```python
# Cross-validation
from sklearn.model_selection import cross_val_score

# Metrics
- R² Score (Açıklama gücü)
- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)
- Adjusted R² (Feature sayısına göre düzeltilmiş)
```

## Veri İşleme Adımları

### 1. Data Cleaning
- **Maaş Normalizasyonu**: "61-70" → 65 (aralık ortalaması)
- **Teknoloji Ayrıştırma**: "React, Redux" → ayrı dummy variables
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
- **Isolation Forest**: ML-based outlier detection

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

### Model Performance Reporting
- **Cross-validation Results**: Mean ± SD
- **Feature Importance**: Ranked list
- **Residual Analysis**: Normality, homoscedasticity
- **Model Comparison**: Statistical significance

# Metodoloji

Bu doküman, `2025_maas_anket.csv` veri setinin temizlenmesi, ön işlenmesi, encode edilmesi, analiz için hazırlanması ve hipotez testleri süreçlerini detaylandırır. Temizlenmiş veri seti (`2025_cleaned_data.csv`) grafik üretimi ve analizlerde kullanılacaktır. Tüm adımlar, 100 satırlık örnek veri üzerinden test edilmiş ve tam veri seti (n=2,970) için genellenebilir. Adımlar, `DATASET_SPECIFICATIONS.MD` ile uyumludur ve istatistik bilmeyen okuyuculara hitap edecek şekilde ilgi çekici, anlaşılır ilişkiler vurgulanır.

## 1. Veri Yükleme ve İlk Kontroller

- **Amaç**: Ham veri setini (`2025_maas_anket.csv`) yüklemek ve temel kontrolleri yapmak.
- **Adımlar**:
  - Veri setini `pandas` ile yükle: `pd.read_csv('2025_maas_anket.csv')`.
  - Eksik veri kontrolü: `df.isna().sum()` (örnek veride %0 eksik veri doğrulandı).
  - Sütun adlarını İngilizce’ye çevir (ör. `Şirket lokasyon` → `company_location`).
  - Veri tiplerini kontrol et: `df.dtypes`.
- **Not**: Türkçe sütun adları, kodlama kolaylığı ve uluslararası paylaşım için İngilizce’ye çevrilecek.

**Örnek Kod**:

```python
import pandas as pd

# Veri yükleme
df = pd.read_csv('2025_maas_anket.csv')

# Sütun adlarını İngilizce'ye çevirme
df.columns = [
    'timestamp', 'company_location', 'employment_type', 'work_mode', 'gender',
    'experience_years', 'level', 'programming_languages', 'role',
    'frontend_technologies', 'tools', 'salary_range'
]

# Timestamp'i datetime objesine dönüştür
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Eksik veri kontrolü
assert df.isna().sum().sum() == 0, "Eksik veri tespit edildi!"
print(df.dtypes)
```

## 2. Maaş Normalizasyonu

- **Amaç**: `salary_range` sütununu sayısal bir feature’a (`salary_numeric`) dönüştürmek.
- **Adımlar**:
  - Aralıkları midpoint’e çevir: `0-10 → 5`, `61-70 → 65.5`, `300+ → 350`.
  - Formül: `midpoint = (lower + upper) / 2` (`300+` için sabit 350).
  - `pandas` ile regex parsing: `str.extract` kullanarak aralıkları ayır.
- **Çıktı**: Yeni sütun `salary_numeric` (bin TL cinsinden).

**Örnek Kod**:

```python
def normalize_salary(bin_str):
    if bin_str == '300 +':
        return 350
    lower, upper = map(float, bin_str.split(' - '))
    return (lower + upper) / 2

df['salary_range'] = df['salary_range'].str.replace('300 +', '300 - 300')
df['salary_numeric'] = df['salary_range'].apply(normalize_salary)
```

## 3. Çoklu Seçim Parsing

- **Amaç**: `programming_languages`, `frontend_technologies`, `tools` sütunlarındaki virgülle ayrılmış değerleri multi-hot encoding’e dönüştürmek.
- **Adımlar**:
  - Her sütun için `str.split(',')` ile değerleri ayır.
  - `sklearn.preprocessing.MultiLabelBinarizer` ile binary sütunlar oluştur (ör. `programming_Python`, `frontend_React`, `tool_redux`).
  - Boş değerler için `Hiçbiri` varsayımı.
- **Çıktı**: Her etiket için binary sütunlar (ör. `programming_Python=1`).

**Örnek Kod**:

```python
from sklearn.preprocessing import MultiLabelBinarizer

mlb = MultiLabelBinarizer()
for col in ['programming_languages', 'frontend_technologies', 'tools']:
    df[col] = df[col].str.split(',').fillna(['Hiçbiri'])
    encoded = pd.DataFrame(mlb.fit_transform(df[col]), columns=[f'{col.split("_")[0]}-{x}' for x in mlb.classes_], index=df.index, dtype=int)
    df = pd.concat([df, encoded], axis=1)
```

## 4. Kategorik Kodlama

- **Amaç**: Kategorik ve ordinal sütunları analiz için uygun formata dönüştürmek.
- **Adımlar**:
  - **Kategorik Sütunlar**:
    - `company_location`, `employment_type`, `work_mode`, `role` için `pd.get_dummies` (One-Hot Encoding).
    - Örnek: `company_location_Türkiye`, `company_location_Avrupa`.
  - **Ordinal Sütunlar**:
    - `experience_years`: Orta nokta ile sayısal dönüşüm (ör. `11-15 → 13`, `30+ → 30`).
    - **`level` (Hangi seviyedesin?) için `seniority_level_ic`**:
      - Teknik seviyeler (Junior, Mid, Senior, Staff Engineer, Team Lead, Architect) sıralı bir hiyerarşiye sahiptir (Junior < Mid < Senior < ... < Architect). Bu yüzden, bu seviyelere sayısal değerler atanır: `Junior=1`, `Mid=2`, `Senior=3`, `Staff Engineer=4`, `Team Lead=5`, `Architect=6`. Bu, `seniority_level_ic` sütununu oluşturur.
      - Yönetim rolleri (Engineering Manager, Director Level Manager, C-Level Manager, Partner) bu sıralı hiyerarşiye uymaz, çünkü teknik rollerdense yönetimsel pozisyonlardır. Bu yüzden, bu rollere `seniority_level_ic` için `0` atanır.
  - **Binary Sütunlar**:
    - `gender`: `Erkek=0`, `Kadın=1`.
    - `is_manager`: `Engineering Manager`, `Director Level Manager`, `C-Level Manager`, `Partner` → `1`, diğerleri → `0`.
  - **Yönetim ve Teknik Seviyeleri için Kategorik Kodlama**:
    - `level` sütunu, tüm seviyeleri (teknik ve yönetim) ayrı kategoriler olarak ele almak için `pd.get_dummies` ile One-Hot Encoding'e tabi tutulur. Bu, aşağıdaki sütunları üretir:
      - Teknik seviyeler: `management_Junior`, `management_Mid`, `management_Senior`, `management_Staff_Engineer`, `management_Team_Lead`, `management_Architect`.
      - Yönetim seviyeleri: `management_Engineering_Manager`, `management_Director_Level_Manager`, `management_C_Level_Manager`, `management_Partner`.
    - Bu sütunlar, spesifik bir seviyenin varlığını gösterir (örn. `management_Senior=1` bir çalışanın Senior olduğunu, `management_Engineering_Manager=1` bir çalışanın Engineering Manager olduğunu gösterir).
  - **Neden Hem Ordinal Hem Kategorik?**:
    - `level` sütunu, hem sıralı (teknik seviyeler için) hem de sıralı olmayan (yönetim rolleri için) kategoriler içerir. Bu yüzden:
      - **Ordinal Kodlama (`seniority_level_ic`)**: Teknik seviyeler arasındaki sıralı ilişkiyi (örn. Senior > Mid) analizlerde kullanmak için sayısal değerler atanır. Örneğin, maaşın seviye ile nasıl değiştiğini incelemek için.
      - **Binary Kodlama (`is_manager`)**: Bir çalışanın yönetim rolünde olup olmadığını belirlemek için (örn. "Yöneticiler teknik çalışanlardan daha mı fazla kazanıyor?").
      - **Kategorik Kodlama (`management_*`)**: Her seviyeyi (teknik ve yönetim) ayrı bir kategori olarak ele almak için. Örneğin, "Engineering Manager'lar Director'lardan daha mı fazla kazanıyor?" gibi spesifik karşılaştırmalar için.
    - Bu yaklaşım, analizlerde esneklik sağlar:
      - `seniority_level_ic`: Teknik seviyeler arasındaki maaş farklarını veya hiyerarşik ilişkileri incelemek için.
      - `is_manager`: Yöneticiler ile teknik çalışanlar arasında genel karşılaştırmalar için.
      - `management_*`: Spesifik seviyeler (örn. Senior vs. Engineering Manager) arasında detaylı analizler için.
  - **Sütun İsim Temizleme**:
    - Encoding sonrası tüm sütun isimlerini temizle: boşlukları `_` ile değiştir, Türkçe karakterleri latinize et.
    - Türkçe karakter dönüşümleri: `ı → i`, `ş → s`, `ğ → g`, `ü → u`, `ö → o`, `ç → c`, `İ → I`.
    - Özel karakterler: `-` → `_`, `+` → `_plus`, `#` → `_sharp`, `&` → `_and`.
    - Bu, sütun erişimini kolaylaştırır (örn. `df['management_Staff_Engineer']` yerine `df['management_Staff Engineer']` gibi hataları önler).
    - Örnek: `company_location_Yurtdışı TR hub` → `company_location_Yurtdisi_TR_hub`.

**Örnek Kod**:

```python
from unidecode import unidecode
import re

def clean_column_names(df):
    """Sütun isimlerini temizle: boşlukları _ ile değiştir, Türkçe karakterleri latinize et"""
    new_columns = {}
    for col in df.columns:
        # Türkçe karakterleri latinize et
        cleaned = unidecode(col)
        # Boşlukları _ ile değiştir
        cleaned = re.sub(r'\s+', '_', cleaned)
        # Özel karakterleri değiştir
        cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', cleaned)
        # Birden fazla _'yi tek _'ye çevir
        cleaned = re.sub(r'_+', '_', cleaned)
        # Başındaki ve sonundaki _'leri kaldır
        cleaned = cleaned.strip('_')
        new_columns[col] = cleaned
    return df.rename(columns=new_columns)

# Kategorik encoding (sayısal 0/1 değerleri için dtype=int kullan)
df = pd.get_dummies(df, columns=['company_location', 'employment_type', 'work_mode', 'role'], dtype=int)

# Gender encoding
df['gender'] = df['gender'].map({'Erkek': 0, 'Kadın': 1})

# Experience years encoding
experience_map = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                  '10': 10, '11 - 15': 13, '16 - 20': 18, '20 - 30': 25, '30+': 30}
df['experience_years'] = df['experience_years'].map(experience_map)

# Seniority level encoding
ic_map = {'Junior': 1, 'Mid': 2, 'Senior': 3, 'Staff Engineer': 4, 'Team Lead': 5, 'Architect': 6}
df['seniority_level_ic'] = df['level'].map(ic_map).fillna(0)  # Yönetim rolleri için 0
df['is_manager'] = df['level'].isin(['Engineering Manager', 'Director Level Manager', 'C-Level Manager', 'Partner']).astype(int)
df = pd.get_dummies(df, columns=['level'], prefix='management', dtype=int)

# Sütun isimlerini temizle
df = clean_column_names(df)

# Artık sütunlara güvenli şekilde erişebiliriz
# Örnek: df['management_Staff_Engineer'] (boşluk olmadan)
# Örnek: df['company_location_Yurtdisi_TR_hub'] (Türkçe karakter olmadan)
```

## 5. Çalışan Lokasyon Tahmini

- **Amaç**: `company_location` ve `work_mode` kombinasyonuna göre çalışanın lokasyonunu tahmin etmek.
- **Varsayım**: `company_location="Avrupa"` ve `work_mode="Office"` veya `work_mode="Hybrid"` ise, çalışanın büyük olasılıkla Avrupa’da bulunduğu varsayılır.
- **Adımlar**:
  - Yeni feature: `is_likely_in_company_location` (binary, 1=Office/Hybrid, 0=diğer).
  - Grafiklerde not: “Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır (Office/Hybrid → şirket lokasyonunda). Kesin değildir.”
- **Çıktı**: `is_likely_in_company_location` sütunu.

**Örnek Kod**:

```python
df['is_likely_in_company_location'] = ((df['work_mode'].isin(['Office', 'Hybrid'])) & (df['company_location'] != '')).astype(int)
```

## 6. Aykırı Değer İşleme

- **Amaç**: `salary_numeric` için aykırı değerleri sınırlandırmak.
- **Adımlar**:
  - **IQR Yöntemi**: `Q1 - 1.5*IQR` ve `Q3 + 1.5*IQR` ile alt/üst sınırlar.
  - **Z-Score Yöntemi**: |z| > 3 olan değerler aykırı kabul edilir ve sınırlandırılır.
  - Üst sınır: `salary_numeric > 350` için capping (350’ye sabitle).
  - Her iki yöntem karşılaştırılabilir; Z-Score daha hassas aykırı değer tespiti için tercih edilebilir.
- **Not**: Örnek veride aykırı değer kontrolü yapıldı, `300+` zaten 350’ye sabitleniyor.

**Örnek Kod**:

```python
import numpy as np

# IQR yöntemi
Q1 = df['salary_numeric'].quantile(0.25)
Q3 = df['salary_numeric'].quantile(0.75)
IQR = Q3 - Q1
lower_bound_iqr = Q1 - 1.5 * IQR
upper_bound_iqr = min(Q3 + 1.5 * IQR, 350)  # Üst sınır 350

# Z-Score yöntemi
z_scores = np.abs((df['salary_numeric'] - df['salary_numeric'].mean()) / df['salary_numeric'].std())
upper_bound_z = df['salary_numeric'][z_scores <= 3].max()
lower_bound_z = df['salary_numeric'][z_scores <= 3].min()

# IQR ve Z-Score sınırlarını birleştir
lower_bound = max(lower_bound_iqr, lower_bound_z)
upper_bound = min(upper_bound_iqr, upper_bound_z, 350)
df['salary_numeric'] = df['salary_numeric'].clip(lower=lower_bound, upper=upper_bound)
```

## 7. Temizlenmiş Veri Seti Oluşturma

- **Amaç**: Ham veriyi işlenmiş haliyle `2025_cleaned_data.csv` olarak kaydetmek.
- **Adımlar**:
  - Tüm encoding'ler ve türetilmiş feature'lar (`salary_numeric`, `seniority_level_ic`, `is_manager`, `is_likely_in_company_location`) dahil edilir.
  - **ÖNEMLİ**: `timestamp` sütunu korunmalı ve datetime objesi olarak saklanmalı (saat bazlı analizler için).
  - Orijinal Türkçe sütunlar kaldırılır.
  - Çıktı: `2025_cleaned_data.csv` (grafik ve analiz için ana veri kaynağı).
- **Not**: Bu dosya, Streamlit dashboard ve grafik üretiminde kullanılacak.

**Örnek Kod**:

```python
# Orijinal Türkçe sütunları kaldır (timestamp korunmalı)
df = df.drop(columns=['salary_range', 'programming_languages', 'frontend_technologies', 'tools'])
# timestamp sütununu datetime objesine dönüştür
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Temizlenmiş veri kaydet
df.to_csv('2025_cleaned_data.csv', index=False)
```

## 8. Hipotez Testleri

- **Amaç**: Verideki ilişkileri istatistiksel olarak test etmek, ancak istatistik bilmeyen okuyucular için sonuçları basit ve sezgisel bir şekilde sunmak.
- **Adımlar**:
  - **Yöntemler**:
    - **T-Testi** veya **Mann-Whitney U Testi**: İki grup arasında maaş farkı var mı? (örn. Remote vs. Office çalışanlar).
    - **ANOVA** veya **Kruskal-Wallis Testi**: Çoklu gruplar arasında maaş farkı (örn. seviye bazında).
    - **Post-hoc Testi (Tukey HSD)**: ANOVA sonrası hangi grupların farklı olduğunu belirlemek (örn. Junior vs. Senior maaş farkı).
    - **Pearson Korelasyonu**: Sayısal değişkenler arasındaki ilişkiyi ölçmek (örn. deneyim yılı ile maaş arasındaki ilişki).
    - Testler, istatistik bilmeyen okuyucular için “fark var mı?” veya “ilişki ne kadar güçlü?” gibi basit sorularla açıklanacak.
  - **Örnek Hipotezler** (detaylar `ANALYSIS_OBJECTIVES.MD`’de):
    - “Remote çalışanlar, ofis çalışanlarından daha yüksek maaş alıyor mu?”
    - “Avrupa merkezli şirketlerde çalışanlar, Türkiye merkezli olanlara göre daha yüksek maaş alıyor mu?”
    - “React kullanan frontend geliştiriciler, diğerlerinden daha yüksek maaş alıyor mu?”
    - “Deneyim yılı arttıkça maaş artar mı?” (Pearson korelasyonu ile).
  - **Not**: Test sonuçları, grafiklerle desteklenecek ve teknik terimler yerine anlaşılır ifadeler kullanılacak (örn. “ortalama maaş farkı” yerine “Remote çalışanlar ayda 20 bin TL daha fazla kazanıyor” veya “Deneyim yılı arttıkça maaş genellikle yükseliyor”).
- **Çıktı**: Hipotez test sonuçları, `ANALYSIS_OBJECTIVES.MD`’de tanımlanan hedeflere göre raporlanacak.

**Örnek Kod**:

```python
from scipy.stats import ttest_ind, mannwhitneyu, pearsonr
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Örnek: Remote vs. Office maaş farkı (temizlenmiş sütun isimleri)
remote_salaries = df[df['work_mode_Remote'] == 1]['salary_numeric']
office_salaries = df[df['work_mode_Office'] == 1]['salary_numeric']
t_stat, p_value = ttest_ind(remote_salaries, office_salaries, equal_var=False)
print(f"Remote vs. Office maaş farkı: p-değeri = {p_value:.3f}")
if p_value < 0.05:
    print("Remote ve Office çalışanların maaşları arasında anlamlı bir fark var.")
else:
    print("Remote ve Office çalışanların maaşları arasında anlamlı bir fark yok.")

# Örnek: Deneyim vs. maaş (Pearson korelasyonu)
corr, p_value = pearsonr(df['experience_years'], df['salary_numeric'])
print(f"Deneyim-Maaş korelasyonu: r = {corr:.3f}, p-değeri = {p_value:.3f}")
if p_value < 0.05:
    print("Deneyim yılı ile maaş arasında anlamlı bir ilişki var.")
else:
    print("Deneyim yılı ile maaş arasında anlamlı bir ilişki yok.")

# Örnek: Post-hoc testi (seviye bazında maaş farkı)
tukey = pairwise_tukeyhsd(endog=df['salary_numeric'], groups=df['seniority_level_ic'], alpha=0.05)
print(tukey)

# Örnek: Temizlenmiş sütun isimleri ile güvenli erişim
# df['management_Staff_Engineer'] (boşluk olmadan)
# df['company_location_Yurtdisi_TR_hub'] (Türkçe karakter olmadan)
```

## 9. Grafik Üretimi

- **Amaç**: `2025_cleaned_data.csv` kullanılarak istatistik bilmeyen okuyuculara hitap eden, ilgi çekici ve anlaşılır görselleştirmeler oluşturmak.
- **Adımlar**:
  - **Veri Kaynağı**: `2025_cleaned_data.csv`.
  - **Araçlar**: `seaborn`, `matplotlib` veya Streamlit için `plotly`.
  - **Örnek Grafikler**:
    - Maaş dağılımı (seviye bazında): `sns.boxplot(x='seniority_level_ic', y='salary_numeric')`.
    - Lokasyon tahmini analizi: `sns.boxplot(x='is_likely_in_company_location', y='salary_numeric')`.
    - Programlama dili kullanımı: `sns.barplot(x='programming_Python', y='salary_numeric')`.
    - Deneyim vs. maaş ilişkisi: `sns.scatterplot(x='experience_years', y='salary_numeric')` (Pearson korelasyonu ile desteklenir).
    - Kariyer Gelişim Grafiği (Career Progression - Salary Growth): `is_likely_in_company_location == 1` filtresiyle, `company_location ∈ {Türkiye, Avrupa, Amerika}` için `seniority_level_ic ∈ {1,2,3}` (Junior, Mid, Senior) bazında ortalama `salary_numeric` çizgileri.
    - Top Tech Combinations by Role: `role` x (diller: `programming_*` + frontend: `frontend_*` + araçlar: `tools_*`) kombinasyonlarının ortalama `salary_numeric` karşılaştırması; "Hiçbiri" ve "Kullanmıyorum" etiketleri analiz dışı bırakılır; en yüksek ve en düşük ilk 10 kombinasyon raporlanır.
    - Korelasyon Isı Haritası: `salary_numeric`, `experience_years`, `seniority_level_ic`, seçili teknoloji/araç sütunları için Pearson korelasyon matrisi (mutlak değeri en yüksek ilk 20 özellik vurgulanır).
    - Work Type x Location Isı Haritası: `work_mode` x `company_location` kesişimlerinde ortalama `salary_numeric` (n≥10 hücreler gösterilir).
    - Çalışma Düzeni ve Rol (Work Arrangement by Role): Örneklem sayısı en yüksek 10–15 rol için `work_mode` yüzdelik yığılmış bar (100% stacked); opsiyonel olarak rol başına ortalama maaş çizgisi.
    - Araç Benimseme Grafiği (Top Tool Adoption by Role): `tools_*` sütunlarının rol bazında ortalamaları (kullanım oranı) ile ısı haritası; "Kullanmıyorum" hariç; n≥20 roller.
    - Keman Grafiği (Skill Diversity): Toplam beceri çeşitliliği (`skill_diversity_total`) ile `salary_numeric` dağılımının `sns.violinplot` ile görselleştirilmesi.
    - **Not**: Tüm sütun isimleri temizlenmiş haliyle kullanılır (örn. `management_Staff_Engineer`, `company_location_Yurtdisi_TR_hub`).
  - **Not**: Grafikler, “maaş farkı”, “popüler teknolojiler”, “deneyim-maaş ilişkisi” gibi merak uyandıran ilişkilere odaklanacak. `company_location` içeren grafiklerde şu not eklenecek:
    - “Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır (Office/Hybrid → şirket lokasyonunda). Kesin değildir.”
- **Çıktı**: PNG veya interaktif grafikler (Streamlit için).

**Örnek Kod** (Deneyim vs. maaş scatter plot):

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Deneyim vs. maaş scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x='experience_years', y='salary_numeric', data=df)
plt.title('Deneyim Yılı ve Maaş İlişkisi')
plt.xlabel('Deneyim Yılı')
plt.ylabel('Aylık Net Maaş (bin TL)')
plt.figtext(0.5, 0.01, 'Not: Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır (Office/Hybrid → şirket lokasyonunda). Kesin değildir.', 
            ha='center', fontsize=10)
plt.savefig('experience_vs_salary.png', dpi=300)
plt.show()
```

## 10. Kalite Kontrol ve Doğrulama

- **Amaç**: Veri işleme adımlarının doğruluğunu ve tekrarlanabilirliğini sağlamak.
- **Adımlar**:
  - Eksik veri kontrolü: `df.isna().sum()` (örnek veride 0).
  - Encoding doğrulama: `pd.get_dummies` sonrası sütun sayısını kontrol et (`df.shape`).
  - Maaş normalizasyonu kontrolü: `salary_numeric` dağılımı (`df['salary_numeric'].describe()`).
  - Lokasyon tahmini kontrolü: `is_likely_in_company_location` dağılımı (`df['is_likely_in_company_location'].value_counts()`).
  - Korelasyon kontrolü: `experience_years` ve `salary_numeric` arasındaki Pearson korelasyonu.
- **Not**: Tüm adımlar bir Jupyter notebook’ta dokümante edilecek.

**Örnek Kod**:

```python
# Kalite kontrol
print("Eksik veri:", df.isna().sum().sum())
print("Sütun sayısı:", df.shape[1])
print("Maaş dağılımı:", df['salary_numeric'].describe())
print("Lokasyon tahmini:", df['is_likely_in_company_location'].value_counts())
corr, p_value = pearsonr(df['experience_years'], df['salary_numeric'])
print(f"Deneyim-Maaş korelasyonu: r = {corr:.3f}, p-değeri = {p_value:.3f}")
```

## Notlar

- **Erişim**: Google Sheets linki sınırlı (https://docs.google.com/spreadsheets/d/1J_MW7t9e2Yi1cErFe5XCnNGaFqXkrdufgZv9Ggnm-RE/edit?usp=sharing). Örnek veri (100 satır) ile test yapıldı, tam veri (n=2,970) önerilir.
- **Timestamp**: Anket 2 günde toplandığından, zaman bazlı analiz sınırlı (örn. saatlik trendler anlamlız).
- **Çalışan Lokasyon Tahmini**: `is_likely_in_company_location` feature’ı, grafiklerde ve alt grup analizlerinde kullanılacak. Grafiklerde not zorunlu: “Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır (Office/Hybrid → şirket lokasyonunda). Kesin değildir.”
- **Okuyucu Odaklı Analiz**: Grafikler ve hipotez testleri, istatistik bilmeyen okuyucular için anlaşılır ve merak uyandıran ilişkiler (örn. maaş-lokasyon, maaş-rol, maaş-dil, deneyim-maaş) üzerine odaklanacak.
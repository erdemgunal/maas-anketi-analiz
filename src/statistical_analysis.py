"""
İstatistiksel Analiz Modülü

Bu modül, maaş anketi verisinin istatistiksel analizi için gerekli
fonksiyonları içerir.

Fonksiyonlar:
- descriptive_statistics: Temel istatistikler ve dağılım analizi
- hypothesis_testing: Hipotez testleri (t-test, ANOVA, chi-square)
- correlation_analysis: Korelasyon analizi
- effect_size_calculations: Etki büyüklüğü hesaplamaları
- statistical_report: İstatistiksel rapor oluşturma
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_ind, f_oneway, chi2_contingency, pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')

# Görselleştirme ayarları
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12


def load_cleaned_data(file_path: str = '../data/cleaned_data.csv') -> pd.DataFrame:
    """
    Temizlenmiş veriyi yükler.
    
    Args:
        file_path: Temizlenmiş veri dosya yolu
        
    Returns:
        pd.DataFrame: Temizlenmiş veri seti
    """
    df = pd.read_csv(file_path)
    print(f"Temizlenmiş veri yüklendi. Boyut: {df.shape}")
    return df


def descriptive_statistics(df: pd.DataFrame, salary_column: str = 'salary_normalized') -> dict:
    """
    Temel istatistikler ve dağılım analizi yapar.
    
    Args:
        df: Veri seti
        salary_column: Maaş sütunu adı
        
    Returns:
        dict: İstatistiksel özet
    """
    print("=== TEMEL İSTATİSTİKLER ===")
    
    # Maaş istatistikleri
    salary_stats = {
        'count': len(df[salary_column]),
        'mean': df[salary_column].mean(),
        'median': df[salary_column].median(),
        'std': df[salary_column].std(),
        'min': df[salary_column].min(),
        'max': df[salary_column].max(),
        'q25': df[salary_column].quantile(0.25),
        'q75': df[salary_column].quantile(0.75),
        'skewness': df[salary_column].skew(),
        'kurtosis': df[salary_column].kurtosis()
    }
    
    print(f"Maaş İstatistikleri:")
    print(f"  Ortalama: {salary_stats['mean']:.2f} bin TL")
    print(f"  Medyan: {salary_stats['median']:.2f} bin TL")
    print(f"  Standart Sapma: {salary_stats['std']:.2f} bin TL")
    print(f"  Minimum: {salary_stats['min']:.2f} bin TL")
    print(f"  Maksimum: {salary_stats['max']:.2f} bin TL")
    print(f"  Çarpıklık: {salary_stats['skewness']:.3f}")
    print(f"  Basıklık: {salary_stats['kurtosis']:.3f}")
    
    # Demografik istatistikler
    print(f"\nDemografik İstatistikler:")
    print(f"  Toplam katılımcı: {len(df)}")
    print(f"  Erkek oranı: {(df['Cinsiyet'] == 0).mean()*100:.1f}%")
    print(f"  Kadın oranı: {(df['Cinsiyet'] == 1).mean()*100:.1f}%")
    
    # Deneyim seviyesi dağılımı
    experience_dist = df['Hangi seviyedesin?'].value_counts()
    print(f"\nDeneyim Seviyesi Dağılımı:")
    for level, count in experience_dist.items():
        percentage = (count / len(df)) * 100
        print(f"  Seviye {level}: {count} ({percentage:.1f}%)")
    
    return salary_stats


def hypothesis_testing(df: pd.DataFrame, salary_column: str = 'salary_normalized') -> dict:
    """
    Hipotez testlerini uygular.
    
    Args:
        df: Veri seti
        salary_column: Maaş sütunu adı
        
    Returns:
        dict: Test sonuçları
    """
    print("\n=== HİPOTEZ TESTLERİ ===")
    
    results = {}
    
    # 1. React vs non-React t-test
    print("1. React vs Non-React Maaş Farkı (t-test)")
    react_salary = df[df['Frontend_React'] == 1][salary_column]
    non_react_salary = df[df['Frontend_React'] == 0][salary_column]
    
    t_stat, p_value = ttest_ind(react_salary, non_react_salary)
    mean_diff = react_salary.mean() - non_react_salary.mean()
    
    results['react_vs_nonreact'] = {
        'test_type': 't-test',
        't_statistic': t_stat,
        'p_value': p_value,
        'mean_difference': mean_diff,
        'react_mean': react_salary.mean(),
        'non_react_mean': non_react_salary.mean(),
        'significant': p_value < 0.05
    }
    
    print(f"  React kullananlar ortalama: {react_salary.mean():.2f} bin TL")
    print(f"  React kullanmayanlar ortalama: {non_react_salary.mean():.2f} bin TL")
    print(f"  Fark: {mean_diff:.2f} bin TL")
    print(f"  t-istatistiği: {t_stat:.3f}")
    print(f"  p-değeri: {p_value:.6f}")
    print(f"  Anlamlı fark: {'Evet' if p_value < 0.05 else 'Hayır'}")
    
    # 2. Remote vs Office vs Hybrid ANOVA
    print(f"\n2. Çalışma Şekli Maaş Farkı (ANOVA)")
    remote_salary = df[df['Çalışma şekli'] == 0][salary_column]  # Remote
    hybrid_salary = df[df['Çalışma şekli'] == 1][salary_column]  # Hybrid
    office_salary = df[df['Çalışma şekli'] == 2][salary_column]  # Office
    
    f_stat, p_value = f_oneway(remote_salary, hybrid_salary, office_salary)
    
    results['work_type_anova'] = {
        'test_type': 'ANOVA',
        'f_statistic': f_stat,
        'p_value': p_value,
        'remote_mean': remote_salary.mean(),
        'hybrid_mean': hybrid_salary.mean(),
        'office_mean': office_salary.mean(),
        'significant': p_value < 0.05
    }
    
    print(f"  Remote ortalama: {remote_salary.mean():.2f} bin TL")
    print(f"  Hybrid ortalama: {hybrid_salary.mean():.2f} bin TL")
    print(f"  Office ortalama: {office_salary.mean():.2f} bin TL")
    print(f"  F-istatistiği: {f_stat:.3f}")
    print(f"  p-değeri: {p_value:.6f}")
    print(f"  Anlamlı fark: {'Evet' if p_value < 0.05 else 'Hayır'}")
    
    # 3. Cinsiyet bazlı maaş farkı
    print(f"\n3. Cinsiyet Bazlı Maaş Farkı (t-test)")
    male_salary = df[df['Cinsiyet'] == 0][salary_column]  # Erkek
    female_salary = df[df['Cinsiyet'] == 1][salary_column]  # Kadın
    
    t_stat, p_value = ttest_ind(male_salary, female_salary)
    mean_diff = male_salary.mean() - female_salary.mean()
    
    results['gender_gap'] = {
        'test_type': 't-test',
        't_statistic': t_stat,
        'p_value': p_value,
        'mean_difference': mean_diff,
        'male_mean': male_salary.mean(),
        'female_mean': female_salary.mean(),
        'significant': p_value < 0.05
    }
    
    print(f"  Erkek ortalama: {male_salary.mean():.2f} bin TL")
    print(f"  Kadın ortalama: {female_salary.mean():.2f} bin TL")
    print(f"  Fark: {mean_diff:.2f} bin TL")
    print(f"  t-istatistiği: {t_stat:.3f}")
    print(f"  p-değeri: {p_value:.6f}")
    print(f"  Anlamlı fark: {'Evet' if p_value < 0.05 else 'Hayır'}")
    
    # 4. Deneyim seviyesi ANOVA
    print(f"\n4. Deneyim Seviyesi Maaş Farkı (ANOVA)")
    junior_salary = df[df['Hangi seviyedesin?'] == 0][salary_column]  # Junior
    mid_salary = df[df['Hangi seviyedesin?'] == 1][salary_column]     # Mid
    senior_salary = df[df['Hangi seviyedesin?'] == 2][salary_column]  # Senior
    
    f_stat, p_value = f_oneway(junior_salary, mid_salary, senior_salary)
    
    results['experience_level_anova'] = {
        'test_type': 'ANOVA',
        'f_statistic': f_stat,
        'p_value': p_value,
        'junior_mean': junior_salary.mean(),
        'mid_mean': mid_salary.mean(),
        'senior_mean': senior_salary.mean(),
        'significant': p_value < 0.05
    }
    
    print(f"  Junior ortalama: {junior_salary.mean():.2f} bin TL")
    print(f"  Mid ortalama: {mid_salary.mean():.2f} bin TL")
    print(f"  Senior ortalama: {senior_salary.mean():.2f} bin TL")
    print(f"  F-istatistiği: {f_stat:.3f}")
    print(f"  p-değeri: {p_value:.6f}")
    print(f"  Anlamlı fark: {'Evet' if p_value < 0.05 else 'Hayır'}")
    
    return results


def correlation_analysis(df: pd.DataFrame, salary_column: str = 'salary_normalized') -> dict:
    """
    Korelasyon analizi yapar.
    
    Args:
        df: Veri seti
        salary_column: Maaş sütunu adı
        
    Returns:
        dict: Korelasyon sonuçları
    """
    print("\n=== KORELASYON ANALİZİ ===")
    
    # Sayısal sütunları seç
    numerical_columns = df.select_dtypes(include=[np.number]).columns
    numerical_columns = [col for col in numerical_columns if col != salary_column]
    
    correlations = {}
    
    # Her sayısal değişken ile maaş arasındaki korelasyon
    print("Maaş ile Korelasyon Analizi:")
    for col in numerical_columns[:10]:  # İlk 10 değişken
        if col in df.columns:
            corr, p_value = pearsonr(df[salary_column], df[col])
            correlations[col] = {
                'pearson_corr': corr,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
            
            significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else ""
            print(f"  {col}: {corr:.3f}{significance} (p={p_value:.4f})")
    
    # En yüksek korelasyonlu değişkenler
    sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]['pearson_corr']), reverse=True)
    
    print(f"\nEn Yüksek Korelasyonlu Değişkenler:")
    for col, corr_info in sorted_correlations[:5]:
        print(f"  {col}: {corr_info['pearson_corr']:.3f}")
    
    return correlations


def effect_size_calculations(df: pd.DataFrame, salary_column: str = 'salary_normalized') -> dict:
    """
    Etki büyüklüğü hesaplamaları yapar.
    
    Args:
        df: Veri seti
        salary_column: Maaş sütunu adı
        
    Returns:
        dict: Etki büyüklüğü sonuçları
    """
    print("\n=== ETKİ BÜYÜKLÜĞÜ HESAPLAMALARI ===")
    
    effect_sizes = {}
    
    # 1. React vs Non-React (Cohen's d)
    react_salary = df[df['Frontend_React'] == 1][salary_column]
    non_react_salary = df[df['Frontend_React'] == 0][salary_column]
    
    pooled_std = np.sqrt(((len(react_salary) - 1) * react_salary.var() + 
                         (len(non_react_salary) - 1) * non_react_salary.var()) / 
                        (len(react_salary) + len(non_react_salary) - 2))
    
    cohens_d = (react_salary.mean() - non_react_salary.mean()) / pooled_std
    
    effect_sizes['react_cohens_d'] = cohens_d
    
    print(f"1. React vs Non-React (Cohen's d): {cohens_d:.3f}")
    if abs(cohens_d) < 0.2:
        print("  Etki büyüklüğü: Küçük")
    elif abs(cohens_d) < 0.5:
        print("  Etki büyüklüğü: Orta")
    elif abs(cohens_d) < 0.8:
        print("  Etki büyüklüğü: Büyük")
    else:
        print("  Etki büyüklüğü: Çok büyük")
    
    # 2. Cinsiyet farkı (Cohen's d)
    male_salary = df[df['Cinsiyet'] == 0][salary_column]
    female_salary = df[df['Cinsiyet'] == 1][salary_column]
    
    pooled_std = np.sqrt(((len(male_salary) - 1) * male_salary.var() + 
                         (len(female_salary) - 1) * female_salary.var()) / 
                        (len(male_salary) + len(female_salary) - 2))
    
    cohens_d = (male_salary.mean() - female_salary.mean()) / pooled_std
    
    effect_sizes['gender_cohens_d'] = cohens_d
    
    print(f"\n2. Cinsiyet Farkı (Cohen's d): {cohens_d:.3f}")
    if abs(cohens_d) < 0.2:
        print("  Etki büyüklüğü: Küçük")
    elif abs(cohens_d) < 0.5:
        print("  Etki büyüklüğü: Orta")
    elif abs(cohens_d) < 0.8:
        print("  Etki büyüklüğü: Büyük")
    else:
        print("  Etki büyüklüğü: Çok büyük")
    
    # 3. Deneyim seviyesi (Eta-squared)
    junior_salary = df[df['Hangi seviyedesin?'] == 0][salary_column]
    mid_salary = df[df['Hangi seviyedesin?'] == 1][salary_column]
    senior_salary = df[df['Hangi seviyedesin?'] == 2][salary_column]
    
    f_stat, p_value = f_oneway(junior_salary, mid_salary, senior_salary)
    
    # Eta-squared hesaplama
    ss_between = (len(junior_salary) * (junior_salary.mean() - df[salary_column].mean())**2 +
                 len(mid_salary) * (mid_salary.mean() - df[salary_column].mean())**2 +
                 len(senior_salary) * (senior_salary.mean() - df[salary_column].mean())**2)
    
    ss_total = sum((df[salary_column] - df[salary_column].mean())**2)
    eta_squared = ss_between / ss_total
    
    effect_sizes['experience_eta_squared'] = eta_squared
    
    print(f"\n3. Deneyim Seviyesi (Eta-squared): {eta_squared:.3f}")
    if eta_squared < 0.01:
        print("  Etki büyüklüğü: Küçük")
    elif eta_squared < 0.06:
        print("  Etki büyüklüğü: Orta")
    elif eta_squared < 0.14:
        print("  Etki büyüklüğü: Büyük")
    else:
        print("  Etki büyüklüğü: Çok büyük")
    
    return effect_sizes


def create_statistical_tables(results: dict, output_path: str = '../outputs/tables/') -> None:
    """
    İstatistiksel test sonuçlarını tablo formatında kaydeder.
    
    Args:
        results: Test sonuçları
        output_path: Kayıt yolu
    """
    import os
    os.makedirs(output_path, exist_ok=True)
    
    # Hipotez testleri tablosu
    hypothesis_table = []
    for test_name, test_result in results.items():
        if 'test_type' in test_result:
            hypothesis_table.append({
                'Test': test_name,
                'Test Türü': test_result['test_type'],
                'İstatistik': f"{test_result.get('t_statistic', test_result.get('f_statistic', 'N/A')):.3f}",
                'p-değeri': f"{test_result['p_value']:.6f}",
                'Anlamlı': 'Evet' if test_result['significant'] else 'Hayır'
            })
    
    hypothesis_df = pd.DataFrame(hypothesis_table)
    hypothesis_df.to_csv(f"{output_path}hypothesis_tests.csv", index=False)
    print(f"Hipotez testleri tablosu kaydedildi: {output_path}hypothesis_tests.csv")


def statistical_report(df: pd.DataFrame, output_path: str = '../outputs/tables/') -> dict:
    """
    Kapsamlı istatistiksel rapor oluşturur.
    
    Args:
        df: Veri seti
        output_path: Çıktı yolu
        
    Returns:
        dict: Tüm analiz sonuçları
    """
    print("=== İSTATİSTİKSEL ANALİZ RAPORU ===")
    
    # 1. Temel istatistikler
    desc_stats = descriptive_statistics(df)
    
    # 2. Hipotez testleri
    hypothesis_results = hypothesis_testing(df)
    
    # 3. Korelasyon analizi
    correlation_results = correlation_analysis(df)
    
    # 4. Etki büyüklüğü hesaplamaları
    effect_size_results = effect_size_calculations(df)
    
    # 5. Tabloları kaydet
    create_statistical_tables(hypothesis_results, output_path)
    
    # 6. Özet rapor
    print(f"\n=== ÖZET RAPOR ===")
    print(f"Toplam test sayısı: {len(hypothesis_results)}")
    print(f"Anlamlı test sayısı: {sum(1 for r in hypothesis_results.values() if r.get('significant', False))}")
    print(f"En yüksek korelasyon: {max(correlation_results.values(), key=lambda x: abs(x['pearson_corr']))['pearson_corr']:.3f}")
    
    return {
        'descriptive_stats': desc_stats,
        'hypothesis_tests': hypothesis_results,
        'correlations': correlation_results,
        'effect_sizes': effect_size_results
    }


if __name__ == "__main__":
    # Test çalıştırması
    df = load_cleaned_data()
    results = statistical_report(df)
    print(f"\nİstatistiksel analiz tamamlandı!")

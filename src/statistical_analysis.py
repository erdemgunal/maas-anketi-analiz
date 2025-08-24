"""
İstatistiksel Analiz Modülü

Bu modül, Sprint 2 kapsamında temel istatistiksel hipotez testlerini, etki büyüklüklerini
ve korelasyon analizlerini gerçekleştirir.

Author: Erdem Gunal
Date: 2024
Sprint: 2 - Temel İstatistiksel Analiz ve Hipotez Testleri
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import ttest_ind, f_oneway, pearsonr, spearmanr
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import logging
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Ortak fonksiyonları import et
try:
    from .utils import (
        load_data, interpret_cohens_d, interpret_eta_squared, interpret_correlation,
        save_results_to_csv, CAREER_LEVELS, WORK_TYPES, GENDER_MAPPING
    )
except ImportError:
    # Doğrudan çalıştırıldığında absolute import kullan
    from utils import (
        load_data, interpret_cohens_d, interpret_eta_squared, interpret_correlation,
        save_results_to_csv, CAREER_LEVELS, WORK_TYPES, GENDER_MAPPING
    )

# Logging konfigürasyonu
logger = logging.getLogger(__name__)


class StatisticalAnalyzer:
    """
    İstatistiksel analiz için ana sınıf.
    """
    
    def __init__(self, data_path: str = "data/cleaned_data.csv"):
        """
        StatisticalAnalyzer sınıfını başlatır.
        
        Args:
            data_path (str): Temizlenmiş veri dosyasının yolu
        """
        self.data_path = data_path
        self.df = None
        self.results = {}
        
    def load_data(self) -> pd.DataFrame:
        """
        Temizlenmiş veriyi yükler.
        
        Returns:
            pd.DataFrame: Yüklenen veri seti
        """
        self.df = load_data(self.data_path)
        return self.df
    
    def react_salary_analysis(self) -> Dict:
        """
        React kullanımının maaşa etkisini analiz eder (t-test).
        
        Returns:
            Dict: Test sonuçları
        """
        logger.info("React kullanımının maaşa etkisi analiz ediliyor...")
        
        if 'frontend_react' not in self.df.columns or 'ortalama_maas' not in self.df.columns:
            raise ValueError("Gerekli sütunlar bulunamadı: frontend_react, ortalama_maas")
        
        # Grupları ayır
        react_users = self.df[self.df['frontend_react'] == 1]['ortalama_maas']
        non_react_users = self.df[self.df['frontend_react'] == 0]['ortalama_maas']
        
        # T-test uygula
        t_stat, p_value = ttest_ind(react_users, non_react_users)
        
        # Cohen's d etki büyüklüğü hesapla
        pooled_std = np.sqrt(((len(react_users) - 1) * react_users.var() + 
                             (len(non_react_users) - 1) * non_react_users.var()) / 
                            (len(react_users) + len(non_react_users) - 2))
        cohens_d = (react_users.mean() - non_react_users.mean()) / pooled_std
        
        # Güven aralığı hesapla
        diff = react_users.mean() - non_react_users.mean()
        se_diff = np.sqrt(react_users.var() / len(react_users) + non_react_users.var() / len(non_react_users))
        ci_lower = diff - 1.96 * se_diff
        ci_upper = diff + 1.96 * se_diff
        
        results = {
            'test_type': 'Independent t-test',
            'groups': ['React Kullanıcıları', 'React Kullanmayanlar'],
            'n1': len(react_users),
            'n2': len(non_react_users),
            'mean1': react_users.mean(),
            'mean2': non_react_users.mean(),
            'std1': react_users.std(),
            'std2': non_react_users.std(),
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'effect_size_interpretation': self._interpret_cohens_d(cohens_d),
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'significant': p_value < 0.05
        }
        
        logger.info(f"React analizi tamamlandı. p-value: {p_value:.4f}, Cohen's d: {cohens_d:.3f}")
        return results
    
    def work_type_salary_analysis(self) -> Dict:
        """
        Çalışma şeklinin maaşa etkisini analiz eder (ANOVA).
        
        Returns:
            Dict: Test sonuçları
        """
        logger.info("Çalışma şeklinin maaşa etkisi analiz ediliyor...")
        
        if 'calisma_sekli' not in self.df.columns or 'ortalama_maas' not in self.df.columns:
            raise ValueError("Gerekli sütunlar bulunamadı: calisma_sekli, ortalama_maas")
        
        # Grupları ayır (0: Remote, 1: Office, 2: Hybrid)
        groups = []
        group_names = ['Remote', 'Office', 'Hybrid']
        
        for i in range(3):
            group_data = self.df[self.df['calisma_sekli'] == i]['ortalama_maas']
            if len(group_data) > 0:
                groups.append(group_data)
        
        if len(groups) < 2:
            raise ValueError("En az 2 grup gerekli")
        
        # ANOVA uygula
        f_stat, p_value = f_oneway(*groups)
        
        # Eta-squared hesapla
        total_ss = sum([((group - group.mean()) ** 2).sum() for group in groups])
        between_ss = sum([len(group) * ((group.mean() - self.df['ortalama_maas'].mean()) ** 2) for group in groups])
        eta_squared = between_ss / (between_ss + total_ss)
        
        # Post-hoc test (Tukey HSD)
        all_data = []
        all_labels = []
        for i, group in enumerate(groups):
            all_data.extend(group)
            all_labels.extend([group_names[i]] * len(group))
        
        tukey_result = pairwise_tukeyhsd(all_data, all_labels)
        
        # Grup istatistikleri
        group_stats = {}
        for i, group in enumerate(groups):
            group_stats[group_names[i]] = {
                'n': len(group),
                'mean': group.mean(),
                'std': group.std()
            }
        
        results = {
            'test_type': 'One-way ANOVA',
            'groups': group_names,
            'group_stats': group_stats,
            'f_statistic': f_stat,
            'p_value': p_value,
            'eta_squared': eta_squared,
            'effect_size_interpretation': self._interpret_eta_squared(eta_squared),
            'tukey_result': tukey_result,
            'significant': p_value < 0.05
        }
        
        logger.info(f"Çalışma şekli analizi tamamlandı. p-value: {p_value:.4f}, Eta-squared: {eta_squared:.3f}")
        return results
    
    def location_salary_analysis(self) -> Dict:
        """
        Şirket lokasyonunun maaşa etkisini analiz eder (ANOVA).
        
        Returns:
            Dict: Test sonuçları
        """
        logger.info("Şirket lokasyonunun maaşa etkisi analiz ediliyor...")
        
        # Lokasyon sütunlarını bul
        location_cols = [col for col in self.df.columns if col.startswith('location_')]
        
        if not location_cols or 'ortalama_maas' not in self.df.columns:
            raise ValueError("Lokasyon sütunları veya ortalama_maas bulunamadı")
        
        # Grupları ayır
        groups = []
        group_names = []
        
        for col in location_cols:
            group_data = self.df[self.df[col] == 1]['ortalama_maas']
            if len(group_data) > 0:
                groups.append(group_data)
                group_names.append(col.replace('location_', '').replace('_', ' ').title())
        
        if len(groups) < 2:
            raise ValueError("En az 2 lokasyon grubu gerekli")
        
        # ANOVA uygula
        f_stat, p_value = f_oneway(*groups)
        
        # Eta-squared hesapla
        total_ss = sum([((group - group.mean()) ** 2).sum() for group in groups])
        between_ss = sum([len(group) * ((group.mean() - self.df['ortalama_maas'].mean()) ** 2) for group in groups])
        eta_squared = between_ss / (between_ss + total_ss)
        
        # Post-hoc test (Tukey HSD)
        all_data = []
        all_labels = []
        for i, group in enumerate(groups):
            all_data.extend(group)
            all_labels.extend([group_names[i]] * len(group))
        
        tukey_result = pairwise_tukeyhsd(all_data, all_labels)
        
        # Grup istatistikleri
        group_stats = {}
        for i, group in enumerate(groups):
            group_stats[group_names[i]] = {
                'n': len(group),
                'mean': group.mean(),
                'std': group.std()
            }
        
        results = {
            'test_type': 'One-way ANOVA',
            'groups': group_names,
            'group_stats': group_stats,
            'f_statistic': f_stat,
            'p_value': p_value,
            'eta_squared': eta_squared,
            'effect_size_interpretation': self._interpret_eta_squared(eta_squared),
            'tukey_result': tukey_result,
            'significant': p_value < 0.05
        }
        
        logger.info(f"Lokasyon analizi tamamlandı. p-value: {p_value:.4f}, Eta-squared: {eta_squared:.3f}")
        return results
    
    def gender_salary_analysis(self) -> Dict:
        """
        Cinsiyet bazlı maaş farkını analiz eder (t-test).
        
        Returns:
            Dict: Test sonuçları
        """
        logger.info("Cinsiyet bazlı maaş farkı analiz ediliyor...")
        
        if 'cinsiyet' not in self.df.columns or 'ortalama_maas' not in self.df.columns:
            raise ValueError("Gerekli sütunlar bulunamadı: cinsiyet, ortalama_maas")
        
        # Grupları ayır (0: Erkek, 1: Kadın)
        male_salary = self.df[self.df['cinsiyet'] == 0]['ortalama_maas']
        female_salary = self.df[self.df['cinsiyet'] == 1]['ortalama_maas']
        
        # T-test uygula
        t_stat, p_value = ttest_ind(male_salary, female_salary)
        
        # Cohen's d etki büyüklüğü hesapla
        pooled_std = np.sqrt(((len(male_salary) - 1) * male_salary.var() + 
                             (len(female_salary) - 1) * female_salary.var()) / 
                            (len(male_salary) + len(female_salary) - 2))
        cohens_d = (male_salary.mean() - female_salary.mean()) / pooled_std
        
        # Güven aralığı hesapla
        diff = male_salary.mean() - female_salary.mean()
        se_diff = np.sqrt(male_salary.var() / len(male_salary) + female_salary.var() / len(female_salary))
        ci_lower = diff - 1.96 * se_diff
        ci_upper = diff + 1.96 * se_diff
        
        # Gender gap yüzdesi
        gender_gap_percentage = (diff / female_salary.mean()) * 100
        
        results = {
            'test_type': 'Independent t-test',
            'groups': ['Erkek', 'Kadın'],
            'n1': len(male_salary),
            'n2': len(female_salary),
            'mean1': male_salary.mean(),
            'mean2': female_salary.mean(),
            'std1': male_salary.std(),
            'std2': female_salary.std(),
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'effect_size_interpretation': self._interpret_cohens_d(cohens_d),
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'gender_gap_percentage': gender_gap_percentage,
            'significant': p_value < 0.05
        }
        
        logger.info(f"Gender gap analizi tamamlandı. p-value: {p_value:.4f}, Gap: {gender_gap_percentage:.1f}%")
        return results
    
    def experience_salary_correlation(self) -> Dict:
        """
        Deneyim seviyesi ile maaş arasındaki korelasyonu analiz eder.
        
        Returns:
            Dict: Korelasyon sonuçları
        """
        logger.info("Deneyim-maaş korelasyonu analiz ediliyor...")
        
        if 'kariyer_seviyesi' not in self.df.columns or 'ortalama_maas' not in self.df.columns:
            raise ValueError("Gerekli sütunlar bulunamadı: kariyer_seviyesi, ortalama_maas")
        
        # Pearson korelasyonu
        pearson_r, pearson_p = pearsonr(self.df['kariyer_seviyesi'], self.df['ortalama_maas'])
        
        # Spearman korelasyonu
        spearman_r, spearman_p = spearmanr(self.df['kariyer_seviyesi'], self.df['ortalama_maas'])
        
        results = {
            'pearson_r': pearson_r,
            'pearson_p': pearson_p,
            'spearman_r': spearman_r,
            'spearman_p': spearman_p,
            'pearson_significant': pearson_p < 0.05,
            'spearman_significant': spearman_p < 0.05,
            'correlation_interpretation': self._interpret_correlation(pearson_r),
            'p_value': pearson_p,  # Ana p_value anahtarı eklendi
            'significant': pearson_p < 0.05  # Ana significant anahtarı eklendi
        }
        
        logger.info(f"Korelasyon analizi tamamlandı. Pearson r: {pearson_r:.3f}, Spearman r: {spearman_r:.3f}")
        return results
    
    def _interpret_cohens_d(self, cohens_d: float) -> str:
        """Cohen's d etki büyüklüğünü yorumlar."""
        abs_d = abs(cohens_d)
        if abs_d < 0.2:
            return "Küçük"
        elif abs_d < 0.5:
            return "Orta"
        elif abs_d < 0.8:
            return "Büyük"
        else:
            return "Çok Büyük"
    
    def _interpret_eta_squared(self, eta_squared: float) -> str:
        """Eta-squared etki büyüklüğünü yorumlar."""
        if eta_squared < 0.01:
            return "Küçük"
        elif eta_squared < 0.06:
            return "Orta"
        elif eta_squared < 0.14:
            return "Büyük"
        else:
            return "Çok Büyük"
    
    def _interpret_correlation(self, r: float) -> str:
        """Korelasyon katsayısını yorumlar."""
        abs_r = abs(r)
        if abs_r < 0.1:
            return "Çok Zayıf"
        elif abs_r < 0.3:
            return "Zayıf"
        elif abs_r < 0.5:
            return "Orta"
        elif abs_r < 0.7:
            return "Güçlü"
        else:
            return "Çok Güçlü"
    
    def run_all_analyses(self) -> Dict:
        """
        Tüm istatistiksel analizleri çalıştırır.
        
        Returns:
            Dict: Tüm test sonuçları
        """
        logger.info("Tüm istatistiksel analizler başlatılıyor...")
        
        if self.df is None:
            self.load_data()
        
        all_results = {
            'react_analysis': self.react_salary_analysis(),
            'work_type_analysis': self.work_type_salary_analysis(),
            'location_analysis': self.location_salary_analysis(),
            'gender_analysis': self.gender_salary_analysis(),
            'correlation_analysis': self.experience_salary_correlation()
        }
        
        self.results = all_results
        logger.info("Tüm analizler tamamlandı!")
        
        return all_results
    
    def save_results(self, output_path: str = "tables/statistical_results_summary.csv") -> None:
        """
        Test sonuçlarını CSV formatında kaydeder.
        
        Args:
            output_path (str): Çıktı dosyasının yolu
        """
        if not self.results:
            raise ValueError("Önce analizleri çalıştırın (run_all_analyses)")
        
        # Sonuçları DataFrame'e dönüştür
        summary_data = []
        
        for test_name, result in self.results.items():
            if test_name == 'correlation_analysis':
                summary_data.append({
                    'Test': 'Deneyim-Maaş Korelasyonu',
                    'Test_Type': 'Pearson Correlation',
                    'Statistic': result['pearson_r'],
                    'P_Value': result['pearson_p'],
                    'Effect_Size': result['pearson_r'],
                    'Effect_Size_Type': 'Correlation Coefficient',
                    'Significant': result['pearson_significant'],
                    'Interpretation': result['correlation_interpretation']
                })
            else:
                if 't_statistic' in result:
                    # T-test sonuçları
                    summary_data.append({
                        'Test': test_name.replace('_', ' ').title(),
                        'Test_Type': result['test_type'],
                        'Statistic': result['t_statistic'],
                        'P_Value': result['p_value'],
                        'Effect_Size': result.get('cohens_d', np.nan),
                        'Effect_Size_Type': 'Cohen\'s d',
                        'Significant': result['significant'],
                        'Interpretation': result.get('effect_size_interpretation', 'N/A')
                    })
                else:
                    # ANOVA sonuçları
                    summary_data.append({
                        'Test': test_name.replace('_', ' ').title(),
                        'Test_Type': result['test_type'],
                        'Statistic': result['f_statistic'],
                        'P_Value': result['p_value'],
                        'Effect_Size': result.get('eta_squared', np.nan),
                        'Effect_Size_Type': 'Eta-squared',
                        'Significant': result['significant'],
                        'Interpretation': result.get('effect_size_interpretation', 'N/A')
                    })
        
        summary_df = pd.DataFrame(summary_data)
        
        # Dosyayı kaydet
        summary_df.to_csv(output_path, index=False)
        logger.info(f"Sonuçlar kaydedildi: {output_path}")
        
        return summary_df


def main():
    """Ana fonksiyon - tüm istatistiksel analizleri çalıştırır."""
    try:
        # StatisticalAnalyzer örneği oluştur
        analyzer = StatisticalAnalyzer()
        
        # Tüm analizleri çalıştır
        results = analyzer.run_all_analyses()
        
        # Sonuçları kaydet
        summary_df = analyzer.save_results()
        
        # Özet bilgileri yazdır
        print("\n=== İSTATİSTİKSEL ANALİZ ÖZETİ ===")
        print(f"Toplam test sayısı: {len(results)}")
        
        for test_name, result in results.items():
            print(f"\n{test_name.replace('_', ' ').title()}:")
            print(f"  P-değeri: {result['p_value']:.4f}")
            print(f"  Anlamlı: {'Evet' if result['significant'] else 'Hayır'}")
            
            if 'cohens_d' in result:
                print(f"  Cohen's d: {result['cohens_d']:.3f}")
            elif 'eta_squared' in result:
                print(f"  Eta-squared: {result['eta_squared']:.3f}")
            elif 'pearson_r' in result:
                print(f"  Pearson r: {result['pearson_r']:.3f}")
        
        print("\nİstatistiksel analiz süreci başarıyla tamamlandı!")
        
    except Exception as e:
        logger.error(f"İstatistiksel analiz hatası: {str(e)}")
        raise


if __name__ == "__main__":
    main()

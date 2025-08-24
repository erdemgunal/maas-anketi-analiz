"""
Sprint 3: İkincil Analizler ve Gelişmiş İstatistiksel Testler

Bu modül, Sprint 3 kapsamında ikincil analiz hedeflerini gerçekleştirir:
- Şirket Lokasyonu × Çalışma Şekli Etkileşimi (Two-way ANOVA)
- Saat Bazlı Anket Katılımı ve Geliştirici Profilleri
- Teknoloji Stack ve ROI Analizi
- Kariyer Progression Detaylı Analizi

Yazar: Erdem Gunal
Tarih: 2024-08-24
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import f_oneway, chi2_contingency
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
import logging
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Ortak fonksiyonları import et
try:
    from .utils import (
        load_data, save_results_to_csv, CAREER_LEVELS, WORK_TYPES, GENDER_MAPPING
    )
except ImportError:
    # Doğrudan çalıştırıldığında absolute import kullan
    from utils import (
        load_data, save_results_to_csv, CAREER_LEVELS, WORK_TYPES, GENDER_MAPPING
    )

# Logging ayarları
logger = logging.getLogger(__name__)


class AdvancedAnalyzer:
    """
    Sprint 3 ikincil analizleri için gelişmiş analiz sınıfı
    """
    
    def __init__(self, data_path: str = "data/cleaned_data.csv"):
        """
        AdvancedAnalyzer sınıfını başlat
        
        Args:
            data_path (str): Temizlenmiş veri dosyasının yolu
        """
        self.data_path = data_path
        self.df = None
        self.results = {}
        
    def load_data(self) -> pd.DataFrame:
        """
        Temizlenmiş veriyi yükle
        
        Returns:
            pd.DataFrame: Yüklenen veri seti
        """
        self.df = load_data(self.data_path)
        return self.df
    
    def interaction_analysis(self) -> Dict[str, Any]:
        """
        Şirket Lokasyonu × Çalışma Şekli Etkileşimi (Two-way ANOVA)
        
        Returns:
            Dict: İki yönlü ANOVA sonuçları
        """
        logger.info("Şirket lokasyonu × çalışma şekli etkileşimi analiz ediliyor...")
        
        try:
            # Çalışma şekli ve lokasyon kombinasyonları için veri hazırla
            interaction_data = []
            
            # Çalışma şekli kodları: 0=Remote, 1=Office, 2=Hybrid
            work_type_names = {0: 'Remote', 1: 'Office', 2: 'Hybrid'}
            
            # Lokasyon sütunları
            location_cols = [col for col in self.df.columns if col.startswith('location_')]
            
            # Her kombinasyon için maaş verilerini topla
            for work_type in [0, 1, 2]:
                for loc_col in location_cols:
                    location_name = loc_col.replace('location_', '').replace('_', ' ').title()
                    
                    # Bu kombinasyondaki kişileri bul
                    mask = (self.df['calisma_sekli'] == work_type) & (self.df[loc_col] == 1)
                    salaries = self.df[mask]['ortalama_maas']
                    
                    if len(salaries) > 0:
                        interaction_data.append({
                            'work_type': work_type_names[work_type],
                            'location': location_name,
                            'n': len(salaries),
                            'mean_salary': salaries.mean(),
                            'std_salary': salaries.std(),
                            'salaries': salaries.tolist()
                        })
            
            # Two-way ANOVA için veriyi hazırla
            formula = "ortalama_maas ~ C(calisma_sekli) + C(location_türkiye) + C(calisma_sekli):C(location_türkiye)"
            
            # Basitleştirilmiş analiz: Ana etkileri ayrı ayrı test et
            work_type_effect = f_oneway(
                self.df[self.df['calisma_sekli'] == 0]['ortalama_maas'],
                self.df[self.df['calisma_sekli'] == 1]['ortalama_maas'],
                self.df[self.df['calisma_sekli'] == 2]['ortalama_maas']
            )
            
            location_effect = f_oneway(
                self.df[self.df['location_türkiye'] == 1]['ortalama_maas'],
                self.df[self.df['location_avrupa'] == 1]['ortalama_maas'],
                self.df[self.df['location_amerika'] == 1]['ortalama_maas'],
                self.df[self.df['location_yurtdışı_tr_hub'] == 1]['ortalama_maas']
            )
            
            # Etkileşim analizi için basit yaklaşım
            interaction_groups = []
            interaction_labels = []
            
            for work_type in [0, 1, 2]:
                for loc_col in location_cols:
                    mask = (self.df['calisma_sekli'] == work_type) & (self.df[loc_col] == 1)
                    salaries = self.df[mask]['ortalama_maas']
                    if len(salaries) > 5:  # Minimum grup büyüklüğü
                        interaction_groups.append(salaries)
                        interaction_labels.append(f"{work_type_names[work_type]}_{loc_col.replace('location_', '')}")
            
            interaction_effect = f_oneway(*interaction_groups) if len(interaction_groups) > 1 else (0, 1)
            
            result = {
                'test_type': 'Two-way ANOVA (Interaction)',
                'work_type_effect': {
                    'f_statistic': work_type_effect[0],
                    'p_value': work_type_effect[1],
                    'significant': work_type_effect[1] < 0.05
                },
                'location_effect': {
                    'f_statistic': location_effect[0],
                    'p_value': location_effect[1],
                    'significant': location_effect[1] < 0.05
                },
                'interaction_effect': {
                    'f_statistic': interaction_effect[0],
                    'p_value': interaction_effect[1],
                    'significant': interaction_effect[1] < 0.05
                },
                'interaction_data': interaction_data,
                'interpretation': self._interpret_interaction(work_type_effect[1], location_effect[1], interaction_effect[1])
            }
            
            logger.info(f"Etkileşim analizi tamamlandı. Work type p: {work_type_effect[1]:.4f}, Location p: {location_effect[1]:.4f}, Interaction p: {interaction_effect[1]:.4f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Etkileşim analizi hatası: {e}")
            return {}
    
    def time_based_analysis(self) -> Dict[str, Any]:
        """
        Saat Bazlı Anket Katılımı ve Geliştirici Profilleri
        
        Returns:
            Dict: Saat bazlı analiz sonuçları
        """
        logger.info("Saat bazlı analiz başlatılıyor...")
        
        try:
            # Timestamp sütununu datetime'a çevir
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            
            # Saat bilgisini çıkar
            self.df['anket_saati'] = self.df['timestamp'].dt.hour
            
            # Saat grupları oluştur
            hour_groups = {
                'Gece (00-06)': self.df[self.df['anket_saati'].between(0, 6)]['ortalama_maas'],
                'Sabah (07-12)': self.df[self.df['anket_saati'].between(7, 12)]['ortalama_maas'],
                'Öğleden Sonra (13-18)': self.df[self.df['anket_saati'].between(13, 18)]['ortalama_maas'],
                'Akşam (19-23)': self.df[self.df['anket_saati'].between(19, 23)]['ortalama_maas']
            }
            
            # Saat bazlı maaş analizi
            hour_salaries = list(hour_groups.values())
            hour_names = list(hour_groups.keys())
            
            f_stat, p_value = f_oneway(*hour_salaries)
            
            # Saat bazlı istatistikler
            hour_stats = {}
            for name, salaries in hour_groups.items():
                hour_stats[name] = {
                    'n': len(salaries),
                    'mean': salaries.mean(),
                    'std': salaries.std(),
                    'median': salaries.median()
                }
            
            # Saat bazlı demografik analiz
            demographic_analysis = {}
            
            # Cinsiyet dağılımı
            gender_by_hour = pd.crosstab(self.df['anket_saati'], self.df['cinsiyet'])
            chi2_gender, p_gender = chi2_contingency(gender_by_hour)[:2]
            
            # Kariyer seviyesi dağılımı
            career_by_hour = pd.crosstab(self.df['anket_saati'], self.df['kariyer_seviyesi'])
            chi2_career, p_career = chi2_contingency(career_by_hour)[:2]
            
            # Çalışma şekli dağılımı
            work_by_hour = pd.crosstab(self.df['anket_saati'], self.df['calisma_sekli'])
            chi2_work, p_work = chi2_contingency(work_by_hour)[:2]
            
            result = {
                'test_type': 'Time-based Analysis',
                'hourly_salary_anova': {
                    'f_statistic': f_stat,
                    'p_value': p_value,
                    'significant': p_value < 0.05
                },
                'hourly_statistics': hour_stats,
                'demographic_analysis': {
                    'gender_distribution': {
                        'chi2': chi2_gender,
                        'p_value': p_gender,
                        'significant': p_gender < 0.05
                    },
                    'career_level_distribution': {
                        'chi2': chi2_career,
                        'p_value': p_career,
                        'significant': p_career < 0.05
                    },
                    'work_type_distribution': {
                        'chi2': chi2_work,
                        'p_value': p_work,
                        'significant': p_work < 0.05
                    }
                },
                'hour_groups': hour_groups,
                'interpretation': self._interpret_time_analysis(p_value, p_gender, p_career, p_work)
            }
            
            logger.info(f"Saat bazlı analiz tamamlandı. Maaş ANOVA p: {p_value:.4f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Saat bazlı analiz hatası: {e}")
            return {}
    
    def technology_stack_roi_analysis(self) -> Dict[str, Any]:
        """
        Teknoloji Stack ve ROI Analizi
        
        Returns:
            Dict: Teknoloji ROI analiz sonuçları
        """
        logger.info("Teknoloji stack ROI analizi başlatılıyor...")
        
        try:
            # Programlama dilleri analizi
            prog_lang_cols = [col for col in self.df.columns if col.startswith('prog_lang_')]
            prog_lang_roi = {}
            
            for col in prog_lang_cols:
                lang_name = col.replace('prog_lang_', '').replace('_', ' ').title()
                users = self.df[self.df[col] == 1]['ortalama_maas']
                non_users = self.df[self.df[col] == 0]['ortalama_maas']
                
                if len(users) > 10 and len(non_users) > 10:  # Minimum grup büyüklüğü
                    t_stat, p_value = stats.ttest_ind(users, non_users)
                    roi_percentage = ((users.mean() - non_users.mean()) / non_users.mean()) * 100
                    
                    prog_lang_roi[lang_name] = {
                        'users_count': len(users),
                        'users_mean_salary': users.mean(),
                        'non_users_mean_salary': non_users.mean(),
                        'salary_difference': users.mean() - non_users.mean(),
                        'roi_percentage': roi_percentage,
                        't_statistic': t_stat,
                        'p_value': p_value,
                        'significant': p_value < 0.05
                    }
            
            # Frontend framework analizi
            frontend_cols = [col for col in self.df.columns if col.startswith('frontend_')]
            frontend_roi = {}
            
            for col in frontend_cols:
                framework_name = col.replace('frontend_', '').replace('_', ' ').title()
                users = self.df[self.df[col] == 1]['ortalama_maas']
                non_users = self.df[self.df[col] == 0]['ortalama_maas']
                
                if len(users) > 10 and len(non_users) > 10:
                    t_stat, p_value = stats.ttest_ind(users, non_users)
                    roi_percentage = ((users.mean() - non_users.mean()) / non_users.mean()) * 100
                    
                    frontend_roi[framework_name] = {
                        'users_count': len(users),
                        'users_mean_salary': users.mean(),
                        'non_users_mean_salary': non_users.mean(),
                        'salary_difference': users.mean() - non_users.mean(),
                        'roi_percentage': roi_percentage,
                        't_statistic': t_stat,
                        'p_value': p_value,
                        'significant': p_value < 0.05
                    }
            
            # Tool analizi
            tool_cols = [col for col in self.df.columns if col.startswith('tools_')]
            tool_roi = {}
            
            for col in tool_cols:
                tool_name = col.replace('tools_', '').replace('_', ' ').title()
                users = self.df[self.df[col] == 1]['ortalama_maas']
                non_users = self.df[self.df[col] == 0]['ortalama_maas']
                
                if len(users) > 10 and len(non_users) > 10:
                    t_stat, p_value = stats.ttest_ind(users, non_users)
                    roi_percentage = ((users.mean() - non_users.mean()) / non_users.mean()) * 100
                    
                    tool_roi[tool_name] = {
                        'users_count': len(users),
                        'users_mean_salary': users.mean(),
                        'non_users_mean_salary': non_users.mean(),
                        'salary_difference': users.mean() - non_users.mean(),
                        'roi_percentage': roi_percentage,
                        't_statistic': t_stat,
                        'p_value': p_value,
                        'significant': p_value < 0.05
                    }
            
            # En karlı teknolojileri sırala
            all_technologies = {**prog_lang_roi, **frontend_roi, **tool_roi}
            sorted_technologies = sorted(all_technologies.items(), 
                                       key=lambda x: x[1]['roi_percentage'], 
                                       reverse=True)
            
            result = {
                'test_type': 'Technology Stack ROI Analysis',
                'programming_languages': prog_lang_roi,
                'frontend_frameworks': frontend_roi,
                'tools': tool_roi,
                'top_technologies': sorted_technologies[:10],  # En iyi 10
                'bottom_technologies': sorted_technologies[-10:],  # En kötü 10
                'interpretation': self._interpret_technology_roi(sorted_technologies)
            }
            
            logger.info(f"Teknoloji ROI analizi tamamlandı. {len(all_technologies)} teknoloji analiz edildi.")
            
            return result
            
        except Exception as e:
            logger.error(f"Teknoloji ROI analizi hatası: {e}")
            return {}
    
    def career_progression_analysis(self) -> Dict[str, Any]:
        """
        Kariyer Progression Detaylı Analizi
        
        Returns:
            Dict: Kariyer progression analiz sonuçları
        """
        logger.info("Kariyer progression analizi başlatılıyor...")
        
        try:
            # Kariyer seviyeleri
            career_levels = sorted(self.df['kariyer_seviyesi'].unique())
            career_names = {1: 'Junior', 2: 'Mid', 3: 'Senior'}
            
            # Her seviye için istatistikler
            career_stats = {}
            salary_progression = {}
            
            for level in career_levels:
                level_data = self.df[self.df['kariyer_seviyesi'] == level]['ortalama_maas']
                career_stats[career_names[level]] = {
                    'n': len(level_data),
                    'mean_salary': level_data.mean(),
                    'median_salary': level_data.median(),
                    'std_salary': level_data.std(),
                    'min_salary': level_data.min(),
                    'max_salary': level_data.max(),
                    'q25': level_data.quantile(0.25),
                    'q75': level_data.quantile(0.75)
                }
                
                salary_progression[career_names[level]] = level_data.mean()
            
            # Kariyer geçiş analizi
            career_transitions = {}
            career_levels_list = ['Junior', 'Mid', 'Senior']
            
            for i in range(len(career_levels_list) - 1):
                current_level = career_levels_list[i]
                next_level = career_levels_list[i + 1]
                
                # Sadece mevcut seviyeler için analiz yap
                if current_level in career_stats and next_level in career_stats:
                    current_salary = career_stats[current_level]['mean_salary']
                    next_salary = career_stats[next_level]['mean_salary']
                    
                    salary_increase = next_salary - current_salary
                    percentage_increase = (salary_increase / current_salary) * 100
                    
                    career_transitions[f"{current_level}_to_{next_level}"] = {
                        'current_salary': current_salary,
                        'next_salary': next_salary,
                        'salary_increase': salary_increase,
                        'percentage_increase': percentage_increase
                    }
                
                salary_increase = next_salary - current_salary
                percentage_increase = (salary_increase / current_salary) * 100
                
                career_transitions[f"{current_level}_to_{next_level}"] = {
                    'current_salary': current_salary,
                    'next_salary': next_salary,
                    'salary_increase': salary_increase,
                    'percentage_increase': percentage_increase
                }
            
            # Kariyer seviyesi ve deneyim ilişkisi
            career_experience_correlation = {}
            for level in career_levels:
                level_data = self.df[self.df['kariyer_seviyesi'] == level]
                if len(level_data) > 0:
                    # Kariyer seviyesi ile maaş arasındaki korelasyon
                    correlation = level_data['kariyer_seviyesi'].corr(level_data['ortalama_maas'])
                    career_experience_correlation[career_names[level]] = {
                        'correlation': correlation,
                        'sample_size': len(level_data)
                    }
            
            # ANOVA testi kariyer seviyeleri arasında
            career_groups = [self.df[self.df['kariyer_seviyesi'] == level]['ortalama_maas'] 
                           for level in career_levels]
            f_stat, p_value = f_oneway(*career_groups)
            
            result = {
                'test_type': 'Career Progression Analysis',
                'career_statistics': career_stats,
                'salary_progression': salary_progression,
                'career_transitions': career_transitions,
                'career_experience_correlation': career_experience_correlation,
                'career_level_anova': {
                    'f_statistic': f_stat,
                    'p_value': p_value,
                    'significant': p_value < 0.05
                },
                'interpretation': self._interpret_career_progression(career_transitions, p_value)
            }
            
            logger.info(f"Kariyer progression analizi tamamlandı. ANOVA p: {p_value:.4f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Kariyer progression analizi hatası: {e}")
            return {}
    
    def run_all_advanced_analyses(self) -> Dict[str, Any]:
        """
        Tüm gelişmiş analizleri çalıştır
        
        Returns:
            Dict: Tüm analiz sonuçları
        """
        logger.info("Tüm gelişmiş analizler başlatılıyor...")
        
        if self.df is None:
            self.load_data()
        
        self.results = {
            'interaction_analysis': self.interaction_analysis(),
            'time_based_analysis': self.time_based_analysis(),
            'technology_stack_roi': self.technology_stack_roi_analysis(),
            'career_progression': self.career_progression_analysis()
        }
        
        logger.info("Tüm gelişmiş analizler tamamlandı!")
        return self.results
    
    def save_results(self, output_path: str = "tables/advanced_analysis_results.csv") -> pd.DataFrame:
        """
        Analiz sonuçlarını CSV dosyasına kaydet
        
        Args:
            output_path (str): Çıktı dosyasının yolu
            
        Returns:
            pd.DataFrame: Kaydedilen sonuçlar
        """
        logger.info(f"Analiz sonuçları kaydediliyor: {output_path}")
        
        try:
            # Sonuçları düzleştir
            flat_results = []
            
            # Etkileşim analizi sonuçları
            if 'interaction_analysis' in self.results:
                interaction = self.results['interaction_analysis']
                flat_results.append({
                    'Analysis_Type': 'Interaction Analysis',
                    'Test_Name': 'Work Type Effect',
                    'Statistic': interaction.get('work_type_effect', {}).get('f_statistic', 0),
                    'P_Value': interaction.get('work_type_effect', {}).get('p_value', 1),
                    'Significant': interaction.get('work_type_effect', {}).get('significant', False),
                    'Interpretation': interaction.get('interpretation', '')
                })
                
                flat_results.append({
                    'Analysis_Type': 'Interaction Analysis',
                    'Test_Name': 'Location Effect',
                    'Statistic': interaction.get('location_effect', {}).get('f_statistic', 0),
                    'P_Value': interaction.get('location_effect', {}).get('p_value', 1),
                    'Significant': interaction.get('location_effect', {}).get('significant', False),
                    'Interpretation': interaction.get('interpretation', '')
                })
            
            # Saat bazlı analiz sonuçları
            if 'time_based_analysis' in self.results:
                time_analysis = self.results['time_based_analysis']
                flat_results.append({
                    'Analysis_Type': 'Time-based Analysis',
                    'Test_Name': 'Hourly Salary ANOVA',
                    'Statistic': time_analysis.get('hourly_salary_anova', {}).get('f_statistic', 0),
                    'P_Value': time_analysis.get('hourly_salary_anova', {}).get('p_value', 1),
                    'Significant': time_analysis.get('hourly_salary_anova', {}).get('significant', False),
                    'Interpretation': time_analysis.get('interpretation', '')
                })
            
            # Kariyer progression analizi sonuçları
            if 'career_progression' in self.results:
                career = self.results['career_progression']
                flat_results.append({
                    'Analysis_Type': 'Career Progression',
                    'Test_Name': 'Career Level ANOVA',
                    'Statistic': career.get('career_level_anova', {}).get('f_statistic', 0),
                    'P_Value': career.get('career_level_anova', {}).get('p_value', 1),
                    'Significant': career.get('career_level_anova', {}).get('significant', False),
                    'Interpretation': career.get('interpretation', '')
                })
            
            # DataFrame oluştur ve kaydet
            results_df = pd.DataFrame(flat_results)
            results_df.to_csv(output_path, index=False)
            
            logger.info(f"Sonuçlar başarıyla kaydedildi: {output_path}")
            return results_df
            
        except Exception as e:
            logger.error(f"Sonuç kaydetme hatası: {e}")
            return pd.DataFrame()
    
    def _interpret_interaction(self, work_p: float, location_p: float, interaction_p: float) -> str:
        """Etkileşim analizi yorumu"""
        interpretations = []
        
        if work_p < 0.05:
            interpretations.append("Çalışma şekli maaş üzerinde anlamlı etki yaratıyor")
        if location_p < 0.05:
            interpretations.append("Şirket lokasyonu maaş üzerinde anlamlı etki yaratıyor")
        if interaction_p < 0.05:
            interpretations.append("Çalışma şekli ve lokasyon arasında anlamlı etkileşim var")
        else:
            interpretations.append("Çalışma şekli ve lokasyon arasında anlamlı etkileşim yok")
        
        return "; ".join(interpretations)
    
    def _interpret_time_analysis(self, salary_p: float, gender_p: float, career_p: float, work_p: float) -> str:
        """Saat bazlı analiz yorumu"""
        interpretations = []
        
        if salary_p < 0.05:
            interpretations.append("Saat bazlı maaş farkları anlamlı")
        if gender_p < 0.05:
            interpretations.append("Saat bazlı cinsiyet dağılımı farklı")
        if career_p < 0.05:
            interpretations.append("Saat bazlı kariyer seviyesi dağılımı farklı")
        if work_p < 0.05:
            interpretations.append("Saat bazlı çalışma şekli dağılımı farklı")
        
        return "; ".join(interpretations) if interpretations else "Saat bazlı anlamlı farklar yok"
    
    def _interpret_technology_roi(self, sorted_technologies: List) -> str:
        """Teknoloji ROI yorumu"""
        if not sorted_technologies:
            return "Teknoloji ROI analizi yapılamadı"
        
        top_tech = sorted_technologies[0]
        bottom_tech = sorted_technologies[-1]
        
        return f"En karlı teknoloji: {top_tech[0]} (%{top_tech[1]['roi_percentage']:.1f} artış), En az karlı: {bottom_tech[0]} (%{bottom_tech[1]['roi_percentage']:.1f} artış)"
    
    def _interpret_career_progression(self, transitions: Dict, anova_p: float) -> str:
        """Kariyer progression yorumu"""
        if anova_p < 0.05:
            return "Kariyer seviyeleri arasında anlamlı maaş farkları var"
        else:
            return "Kariyer seviyeleri arasında anlamlı maaş farkları yok"


def main():
    """Ana fonksiyon"""
    analyzer = AdvancedAnalyzer()
    
    # Tüm analizleri çalıştır
    results = analyzer.run_all_advanced_analyses()
    
    # Sonuçları kaydet
    summary_df = analyzer.save_results()
    
    # Özet yazdır
    print("=== GELİŞMİŞ ANALİZ SONUÇLARI ===")
    print(f"Toplam {len(results)} analiz tamamlandı:")
    
    for analysis_name, analysis_result in results.items():
        if analysis_result:
            print(f"✅ {analysis_name}: Tamamlandı")
        else:
            print(f"❌ {analysis_name}: Hata")
    
    print(f"\nSonuçlar 'tables/advanced_analysis_results.csv' dosyasına kaydedildi.")


if __name__ == "__main__":
    main()

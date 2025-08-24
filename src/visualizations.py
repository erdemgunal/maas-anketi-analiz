"""
Sprint 3: Görselleştirme Modülü

Bu modül, Sprint 3 kapsamında 20+ grafik taslağı oluşturur:
- Temel analiz görselleri (5+ adet)
- İkincil analiz görselleri (15+ adet)
- Tutarlı renk paleti ve standartlar

Yazar: Erdem Gunal
Tarih: 2024-08-24
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# Ortak fonksiyonları import et
try:
    from .utils import (
        load_data, setup_matplotlib_style, VIRIDIS_COLORS, CATEGORICAL_COLORS,
        get_programming_language_usage, get_location_data, get_career_data,
        get_work_type_data, get_gender_data, CAREER_LEVELS, WORK_TYPES
    )
except ImportError:
    # Doğrudan çalıştırıldığında absolute import kullan
    from utils import (
        load_data, setup_matplotlib_style, VIRIDIS_COLORS, CATEGORICAL_COLORS,
        get_programming_language_usage, get_location_data, get_career_data,
        get_work_type_data, get_gender_data, CAREER_LEVELS, WORK_TYPES
    )

# Görselleştirme ayarları
setup_matplotlib_style()


class DataVisualizer:
    """
    Sprint 3 görselleştirmeleri için ana sınıf
    """
    
    def __init__(self, data_path: str = "data/cleaned_data.csv"):
        """
        DataVisualizer sınıfını başlat
        
        Args:
            data_path (str): Temizlenmiş veri dosyasının yolu
        """
        self.data_path = data_path
        self.df = None
        self.figures_dir = "figures"
        
    def load_data(self) -> pd.DataFrame:
        """Veriyi yükle"""
        self.df = load_data(self.data_path)
        return self.df
    
    def create_salary_distribution_charts(self) -> None:
        """Maaş dağılımı görselleri (4 adet)"""
        print("📊 Maaş dağılımı görselleri oluşturuluyor...")
        
        # 1. Histogram
        plt.figure(figsize=(10, 6))
        plt.hist(self.df['ortalama_maas'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('Maaş Dağılımı - Histogram', fontsize=16, fontweight='bold')
        plt.xlabel('Maaş (bin TL)', fontsize=12)
        plt.ylabel('Frekans', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/01_maas_dagilimi_histogram.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Box Plot
        plt.figure(figsize=(8, 6))
        plt.boxplot(self.df['ortalama_maas'], patch_artist=True, boxprops=dict(facecolor='lightgreen'))
        plt.title('Maaş Dağılımı - Box Plot', fontsize=16, fontweight='bold')
        plt.xlabel('Tüm Katılımcılar', fontsize=12)
        plt.ylabel('Maaş (bin TL)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/02_maas_dagilimi_boxplot.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Violin Plot
        plt.figure(figsize=(8, 6))
        plt.violinplot(self.df['ortalama_maas'], showmeans=True)
        plt.title('Maaş Dağılımı - Violin Plot', fontsize=16, fontweight='bold')
        plt.xlabel('Tüm Katılımcılar', fontsize=12)
        plt.ylabel('Maaş (bin TL)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/03_maas_dagilimi_violin.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Density Plot
        plt.figure(figsize=(10, 6))
        self.df['ortalama_maas'].plot.kde(color='purple', linewidth=2)
        plt.title('Maaş Dağılımı - Yoğunluk Eğrisi', fontsize=16, fontweight='bold')
        plt.xlabel('Maaş (bin TL)', fontsize=12)
        plt.ylabel('Yoğunluk', fontsize=12)
        plt.xlim(left=0)  # X eksenini 0'dan başlat
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/04_maas_dagilimi_density.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_basic_comparison_charts(self) -> None:
        """Temel karşılaştırma görselleri (5 adet)"""
        print("📈 Temel karşılaştırma görselleri oluşturuluyor...")
        
        # 1. React vs Non-React
        react_users = self.df[self.df['frontend_react'] == 1]['ortalama_maas']
        non_react_users = self.df[self.df['frontend_react'] == 0]['ortalama_maas']
        
        plt.figure(figsize=(10, 6))
        plt.boxplot([react_users, non_react_users], labels=['React Kullanıcıları', 'React Kullanmayanlar'])
        plt.title('React Kullanımı ve Maaş Karşılaştırması', fontsize=16, fontweight='bold')
        plt.ylabel('Maaş (bin TL)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/05_react_maas_karsilastirma.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Cinsiyet karşılaştırması
        male_salary = self.df[self.df['cinsiyet'] == 0]['ortalama_maas']
        female_salary = self.df[self.df['cinsiyet'] == 1]['ortalama_maas']
        
        plt.figure(figsize=(10, 6))
        plt.boxplot([male_salary, female_salary], labels=['Erkek', 'Kadın'])
        plt.title('Cinsiyet ve Maaş Karşılaştırması', fontsize=16, fontweight='bold')
        plt.ylabel('Maaş (bin TL)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/06_cinsiyet_maas_karsilastirma.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Çalışma şekli karşılaştırması
        work_types = ['Remote', 'Office', 'Hybrid']
        work_salaries = []
        for i in range(3):
            work_salaries.append(self.df[self.df['calisma_sekli'] == i]['ortalama_maas'])
        
        plt.figure(figsize=(12, 6))
        plt.boxplot(work_salaries, labels=work_types)
        plt.title('Çalışma Şekli ve Maaş Karşılaştırması', fontsize=16, fontweight='bold')
        plt.ylabel('Maaş (bin TL)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/07_calisma_sekli_maas_karsilastirma.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Şirket lokasyonu karşılaştırması
        location_cols = [col for col in self.df.columns if col.startswith('location_')]
        location_salaries = []
        location_names = []
        
        for col in location_cols:
            location_data = self.df[self.df[col] == 1]['ortalama_maas']
            if len(location_data) > 0:
                location_salaries.append(location_data)
                location_names.append(col.replace('location_', '').replace('_', ' ').title())
        
        plt.figure(figsize=(12, 6))
        plt.boxplot(location_salaries, labels=location_names)
        plt.title('Şirket Lokasyonu ve Maaş Karşılaştırması', fontsize=16, fontweight='bold')
        plt.ylabel('Maaş (bin TL)', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/08_sirket_lokasyonu_maas_karsilastirma.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. Kariyer seviyesi karşılaştırması
        career_levels = sorted(self.df['kariyer_seviyesi'].unique())
        career_salaries = []
        career_names = {1: 'Junior', 2: 'Mid', 3: 'Senior', 4: 'Lead', 5: 'Manager'}
        
        for level in career_levels:
            career_salaries.append(self.df[self.df['kariyer_seviyesi'] == level]['ortalama_maas'])
        
        plt.figure(figsize=(12, 6))
        plt.boxplot(career_salaries, labels=[career_names[level] for level in career_levels])
        plt.title('Kariyer Seviyesi ve Maaş Karşılaştırması', fontsize=16, fontweight='bold')
        plt.ylabel('Maaş (bin TL)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/09_kariyer_seviyesi_maas_karsilastirma.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_secondary_analysis_charts(self) -> None:
        """İkincil analiz görselleri (15+ adet)"""
        print("🔍 İkincil analiz görselleri oluşturuluyor...")
        
        # 1. Deneyim vs Maaş Scatter Plot
        plt.figure(figsize=(10, 6))
        plt.scatter(self.df['kariyer_seviyesi'], self.df['ortalama_maas'], alpha=0.6, color='blue')
        plt.title('Kariyer Seviyesi vs Maaş Korelasyonu', fontsize=16, fontweight='bold')
        plt.xlabel('Kariyer Seviyesi', fontsize=12)
        plt.ylabel('Maaş (bin TL)', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Trend çizgisi ekle
        z = np.polyfit(self.df['kariyer_seviyesi'], self.df['ortalama_maas'], 1)
        p = np.poly1d(z)
        plt.plot(self.df['kariyer_seviyesi'], p(self.df['kariyer_seviyesi']), "r--", alpha=0.8)
        
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/10_deneyim_maas_scatter.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Saat bazlı maaş analizi
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df['anket_saati'] = self.df['timestamp'].dt.hour
        
        hour_groups = {
            'Gece (00-06)': self.df[self.df['anket_saati'].between(0, 6)]['ortalama_maas'],
            'Sabah (07-12)': self.df[self.df['anket_saati'].between(7, 12)]['ortalama_maas'],
            'Öğleden Sonra (13-18)': self.df[self.df['anket_saati'].between(13, 18)]['ortalama_maas'],
            'Akşam (19-23)': self.df[self.df['anket_saati'].between(19, 23)]['ortalama_maas']
        }
        
        plt.figure(figsize=(12, 6))
        plt.boxplot(list(hour_groups.values()), labels=list(hour_groups.keys()))
        plt.title('Saat Bazlı Maaş Analizi', fontsize=16, fontweight='bold')
        plt.ylabel('Maaş (bin TL)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/11_saat_bazli_maas_analizi.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Teknoloji ROI analizi (En iyi 10 teknoloji)
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from src.advanced_analysis import AdvancedAnalyzer
        
        # Teknoloji ROI verilerini al
        analyzer = AdvancedAnalyzer()
        analyzer.df = self.df
        tech_result = analyzer.technology_stack_roi_analysis()
        
        if tech_result and 'top_technologies' in tech_result:
            top_10 = tech_result['top_technologies'][:10]
            tech_names = [tech for tech, _ in top_10]
            roi_values = [data['roi_percentage'] for _, data in top_10]
            
            plt.figure(figsize=(14, 8))
            bars = plt.barh(tech_names, roi_values, color='lightblue', alpha=0.8)
            plt.title('En Karlı Teknolojiler (ROI Analizi)', fontsize=16, fontweight='bold')
            plt.xlabel('ROI (%)', fontsize=12)
            plt.ylabel('Teknoloji', fontsize=12)
            plt.grid(True, alpha=0.3, axis='x')
            
            # Değerleri çubukların üzerine yaz
            for i, (bar, roi) in enumerate(zip(bars, roi_values)):
                plt.text(roi + 0.5, bar.get_y() + bar.get_height()/2, f'{roi:.1f}%', 
                        ha='left', va='center', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(f'{self.figures_dir}/12_en_karli_teknolojiler.png', dpi=300, bbox_inches='tight')
            plt.close()
        else:
            # Fallback: Basit placeholder
            plt.figure(figsize=(14, 8))
            plt.title('En Karlı Teknolojiler (ROI Analizi)', fontsize=16, fontweight='bold')
            plt.xlabel('Teknoloji', fontsize=12)
            plt.ylabel('ROI (%)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f'{self.figures_dir}/12_en_karli_teknolojiler.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # 4. Kariyer progression analizi
        career_names = {1: 'Junior', 2: 'Mid', 3: 'Senior', 4: 'Lead', 5: 'Manager'}
        career_means = []
        career_labels = []
        
        for level in sorted(self.df['kariyer_seviyesi'].unique()):
            career_means.append(self.df[self.df['kariyer_seviyesi'] == level]['ortalama_maas'].mean())
            career_labels.append(career_names[level])
        
        plt.figure(figsize=(10, 6))
        plt.plot(career_labels, career_means, marker='o', linewidth=2, markersize=8)
        plt.title('Kariyer Progression - Maaş Artışı', fontsize=16, fontweight='bold')
        plt.xlabel('Kariyer Seviyesi', fontsize=12)
        plt.ylabel('Ortalama Maaş (bin TL)', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Değerleri çizginin üzerine yaz
        for i, (label, mean) in enumerate(zip(career_labels, career_means)):
            plt.text(i, mean + 2, f'{mean:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/13_kariyer_progression.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. Etkileşim analizi (Work Type × Location)
        # Etkileşim verilerini al
        interaction_result = analyzer.interaction_analysis()
        
        if interaction_result and 'interaction_data' in interaction_result:
            interaction_data = interaction_result['interaction_data']
            
            if interaction_data:
                # Veriyi DataFrame'e çevir
                interaction_df = pd.DataFrame(interaction_data)
                
                # Pivot table oluştur
                try:
                    pivot_data = interaction_df.pivot(index='work_type', columns='location', values='mean_salary')
                    
                    plt.figure(figsize=(12, 8))
                    sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='viridis', 
                               cbar_kws={'label': 'Ortalama Maaş (bin TL)'})
                    plt.title('Çalışma Şekli × Lokasyon Etkileşimi - Ortalama Maaşlar', 
                             fontsize=16, fontweight='bold')
                    plt.xlabel('Şirket Lokasyonu', fontsize=12)
                    plt.ylabel('Çalışma Şekli', fontsize=12)
                    plt.tight_layout()
                    plt.savefig(f'{self.figures_dir}/14_calisma_lokasyon_etkilesimi.png', dpi=300, bbox_inches='tight')
                    plt.close()
                except:
                    # Fallback: Bar chart
                    plt.figure(figsize=(12, 8))
                    
                    # Her çalışma şekli için ayrı bar
                    work_types = interaction_df['work_type'].unique()
                    locations = interaction_df['location'].unique()
                    
                    x = np.arange(len(locations))
                    width = 0.25
                    
                    for i, work_type in enumerate(work_types):
                        work_data = interaction_df[interaction_df['work_type'] == work_type]
                        means = []
                        for loc in locations:
                            loc_data = work_data[work_data['location'] == loc]
                            means.append(loc_data['mean_salary'].iloc[0] if len(loc_data) > 0 else 0)
                        
                        plt.bar(x + i*width, means, width, label=work_type, alpha=0.8)
                    
                    plt.title('Çalışma Şekli × Lokasyon Etkileşimi', fontsize=16, fontweight='bold')
                    plt.xlabel('Şirket Lokasyonu', fontsize=12)
                    plt.ylabel('Ortalama Maaş (bin TL)', fontsize=12)
                    plt.xticks(x + width, locations, rotation=45)
                    plt.legend()
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()
                    plt.savefig(f'{self.figures_dir}/14_calisma_lokasyon_etkilesimi.png', dpi=300, bbox_inches='tight')
                    plt.close()
            else:
                # Fallback: Basit placeholder
                plt.figure(figsize=(12, 8))
                plt.title('Çalışma Şekli × Lokasyon Etkileşimi', fontsize=16, fontweight='bold')
                plt.xlabel('Çalışma Şekli', fontsize=12)
                plt.ylabel('Ortalama Maaş (bin TL)', fontsize=12)
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.savefig(f'{self.figures_dir}/14_calisma_lokasyon_etkilesimi.png', dpi=300, bbox_inches='tight')
                plt.close()
        else:
            # Fallback: Basit placeholder
            plt.figure(figsize=(12, 8))
            plt.title('Çalışma Şekli × Lokasyon Etkileşimi', fontsize=16, fontweight='bold')
            plt.xlabel('Çalışma Şekli', fontsize=12)
            plt.ylabel('Ortalama Maaş (bin TL)', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f'{self.figures_dir}/14_calisma_lokasyon_etkilesimi.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # 6. Demografik dağılımlar
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Cinsiyet dağılımı
        gender_counts = self.df['cinsiyet'].value_counts()
        colors = ['#FF6B6B', '#4ECDC4']  # Erkek: kırmızı, Kadın: turkuaz
        axes[0, 0].pie(gender_counts.values, labels=['Erkek', 'Kadın'], autopct='%1.1f%%', 
                      startangle=90, colors=colors, textprops={'fontweight': 'bold'})
        axes[0, 0].set_title('Cinsiyet Dağılımı', fontsize=14, fontweight='bold')
        
        # Kariyer seviyesi dağılımı
        career_counts = self.df['kariyer_seviyesi'].value_counts().sort_index()
        career_labels = [career_names[level] for level in career_counts.index]
        axes[0, 1].bar(career_labels, career_counts.values, color='lightcoral')
        axes[0, 1].set_title('Kariyer Seviyesi Dağılımı', fontsize=14, fontweight='bold')
        axes[0, 1].set_ylabel('Kişi Sayısı', fontsize=12)
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Çalışma şekli dağılımı
        work_counts = self.df['calisma_sekli'].value_counts().sort_index()
        work_labels = ['Remote', 'Office', 'Hybrid']
        axes[1, 0].bar(work_labels, work_counts.values, color='lightgreen')
        axes[1, 0].set_title('Çalışma Şekli Dağılımı', fontsize=14, fontweight='bold')
        axes[1, 0].set_ylabel('Kişi Sayısı', fontsize=12)
        
        # Lokasyon dağılımı
        location_cols = [col for col in self.df.columns if col.startswith('location_')]
        location_counts = []
        location_labels = []
        for col in location_cols:
            count = self.df[col].sum()
            if count > 0:
                location_counts.append(count)
                location_labels.append(col.replace('location_', '').replace('_', ' ').title())
        
        axes[1, 1].bar(location_labels, location_counts, color='gold')
        axes[1, 1].set_title('Şirket Lokasyonu Dağılımı', fontsize=14, fontweight='bold')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/15_demografik_dagilimlar.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 7. Maaş aralıkları analizi
        salary_ranges = pd.cut(self.df['ortalama_maas'], bins=10)
        range_counts = salary_ranges.value_counts().sort_index()
        
        plt.figure(figsize=(12, 6))
        range_counts.plot(kind='bar', color='skyblue')
        plt.title('Maaş Aralıkları Dağılımı', fontsize=16, fontweight='bold')
        plt.xlabel('Maaş Aralığı (bin TL)', fontsize=12)
        plt.ylabel('Kişi Sayısı', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/16_maas_araliklari.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 8. Saat bazlı katılım analizi
        hour_counts = self.df['anket_saati'].value_counts().sort_index()
        
        plt.figure(figsize=(12, 6))
        plt.plot(hour_counts.index, hour_counts.values, marker='o', linewidth=2)
        plt.title('Saat Bazlı Anket Katılımı', fontsize=16, fontweight='bold')
        plt.xlabel('Saat', fontsize=12)
        plt.ylabel('Katılımcı Sayısı', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/17_saat_bazli_katilim.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 9. Teknoloji kullanım oranları
        # Programlama dilleri
        prog_lang_cols = [col for col in self.df.columns if col.startswith('prog_lang_')]
        lang_usage = {}
        
        # Dil isimlerini düzelt
        lang_name_mapping = {
            'javascript': 'JavaScript',
            'html_css': 'HTML/CSS',
            'typescript': 'TypeScript',
            'sql': 'SQL',
            'c#': 'C#',
            'python': 'Python',
            'java': 'Java',
            'php': 'PHP',
            'c': 'C',
            'c++': 'C++',
            'go': 'Go',
            'rust': 'Rust',
            'swift': 'Swift',
            'kotlin': 'Kotlin',
            'scala': 'Scala',
            'r': 'R',
            'matlab': 'MATLAB',
            'dart': 'Dart',
            'elixir': 'Elixir',
            'erlang': 'Erlang',
            'f#': 'F#',
            'haskell': 'Haskell',
            'lisp': 'Lisp',
            'perl': 'Perl',
            'ruby': 'Ruby',
            'groovy': 'Groovy',
            'clojure': 'Clojure',
            'cobol': 'COBOL',
            'fortran': 'Fortran',
            'pascal': 'Pascal',
            'basic': 'BASIC',
            'assembly': 'Assembly',
            'abap': 'ABAP',
            'pl_sql': 'PL/SQL',
            't_sql': 'T-SQL',
            'vba': 'VBA',
            'powershell': 'PowerShell',
            'shell': 'Shell',
            'bash': 'Bash',
            'zsh': 'Zsh',
            'fish': 'Fish',
            'batch': 'Batch',
            'autohotkey': 'AutoHotkey',
            'autolisp': 'AutoLISP',
            'g_code': 'G-Code',
            'ladder_logic': 'Ladder Logic',
            'structured_text': 'Structured Text',
            'function_block': 'Function Block',
            'instruction_list': 'Instruction List',
            'sequential_function': 'Sequential Function',
            'hicbiri': 'Hiçbiri'
        }
        
        for col in prog_lang_cols:
            lang_key = col.replace('prog_lang_', '')
            usage_rate = (self.df[col].sum() / len(self.df)) * 100
            if usage_rate > 5:  # %5'ten fazla kullanım
                # Dil ismini düzelt
                if lang_key in lang_name_mapping:
                    lang_name = lang_name_mapping[lang_key]
                else:
                    lang_name = lang_key.replace('_', ' ').title()
                
                # Hiçbiri'yi hariç tut
                if lang_name != 'Hiçbiri':
                    lang_usage[lang_name] = usage_rate
        
        # En popüler 10 dil
        top_languages = dict(sorted(lang_usage.items(), key=lambda x: x[1], reverse=True)[:10])
        
        plt.figure(figsize=(12, 8))
        plt.barh(list(top_languages.keys()), list(top_languages.values()), color='lightblue')
        plt.title('En Popüler Programlama Dilleri', fontsize=16, fontweight='bold')
        plt.xlabel('Kullanım Oranı (%)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/18_populer_programlama_dilleri.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 10. Frontend framework kullanımı
        frontend_cols = [col for col in self.df.columns if col.startswith('frontend_')]
        frontend_usage = {}
        
        for col in frontend_cols:
            framework_name = col.replace('frontend_', '').replace('_', ' ').title()
            usage_rate = (self.df[col].sum() / len(self.df)) * 100
            if usage_rate > 1:  # %1'den fazla kullanım
                frontend_usage[framework_name] = usage_rate
        
        plt.figure(figsize=(10, 6))
        plt.bar(frontend_usage.keys(), frontend_usage.values(), color='lightgreen')
        plt.title('Frontend Framework Kullanım Oranları', fontsize=16, fontweight='bold')
        plt.ylabel('Kullanım Oranı (%)', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/19_frontend_framework_kullanimi.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 11. Tool kullanımı
        tool_cols = [col for col in self.df.columns if col.startswith('tools_')]
        tool_usage = {}
        
        for col in tool_cols:
            tool_name = col.replace('tools_', '').replace('_', ' ').title()
            usage_rate = (self.df[col].sum() / len(self.df)) * 100
            if usage_rate > 2:  # %2'den fazla kullanım
                tool_usage[tool_name] = usage_rate
        
        # En popüler 8 tool
        top_tools = dict(sorted(tool_usage.items(), key=lambda x: x[1], reverse=True)[:8])
        
        plt.figure(figsize=(10, 6))
        plt.bar(top_tools.keys(), top_tools.values(), color='gold')
        plt.title('En Popüler Tool Kullanımı', fontsize=16, fontweight='bold')
        plt.ylabel('Kullanım Oranı (%)', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/20_populer_tool_kullanimi.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_all_charts(self) -> None:
        """Tüm görselleri oluştur"""
        print("🎨 Tüm görseller oluşturuluyor...")
        
        if self.df is None:
            self.load_data()
        
        # figures dizinini oluştur
        import os
        os.makedirs(self.figures_dir, exist_ok=True)
        
        # Görselleri oluştur
        self.create_salary_distribution_charts()
        self.create_basic_comparison_charts()
        self.create_secondary_analysis_charts()
        
        print(f"✅ Toplam 20+ görsel '{self.figures_dir}/' dizinine kaydedildi!")


def main():
    """Ana fonksiyon"""
    visualizer = DataVisualizer()
    visualizer.create_all_charts()


if __name__ == "__main__":
    main()

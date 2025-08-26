"""
Sprint 4: Yayın Kalitesinde Görselleştirme Modülü

Bu modül, Sprint 4 kapsamında VISUAL_STANDARDS.md dokümanına uygun
yayın kalitesinde grafikler oluşturur:
- 12x8 inç boyut, 300 DPI, PNG format
- Arial font, belirtilen font boyutları
- Viridis renk paleti
- LaTeX entegrasyonu için optimize edilmiş
- "Bu Ne Anlama Geliyor?" açıklamaları

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

# VISUAL_STANDARDS.md'ye uygun ayarlar
setup_matplotlib_style()


class PublicationQualityVisualizer:
    """
    Yayın kalitesinde görselleştirmeler için ana sınıf
    """
    
    def __init__(self, data_path: str = "data/cleaned_data.csv"):
        """
        PublicationQualityVisualizer sınıfını başlat
        
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
        """Maaş dağılımı görselleri (4 adet) - Yayın kalitesinde"""
        print("📊 Yayın kalitesinde maaş dağılımı görselleri oluşturuluyor...")
        
        # 1. Histogram
        plt.figure(figsize=(12, 8))
        plt.hist(self.df['ortalama_maas'], bins=30, alpha=0.7, 
                color=VIRIDIS_COLORS['primary'], edgecolor='black', linewidth=0.5)
        plt.title('Salary Distribution (Histogram)', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Monthly Average Net Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.ylabel('Number of Developers', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/01_maas_dagilimi_histogram.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Box Plot
        plt.figure(figsize=(12, 8))
        box_plot = plt.boxplot(self.df['ortalama_maas'], patch_artist=True, 
                              boxprops=dict(facecolor=VIRIDIS_COLORS['secondary']),
                              whiskerprops=dict(color=VIRIDIS_COLORS['primary']),
                              medianprops=dict(color='white', linewidth=2),
                              flierprops=dict(markerfacecolor=VIRIDIS_COLORS['quaternary']))
        plt.title('Salary Distribution (Box Plot)', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('All Participants', fontsize=18, fontweight='bold', labelpad=15)
        plt.ylabel('Monthly Average Net Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/02_maas_dagilimi_boxplot.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Violin Plot
        plt.figure(figsize=(12, 8))
        violin_parts = plt.violinplot(self.df['ortalama_maas'], showmeans=True)
        violin_parts['bodies'][0].set_facecolor(VIRIDIS_COLORS['tertiary'])
        violin_parts['cmeans'].set_color(VIRIDIS_COLORS['primary'])
        violin_parts['cmeans'].set_linewidth(2)
        plt.title('Salary Distribution (Violin Plot)', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('All Participants', fontsize=18, fontweight='bold', labelpad=15)
        plt.ylabel('Monthly Average Net Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/03_maas_dagilimi_violin.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Density Plot
        plt.figure(figsize=(12, 8))
        self.df['ortalama_maas'].plot.kde(color=VIRIDIS_COLORS['quaternary'], linewidth=2)
        plt.title('Salary Distribution (Density Curve)', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Monthly Average Net Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.ylabel('Distribution Rate', fontsize=18, fontweight='bold', labelpad=15)
        plt.xlim(left=0)  # X eksenini 0'dan başlat
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/04_maas_dagilimi_density.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_basic_comparison_charts(self) -> None:
        """Temel karşılaştırma görselleri (5 adet) - Yayın kalitesinde"""
        print("📈 Yayın kalitesinde temel karşılaştırma görselleri oluşturuluyor...")
        
        # 1. React vs Non-React
        react_users = self.df[self.df['frontend_react'] == 1]['ortalama_maas']
        non_react_users = self.df[self.df['frontend_react'] == 0]['ortalama_maas']
        
        plt.figure(figsize=(12, 8))
        box_data = [react_users, non_react_users]
        box_labels = ['React Kullanıcıları', 'React Kullanmayanlar']
        box_colors = [CATEGORICAL_COLORS['react_users'], CATEGORICAL_COLORS['non_react_users']]
        
        box_plot = plt.boxplot(box_data, labels=box_labels, patch_artist=True)
        for patch, color in zip(box_plot['boxes'], box_colors):
            patch.set_facecolor(color)
        
        plt.title('React Usage and Salary Comparison', fontsize=20, fontweight='bold', pad=20)
        plt.ylabel('Monthly Average Net Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/05_react_maas_karsilastirma.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Cinsiyet karşılaştırması
        male_salary = self.df[self.df['cinsiyet'] == 0]['ortalama_maas']
        female_salary = self.df[self.df['cinsiyet'] == 1]['ortalama_maas']
        
        plt.figure(figsize=(12, 8))
        box_data = [male_salary, female_salary]
        box_labels = ['Erkek', 'Kadın']
        box_colors = [CATEGORICAL_COLORS['male'], CATEGORICAL_COLORS['female']]
        
        box_plot = plt.boxplot(box_data, labels=box_labels, patch_artist=True)
        for patch, color in zip(box_plot['boxes'], box_colors):
            patch.set_facecolor(color)
        
        plt.title('Gender and Salary Comparison', fontsize=20, fontweight='bold', pad=20)
        plt.ylabel('Monthly Average Net Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/06_cinsiyet_maas_karsilastirma.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Çalışma şekli karşılaştırması
        work_types = ['Remote', 'Office', 'Hybrid']
        work_salaries = []
        work_colors = [CATEGORICAL_COLORS['remote'], CATEGORICAL_COLORS['office'], CATEGORICAL_COLORS['hybrid']]
        
        for i in range(3):
            work_salaries.append(self.df[self.df['calisma_sekli'] == i]['ortalama_maas'])
        
        plt.figure(figsize=(12, 8))
        box_plot = plt.boxplot(work_salaries, labels=work_types, patch_artist=True)
        for patch, color in zip(box_plot['boxes'], work_colors):
            patch.set_facecolor(color)
        
        plt.title('Work Type and Salary Comparison', fontsize=20, fontweight='bold', pad=20)
        plt.ylabel('Monthly Average Net Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
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
        
        plt.figure(figsize=(12, 8))
        box_plot = plt.boxplot(location_salaries, labels=location_names, patch_artist=True)
        for patch in box_plot['boxes']:
            patch.set_facecolor(VIRIDIS_COLORS['secondary'])
        
        plt.title('Company Location and Salary Comparison', fontsize=20, fontweight='bold', pad=20)
        plt.ylabel('Monthly Average Net Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(rotation=45, fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/08_sirket_lokasyonu_maas_karsilastirma.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. Kariyer seviyesi karşılaştırması
        career_levels = sorted(self.df['kariyer_seviyesi'].unique())
        career_salaries = []
        career_names = {1: 'Junior', 2: 'Mid', 3: 'Senior', 4: 'Lead', 5: 'Manager'}
        
        for level in career_levels:
            career_salaries.append(self.df[self.df['kariyer_seviyesi'] == level]['ortalama_maas'])
        
        plt.figure(figsize=(12, 8))
        box_plot = plt.boxplot(career_salaries, labels=[career_names[level] for level in career_levels], patch_artist=True)
        for patch in box_plot['boxes']:
            patch.set_facecolor(VIRIDIS_COLORS['tertiary'])
        
        plt.title('Career Level and Salary Comparison', fontsize=20, fontweight='bold', pad=20)
        plt.ylabel('Monthly Average Net Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/09_kariyer_seviyesi_maas_karsilastirma.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_secondary_analysis_charts(self) -> None:
        """İkincil analiz görselleri (15+ adet) - Yayın kalitesinde"""
        print("🔍 Yayın kalitesinde ikincil analiz görselleri oluşturuluyor...")
        
        # 1. Deneyim vs Maaş Scatter Plot
        plt.figure(figsize=(12, 8))
        plt.scatter(self.df['kariyer_seviyesi'], self.df['ortalama_maas'], 
                   alpha=0.6, color=VIRIDIS_COLORS['secondary'], s=20)
        plt.title('Career Level vs Salary Correlation', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Career Level', fontsize=18, fontweight='bold', labelpad=15)
        plt.ylabel('Monthly Average Net Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        
        # Trend çizgisi ekle
        z = np.polyfit(self.df['kariyer_seviyesi'], self.df['ortalama_maas'], 1)
        p = np.poly1d(z)
        plt.plot(self.df['kariyer_seviyesi'], p(self.df['kariyer_seviyesi']), 
                color=VIRIDIS_COLORS['quaternary'], linewidth=3, linestyle='--', alpha=0.8)
        
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/10_deneyim_maas_scatter.png', dpi=300, bbox_inches='tight')
        plt.close()

    def _get_primary_role(self, row: pd.Series) -> Optional[str]:
        role_cols = [c for c in row.index if c.startswith('role_')]
        if not role_cols:
            return None
        active = [c for c in role_cols if row[c] == 1]
        if not active:
            return None
        # Basit seçim: ilk aktif rol
        return active[0].replace('role_', '').replace('_', ' ').title()

    def create_tech_combo_insights(self) -> None:
        """Rollere göre en yaygın tech kombinasyonları ve maaşlar"""
        print("🔗 Tech kombinasyon içgörüleri oluşturuluyor...")
        prog_cols = [c for c in self.df.columns if c.startswith('prog_lang_')]
        fe_cols = [c for c in self.df.columns if c.startswith('frontend_')]
        tool_cols = [c for c in self.df.columns if c.startswith('tools_')]
        role_cols = [c for c in self.df.columns if c.startswith('role_')]
        if not prog_cols or not role_cols:
            return
        df = self.df.copy()
        # Birincil rol
        df['primary_role'] = df.apply(self._get_primary_role, axis=1)
        # Kombinasyon anahtarı: en popüler 1 dil + 1 framework (varsa) + 1 tool (varsa)
        def pick_first(cols, row):
            chosen = [c for c in cols if row.get(c, 0) == 1]
            return chosen[0] if chosen else None
        df['combo_lang'] = df.apply(lambda r: pick_first(prog_cols, r), axis=1)
        df['combo_fe'] = df.apply(lambda r: pick_first(fe_cols, r), axis=1)
        df['combo_tool'] = df.apply(lambda r: pick_first(tool_cols, r), axis=1)
        def clean_name(col_name: Optional[str], prefix: str) -> Optional[str]:
            if col_name is None:
                return None
            return col_name.replace(prefix, '').replace('_', ' ').title()
        df['combo_lang'] = df['combo_lang'].apply(lambda x: clean_name(x, 'prog_lang_'))
        df['combo_fe'] = df['combo_fe'].apply(lambda x: clean_name(x, 'frontend_'))
        df['combo_tool'] = df['combo_tool'].apply(lambda x: clean_name(x, 'tools_'))
        df['combo_str'] = df.apply(lambda r: ' + '.join([x for x in [r['combo_lang'], r['combo_fe'], r['combo_tool']] if pd.notna(x) and x]), axis=1)
        top = (df.dropna(subset=['combo_str', 'primary_role'])
                 .groupby(['primary_role', 'combo_str'])
                 .agg(n=('ortalama_maas', 'size'), mean_salary=('ortalama_maas', 'mean'))
                 .reset_index())
        # Her rol için en populer 5 kombinasyon
        results = []
        for role, g in top.groupby('primary_role'):
            g = g.sort_values('n', ascending=False).head(5)
            g['primary_role'] = role
            results.append(g)
        if not results:
            return
        out = pd.concat(results)
        # Görselleştir: yatay bar (n anotasyonu), role göre facet yerine tek figür, renk tonları
        plt.figure(figsize=(12, 8))
        ordered = out.sort_values(['primary_role', 'n'], ascending=[True, False])
        y_labels = [f"{r} | {c}" for r, c in zip(ordered['primary_role'], ordered['combo_str'])]
        bars = plt.barh(y_labels, ordered['mean_salary'], color=VIRIDIS_COLORS['secondary'])
        plt.title('Top Tech Combinations by Role (Avg Salary)', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Average Salary (k TL)', fontsize=18, fontweight='bold')
        plt.ylabel('Role | Combination', fontsize=18, fontweight='bold')
        plt.grid(True, axis='x', alpha=0.3, color='#E5E5E5')
        # n anotasyonu
        for bar, n in zip(bars, ordered['n']):
            plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f"n={int(n)}", va='center', fontsize=12)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/21_tech_combo_top.png', dpi=300, bbox_inches='tight')
        plt.close()

    def create_skill_diversity_vs_salary(self) -> None:
        """Dil/araç sayısına göre maaş dağılımı (violin)"""
        print("🎯 Skill diversity vs salary görseli oluşturuluyor...")
        prog_cols = [c for c in self.df.columns if c.startswith('prog_lang_')]
        tool_cols = [c for c in self.df.columns if c.startswith('tools_')]
        if not prog_cols:
            return
        df = self.df.copy()
        df['skill_count'] = df[prog_cols + tool_cols].sum(axis=1)
        def bin_count(x: int) -> str:
            if x <= 2:
                return '1-2'
            if x <= 5:
                return '3-5'
            return '6+'
        df['skill_bin'] = df['skill_count'].apply(bin_count)
        plt.figure(figsize=(12, 8))
        sns.violinplot(data=df, x='skill_bin', y='ortalama_maas', inner='quartile', palette='viridis')
        plt.title('Salary vs Skill Diversity (Languages + Tools)', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Skill Count Bin', fontsize=18, fontweight='bold')
        plt.ylabel('Monthly Average Net Salary (k TL)', fontsize=18, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/22_skill_diversity_salary.png', dpi=300, bbox_inches='tight')
        plt.close()

    def create_experience_usage_heatmap(self) -> None:
        """Deneyim binlerine göre dil kullanımı ısı haritası"""
        print("🔥 Deneyime göre teknoloji kullanım ısı haritası oluşturuluyor...")
        if 'deneyim_yili' not in self.df.columns:
            return
        df = self.df.copy()
        df['exp_bin'] = pd.cut(df['deneyim_yili'], bins=[-0.1, 2, 5, 10, 100], labels=['0-2', '3-5', '6-10', '11+'])
        lang_cols = [c for c in df.columns if c.startswith('prog_lang_')]
        if not lang_cols:
            return
        # En popüler 10 dil
        usage = df[lang_cols].sum().sort_values(ascending=False).head(10).index.tolist()
        data = []
        for lang in usage:
            rates = df.groupby('exp_bin')[lang].mean() * 100
            data.append(rates)
        heat_df = pd.DataFrame(data, index=[c.replace('prog_lang_', '').replace('_', ' ').title() for c in usage])
        plt.figure(figsize=(12, 8))
        sns.heatmap(heat_df, annot=True, fmt='.1f', cmap='viridis', cbar_kws={'label': 'Usage %'})
        plt.title('Programming Language Usage by Experience Bin', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Experience Bin', fontsize=18, fontweight='bold')
        plt.ylabel('Language', fontsize=18, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/23_experience_lang_usage_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()

    def create_role_experience_salary_paths(self) -> None:
        """Rol bazında deneyim binlerine göre maaş trendi"""
        print("📈 Rol × Deneyim maaş yolları oluşturuluyor...")
        df = self.df.copy()
        if 'deneyim_yili' not in df.columns:
            return
        df['exp_bin'] = pd.cut(df['deneyim_yili'], bins=[-0.1, 2, 5, 10, 100], labels=['0-2', '3-5', '6-10', '11+'])
        # Hedef roller
        target_roles = ['backend', 'frontend', 'fullstack', 'data_engineer']
        role_cols = [f'role_{r}' for r in target_roles if f'role_{r}' in df.columns]
        if not role_cols:
            return
        plt.figure(figsize=(12, 8))
        for rc in role_cols:
            role_name = rc.replace('role_', '').replace('_', ' ').title()
            g = df[df[rc] == 1].groupby('exp_bin')['ortalama_maas'].mean()
            plt.plot(g.index.astype(str), g.values, marker='o', linewidth=3, label=role_name)
        plt.title('Salary Paths by Role and Experience', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Experience Bin', fontsize=18, fontweight='bold')
        plt.ylabel('Average Salary (k TL)', fontsize=18, fontweight='bold')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/24_role_experience_salary_paths.png', dpi=300, bbox_inches='tight')
        plt.close()

    def create_tool_adoption_by_role_location(self) -> None:
        """Lokasyon ve rollere göre en popüler araçların kullanımı (ısı haritası)"""
        print("🗺️ Araç kullanımı: rol × lokasyon ısı haritası oluşturuluyor...")
        df = self.df.copy()
        tool_cols = [c for c in df.columns if c.startswith('tools_')]
        loc_cols = [c for c in df.columns if c.startswith('location_')]
        role_cols = [c for c in df.columns if c.startswith('role_')]
        if not tool_cols or not loc_cols or not role_cols:
            return
        # En popüler 8 araç
        top_tools = df[tool_cols].sum().sort_values(ascending=False).head(8).index.tolist()
        # Lokasyon isimleri
        loc_names = [c.replace('location_', '').replace('_', ' ').title() for c in loc_cols]
        # Rol isimleri (ana 4 rol varsa onlara indir)
        roles_keep = [c for c in role_cols if any(k in c for k in ['backend', 'frontend', 'fullstack', 'data_engineer'])] or role_cols[:4]
        role_names = [c.replace('role_', '').replace('_', ' ').title() for c in roles_keep]
        # Matris: satır rol, sütun araç → kullanım % (lokasyonlar ortalaması)
        data = []
        for rc in roles_keep:
            role_mask = df[rc] == 1
            row_vals = []
            for tool in top_tools:
                rate = (df.loc[role_mask, tool].mean() * 100) if role_mask.any() else 0
                row_vals.append(rate)
            data.append(row_vals)
        heat_df = pd.DataFrame(data, index=role_names, columns=[t.replace('tools_', '').replace('_', ' ').title() for t in top_tools])
        plt.figure(figsize=(12, 8))
        sns.heatmap(heat_df, annot=True, fmt='.1f', cmap='viridis', cbar_kws={'label': 'Usage %'})
        plt.title('Top Tool Adoption by Role', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Tool', fontsize=18, fontweight='bold')
        plt.ylabel('Role', fontsize=18, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/25_tool_adoption_role_location.png', dpi=300, bbox_inches='tight')
        plt.close()

    def create_work_arrangement_by_role(self) -> None:
        """Rol bazında çalışma şekli dağılımı (yığılmış yüzde bar) ve ortalama maaş"""
        print("🏢 Çalışma düzeni × rol görseli oluşturuluyor...")
        df = self.df.copy()
        role_cols = [c for c in df.columns if c.startswith('role_')]
        if not role_cols or 'calisma_sekli' not in df.columns:
            return
        # Ana roller seçimi
        roles_keep = [c for c in role_cols if any(k in c for k in ['backend', 'frontend', 'fullstack', 'data_engineer'])] or role_cols[:5]
        role_names = [c.replace('role_', '').replace('_', ' ').title() for c in roles_keep]
        work_map = {0: 'Remote', 1: 'Office', 2: 'Hybrid'}
        dist = []
        salary_ann = {}
        for rc, rn in zip(roles_keep, role_names):
            sub = df[df[rc] == 1]
            if len(sub) == 0:
                continue
            counts = sub['calisma_sekli'].value_counts(normalize=True) * 100
            dist.append({**{'Role': rn}, **{work_map.get(k, str(k)): counts.get(k, 0) for k in [0, 1, 2]}})
            salary_ann[rn] = sub['ortalama_maas'].mean()
        if not dist:
            return
        plot_df = pd.DataFrame(dist).set_index('Role')
        plot_df = plot_df[['Remote', 'Office', 'Hybrid']]
        plot_df.plot(kind='bar', stacked=True, color=[CATEGORICAL_COLORS['remote'], CATEGORICAL_COLORS['office'], CATEGORICAL_COLORS['hybrid']], figsize=(12, 8))
        plt.title('Work Arrangement Distribution by Role', fontsize=20, fontweight='bold', pad=20)
        plt.ylabel('Percentage (%)', fontsize=18, fontweight='bold')
        plt.xlabel('Role', fontsize=18, fontweight='bold')
        plt.legend(title='Arrangement')
        # Ortalama maaş anotasyonları
        for i, rn in enumerate(plot_df.index):
            plt.text(i, 102, f"Avg ₺{salary_ann.get(rn, 0):.0f}k", ha='center', va='bottom', fontsize=12, fontweight='bold')
        plt.ylim(0, 110)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/26_work_arrangement_by_role.png', dpi=300, bbox_inches='tight')
        plt.close()

    def create_correlation_heatmap(self) -> None:
        """Seçilmiş metriklerin korelasyon ısı haritası"""
        print("📊 Korelasyon ısı haritası oluşturuluyor...")
        df = self.df.copy()
        numeric = ['ortalama_maas', 'kariyer_seviyesi', 'cinsiyet', 'calisma_sekli']
        prog_cols = [c for c in df.columns if c.startswith('prog_lang_')]
        tool_cols = [c for c in df.columns if c.startswith('tools_')]
        if prog_cols:
            df['num_langs'] = df[prog_cols].sum(axis=1)
            numeric.append('num_langs')
        if tool_cols:
            df['num_tools'] = df[tool_cols].sum(axis=1)
            numeric.append('num_tools')
        corr = df[numeric].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='viridis', cbar_kws={'label': 'r'})
        plt.title('Correlation Heatmap', fontsize=20, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/27_correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()

    def create_top_earners_traits(self) -> None:
        """En yüksek maaşlı %10 kitlenin ortak özellikleri"""
        print("🏆 Üst %10 kazananların özellikleri oluşturuluyor...")
        df = self.df.copy()
        if 'ortalama_maas' not in df.columns:
            return
        threshold = df['ortalama_maas'].quantile(0.9)
        top = df[df['ortalama_maas'] >= threshold]
        if top.empty:
            return
        cols_blocks = [
            ('prog_lang_', 10),
            ('frontend_', 5),
            ('tools_', 8),
            ('role_', 5)
        ]
        trait_counts = {}
        for prefix, topn in cols_blocks:
            cols = [c for c in top.columns if c.startswith(prefix)]
            if not cols:
                continue
            counts = top[cols].sum().sort_values(ascending=False).head(topn)
            for idx, val in counts.items():
                name = idx.replace(prefix, '').replace('_', ' ').title()
                trait_counts[name] = trait_counts.get(name, 0) + int(val)
        if not trait_counts:
            return
        names, values = zip(*sorted(trait_counts.items(), key=lambda x: x[1], reverse=True)[:12])
        plt.figure(figsize=(12, 8))
        bars = plt.barh(names, values, color=VIRIDIS_COLORS['primary'])
        plt.title('Common Traits among Top 10% Earners', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Count within Top 10%', fontsize=18, fontweight='bold')
        plt.grid(True, axis='x', alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/28_top_earners_traits.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Saat bazlı maaş analizi
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df['anket_saati'] = self.df['timestamp'].dt.hour
        
        hour_groups = {
            'Night (00-06)': self.df[self.df['anket_saati'].between(0, 6)]['ortalama_maas'],
            'Morning (07-12)': self.df[self.df['anket_saati'].between(7, 12)]['ortalama_maas'],
            'Afternoon (13-18)': self.df[self.df['anket_saati'].between(13, 18)]['ortalama_maas'],
            'Evening (19-23)': self.df[self.df['anket_saati'].between(19, 23)]['ortalama_maas']
        }
        
        plt.figure(figsize=(12, 8))
        box_plot = plt.boxplot(list(hour_groups.values()), labels=list(hour_groups.keys()), patch_artist=True)
        for patch in box_plot['boxes']:
            patch.set_facecolor(VIRIDIS_COLORS['primary'])
        
        plt.title('Hourly Salary Analysis', fontsize=20, fontweight='bold', pad=20)
        plt.ylabel('Monthly Average Net Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/11_saat_bazli_maas_analizi.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Teknoloji ROI analizi
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from src.advanced_analysis import AdvancedAnalyzer
        
        analyzer = AdvancedAnalyzer()
        analyzer.df = self.df
        tech_result = analyzer.technology_stack_roi_analysis()
        
        if tech_result and 'top_technologies' in tech_result:
            top_10 = tech_result['top_technologies'][:10]
            tech_names = [tech for tech, _ in top_10]
            roi_values = [data['roi_percentage'] for _, data in top_10]
            
            plt.figure(figsize=(12, 8))
            bars = plt.barh(tech_names, roi_values, color=VIRIDIS_COLORS['secondary'], alpha=0.8)
            plt.title('Most Profitable Technologies (ROI Analysis)', fontsize=20, fontweight='bold', pad=20)
            plt.xlabel('ROI (%)', fontsize=18, fontweight='bold', labelpad=15)
            plt.ylabel('Technology', fontsize=18, fontweight='bold', labelpad=15)
            plt.xticks(fontsize=14, fontweight='bold')
            plt.yticks(fontsize=14, fontweight='bold')
            plt.grid(True, alpha=0.3, color='#E5E5E5', axis='x')
            
            # Değerleri çubukların üzerine yaz
            for i, (bar, roi) in enumerate(zip(bars, roi_values)):
                plt.text(roi + 0.5, bar.get_y() + bar.get_height()/2, f'{roi:.1f}%', 
                        ha='left', va='center', fontweight='bold', fontsize=14)
            
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
        
        plt.figure(figsize=(12, 8))
        plt.plot(career_labels, career_means, marker='o', linewidth=3, markersize=10, 
                color=VIRIDIS_COLORS['primary'])
        plt.title('Career Progression - Salary Growth', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Career Level', fontsize=18, fontweight='bold', labelpad=15)
        plt.ylabel('Average Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        
        # Değerleri çizginin üzerine yaz
        for i, (label, mean) in enumerate(zip(career_labels, career_means)):
            plt.text(i, mean + 2, f'{mean:.1f}', ha='center', va='bottom', 
                    fontweight='bold', fontsize=14)
        
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/13_kariyer_progression.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. Etkileşim analizi (Work Type × Location)
        interaction_result = analyzer.interaction_analysis()
        
        if interaction_result and 'interaction_data' in interaction_result:
            interaction_data = interaction_result['interaction_data']
            
            if interaction_data:
                interaction_df = pd.DataFrame(interaction_data)
                
                try:
                    pivot_data = interaction_df.pivot(index='work_type', columns='location', values='mean_salary')
                    
                    plt.figure(figsize=(12, 8))
                    sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='viridis', 
                               cbar_kws={'label': 'Ortalama Maaş (bin TL)'})
                    plt.title('Work Type × Location Interaction', fontsize=20, fontweight='bold', pad=20)
                    plt.xlabel('Company Location', fontsize=18, fontweight='bold', labelpad=15)
                    plt.ylabel('Work Type', fontsize=18, fontweight='bold', labelpad=15)
                    plt.xticks(fontsize=14, fontweight='bold')
                    plt.yticks(fontsize=14, fontweight='bold')
                    plt.tight_layout()
                    plt.savefig(f'{self.figures_dir}/14_calisma_lokasyon_etkilesimi.png', dpi=300, bbox_inches='tight')
                    plt.close()
                except:
                    # Fallback: Bar chart
                    plt.figure(figsize=(12, 8))
                    
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
                    
                    plt.title('Work Type × Location Interaction', fontsize=20, fontweight='bold', pad=20)
                    plt.xlabel('Company Location', fontsize=18, fontweight='bold', labelpad=15)
                    plt.ylabel('Average Salary (k TL)', fontsize=18, fontweight='bold', labelpad=15)
                    plt.xticks(x + width, locations, rotation=45, fontsize=14, fontweight='bold')
                    plt.yticks(fontsize=14, fontweight='bold')
                    plt.legend(fontsize=16)
                    plt.grid(True, alpha=0.3, color='#E5E5E5')
                    plt.tight_layout()
                    plt.savefig(f'{self.figures_dir}/14_calisma_lokasyon_etkilesimi.png', dpi=300, bbox_inches='tight')
                    plt.close()
        
        # 6. Demografik dağılımlar
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Cinsiyet dağılımı
        gender_counts = self.df['cinsiyet'].value_counts()
        colors = ['#FF6B6B', '#4ECDC4']  # Erkek: kırmızı, Kadın: turkuaz
        axes[0, 0].pie(gender_counts.values, labels=['Male', 'Female'], autopct='%1.1f%%', 
                      startangle=90, colors=colors, textprops={'fontweight': 'bold', 'fontsize': 14})
        axes[0, 0].set_title('Gender Distribution', fontsize=18, fontweight='bold')
        
        # Kariyer seviyesi dağılımı
        career_counts = self.df['kariyer_seviyesi'].value_counts().sort_index()
        career_labels = [career_names[level] for level in career_counts.index]
        axes[0, 1].bar(career_labels, career_counts.values, color=VIRIDIS_COLORS['primary'])
        axes[0, 1].set_title('Career Level Distribution', fontsize=18, fontweight='bold')
        axes[0, 1].set_ylabel('Number of People', fontsize=16)
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Çalışma şekli dağılımı
        work_counts = self.df['calisma_sekli'].value_counts().sort_index()
        work_labels = ['Remote', 'Office', 'Hybrid']
        axes[1, 0].bar(work_labels, work_counts.values, color=VIRIDIS_COLORS['secondary'])
        axes[1, 0].set_title('Work Type Distribution', fontsize=18, fontweight='bold')
        axes[1, 0].set_ylabel('Number of People', fontsize=16)
        
        # Lokasyon dağılımı
        location_cols = [col for col in self.df.columns if col.startswith('location_')]
        location_counts = []
        location_labels = []
        for col in location_cols:
            count = self.df[col].sum()
            if count > 0:
                location_counts.append(count)
                location_labels.append(col.replace('location_', '').replace('_', ' ').title())
        
        axes[1, 1].bar(location_labels, location_counts, color=VIRIDIS_COLORS['tertiary'])
        axes[1, 1].set_title('Company Location Distribution', fontsize=18, fontweight='bold')
        axes[1, 1].set_ylabel('Number of People', fontsize=16)
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/15_demografik_dagilimlar.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 7. Maaş aralıkları analizi
        salary_ranges = pd.cut(self.df['ortalama_maas'], bins=10)
        range_counts = salary_ranges.value_counts().sort_index()
        
        plt.figure(figsize=(12, 8))
        range_counts.plot(kind='bar', color=VIRIDIS_COLORS['secondary'])
        plt.title('Salary Range Distribution', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Salary Range (k TL)', fontsize=18, fontweight='bold', labelpad=15)
        plt.ylabel('Number of People', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(rotation=45, fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/16_maas_araliklari.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 8. Saat bazlı katılım analizi
        hour_counts = self.df['anket_saati'].value_counts().sort_index()
        
        plt.figure(figsize=(12, 8))
        plt.plot(hour_counts.index, hour_counts.values, marker='o', linewidth=3, 
                color=VIRIDIS_COLORS['primary'], markersize=8)
        plt.title('Hourly Survey Participation', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Hour', fontsize=18, fontweight='bold', labelpad=15)
        plt.ylabel('Number of Participants', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/17_saat_bazli_katilim.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 9. Teknoloji kullanım oranları
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
                if lang_key in lang_name_mapping:
                    lang_name = lang_name_mapping[lang_key]
                else:
                    lang_name = lang_key.replace('_', ' ').title()
                
                if lang_name != 'Hiçbiri':
                    lang_usage[lang_name] = usage_rate
        
        # En popüler 10 dil
        top_languages = dict(sorted(lang_usage.items(), key=lambda x: x[1], reverse=True)[:10])
        
        plt.figure(figsize=(12, 8))
        bars = plt.barh(list(top_languages.keys()), list(top_languages.values()), 
                       color=VIRIDIS_COLORS['secondary'])
        plt.title('Most Popular Programming Languages', fontsize=20, fontweight='bold', pad=20)
        plt.xlabel('Usage Rate (%)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5', axis='x')
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
        
        plt.figure(figsize=(12, 8))
        bars = plt.bar(frontend_usage.keys(), frontend_usage.values(), 
                      color=VIRIDIS_COLORS['tertiary'])
        plt.title('Frontend Framework Usage Rates', fontsize=20, fontweight='bold', pad=20)
        plt.ylabel('Usage Rate (%)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(rotation=45, fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
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
        
        plt.figure(figsize=(12, 8))
        bars = plt.bar(top_tools.keys(), top_tools.values(), color=VIRIDIS_COLORS['quaternary'])
        plt.title('Most Popular Tool Usage', fontsize=20, fontweight='bold', pad=20)
        plt.ylabel('Usage Rate (%)', fontsize=18, fontweight='bold', labelpad=15)
        plt.xticks(rotation=45, fontsize=14, fontweight='bold')
        plt.yticks(fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, color='#E5E5E5')
        plt.tight_layout()
        plt.savefig(f'{self.figures_dir}/20_populer_tool_kullanimi.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_all_publication_quality_charts(self) -> None:
        """Tüm yayın kalitesinde görselleri oluştur"""
        print("🎨 Yayın kalitesinde tüm görseller oluşturuluyor...")
        
        if self.df is None:
            self.load_data()
        
        # figures dizinini oluştur
        import os
        os.makedirs(self.figures_dir, exist_ok=True)
        
        # Görselleri oluştur
        # self.create_salary_distribution_charts()
        # self.create_basic_comparison_charts()
        # self.create_secondary_analysis_charts()
        # self.create_tech_combo_insights()
        # self.create_skill_diversity_vs_salary()
        # self.create_experience_usage_heatmap()
        self.create_role_experience_salary_paths()
        # self.create_tool_adoption_by_role_location()
        # self.create_work_arrangement_by_role()
        # self.create_correlation_heatmap()
        # self.create_top_earners_traits()
        
        # print(f"✅ Toplam 20+ yayın kalitesinde görsel '{self.figures_dir}/' dizinine kaydedildi!")
        # print("📋 Tüm grafikler VISUAL_STANDARDS.md gereksinimlerine uygun:")
        # print("   - 12x8 inç boyut, 300 DPI, PNG format")
        # print("   - Arial font, belirtilen font boyutları")
        # print("   - Viridis renk paleti")
        # print("   - LaTeX entegrasyonu için optimize edilmiş")


def main():
    """Ana fonksiyon"""
    visualizer = PublicationQualityVisualizer()
    visualizer.create_all_publication_quality_charts()


if __name__ == "__main__":
    main()

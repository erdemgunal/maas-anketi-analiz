"""
Görselleştirme Modülü

Bu modül, analiz sonuçlarını yayın kalitesinde görselleştirmek için
fonksiyonlar içerir.

Fonksiyonlar:
- set_publication_style: Yayın kalite stil ayarları
- ensure_dirs: Çıktı klasörlerini oluşturur
- basic_distribution_plots: Temel dağılım grafiklerini üretir
- salary_comparison_plots: Maaş karşılaştırma grafiklerini üretir
- correlation_plots: Korelasyon ve heatmap grafiklerini üretir
- technology_plots: Teknoloji kullanımı ile ilgili grafikler
- model_performance_plots: ML performans grafikleri
- clustering_plots: Kümelerle ilgili grafikler
- generate_all_figures: Tüm grafiklerin üretimi
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

FIG_DIR = '../outputs/figures'
DPI = 300
FIGSIZE = (12, 8)


def set_publication_style():
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    plt.rcParams.update({
        'figure.figsize': FIGSIZE,
        'figure.dpi': DPI,
        'savefig.dpi': DPI,
        'axes.titlesize': 16,
        'axes.labelsize': 13,
        'font.size': 12,
        'axes.grid': True,
        'grid.alpha': 0.2,
        'font.family': 'Arial'
    })


def ensure_dirs():
    os.makedirs(FIG_DIR, exist_ok=True)


def savefig(path: str):
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, path), dpi=DPI, bbox_inches='tight')
    plt.close()


def basic_distribution_plots(df: pd.DataFrame):
    # 1. Salary histogram
    plt.figure()
    sns.histplot(df['salary_normalized'], bins=40, kde=True, color='#4ECDC4')
    plt.title('Maaş Dağılımı (Histogram + KDE)')
    plt.xlabel('Maaş (bin TL)')
    plt.ylabel('Frekans')
    savefig('01_salary_hist_kde.png')

    # 2. Salary boxplot
    plt.figure()
    sns.boxplot(y=df['salary_normalized'], color='#FF6B6B')
    plt.title('Maaş Dağılımı (Box Plot)')
    plt.ylabel('Maaş (bin TL)')
    savefig('02_salary_boxplot.png')

    # 3. Salary violin
    plt.figure()
    sns.violinplot(y=df['salary_normalized'], color='#45B7D1')
    plt.title('Maaş Dağılımı (Violin Plot)')
    plt.ylabel('Maaş (bin TL)')
    savefig('03_salary_violin.png')

    # 4. QQ plot (manual via scipy not required here) -> use rank vs normal
    from scipy import stats
    plt.figure()
    stats.probplot(df['salary_normalized'], dist='norm', plot=plt)
    plt.title('Maaş Normalite Q-Q Plot')
    savefig('04_salary_qqplot.png')

    # 5. Experience histogram
    exp_col = 'Toplam kaç yıllık iş deneyimin var?'
    if exp_col in df.columns:
        plt.figure()
        sns.histplot(df[exp_col], bins=30, kde=True, color='#FFA07A')
        plt.title('Toplam İş Deneyimi Dağılımı')
        plt.xlabel('Yıl')
        plt.ylabel('Frekans')
        savefig('05_experience_hist.png')

    # 6. Level countplot
    level_col = 'Hangi seviyedesin?'
    if level_col in df.columns:
        plt.figure()
        sns.countplot(x=df[level_col], color='#96CEB4')
        plt.title('Deneyim Seviyesi Dağılımı')
        plt.xlabel('Seviye')
        plt.ylabel('Adet')
        savefig('06_level_count.png')


def salary_comparison_plots(df: pd.DataFrame):
    # 7. React vs Non-React boxplot
    if 'Frontend_React' in df.columns:
        plt.figure()
        sns.boxplot(x=df['Frontend_React'], y=df['salary_normalized'], palette=['#FF6B6B', '#4ECDC4'])
        plt.title('React Kullanımı vs Maaş')
        plt.xlabel('React (0=Hayır, 1=Evet)')
        plt.ylabel('Maaş (bin TL)')
        savefig('07_react_salary_box.png')

    # 8. Gender vs salary
    if 'Cinsiyet' in df.columns:
        plt.figure()
        sns.boxplot(x=df['Cinsiyet'], y=df['salary_normalized'], palette=['#45B7D1', '#FFA07A'])
        plt.title('Cinsiyet vs Maaş')
        plt.xlabel('Cinsiyet (0=Erkek, 1=Kadın)')
        plt.ylabel('Maaş (bin TL)')
        savefig('08_gender_salary_box.png')

    # 9. Work type ANOVA view
    work_col = 'Çalışma şekli'
    if work_col in df.columns:
        plt.figure()
        sns.boxplot(x=df[work_col], y=df['salary_normalized'], palette='husl')
        plt.title('Çalışma Şekli vs Maaş')
        plt.xlabel('Çalışma Şekli (0=Remote,1=Hybrid,2=Office)')
        plt.ylabel('Maaş (bin TL)')
        savefig('09_worktype_salary_box.png')

    # 10. Salary by level bars
    level_col = 'Hangi seviyedesin?'
    if level_col in df.columns:
        plt.figure()
        means = df.groupby(level_col)['salary_normalized'].mean().reset_index()
        sns.barplot(data=means, x=level_col, y='salary_normalized', color='#6C5B7B')
        plt.title('Seviyeye Göre Ortalama Maaş')
        plt.xlabel('Seviye')
        plt.ylabel('Ortalama Maaş (bin TL)')
        savefig('10_salary_by_level_bar.png')

    # 11. Salary by experience scatter
    exp_col = 'Toplam kaç yıllık iş deneyimin var?'
    if exp_col in df.columns:
        plt.figure()
        sns.scatterplot(x=df[exp_col], y=df['salary_normalized'], alpha=0.4, color='#355C7D')
        plt.title('Maaş vs İş Deneyimi')
        plt.xlabel('İş Deneyimi (yıl)')
        plt.ylabel('Maaş (bin TL)')
        savefig('11_salary_vs_experience_scatter.png')

    # 12. Salary distribution by location (if exists)
    if 'Şirket lokasyon' in df.columns:
        plt.figure()
        means = df.groupby('Şirket lokasyon')['salary_normalized'].mean().sort_values()
        means.plot(kind='bar', color='#F8B195')
        plt.title('Lokasyona Göre Ortalama Maaş')
        plt.xlabel('Lokasyon')
        plt.ylabel('Ortalama Maaş (bin TL)')
        savefig('12_salary_by_location_bar.png')


def correlation_plots(df: pd.DataFrame):
    # 13. Correlation heatmap (top 15 with salary)
    num_cols = df.select_dtypes(include=[np.number]).columns
    corr = df[num_cols].corr()
    top_corr = corr['salary_normalized'].abs().sort_values(ascending=False).head(15).index
    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones((len(top_corr), len(top_corr)), dtype=bool))
    sns.heatmap(corr.loc[top_corr, top_corr], annot=True, cmap='coolwarm', center=0, fmt='.2f', mask=mask)
    plt.title('Maaş ile En Yüksek Korelasyonlu Değişkenler (Heatmap)')
    savefig('13_correlation_heatmap.png')

    # 14. Pairplot (subset)
    subset = [c for c in ['salary_normalized', 'Hangi seviyedesin?', 'Toplam kaç yıllık iş deneyimin var?'] if c in df.columns]
    if len(subset) >= 2:
        g = sns.pairplot(df[subset].sample(min(500, len(df))), corner=True, plot_kws={'alpha':0.5, 's':20})
        g.fig.suptitle('Seçilmiş Değişkenler Pairplot', y=1.02)
        g.savefig(os.path.join(FIG_DIR, '14_pairplot.png'), dpi=DPI, bbox_inches='tight')
        plt.close('all')

    # 15. Salary vs top 5 correlated vars (scatter)
    top5 = corr['salary_normalized'].abs().sort_values(ascending=False).index[1:6]
    for i, col in enumerate(top5, start=1):
        plt.figure()
        sns.scatterplot(x=df[col], y=df['salary_normalized'], alpha=0.4)
        plt.title(f'Maaş vs {col}')
        plt.xlabel(col)
        plt.ylabel('Maaş (bin TL)')
        savefig(f'15_scatter_salary_vs_{i}.png')


def technology_plots(df: pd.DataFrame):
    # 16. Tech frequency bar (from parsed columns prefix)
    tech_prefixes = ['Hangi_', 'Frontend_']
    tech_cols = [c for c in df.columns if any(c.startswith(p) for p in tech_prefixes)]
    if tech_cols:
        tech_means = df[tech_cols].mean().sort_values(ascending=False).head(15)
        plt.figure(figsize=(14, 8))
        tech_means.plot(kind='bar', color='#4ECDC4')
        plt.title('En Çok Kullanılan 15 Teknoloji (Oran)')
        plt.ylabel('Kullanım Oranı')
        plt.xlabel('Teknoloji')
        savefig('16_top_tech_usage.png')

    # 17. React vs others salary difference (bar)
    if 'Frontend_React' in df.columns:
        means = df.groupby('Frontend_React')['salary_normalized'].mean()
        plt.figure()
        sns.barplot(x=means.index, y=means.values, palette=['#FF6B6B', '#4ECDC4'])
        plt.title('React Kullanımı - Ortalama Maaş Karşılaştırması')
        plt.xlabel('React (0=Hayır,1=Evet)')
        plt.ylabel('Ortalama Maaş (bin TL)')
        savefig('17_react_salary_mean_bar.png')

    # 18. Tools usage correlation with salary (top 10)
    tool_cols = [c for c in df.columns if "tool" in c.lower() or 'Tool' in c]
    if tool_cols:
        corrs = {c: df[['salary_normalized', c]].corr().iloc[0,1] for c in tool_cols}
        top10 = sorted(corrs.items(), key=lambda x: abs(x[1] if x[1] is not None else 0), reverse=True)[:10]
        labels = [k for k, _ in top10]
        values = [v for _, v in top10]
        plt.figure(figsize=(14, 8))
        sns.barplot(x=values, y=labels, color='#355C7D')
        plt.title('Maaş ile En Yüksek Korelasyonlu 10 Tool')
        plt.xlabel('Pearson Korelasyonu')
        plt.ylabel('Tool')
        savefig('18_salary_tool_correlations.png')


def model_performance_plots():
    # 19. Read model comparison table if exists
    path = '../outputs/tables/model_comparison.csv'
    if os.path.exists(path):
        comp = pd.read_csv(path)
        plt.figure()
        sns.barplot(data=comp, x='Model', y='Test R²', color='#4ECDC4')
        plt.ylim(0, 1.05)
        plt.title('Modellerin Test R² Karşılaştırması')
        savefig('19_model_test_r2.png')

        plt.figure()
        sns.barplot(data=comp, x='Model', y='CV R²', color='#FF6B6B')
        plt.ylim(0, 1.05)
        plt.title('Modellerin CV R² Karşılaştırması')
        savefig('20_model_cv_r2.png')

        plt.figure()
        comp_melt = comp.melt(id_vars='Model', value_vars=['Test MAE', 'Test RMSE'], var_name='Metric', value_name='Value')
        sns.barplot(data=comp_melt, x='Model', y='Value', hue='Metric')
        plt.title('Test MAE ve RMSE Karşılaştırması')
        savefig('21_model_mae_rmse.png')


def clustering_plots(df: pd.DataFrame):
    # 22. K-means clustering scatter (salary vs experience)
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    exp_col = 'Toplam kaç yıllık iş deneyimin var?'
    if exp_col in df.columns:
        features = ['salary_normalized', exp_col]
        data = df[features].dropna()
        scaler = StandardScaler()
        X = scaler.fit_transform(data)
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        plt.figure()
        plt.scatter(data[exp_col], data['salary_normalized'], c=labels, cmap='viridis', alpha=0.6)
        plt.xlabel('İş Deneyimi (yıl)')
        plt.ylabel('Maaş (bin TL)')
        plt.title('K-Means Kümeleri (Maaş vs Deneyim)')
        savefig('22_kmeans_salary_experience.png')

    # 23. Cluster size pie
    if exp_col in df.columns:
        plt.figure()
        unique, counts = np.unique(labels, return_counts=True)
        plt.pie(counts, labels=[f'Küme {u}' for u in unique], autopct='%1.1f%%', startangle=90)
        plt.title('Küme Dağılımı')
        savefig('23_cluster_pie.png')


def generate_all_figures(file_path: str = '../data/cleaned_data.csv') -> list:
    set_publication_style()
    ensure_dirs()

    df = pd.read_csv(file_path)

    generated = []

    # Basic
    basic_distribution_plots(df); generated += list(range(1, 7))
    # Salary comparisons
    salary_comparison_plots(df); generated += list(range(7, 13))
    # Correlations
    correlation_plots(df); generated += list(range(13, 16)) + [15]
    # Technology
    technology_plots(df); generated += list(range(16, 19))
    # Model performance (reads table if exists)
    model_performance_plots(); generated += [19, 20, 21]
    # Clustering
    clustering_plots(df); generated += [22, 23]

    print(f"{len(os.listdir(FIG_DIR))} figür oluşturuldu ve kaydedildi: {FIG_DIR}")
    return os.listdir(FIG_DIR)


if __name__ == '__main__':
    generate_all_figures()

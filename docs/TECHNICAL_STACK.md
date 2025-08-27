# Teknik Altyapı

Bu doküman, **Yazılım Sektörü Maaş Analizi 2025** projesinde kullanılan teknik araçları ve bağımlılıkları tanımlar. Araçlar, veri ön işleme, istatistiksel analiz, görselleştirme ve raporlama süreçlerini destekler. Tüm araçlar, `ANALYSIS_OBJECTIVES.md`, `METHODOLOGY.md`, `DATASET_SPECIFICATIONS.md`, `EXPECTED_OUTPUTS.md` ve `PRD.md` ile uyumludur ve React staj grubu ile geniş kitle için anlaşılır çıktılar üretmek amacıyla seçilmiştir.

## 1. Programlama Dili
- **Python (3.9+)**:
  - **Amaç**: Veri ön işleme, istatistiksel analiz ve görselleştirme.
  - **Neden?**: Zengin kütüphane ekosistemi, veri bilimi ve görselleştirme için yaygın kullanım.
  - **Kullanılan Sürümler**: 3.9 veya üstü (Pyodide uyumluluğu için Streamlit dashboard’da).

## 2. Veri İşleme ve Analiz Kütüphaneleri
- **pandas (2.2+)**:
  - **Amaç**: Veri yükleme (`2025_maas_anket.csv`), temizleme, normalizasyon, encoding (`get_dummies`, `MultiLabelBinarizer`), türev feature oluşturma (`salary_numeric`, `is_likely_in_company_location`).
  - **Örnek Kullanım**: `df = pd.read_csv('2025_maas_anket.csv')`, `df['salary_numeric'] = df['salary_range'].apply(normalize_salary)`.
- **numpy (1.26+)**:
  - **Amaç**: Sayısal hesaplamalar, aykırı değer kontrolü (IQR, Z-score).
  - **Örnek Kullanım**: `np.abs((df['salary_numeric'] - df['salary_numeric'].mean()) / df['salary_numeric'].std())`.
- **sklearn.preprocessing (1.4+)**:
  - **Amaç**: Çoklu seçim encoding (`MultiLabelBinarizer`).
  - **Örnek Kullanım**: `mlb = MultiLabelBinarizer(); encoded = mlb.fit_transform(df['programming_languages'])`.

## 3. İstatistiksel Analiz Kütüphaneleri
- **scipy.stats (1.12+)**:
  - **Amaç**: İstatistiksel testler (T-testi, Mann-Whitney U, ANOVA, Kruskal-Wallis, Pearson korelasyonu).
  - **Örnek Kullanım**: `t_stat, p_value = ttest_ind(remote_salaries, office_salaries)`.
- **statsmodels (0.14+)**:
  - **Amaç**: Post-hoc testler (Tukey HSD).
  - **Örnek Kullanım**: `tukey = pairwise_tukeyhsd(df['salary_numeric'], df['seniority_level_ic'])`.

## 4. Görselleştirme Kütüphaneleri
- **seaborn (0.13+)**:
  - **Amaç**: Statik grafikler (boxplot, bar plot, scatter plot, heatmap).
  - **Örnek Kullanım**: `sns.boxplot(x='employment_type', y='salary_numeric')`.
- **matplotlib (3.8+)**:
  - **Amaç**: Grafik özelleştirme ve PNG çıktıları.
  - **Örnek Kullanım**: `plt.savefig('boxplot_seniority.png', dpi=300)`.
- **plotly (5.18+)**:
  - **Amaç**: İnteraktif grafikler (Streamlit dashboard için boxplot, bar plot, scatter plot, heatmap, Sankey diyagramı).
  - **Örnek Kullanım**: `fig = px.box(df, x='seniority_level_ic', y='salary_numeric')`.

## 5. Dashboard Platformu
- **Streamlit (1.31+)**:
  - **Amaç**: İnteraktif dashboard oluşturma, filtreleme (`company_location`, `employment_type`, vb.) ve `plotly` grafikleri sunma.
  - **Örnek Kullanım**: `st.plotly_chart(fig)`, `st.selectbox('Lokasyon', df['company_location'].unique())`.
  - **Not**: Yerel veya Streamlit Cloud üzerinde çalıştırılabilir.

## 6. Raporlama Aracı
- **LaTeX (TeX Live 2024, Overleaf)**:
  - **Amaç**: Statik PDF rapor (`maas_analizi_2025.pdf`) üretimi.
  - **Paketler**: `geometry`, `graphicx`, `booktabs`, `amsmath` (PDFLaTeX uyumlu).
  - **Örnek Kullanım**: `\includegraphics[width=\textwidth]{boxplot_seniority.png}`.
  - **Font**: Noto Serif (Türkçe karakter desteği için).

## 7. Bağımlılıklar ve Ortam
- **Ortam**: Python virtual environment (`venv`) veya Jupyter Notebook.
- **Bağımlılıklar**: 
  ```bash
  pip install pandas==2.2.2 numpy==1.26.4 scikit-learn==1.4.2 scipy==1.12.0 statsmodels==0.14.1 seaborn==0.13.2 matplotlib==3.8.3 plotly==5.18.0 streamlit==1.31.0
  ```
- **Test Ortamı**: 100 satırlık örnek veriyle test edildi, tam veri (n=2,970) için genellenebilir.
- **Erişim**: Google Sheets linki sınırlı (https://docs.google.com/spreadsheets/d/1J_MW7t9e2Yi1cErFe5XCnNGaFqXkrdufgZv9Ggnm-RE/edit?usp=sharing).

## 8. Notlar
- **Tekrarlanabilirlik**: Kodlar, Jupyter Notebook veya Python script’lerinde dokümante edilecek.
- **Gizlilik**: Analizler, k-anonimite (n≥10) ile agregasyon seviyesinde.
- **Hedef Kitle**: Araçlar, React staj grubu ve geniş kitle için anlaşılır çıktılar üretmek için optimize edildi.
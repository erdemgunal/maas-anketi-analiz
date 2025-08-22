# 📁 DOSYA YAPISI (FILE STRUCTURE)

## Proje Organizasyonu

```
salary_analysis_project/
├── data/                           # Veri dosyaları
│   ├── maas_anketi.csv            # Raw data (2970 satır)
│   ├── cleaned_data.csv           # Processed data
│   └── benchmark_data.json        # External benchmark data
│
├── src/                           # Kaynak kodlar
│   ├── data_cleaning.py           # Data preprocessing functions
│   ├── statistical_analysis.py    # Hypothesis testing, correlations
│   ├── machine_learning.py        # ML models and predictions
│   ├── visualizations.py          # All plotting functions
│   ├── utils.py                   # Helper functions
│   └── config.py                  # Configuration settings
│
├── notebooks/                     # Jupyter notebooks
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_statistical_tests.ipynb
│   ├── 03_machine_learning.ipynb
│   └── 04_final_analysis.ipynb
│
├── outputs/                       # Çıktı dosyaları
│   ├── figures/                   # All PNG charts (20+ graphs)
│   │   ├── salary_distribution.png
│   │   ├── skill_heatmap.png
│   │   ├── correlation_matrix.png
│   │   ├── experience_salary_scatter.png
│   │   ├── location_salary_boxplot.png
│   │   ├── gender_analysis_stacked_bar.png
│   │   ├── technology_popularity_wordcloud.png
│   │   ├── career_progression_line.png
│   │   ├── clustering_visualization.png
│   │   ├── feature_importance_bar.png
│   │   ├── regression_residuals.png
│   │   └── ... (10+ more)
│   │
│   ├── tables/                    # Statistical results
│   │   ├── hypothesis_test_results.csv
│   │   ├── model_performance.csv
│   │   ├── feature_importance.csv
│   │   ├── descriptive_statistics.csv
│   │   ├── salary_prediction_results.csv
│   │   └── cluster_characteristics.csv
│   │
│   └── models/                    # Trained models
│       ├── salary_predictor.pkl
│       └── clustering_model.pkl
│
├── reports/                       # Raporlar
│   ├── latex_report/              # LaTeX source files
│   │   ├── main.tex               # Main LaTeX file
│   │   ├── sections/              # Section files
│   │   │   ├── introduction.tex
│   │   │   ├── methodology.tex
│   │   │   ├── results.tex
│   │   │   └── conclusion.tex
│   │   └── references.bib         # Bibliography
│   │
│   └── final_report.pdf           # Final PDF report
│
├── dashboard/                     # Streamlit dashboard
│   ├── app.py                     # Main dashboard application
│   ├── requirements.txt           # Dashboard dependencies
│   └── README.md                  # Dashboard documentation
│
├── docs/                          # Dokümantasyon
│   ├── PROJECT_OVERVIEW.md        # Proje özeti
│   ├── DATASET_SPECIFICATIONS.md  # Veri seti detayları
│   ├── ANALYSIS_OBJECTIVES.md     # Analiz hedefleri
│   ├── METHODOLOGY.md             # Metodoloji
│   ├── TECHNICAL_STACK.md         # Teknik stack
│   ├── FILE_STRUCTURE.md          # Bu dosya
│   ├── EXPECTED_OUTPUTS.md        # Beklenen çıktılar
│   ├── SUCCESS_CRITERIA.md        # Başarı kriterleri
│   ├── WORKFLOW.md                # İş akışı
│   ├── VISUAL_STANDARDS.md        # Görsel standartlar
│   └── CODING_GUIDELINES.md       # Kod yazım kuralları
│
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
└── .gitignore                     # Git ignore file
```

## Dosya Açıklamaları

### Data Directory
- **maas_anketi.csv**: Orijinal anket verisi (2970 satır)
- **cleaned_data.csv**: Temizlenmiş ve işlenmiş veri
- **benchmark_data.json**: Karşılaştırma için dış veri

### Source Code (src/)
- **data_cleaning.py**: Veri temizleme ve preprocessing
- **statistical_analysis.py**: İstatistiksel testler ve analizler
- **machine_learning.py**: ML modelleri ve tahminler
- **visualizations.py**: Grafik ve görselleştirme fonksiyonları
- **utils.py**: Yardımcı fonksiyonlar
- **config.py**: Konfigürasyon ve sabitler

### Notebooks
- **01_exploratory_data_analysis.ipynb**: Keşifsel veri analizi
- **02_statistical_tests.ipynb**: İstatistiksel testler
- **03_machine_learning.ipynb**: Makine öğrenmesi modelleri
- **04_final_analysis.ipynb**: Final analiz ve raporlama

### Outputs
- **figures/**: 20+ PNG grafik dosyası
- **tables/**: İstatistiksel sonuç tabloları
- **models/**: Eğitilmiş ML modelleri

### Reports
- **latex_report/**: LaTeX kaynak dosyaları
- **final_report.pdf**: Final PDF raporu

### Dashboard
- **app.py**: Streamlit dashboard uygulaması
- **requirements.txt**: Dashboard bağımlılıkları

## Naming Conventions

### Dosya İsimlendirme
- **snake_case**: Python dosyaları ve modüller
- **kebab-case**: Markdown dosyaları
- **PascalCase**: Sınıf isimleri
- **UPPER_CASE**: Sabitler ve konfigürasyon

### Klasör İsimlendirme
- **lowercase**: Klasör isimleri
- **descriptive**: Açıklayıcı isimler
- **plural**: Çoklu dosya içeren klasörler

## Version Control

### Git Structure
```
main/                    # Production branch
├── develop/            # Development branch
├── feature/            # Feature branches
└── hotfix/             # Hotfix branches
```

### Commit Messages
- **feat**: Yeni özellik
- **fix**: Hata düzeltmesi
- **docs**: Dokümantasyon
- **style**: Kod formatı
- **refactor**: Kod yeniden düzenleme
- **test**: Test ekleme/düzenleme
- **chore**: Genel bakım

## Dependencies Management

### Requirements Structure
```
requirements.txt        # Production dependencies
requirements-dev.txt    # Development dependencies
requirements-test.txt   # Testing dependencies
```

### Virtual Environment
```
venv/                   # Virtual environment
├── bin/               # Executables
├── lib/               # Libraries
└── include/           # Headers
```

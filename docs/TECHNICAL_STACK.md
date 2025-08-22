# 🛠️ TEKNIK STACK (TECHNICAL STACK)

## Python Libraries

### Data Processing
```python
import pandas as pd          # Veri manipülasyonu ve analizi
import numpy as np           # Sayısal hesaplamalar
from scipy import stats      # İstatistiksel testler
```

### Statistical Analysis
```python
# Core Statistical Libraries
from scipy.stats import ttest_ind, f_oneway, chi2_contingency
from scipy.stats import pearsonr, spearmanr, kendalltau
from scipy.stats import shapiro, normaltest, levene
from scipy.stats import effect_size, power_analysis

# Advanced Statistics
from statsmodels.stats.power import TTestPower, FTestPower
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.diagnostic import het_breuschpagan
```

### Visualization
```python
# Static Plots
import matplotlib.pyplot as plt
import seaborn as sns

# Interactive Plots
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Word Clouds
from wordcloud import WordCloud
```

### Dashboard & Web
```python
import streamlit as st       # Web dashboard
import jinja2               # Template rendering (LaTeX)
```

### Additional Utilities
```python
import warnings             # Warning management
import logging             # Logging system
from typing import Dict, List, Tuple, Optional  # Type hints
import json                # JSON handling
```

## Output Formats

### Graphs & Charts
- **Format**: PNG files
- **Quality**: 300 DPI, publication quality
- **Size**: 12x8 inches (standard)
- **Color Scheme**: Consistent palette

### Tables & Data
- **CSV**: Raw data and processed results
- **LaTeX**: Formatted tables for reports
- **JSON**: Configuration and metadata

### Reports
- **LaTeX**: Scientific report generation
- **PDF**: Final report output
- **HTML**: Interactive dashboard

## Development Environment

### Python Version
- **Python**: 3.8+ (recommended 3.9+)
- **Virtual Environment**: venv or conda

### IDE Requirements
- **Jupyter Notebooks**: Interactive analysis
- **VS Code/Cursor**: Code development
- **Git**: Version control

### Package Management
```bash
# Requirements installation
pip install -r requirements.txt

# Development dependencies
pip install jupyter notebook
pip install black flake8  # Code formatting
```

## Performance Considerations

### Memory Management
- **Chunked Processing**: Large datasets için
- **Data Types**: Memory-efficient dtypes
- **Garbage Collection**: Explicit cleanup

### Computational Optimization
- **Vectorization**: NumPy operations
- **Parallel Processing**: Multiprocessing
- **Caching**: Expensive computations

### Scalability
- **Modular Design**: Reusable components
- **Configuration Files**: Parameter management
- **Logging**: Progress tracking

## Quality Assurance

### Code Quality
```python
# Type Hints
def analyze_salary(df: pd.DataFrame, skill: str) -> Dict[str, float]:
    pass

# Error Handling
try:
    result = process_data(data)
except ValueError as e:
    logger.error(f"Data processing failed: {e}")
    raise

# Documentation
def calculate_salary_percentile(data: np.ndarray, percentile: float) -> float:
    """
    Calculate salary percentile from data array.
    
    Args:
        data: Array of salary values
        percentile: Percentile to calculate (0-100)
        
    Returns:
        float: Calculated percentile value
        
    Raises:
        ValueError: If percentile not in [0, 100]
    """
    pass
```

### Testing Strategy
- **Unit Tests**: Individual functions
- **Integration Tests**: End-to-end workflows
- **Data Validation**: Input/output checks

### Version Control
- **Git Flow**: Feature branches
- **Commit Messages**: Conventional commits
- **Code Review**: Peer review process

## Deployment & Distribution

### Local Development
```bash
# Setup
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Run
python src/main.py
streamlit run dashboard/app.py
```

### Production Ready
- **Docker**: Containerization
- **CI/CD**: Automated testing
- **Monitoring**: Performance tracking

### Documentation
- **README**: Project overview
- **API Docs**: Function documentation
- **User Guide**: Usage instructions

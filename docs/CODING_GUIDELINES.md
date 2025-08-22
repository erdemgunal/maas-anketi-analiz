# ⚡ CURSOR AI AGENT TALIMATLARI (CURSOR AI INSTRUCTIONS)

## Genel Yaklaşım

### Kod Yazım Prensipleri
```
1. Tüm kodları modüler fonksiyonlara böl
2. Her fonksiyon için docstring yaz
3. Error handling ekle
4. Type hints kullan
5. PEP 8 standartlarına uy
```

### Temel Kurallar
- **Single Responsibility**: Her fonksiyon tek bir iş yapmalı
- **DRY (Don't Repeat Yourself)**: Kod tekrarından kaçın
- **KISS (Keep It Simple, Stupid)**: Basit ve anlaşılır kod
- **Clean Code**: Temiz ve okunabilir kod yaz

## Dosya Organizasyonu

### Modül Yapısı
```
1. Her .py dosyası single responsibility principle
2. Import statements alphabetical order
3. Global constants config.py'da
4. All magic numbers as named constants
```

### Import Sıralaması
```python
# 1. Standard library imports
import os
import sys
from typing import Dict, List, Optional

# 2. Third-party imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 3. Local imports
from .config import PRIMARY_COLORS
from .utils import helper_function
```

### Dosya İsimlendirme
- **snake_case**: Python dosyaları (`data_cleaning.py`)
- **PascalCase**: Sınıf isimleri (`SalaryAnalyzer`)
- **UPPER_CASE**: Sabitler (`MAX_ITERATIONS`)

## Kod Kalitesi

### Fonksiyon Yapısı
```python
def analyze_salary_by_skill(df: pd.DataFrame, skill: str) -> Dict[str, float]:
    """
    Analyzes salary differences for developers with/without specific skill.
    
    Args:
        df: Cleaned DataFrame with salary and skill data
        skill: Specific skill to analyze (e.g., 'React', 'TypeScript')
        
    Returns:
        Dict with statistical test results and descriptive stats
        
    Raises:
        ValueError: If skill not found in dataset
        TypeError: If df is not a DataFrame
        
    Example:
        >>> result = analyze_salary_by_skill(df, 'React')
        >>> print(result['mean_difference'])
        15.5
    """
    # Input validation
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    
    if skill not in df.columns:
        raise ValueError(f"Skill '{skill}' not found in dataset")
    
    try:
        # Implementation here
        skill_group = df[df[skill] == 1]['salary']
        no_skill_group = df[df[skill] == 0]['salary']
        
        # Statistical analysis
        t_stat, p_value = stats.ttest_ind(skill_group, no_skill_group)
        
        results = {
            'mean_difference': skill_group.mean() - no_skill_group.mean(),
            't_statistic': t_stat,
            'p_value': p_value,
            'effect_size': calculate_cohens_d(skill_group, no_skill_group)
        }
        
        return results
        
    except Exception as e:
        logger.error(f"Error in analyze_salary_by_skill: {e}")
        raise
```

### Error Handling
```python
def safe_data_processing(data: pd.DataFrame) -> pd.DataFrame:
    """
    Safely process data with comprehensive error handling.
    """
    try:
        # Data validation
        if data.empty:
            raise ValueError("DataFrame is empty")
        
        # Processing steps
        processed_data = data.copy()
        
        # Handle missing values
        if processed_data.isnull().any().any():
            logger.warning("Missing values detected, applying imputation")
            processed_data = handle_missing_values(processed_data)
        
        # Handle outliers
        if detect_outliers(processed_data):
            logger.info("Outliers detected, applying treatment")
            processed_data = handle_outliers(processed_data)
        
        return processed_data
        
    except ValueError as e:
        logger.error(f"Data validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in data processing: {e}")
        raise
```

### Type Hints
```python
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np

def calculate_salary_percentile(
    data: np.ndarray, 
    percentile: float,
    method: str = 'linear'
) -> float:
    """
    Calculate salary percentile from data array.
    
    Args:
        data: Array of salary values
        percentile: Percentile to calculate (0-100)
        method: Interpolation method ('linear', 'lower', 'higher')
        
    Returns:
        float: Calculated percentile value
    """
    pass

def analyze_multiple_skills(
    df: pd.DataFrame,
    skills: List[str],
    confidence_level: float = 0.95
) -> Dict[str, Dict[str, Union[float, str]]]:
    """
    Analyze multiple skills for salary impact.
    
    Returns:
        Nested dictionary with results for each skill
    """
    pass
```

## Konfigürasyon Yönetimi

### Config Dosyası Yapısı
```python
# config.py
from typing import Dict, List

# Data processing constants
DATA_CONFIG = {
    'missing_threshold': 0.05,  # 5% missing data threshold
    'outlier_method': 'iqr',    # IQR method for outlier detection
    'salary_range_mapping': {
        '61 - 70': 65,
        '71 - 80': 75,
        # ... more mappings
    }
}

# Model parameters
MODEL_CONFIG = {
    'random_state': 42,
    'test_size': 0.2,
    'cv_folds': 5,
    'n_estimators': 100
}

# Visualization settings
VISUAL_CONFIG = {
    'figure_size': (12, 8),
    'dpi': 300,
    'color_palette': ['#2E86AB', '#F24236', '#A23B72']
}
```

### Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment
API_KEY = os.getenv('API_KEY')
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
```

## Logging ve Debugging

### Logging Setup
```python
import logging
from typing import Optional

def setup_logging(
    level: str = 'INFO',
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Setup logging configuration.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Usage
logger = setup_logging('DEBUG', 'analysis.log')
```

### Debugging Tools
```python
import pdb
from typing import Any

def debug_function(func):
    """
    Decorator for debugging functions.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            pdb.set_trace()
            raise
    return wrapper

@debug_function
def complex_analysis(data: pd.DataFrame) -> Dict[str, Any]:
    # Function implementation
    pass
```

## Test Yazımı

### Unit Test Örneği
```python
import unittest
import pandas as pd
import numpy as np
from src.data_cleaning import clean_salary_data

class TestDataCleaning(unittest.TestCase):
    """Test cases for data cleaning functions."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_data = pd.DataFrame({
            'salary': ['61 - 70', '71 - 80', '81 - 90'],
            'experience': ['1-3', '4-6', '7-10']
        })
    
    def test_salary_normalization(self):
        """Test salary range normalization."""
        result = clean_salary_data(self.sample_data)
        
        # Assertions
        self.assertIsInstance(result['salary_numeric'], pd.Series)
        self.assertEqual(result['salary_numeric'].iloc[0], 65)
        self.assertFalse(result['salary_numeric'].isnull().any())
    
    def test_invalid_salary_format(self):
        """Test handling of invalid salary formats."""
        invalid_data = pd.DataFrame({
            'salary': ['invalid', '61 - 70', '71 - 80']
        })
        
        with self.assertRaises(ValueError):
            clean_salary_data(invalid_data)

if __name__ == '__main__':
    unittest.main()
```

## Performance Optimization

### Memory Management
```python
def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize DataFrame memory usage.
    """
    # Downcast numeric columns
    for col in df.select_dtypes(include=['int64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    # Convert object columns to category if beneficial
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique values
            df[col] = df[col].astype('category')
    
    return df
```

### Caching
```python
from functools import lru_cache
import pickle
import os

@lru_cache(maxsize=128)
def expensive_calculation(data_hash: str) -> Dict[str, float]:
    """
    Cache expensive calculations.
    """
    # Implementation
    pass

def save_results(results: Dict, filename: str):
    """Save results to file."""
    with open(filename, 'wb') as f:
        pickle.dump(results, f)

def load_results(filename: str) -> Dict:
    """Load results from file."""
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return None
```

## Documentation Standards

### Docstring Format
```python
def complex_analysis_function(
    data: pd.DataFrame,
    parameters: Dict[str, Any],
    output_format: str = 'json'
) -> Union[Dict, str]:
    """
    Perform complex analysis on salary data.
    
    This function performs a comprehensive analysis of salary data including
    statistical tests, machine learning models, and visualization generation.
    
    Args:
        data: Input DataFrame containing salary and demographic data
        parameters: Dictionary containing analysis parameters
        output_format: Output format ('json', 'csv', 'excel')
        
    Returns:
        Analysis results in specified format
        
    Raises:
        ValueError: If data is empty or parameters are invalid
        TypeError: If data is not a DataFrame
        
    Example:
        >>> params = {'confidence_level': 0.95, 'test_type': 't-test'}
        >>> results = complex_analysis_function(df, params, 'json')
        >>> print(results['summary'])
        
    Notes:
        - Function requires at least 100 data points
        - Processing time scales with data size
        - Results are cached for performance
    """
    pass
```

### Code Comments
```python
# Good comments
def calculate_bonus(salary: float, performance_score: float) -> float:
    """
    Calculate bonus based on salary and performance.
    """
    # Base bonus is 10% of salary
    base_bonus = salary * 0.10
    
    # Performance multiplier: 0.5x to 2.0x
    performance_multiplier = 0.5 + (performance_score * 1.5)
    
    # Apply performance multiplier to base bonus
    final_bonus = base_bonus * performance_multiplier
    
    return final_bonus

# Bad comments
def calculate_bonus(salary, performance_score):
    # Calculate bonus
    base_bonus = salary * 0.10  # Multiply salary by 0.10
    performance_multiplier = 0.5 + (performance_score * 1.5)  # Calculate multiplier
    final_bonus = base_bonus * performance_multiplier  # Calculate final bonus
    return final_bonus  # Return final bonus
```

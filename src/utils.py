"""
Ortak Kullanılan Fonksiyonlar Modülü

Bu modül, tüm analiz sınıflarında ortak olan fonksiyonları içerir:
- Veri yükleme fonksiyonları
- Yardımcı fonksiyonlar
- Ortak sabitler ve ayarlar

Yazar: Erdem Gunal
Tarih: 2024-08-24
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ortak sabitler
CAREER_LEVELS = {1: 'Junior', 2: 'Mid', 3: 'Senior', 4: 'Lead', 5: 'Manager'}
WORK_TYPES = {0: 'Remote', 1: 'Office', 2: 'Hybrid'}
GENDER_MAPPING = {0: 'Erkek', 1: 'Kadın'}

# Viridis renk paleti
VIRIDIS_COLORS = {
    'primary': '#440154',      # Koyu mor
    'secondary': '#31688E',    # Mavi
    'tertiary': '#35B779',     # Yeşil
    'quaternary': '#FDE725'    # Sarı
}

# Kategorik renkler
CATEGORICAL_COLORS = {
    'react_users': VIRIDIS_COLORS['primary'],
    'non_react_users': VIRIDIS_COLORS['tertiary'],
    'male': VIRIDIS_COLORS['secondary'],
    'female': VIRIDIS_COLORS['quaternary'],
    'remote': VIRIDIS_COLORS['primary'],
    'office': VIRIDIS_COLORS['secondary'],
    'hybrid': VIRIDIS_COLORS['tertiary']
}

# Dil isimlerini düzeltme sözlüğü
LANG_NAME_MAPPING = {
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


def load_data(data_path: str = "data/cleaned_data.csv") -> pd.DataFrame:
    """
    Veriyi yükle ve temel kontrolleri yap
    
    Args:
        data_path (str): Veri dosyasının yolu
        
    Returns:
        pd.DataFrame: Yüklenen veri
    """
    try:
        logger.info(f"Veri yükleniyor: {data_path}")
        df = pd.read_csv(data_path)
        logger.info(f"Veri başarıyla yüklendi. Boyut: {df.shape}")
        return df
    except FileNotFoundError:
        logger.error(f"Dosya bulunamadı: {data_path}")
        raise
    except Exception as e:
        logger.error(f"Veri yükleme hatası: {e}")
        raise


def get_career_level_name(level: int) -> str:
    """Kariyer seviyesi numarasını isme çevir"""
    return CAREER_LEVELS.get(level, f'Seviye {level}')


def get_work_type_name(work_type: int) -> str:
    """Çalışma şekli numarasını isme çevir"""
    return WORK_TYPES.get(work_type, f'Tip {work_type}')


def get_gender_name(gender: int) -> str:
    """Cinsiyet numarasını isme çevir"""
    return GENDER_MAPPING.get(gender, f'Cinsiyet {gender}')


def fix_language_name(lang_key: str) -> str:
    """Programlama dili ismini düzelt"""
    if lang_key in LANG_NAME_MAPPING:
        return LANG_NAME_MAPPING[lang_key]
    else:
        return lang_key.replace('_', ' ').title()


def get_location_name(location_col: str) -> str:
    """Lokasyon sütun adını düzelt"""
    return location_col.replace('location_', '').replace('_', ' ').title()


def interpret_cohens_d(cohens_d: float) -> str:
    """Cohen's d etki büyüklüğünü yorumla"""
    if abs(cohens_d) < 0.2:
        return "Küçük"
    elif abs(cohens_d) < 0.5:
        return "Orta"
    elif abs(cohens_d) < 0.8:
        return "Büyük"
    else:
        return "Çok Büyük"


def interpret_eta_squared(eta_squared: float) -> str:
    """Eta-squared etki büyüklüğünü yorumla"""
    if eta_squared < 0.01:
        return "Küçük"
    elif eta_squared < 0.06:
        return "Orta"
    elif eta_squared < 0.14:
        return "Büyük"
    else:
        return "Çok Büyük"


def interpret_correlation(r: float) -> str:
    """Korelasyon katsayısını yorumla"""
    if abs(r) < 0.1:
        return "Zayıf"
    elif abs(r) < 0.3:
        return "Düşük"
    elif abs(r) < 0.5:
        return "Orta"
    elif abs(r) < 0.7:
        return "Yüksek"
    else:
        return "Çok Yüksek"


def save_results_to_csv(results: List[Dict], output_path: str) -> None:
    """
    Sonuçları CSV dosyasına kaydet
    
    Args:
        results (List[Dict]): Kaydedilecek sonuçlar
        output_path (str): Çıktı dosyasının yolu
    """
    try:
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df = pd.DataFrame(results)
        df.to_csv(output_path, index=False)
        logger.info(f"Sonuçlar kaydedildi: {output_path}")
    except Exception as e:
        logger.error(f"Sonuç kaydetme hatası: {e}")
        raise


def setup_matplotlib_style():
    """Matplotlib stil ayarlarını yapılandır"""
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    plt.style.use('seaborn-v0_8')
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['savefig.format'] = 'png'
    
    # Font ayarları
    plt.rcParams['font.family'] = ['Arial', 'DejaVu Sans', 'sans-serif']
    plt.rcParams['font.size'] = 16
    plt.rcParams['axes.titlesize'] = 20
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.rcParams['legend.fontsize'] = 16
    
    # Renk paleti
    sns.set_palette("viridis")


def get_programming_language_usage(df: pd.DataFrame, min_usage_rate: float = 5.0) -> Dict[str, float]:
    """
    Programlama dili kullanım oranlarını hesapla
    
    Args:
        df (pd.DataFrame): Veri seti
        min_usage_rate (float): Minimum kullanım oranı (%)
        
    Returns:
        Dict[str, float]: Dil adı ve kullanım oranı
    """
    prog_lang_cols = [col for col in df.columns if col.startswith('prog_lang_')]
    lang_usage = {}
    
    for col in prog_lang_cols:
        lang_key = col.replace('prog_lang_', '')
        usage_rate = (df[col].sum() / len(df)) * 100
        
        if usage_rate > min_usage_rate:
            lang_name = fix_language_name(lang_key)
            if lang_name != 'Hiçbiri':
                lang_usage[lang_name] = usage_rate
    
    return lang_usage


def get_location_data(df: pd.DataFrame) -> List[Dict]:
    """
    Lokasyon verilerini hazırla
    
    Args:
        df (pd.DataFrame): Veri seti
        
    Returns:
        List[Dict]: Lokasyon verileri
    """
    location_cols = [col for col in df.columns if col.startswith('location_')]
    location_data = []
    
    for col in location_cols:
        location_name = get_location_name(col)
        location_salary = df[df[col] == 1]['ortalama_maas']
        
        if len(location_salary) > 0:
            location_data.append({
                'Lokasyon': location_name,
                'Ortalama Maaş': location_salary.mean(),
                'Katılımcı Sayısı': len(location_salary)
            })
    
    return location_data


def get_career_data(df: pd.DataFrame) -> List[Dict]:
    """
    Kariyer seviyesi verilerini hazırla
    
    Args:
        df (pd.DataFrame): Veri seti
        
    Returns:
        List[Dict]: Kariyer verileri
    """
    career_data = []
    
    for level, name in CAREER_LEVELS.items():
        career_salary = df[df['kariyer_seviyesi'] == level]['ortalama_maas']
        if len(career_salary) > 0:
            career_data.append({
                'Kariyer Seviyesi': name,
                'Ortalama Maaş': career_salary.mean(),
                'Katılımcı Sayısı': len(career_salary)
            })
    
    return career_data


def get_work_type_data(df: pd.DataFrame) -> List[Dict]:
    """
    Çalışma şekli verilerini hazırla
    
    Args:
        df (pd.DataFrame): Veri seti
        
    Returns:
        List[Dict]: Çalışma şekli verileri
    """
    work_data = []
    
    for work_val, work_name in WORK_TYPES.items():
        work_salary = df[df['calisma_sekli'] == work_val]['ortalama_maas']
        if len(work_salary) > 0:
            work_data.append({
                'Çalışma Şekli': work_name,
                'Ortalama Maaş': work_salary.mean(),
                'Katılımcı Sayısı': len(work_salary)
            })
    
    return work_data


def get_gender_data(df: pd.DataFrame) -> List[Dict]:
    """
    Cinsiyet verilerini hazırla
    
    Args:
        df (pd.DataFrame): Veri seti
        
    Returns:
        List[Dict]: Cinsiyet verileri
    """
    gender_data = []
    
    for gender_val, gender_name in GENDER_MAPPING.items():
        gender_salary = df[df['cinsiyet'] == gender_val]['ortalama_maas']
        if len(gender_salary) > 0:
            gender_data.append({
                'Cinsiyet': gender_name,
                'Ortalama Maaş': gender_salary.mean(),
                'Katılımcı Sayısı': len(gender_salary)
            })
    
    return gender_data

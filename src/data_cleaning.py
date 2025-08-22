"""
Veri Temizleme ve Ön İşleme Modülü

Bu modül, maaş anketi verisinin temizlenmesi ve ön işlenmesi için gerekli
fonksiyonları içerir.

Fonksiyonlar:
- load_and_explore_data: Veri yükleme ve keşifsel analiz
- normalize_salary_ranges: Maaş aralıklarını sayısal değerlere çevirme
- parse_technologies: Teknoloji sütunlarını ayrıştırma
- handle_missing_values: Eksik veri işleme
- detect_outliers: Aykırı değer tespiti
- clean_data: Ana temizleme fonksiyonu
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, List, Tuple, Optional
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_and_explore_data(file_path: str = '../maas_anketi.csv') -> pd.DataFrame:
    """
    CSV dosyasını yükler ve temel keşifsel analiz yapar.
    
    Args:
        file_path: CSV dosya yolu
        
    Returns:
        pd.DataFrame: Yüklenen veri seti
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Veri başarıyla yüklendi. Boyut: {df.shape}")
        
        # Temel bilgileri logla
        logger.info(f"Satır sayısı: {df.shape[0]}")
        logger.info(f"Sütun sayısı: {df.shape[1]}")
        logger.info(f"Eksik veri oranı: {df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100:.2f}%")
        
        return df
    
    except FileNotFoundError:
        logger.error(f"Dosya bulunamadı: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Veri yükleme hatası: {e}")
        raise


def normalize_salary_ranges(df: pd.DataFrame, salary_column: str = 'Aylık ortalama net kaç bin TL alıyorsun?') -> pd.DataFrame:
    """
    Maaş aralıklarını sayısal ortalamaya çevirir.
    
    Args:
        df: Veri seti
        salary_column: Maaş sütunu adı
        
    Returns:
        pd.DataFrame: Maaş sütunu normalize edilmiş veri seti
    """
    df_clean = df.copy()
    
    # Maaş aralıklarını sayısal değerlere çevir
    def extract_salary_average(salary_str: str) -> float:
        if pd.isna(salary_str):
            return np.nan
        
        # Sayıları çıkar
        numbers = re.findall(r'\d+', str(salary_str))
        
        if len(numbers) >= 2:
            # İlk iki sayıyı al (başlangıç ve bitiş)
            start, end = int(numbers[0]), int(numbers[1])
            return (start + end) / 2
        elif len(numbers) == 1:
            # Tek sayı varsa o değeri kullan
            return float(numbers[0])
        else:
            return np.nan
    
    # Yeni sütun oluştur
    df_clean['salary_normalized'] = df_clean[salary_column].apply(extract_salary_average)
    
    # Orijinal sütunu koru, yeni sütunu ekle
    logger.info(f"Maaş normalizasyonu tamamlandı. Benzersiz değer sayısı: {df_clean['salary_normalized'].nunique()}")
    
    return df_clean


def parse_technologies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Teknoloji sütunlarını ayrıştırır ve binary değişkenler oluşturur.
    
    Args:
        df: Veri seti
        
    Returns:
        pd.DataFrame: Teknoloji sütunları ayrıştırılmış veri seti
    """
    df_clean = df.copy()
    
    # Teknoloji sütunları
    tech_columns = [
        'Hangi programlama dillerini kullanıyorsun',
        'Frontend yazıyorsan hangilerini kullanıyorsun',
        'Hangi tool\'ları kullanıyorsun'
    ]
    
    # Her teknoloji sütunu için ayrıştırma
    for col in tech_columns:
        if col in df_clean.columns:
            # Virgülle ayrılmış teknolojileri ayrıştır
            tech_list = []
            for value in df_clean[col].dropna():
                if isinstance(value, str):
                    # Virgül, noktalı virgül veya 've' ile ayrılmış değerleri al
                    techs = re.split(r'[,;]|\s+ve\s+', value)
                    tech_list.extend([tech.strip() for tech in techs if tech.strip()])
            
            # Benzersiz teknolojileri al
            unique_techs = list(set(tech_list))
            logger.info(f"{col} için {len(unique_techs)} benzersiz teknoloji bulundu")
            
            # Her teknoloji için binary sütun oluştur
            for tech in unique_techs:
                if tech:  # Boş string değilse
                    column_name = f"{col.split()[0]}_{tech.replace(' ', '_').replace('/', '_')}"
                    df_clean[column_name] = df_clean[col].str.contains(tech, case=False, na=False).astype(int)
    
    return df_clean


def handle_missing_values(df: pd.DataFrame, max_missing_threshold: float = 0.05) -> pd.DataFrame:
    """
    Eksik verileri işler.
    
    Args:
        df: Veri seti
        max_missing_threshold: Maksimum eksik veri oranı (varsayılan: %5)
        
    Returns:
        pd.DataFrame: Eksik veriler işlenmiş veri seti
    """
    df_clean = df.copy()
    
    # Eksik veri oranlarını hesapla
    missing_ratios = df_clean.isnull().sum() / len(df_clean)
    
    logger.info("Eksik veri analizi:")
    for col, ratio in missing_ratios.items():
        if ratio > 0:
            logger.info(f"  {col}: {ratio:.3f} ({ratio*100:.1f}%)")
    
    # Yüksek eksik veri oranına sahip sütunları kaldır
    columns_to_drop = missing_ratios[missing_ratios > max_missing_threshold].index
    if len(columns_to_drop) > 0:
        logger.info(f"Yüksek eksik veri oranına sahip sütunlar kaldırılıyor: {list(columns_to_drop)}")
        df_clean = df_clean.drop(columns=columns_to_drop)
    
    # Kategorik sütunlar için mode ile doldur
    categorical_columns = df_clean.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        if df_clean[col].isnull().sum() > 0:
            mode_value = df_clean[col].mode().iloc[0] if not df_clean[col].mode().empty else 'Unknown'
            df_clean[col] = df_clean[col].fillna(mode_value)
            logger.info(f"{col} sütunu mode ile dolduruldu")
    
    # Sayısal sütunlar için median ile doldur
    numerical_columns = df_clean.select_dtypes(include=[np.number]).columns
    for col in numerical_columns:
        if df_clean[col].isnull().sum() > 0:
            median_value = df_clean[col].median()
            df_clean[col] = df_clean[col].fillna(median_value)
            logger.info(f"{col} sütunu median ile dolduruldu")
    
    return df_clean


def detect_outliers(df: pd.DataFrame, salary_column: str = 'salary_normalized', 
                   method: str = 'iqr', threshold: float = 1.5) -> Tuple[pd.DataFrame, List[int]]:
    """
    Aykırı değerleri tespit eder.
    
    Args:
        df: Veri seti
        salary_column: Maaş sütunu adı
        method: Tespit yöntemi ('iqr' veya 'zscore')
        threshold: Eşik değeri
        
    Returns:
        Tuple[pd.DataFrame, List[int]]: Temizlenmiş veri seti ve aykırı değer indeksleri
    """
    df_clean = df.copy()
    
    if salary_column not in df_clean.columns:
        logger.warning(f"Maaş sütunu bulunamadı: {salary_column}")
        return df_clean, []
    
    if method == 'iqr':
        # IQR yöntemi
        Q1 = df_clean[salary_column].quantile(0.25)
        Q3 = df_clean[salary_column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        outliers = df_clean[(df_clean[salary_column] < lower_bound) | 
                           (df_clean[salary_column] > upper_bound)]
        
    elif method == 'zscore':
        # Z-score yöntemi
        z_scores = np.abs((df_clean[salary_column] - df_clean[salary_column].mean()) / 
                         df_clean[salary_column].std())
        outliers = df_clean[z_scores > threshold]
    
    else:
        logger.error(f"Geçersiz yöntem: {method}")
        return df_clean, []
    
    outlier_indices = outliers.index.tolist()
    logger.info(f"Aykırı değer sayısı: {len(outlier_indices)} ({len(outlier_indices)/len(df_clean)*100:.2f}%)")
    
    # Aykırı değerleri kaldır
    df_clean = df_clean.drop(outlier_indices)
    
    return df_clean, outlier_indices


def encode_categorical_variables(df: pd.DataFrame) -> pd.DataFrame:
    """
    Kategorik değişkenleri kodlar.
    
    Args:
        df: Veri seti
        
    Returns:
        pd.DataFrame: Kategorik değişkenler kodlanmış veri seti
    """
    df_clean = df.copy()
    
    # Kategorik sütunları belirle
    categorical_columns = df_clean.select_dtypes(include=['object']).columns
    
    # Label encoding uygula
    for col in categorical_columns:
        if col not in ['Timestamp']:  # Timestamp'i atla
            df_clean[col] = pd.Categorical(df_clean[col]).codes
            logger.info(f"{col} sütunu label encoding ile kodlandı")
    
    return df_clean


def clean_data(file_path: str = '../maas_anketi.csv', 
               save_cleaned: bool = True,
               output_path: str = '../data/cleaned_data.csv') -> pd.DataFrame:
    """
    Ana veri temizleme fonksiyonu.
    
    Args:
        file_path: Ham veri dosya yolu
        save_cleaned: Temizlenmiş veriyi kaydet
        output_path: Temizlenmiş veri kayıt yolu
        
    Returns:
        pd.DataFrame: Temizlenmiş veri seti
    """
    logger.info("Veri temizleme süreci başlatılıyor...")
    
    # 1. Veriyi yükle
    df = load_and_explore_data(file_path)
    
    # 2. Maaş normalizasyonu
    df = normalize_salary_ranges(df)
    
    # 3. Teknoloji ayrıştırma
    df = parse_technologies(df)
    
    # 4. Eksik veri işleme
    df = handle_missing_values(df)
    
    # 5. Aykırı değer tespiti ve temizleme
    df, outliers = detect_outliers(df)
    
    # 6. Kategorik değişken kodlama
    df = encode_categorical_variables(df)
    
    # 7. Temizlenmiş veriyi kaydet
    if save_cleaned:
        df.to_csv(output_path, index=False)
        logger.info(f"Temizlenmiş veri kaydedildi: {output_path}")
    
    logger.info(f"Veri temizleme tamamlandı. Final boyut: {df.shape}")
    
    return df


if __name__ == "__main__":
    # Test çalıştırması
    cleaned_df = clean_data()
    print(f"Temizlenmiş veri boyutu: {cleaned_df.shape}")
    print(f"Temizlenmiş veri sütunları: {list(cleaned_df.columns)}")

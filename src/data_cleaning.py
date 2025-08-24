"""
Veri Temizleme ve Özellik Mühendisliği Modülü

Bu modül, maas_anket.csv verisini temizleyerek analiz edilebilir formata dönüştürür.
Sprint 1: Veri Hazırlama kapsamında geliştirilmiştir.

Author: Erdem Gunal
Date: 2024
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataCleaner:
    """
    Veri temizleme ve özellik mühendisliği için ana sınıf.
    """
    
    def __init__(self, data_path: str = "data/maas_anket.csv"):
        """
        DataCleaner sınıfını başlatır.
        
        Args:
            data_path (str): Ham veri dosyasının yolu
        """
        self.data_path = data_path
        self.df = None
        self.cleaned_df = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Ham veriyi yükler ve genel yapısını inceler.
        
        Returns:
            pd.DataFrame: Yüklenen veri seti
        """
        logger.info(f"Veri yükleniyor: {self.data_path}")
        
        try:
            self.df = pd.read_csv(self.data_path)
            logger.info(f"Veri başarıyla yüklendi. Boyut: {self.df.shape}")
            
            # Genel bilgileri logla
            logger.info(f"Veri seti boyutu: {self.df.shape[0]} satır, {self.df.shape[1]} sütun")
            logger.info(f"Eksik değer sayısı: {self.df.isnull().sum().sum()}")
            
            return self.df
            
        except FileNotFoundError:
            logger.error(f"Dosya bulunamadı: {self.data_path}")
            raise
        except Exception as e:
            logger.error(f"Veri yükleme hatası: {str(e)}")
            raise
    
    def explore_data(self) -> Dict:
        """
        Veri setinin genel yapısını inceler ve özet bilgileri döndürür.
        
        Returns:
            Dict: Veri keşif özeti
        """
        if self.df is None:
            raise ValueError("Önce veriyi yükleyin (load_data)")
        
        exploration_summary = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'missing_percentage': (self.df.isnull().sum() / len(self.df) * 100).to_dict(),
            'numeric_columns': self.df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': self.df.select_dtypes(include=['object']).columns.tolist()
        }
        
        logger.info("Veri keşif özeti:")
        logger.info(f"Toplam satır: {exploration_summary['shape'][0]}")
        logger.info(f"Toplam sütun: {exploration_summary['shape'][1]}")
        logger.info(f"Sayısal sütunlar: {len(exploration_summary['numeric_columns'])}")
        logger.info(f"Kategorik sütunlar: {len(exploration_summary['categorical_columns'])}")
        
        return exploration_summary
    
    def normalize_salary_data(self) -> pd.Series:
        """
        Maaş verilerini normalleştirir ve sayısal değerlere dönüştürür.
        
        Returns:
            pd.Series: Normalleştirilmiş maaş sütunu
        """
        if self.df is None:
            raise ValueError("Önce veriyi yükleyin (load_data)")
        
        salary_column = 'Aylık ortalama net kaç bin TL alıyorsun?'
        
        if salary_column not in self.df.columns:
            raise ValueError(f"Maaş sütunu bulunamadı: {salary_column}")
        
        logger.info("Maaş verileri normalleştiriliyor...")
        
        def extract_salary_value(salary_str: str) -> float:
            """Maaş aralığından ortalama değeri çıkarır."""
            if pd.isna(salary_str):
                return np.nan
            
            salary_str = str(salary_str).strip()
            
            # "300 +" gibi açık uçlu aralıklar için
            if "300 +" in salary_str or "300+" in salary_str:
                return 305.0  # Ortalama + standart sapma yaklaşımı
            
            # Aralık formatı: "0 - 10", "101 - 110" vb.
            if " - " in salary_str:
                try:
                    parts = salary_str.split(" - ")
                    if len(parts) == 2:
                        start = float(parts[0].strip())
                        end = float(parts[1].strip())
                        return (start + end) / 2
                except ValueError:
                    logger.warning(f"Geçersiz maaş formatı: {salary_str}")
                    return np.nan
            
            # Tek değer formatı
            try:
                return float(salary_str)
            except ValueError:
                logger.warning(f"Geçersiz maaş değeri: {salary_str}")
                return np.nan
        
        normalized_salary = self.df[salary_column].apply(extract_salary_value)
        
        logger.info(f"Maaş normalleştirme tamamlandı. Ortalama: {normalized_salary.mean():.2f}")
        logger.info(f"Geçerli maaş değeri sayısı: {normalized_salary.notna().sum()}")
        
        return normalized_salary
    
    def create_one_hot_encodings(self, columns: List[str]) -> pd.DataFrame:
        """
        Belirtilen sütunlardaki virgülle ayrılmış değerleri one-hot encoding'e dönüştürür.
        
        Args:
            columns (List[str]): İşlenecek sütun isimleri
            
        Returns:
            pd.DataFrame: One-hot encoding sonuçları
        """
        if self.df is None:
            raise ValueError("Önce veriyi yükleyin (load_data)")
        
        logger.info(f"One-hot encoding başlatılıyor: {columns}")
        
        one_hot_data = {}
        
        # Sütun ismi kısaltmaları
        column_shortcuts = {
            'Hangi programlama dillerini kullanıyorsun': 'prog_lang',
            'Ne yapıyorsun?': 'role',
            'Frontend yazıyorsan hangilerini kullanıyorsun': 'frontend',
            'Hangi tool\'ları kullanıyorsun': 'tools'
        }
        
        for column in columns:
            if column not in self.df.columns:
                logger.warning(f"Sütun bulunamadı: {column}")
                continue
            
            logger.info(f"İşleniyor: {column}")
            
            # Kısaltma kullan
            shortcut = column_shortcuts.get(column, column.lower().replace(' ', '_'))
            
            # Tüm benzersiz değerleri topla
            all_values = set()
            for value in self.df[column].dropna():
                if isinstance(value, str):
                    # Virgülle ayrılmış değerleri böl
                    values = [v.strip() for v in value.split(',')]
                    all_values.update(values)
            
            # Her değer için binary sütun oluştur
            for unique_value in sorted(all_values):
                # Değer ismini de kısalt
                value_short = unique_value.lower().replace(' ', '_').replace('/', '_')
                column_name = f"{shortcut}_{value_short}"
                
                # Her satır için o değerin var olup olmadığını kontrol et
                one_hot_data[column_name] = self.df[column].apply(
                    lambda x: 1 if pd.notna(x) and unique_value in str(x) else 0
                )
        
        result_df = pd.DataFrame(one_hot_data)
        logger.info(f"One-hot encoding tamamlandı. {len(result_df.columns)} yeni sütun oluşturuldu.")
        
        return result_df
    
    def standardize_categorical_variables(self) -> pd.DataFrame:
        """
        Kategorik değişkenleri standartlaştırır ve kodlar.
        
        Returns:
            pd.DataFrame: Standartlaştırılmış kategorik değişkenler
        """
        if self.df is None:
            raise ValueError("Önce veriyi yükleyin (load_data)")
        
        logger.info("Kategorik değişkenler standartlaştırılıyor...")
        
        standardized_data = {}
        
        # Şirket lokasyonu standartlaştırma
        if 'Şirket lokasyon' in self.df.columns:
            location_mapping = {
                'Amerika': 'Amerika',
                'Türkiye': 'Türkiye',
                'Avrupa': 'Avrupa',
                'Yurtdışı TR hub': 'Yurtdışı TR Hub'
            }
            
            standardized_data['sirket_lokasyon'] = self.df['Şirket lokasyon'].map(
                lambda x: location_mapping.get(x, 'Diğer') if pd.notna(x) else 'Diğer'
            )
        
        # Deneyim yılı dönüştürme
        if 'Toplam kaç yıllık iş deneyimin var?' in self.df.columns:
            def extract_experience_years(exp_str: str) -> float:
                if pd.isna(exp_str):
                    return np.nan
                
                exp_str = str(exp_str).strip()
                
                # "5-10 yıl" formatı
                if "-" in exp_str and "yıl" in exp_str:
                    try:
                        parts = exp_str.split("-")
                        start = float(parts[0].strip())
                        end = float(parts[1].split("yıl")[0].strip())
                        return (start + end) / 2
                    except:
                        return np.nan
                
                # "5 yıl" formatı
                if "yıl" in exp_str:
                    try:
                        return float(exp_str.split("yıl")[0].strip())
                    except:
                        return np.nan
                
                # Sayısal değer
                try:
                    return float(exp_str)
                except:
                    return np.nan
            
            standardized_data['deneyim_yili'] = self.df['Toplam kaç yıllık iş deneyimin var?'].apply(
                extract_experience_years
            )
        
        # Kariyer seviyesi kodlama
        if 'Hangi seviyedesin?' in self.df.columns:
            level_mapping = {
                'Junior': 1,
                'Mid': 2,
                'Senior': 3,
                'Lead': 4,
                'Manager': 5
            }
            
            standardized_data['kariyer_seviyesi'] = self.df['Hangi seviyedesin?'].map(
                lambda x: level_mapping.get(x, 1) if pd.notna(x) else 1
            )
        
        # Cinsiyet kodlama
        if 'Cinsiyet' in self.df.columns:
            gender_mapping = {'Erkek': 0, 'Kadın': 1}
            standardized_data['cinsiyet'] = self.df['Cinsiyet'].map(
                lambda x: gender_mapping.get(x, 0) if pd.notna(x) else 0
            )
        
        # Çalışma şekli kodlama
        if 'Çalışma şekli' in self.df.columns:
            work_type_mapping = {'Remote': 0, 'Office': 1, 'Hybrid': 2}
            standardized_data['calisma_sekli'] = self.df['Çalışma şekli'].map(
                lambda x: work_type_mapping.get(x, 0) if pd.notna(x) else 0
            )
        
        result_df = pd.DataFrame(standardized_data)
        logger.info(f"Kategorik değişkenler standartlaştırıldı. {len(result_df.columns)} sütun oluşturuldu.")
        
        return result_df
    
    def handle_missing_values(self, df: pd.DataFrame, threshold: float = 0.05) -> pd.DataFrame:
        """
        Eksik değerleri yönetir.
        
        Args:
            df (pd.DataFrame): İşlenecek veri seti
            threshold (float): Eksik değer oranı eşiği
            
        Returns:
            pd.DataFrame: Eksik değerleri yönetilmiş veri seti
        """
        logger.info("Eksik değerler yönetiliyor...")
        
        # Eksik değer oranlarını hesapla
        missing_ratios = df.isnull().sum() / len(df)
        
        # Yüksek eksik değer oranına sahip sütunları kaldır
        columns_to_drop = missing_ratios[missing_ratios > threshold].index.tolist()
        if columns_to_drop:
            logger.info(f"Yüksek eksik değer oranına sahip sütunlar kaldırılıyor: {columns_to_drop}")
            df = df.drop(columns=columns_to_drop)
        
        # Kalan eksik değerleri doldur
        for column in df.columns:
            if df[column].isnull().sum() > 0:
                if df[column].dtype in ['int64', 'float64']:
                    # Sayısal sütunlar için medyan
                    median_value = df[column].median()
                    df[column] = df[column].fillna(median_value)
                    logger.info(f"{column}: Medyan ile dolduruldu ({median_value})")
                else:
                    # Kategorik sütunlar için mod
                    mode_value = df[column].mode().iloc[0] if not df[column].mode().empty else 'Bilinmiyor'
                    df[column] = df[column].fillna(mode_value)
                    logger.info(f"{column}: Mod ile dolduruldu ({mode_value})")
        
        logger.info("Eksik değer yönetimi tamamlandı.")
        return df
    
    def detect_outliers(self, df: pd.DataFrame, column: str, method: str = 'iqr') -> Tuple[pd.Series, Dict]:
        """
        Aykırı değerleri tespit eder.
        
        Args:
            df (pd.DataFrame): Veri seti
            column (str): İncelenecek sütun
            method (str): Tespit yöntemi ('iqr' veya 'zscore')
            
        Returns:
            Tuple[pd.Series, Dict]: Aykırı değer maskesi ve istatistikler
        """
        if method == 'iqr':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
            
            stats = {
                'Q1': Q1,
                'Q3': Q3,
                'IQR': IQR,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'outlier_count': outliers.sum(),
                'outlier_percentage': (outliers.sum() / len(df)) * 100
            }
            
        elif method == 'zscore':
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            outliers = z_scores > 3
            
            stats = {
                'mean': df[column].mean(),
                'std': df[column].std(),
                'outlier_count': outliers.sum(),
                'outlier_percentage': (outliers.sum() / len(df)) * 100
            }
        
        logger.info(f"Aykırı değer analizi - {column}: {stats['outlier_count']} aykırı değer (%{stats['outlier_percentage']:.2f})")
        
        return outliers, stats
    
    def clean_data(self) -> pd.DataFrame:
        """
        Tüm veri temizleme adımlarını gerçekleştirir.
        
        Returns:
            pd.DataFrame: Temizlenmiş veri seti
        """
        logger.info("Veri temizleme süreci başlatılıyor...")
        
        # 1. Veriyi yükle
        self.load_data()
        
        # 2. Maaş verilerini normalleştir
        normalized_salary = self.normalize_salary_data()
        
        # 3. One-hot encoding oluştur
        one_hot_columns = [
            'Hangi programlama dillerini kullanıyorsun',
            'Ne yapıyorsun?',
            'Frontend yazıyorsan hangilerini kullanıyorsun',
            'Hangi tool\'ları kullanıyorsun'
        ]
        one_hot_data = self.create_one_hot_encodings(one_hot_columns)
        
        # 4. Kategorik değişkenleri standartlaştır
        categorical_data = self.standardize_categorical_variables()
        
        # 5. Tüm verileri birleştir
        cleaned_data = pd.concat([
            self.df,
            normalized_salary.rename('ortalama_maas'),
            one_hot_data,
            categorical_data
        ], axis=1)
        
        # 5.1. Orijinal sütunları kaldır (işlenmiş versiyonları var)
        columns_to_drop = [
            'Şirket lokasyon',  # sirket_lokasyon var
            'Toplam kaç yıllık iş deneyimin var?',  # deneyim_yili var (eğer varsa)
            'Hangi seviyedesin?',  # kariyer_seviyesi var
            'Cinsiyet',  # cinsiyet var
            'Çalışma şekli',  # calisma_sekli var
            'Hangi programlama dillerini kullanıyorsun',  # one-hot encoding var
            'Ne yapıyorsun?',  # one-hot encoding var
            'Frontend yazıyorsan hangilerini kullanıyorsun',  # one-hot encoding var
            'Hangi tool\'ları kullanıyorsun',  # one-hot encoding var
            'Aylık ortalama net kaç bin TL alıyorsun?'  # ortalama_maas var
            # 'Çalışma türü' kaldırıldı - one-hot encoding için gerekli
        ]
        
        # Sadece mevcut sütunları kaldır
        existing_columns_to_drop = [col for col in columns_to_drop if col in cleaned_data.columns]
        if existing_columns_to_drop:
            cleaned_data = cleaned_data.drop(columns=existing_columns_to_drop)
            logger.info(f"Orijinal sütunlar kaldırıldı: {existing_columns_to_drop}")
        
        # 5.2. Sütun isimlerini İngilizce'ye çevir
        column_mapping = {
            'Timestamp': 'timestamp',
            'Çalışma türü': 'calisma_turu',
            'ortalama_maas': 'ortalama_maas',
            'sirket_lokasyon': 'sirket_lokasyon',
            'kariyer_seviyesi': 'kariyer_seviyesi',
            'cinsiyet': 'cinsiyet',
            'calisma_sekli': 'calisma_sekli'
        }
        
        # Sadece mevcut sütunları yeniden adlandır
        existing_mapping = {k: v for k, v in column_mapping.items() if k in cleaned_data.columns}
        if existing_mapping:
            cleaned_data = cleaned_data.rename(columns=existing_mapping)
            logger.info(f"Sütun isimleri İngilizce'ye çevrildi: {list(existing_mapping.keys())}")
        
        # 5.3. One-hot encoding sütunlarının isimlerini düzelt
        turkish_to_english = {
            'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
            'Ç': 'C', 'Ğ': 'G', 'I': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'
        }
        
        # One-hot encoding sütunlarının isimlerini düzelt
        new_column_names = {}
        for col in cleaned_data.columns:
            if any(turkish_char in col for turkish_char in turkish_to_english.keys()):
                new_name = col
                for turkish, english in turkish_to_english.items():
                    new_name = new_name.replace(turkish, english)
                new_column_names[col] = new_name
        
        if new_column_names:
            cleaned_data = cleaned_data.rename(columns=new_column_names)
            logger.info(f"One-hot encoding sütun isimleri düzeltildi: {len(new_column_names)} sütun")
        
        # 5.4. Calisma_turu ve sirket_lokasyon için one-hot encoding ekle
        additional_one_hot = {}
        
        # Calisma_turu için one-hot encoding (eğer hala varsa)
        if 'calisma_turu' in cleaned_data.columns:
            work_types = cleaned_data['calisma_turu'].unique()
            for work_type in work_types:
                if pd.notna(work_type):
                    work_type_short = work_type.lower().replace(' ', '_')
                    additional_one_hot[f'work_type_{work_type_short}'] = (cleaned_data['calisma_turu'] == work_type).astype(int)
        
        # Sirket_lokasyon için one-hot encoding (eğer hala varsa)
        if 'sirket_lokasyon' in cleaned_data.columns:
            locations = cleaned_data['sirket_lokasyon'].unique()
            for location in locations:
                if pd.notna(location):
                    location_short = location.lower().replace(' ', '_').replace('(', '').replace(')', '')
                    additional_one_hot[f'location_{location_short}'] = (cleaned_data['sirket_lokasyon'] == location).astype(int)
        
        if additional_one_hot:
            additional_df = pd.DataFrame(additional_one_hot)
            cleaned_data = pd.concat([cleaned_data, additional_df], axis=1)
            logger.info(f"Ek one-hot encoding eklendi: {len(additional_one_hot)} sütun")
        
        # 5.5. One-hot encoding sonrası orijinal sütunları kaldır
        final_columns_to_drop = ['calisma_turu', 'sirket_lokasyon']
        existing_final_drop = [col for col in final_columns_to_drop if col in cleaned_data.columns]
        if existing_final_drop:
            cleaned_data = cleaned_data.drop(columns=existing_final_drop)
            logger.info(f"One-hot encoding sonrası orijinal sütunlar kaldırıldı: {existing_final_drop}")
        
        # 6. Eksik değerleri yönet
        cleaned_data = self.handle_missing_values(cleaned_data)
        
        # 7. Aykırı değerleri analiz et
        if 'ortalama_maas' in cleaned_data.columns:
            outliers, outlier_stats = self.detect_outliers(cleaned_data, 'ortalama_maas')
            logger.info(f"Maaş aykırı değer analizi: {outlier_stats}")
        
        self.cleaned_df = cleaned_data
        logger.info(f"Veri temizleme tamamlandı. Final boyut: {cleaned_data.shape}")
        
        return cleaned_data
    
    def save_cleaned_data(self, output_path: str = "data/cleaned_data.csv") -> None:
        """
        Temizlenmiş veriyi kaydeder.
        
        Args:
            output_path (str): Çıktı dosyasının yolu
        """
        if self.cleaned_df is None:
            raise ValueError("Önce veriyi temizleyin (clean_data)")
        
        try:
            self.cleaned_df.to_csv(output_path, index=False)
            logger.info(f"Temizlenmiş veri kaydedildi: {output_path}")
        except Exception as e:
            logger.error(f"Veri kaydetme hatası: {str(e)}")
            raise


def main():
    """Ana fonksiyon - veri temizleme sürecini çalıştırır."""
    try:
        # DataCleaner örneği oluştur
        cleaner = DataCleaner()
        
        # Veriyi temizle
        cleaned_data = cleaner.clean_data()
        
        # Temizlenmiş veriyi kaydet
        cleaner.save_cleaned_data()
        
        # Özet bilgileri yazdır
        print("\n=== VERİ TEMİZLEME ÖZETİ ===")
        print(f"Orijinal veri boyutu: {cleaner.df.shape}")
        print(f"Temizlenmiş veri boyutu: {cleaned_data.shape}")
        print(f"Toplam sütun sayısı artışı: {cleaned_data.shape[1] - cleaner.df.shape[1]}")
        
        if 'ortalama_maas' in cleaned_data.columns:
            print(f"Ortalama maaş: {cleaned_data['ortalama_maas'].mean():.2f} bin TL")
            print(f"Medyan maaş: {cleaned_data['ortalama_maas'].median():.2f} bin TL")
        
        print("Veri temizleme süreci başarıyla tamamlandı!")
        
    except Exception as e:
        logger.error(f"Veri temizleme hatası: {str(e)}")
        raise


if __name__ == "__main__":
    main()

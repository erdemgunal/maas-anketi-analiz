"""
Sprint 1: Veri Hazırlama ve Ön İşleme (Final)
Bu script, 2025_maas_anket.csv dosyasını temizleyip analiz için hazır hale getirir.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from unidecode import unidecode
import re
import warnings
warnings.filterwarnings('ignore')

def _normalize_multi_label_token(value: str) -> str:
    """
    Çoklu seçim alanlarındaki tekil bir değeri normalize et:
    - Kenar boşluklarını kırp
    - Birden fazla boşluğu tek boşluğa indir
    - Alias eşlemesi uygula (örn. Objective C, HTML/CSS vb.)
    """
    if value is None:
        return ''
    text = str(value).strip()
    text = re.sub(r'\s+', ' ', text)

    # Alias haritası (lower-case anahtar)
    key = text.lower().replace('-', ' ').replace('_', ' ')
    alias_map = {
        'objective c': 'Objective C',
        'objective_c': 'Objective C',
        'r language': 'R Language',
        'html css': 'HTML/CSS',
        'html/css': 'HTML/CSS',
        'c sharp': 'C#',
        'c plus plus': 'C++',
        'js': 'JavaScript',
        'ts': 'TypeScript',
    }
    if key in alias_map:
        return alias_map[key]
    return text

def _slugify_label_for_column(name: str) -> str:
    """
    Sütun adı olarak güvenli bir etiket üret (sadece [A-Za-z0-9_]).
    """
    name = unidecode(str(name))
    name = re.sub(r'[^A-Za-z0-9]+', '_', name)
    name = re.sub(r'_+', '_', name).strip('_')
    return name

def clean_column_names(df):
    """
    Sütun isimlerini temizle: boşlukları _ ile değiştir, Türkçe karakterleri latinize et
    """
    new_columns = {}
    for col in df.columns:
        # Türkçe karakterleri latinize et
        cleaned = unidecode(col)
        # Boşlukları _ ile değiştir
        cleaned = re.sub(r'\s+', '_', cleaned)
        # Özel karakterleri değiştir
        cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', cleaned)
        # Birden fazla _'yi tek _'ye çevir
        cleaned = re.sub(r'_+', '_', cleaned)
        # Başındaki ve sonundaki _'leri kaldır
        cleaned = cleaned.strip('_')
        new_columns[col] = cleaned
    return df.rename(columns=new_columns)

def normalize_salary(salary_range):
    """
    Maaş aralıklarını sayısal değerlere dönüştür
    """
    if pd.isna(salary_range):
        return np.nan
    
    salary_str = str(salary_range).strip()
    
    # 300+ durumu
    if '300 +' in salary_str or '300+' in salary_str:
        return 350
    
    # Aralık formatı: "61 - 70" -> 65.5
    if ' - ' in salary_str:
        try:
            lower, upper = map(float, salary_str.split(' - '))
            return (lower + upper) / 2
        except:
            return np.nan
    
    # Tek değer formatı
    try:
        return float(salary_str)
    except:
        return np.nan

def process_multi_label_columns(df, columns_to_process):
    """
    Çoklu seçim sütunlarını multi-hot encoding ile işle
    """
    for col in columns_to_process:
        if col in df.columns:
            # Virgülle ayrılmış değerleri listeye çevir
            df[col] = df[col].fillna('Hiçbiri')
            df[col] = df[col].astype(str).str.split(',')

            # Token bazlı normalizasyon ve satır içi tekilleştirme
            def _normalize_list(values):
                normalized = set()
                for v in values:
                    norm = _normalize_multi_label_token(v)
                    if norm:
                        normalized.add(norm)
                # Deterministik sütun sırası için sırala
                return sorted(normalized)

            df[col] = df[col].apply(_normalize_list)
            
            # MultiLabelBinarizer uygula
            mlb = MultiLabelBinarizer()
            encoded = mlb.fit_transform(df[col])
            
            # Sütun isimlerini oluştur
            prefix = col.split('_')[0] if '_' in col else col
            # Sınıf adlarını sütun adı için güvenli ve tekilleştirilmiş hale getir
            encoded_columns = [f'{prefix}__{_slugify_label_for_column(x)}' for x in mlb.classes_]
            
            # DataFrame oluştur
            encoded_df = pd.DataFrame(encoded, columns=encoded_columns, index=df.index, dtype=int)
            
            # Ana DataFrame'e ekle
            df = pd.concat([df, encoded_df], axis=1)
            
            # Orijinal sütunu kaldır
            df = df.drop(columns=[col])
    
    return df

def main():
    """
    Ana veri işleme fonksiyonu
    """
    print("Sprint 1: Veri Hazırlama ve Ön İşleme Başlıyor...")
    
    # 1. Veri Yükleme
    print("1. Veri yükleniyor...")
    df = pd.read_csv('data/2025_maas_anket.csv')
    print(f"   Yüklenen veri boyutu: {df.shape}")
    
    # 2. Eksik Veri Kontrolü
    print("2. Eksik veri kontrolü yapılıyor...")
    missing_data = df.isna().sum()
    print(f"   Eksik veri sayısı: {missing_data.sum()}")
    assert missing_data.sum() == 0, "Eksik veri tespit edildi!"
    
    # 3. Sütun İsimlerini İngilizce'ye Çevirme
    print("3. Sütun isimleri İngilizce'ye çevriliyor...")
    column_mapping = {
        'Timestamp': 'timestamp',
        'Şirket lokasyon': 'company_location',
        'Çalışma türü': 'employment_type',
        'Çalışma şekli': 'work_mode',
        'Cinsiyet': 'gender',
        'Toplam kaç yıllık iş deneyimin var?': 'experience_years',
        'Hangi seviyedesin?': 'level',
        'Hangi programlama dillerini kullanıyorsun': 'programming_languages',
        'Ne yapıyorsun?': 'role',
        'Frontend yazıyorsan hangilerini kullanıyorsun': 'frontend_technologies',
        'Hangi tool\'ları kullanıyorsun': 'tools',
        'Aylık ortalama net kaç bin TL alıyorsun?': 'salary_range'
    }
    df = df.rename(columns=column_mapping)
    
    # 4. Timestamp'i datetime objesine dönüştürme
    print("4. Timestamp datetime objesine dönüştürülüyor...")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 5. Maaş Normalizasyonu
    print("5. Maaş normalizasyonu yapılıyor...")
    df['salary_numeric'] = df['salary_range'].apply(normalize_salary)
    print(f"   Maaş dağılımı: {df['salary_numeric'].describe()}")
    
    # 6. Çalışan Lokasyon Tahmini (One-Hot encoding'den önce)
    print("6. Çalışan lokasyon tahmini yapılıyor...")

    def infer_location_flag(row):
        # "Yurtdışı TR hub" → her durumda 0 (belirsiz, aykırı değerler dahil)
        if row['company_location'] == 'Yurtdışı TR hub':
            return 0
        
         # Remote → 0 (ikamet kesin tahmin edilemez)
        if row['work_mode'] == 'Remote':
            return 0
        
        # Eğer Office veya Hybrid ise → yüksek ihtimal şirket lokasyonunda yaşıyor
        if row['work_mode'] in ['Office', 'Hybrid']:
            return 1
        
        # Default → belirsiz
        return 0

    df['is_likely_in_company_location'] = df.apply(infer_location_flag, axis=1)
    print("   Tahmin sütunu oluşturuldu. Dağılım:")
    print(df['is_likely_in_company_location'].value_counts())
    
    # 7. Kategorik Kodlama
    print("7. Kategorik kodlama yapılıyor...")
    
    # One-Hot Encoding (kategorik sütunlar için)
    categorical_columns = ['company_location', 'employment_type', 'work_mode', 'role']
    df = pd.get_dummies(df, columns=categorical_columns, dtype=int)
    
    # Gender encoding (binary)
    df['gender'] = df['gender'].map({'Erkek': 0, 'Kadın': 1})
    
    # Experience years encoding (ordinal)
    experience_map = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        '10': 10, '11 - 15': 13, '16 - 20': 18, '20 - 30': 25, '30+': 30
    }
    df['experience_years'] = df['experience_years'].map(experience_map)
    
    # Level encoding (seniority ve management)
    # Teknik seviyeler için ordinal kodlama
    ic_map = {
        'Junior': 1, 'Mid': 2, 'Senior': 3, 'Staff Engineer': 4, 'Team Lead': 5, 'Architect': 6
    }
    df['seniority_level_ic'] = df['level'].map(ic_map).fillna(0)  # Yönetim rolleri için 0
    
    # Yönetici bayrağı
    management_roles = ['Engineering Manager', 'Director Level Manager', 'C-Level Manager', 'Partner']
    df['is_manager'] = df['level'].isin(management_roles).astype(int)
    
    # Level için One-Hot Encoding (tüm seviyeler için)
    df = pd.get_dummies(df, columns=['level'], prefix='management', dtype=int)
    
    # 8. Çoklu Seçim Sütunlarını İşleme
    print("8. Çoklu seçim sütunları işleniyor...")
    multi_label_columns = ['programming_languages', 'frontend_technologies', 'tools']
    df = process_multi_label_columns(df, multi_label_columns)
    
    # 9. Sütun İsimlerini Temizleme
    print("9. Sütun isimleri temizleniyor...")
    df = clean_column_names(df)
    
    # 10. Tekrarlanan Sütunları Kaldırma
    print("10. Tekrarlanan sütunlar kaldırılıyor...")
    # Tekrarlanan sütunları bul ve kaldır
    duplicate_columns = df.columns[df.columns.duplicated()].tolist()
    if duplicate_columns:
        print(f"   Tekrarlanan sütunlar bulundu: {duplicate_columns}")
        df = df.loc[:, ~df.columns.duplicated()]
        print(f"   Tekrarlanan sütunlar kaldırıldı")
    
    # 11. Aykırı Değer İşleme
    print("11. Aykırı değerler işleniyor...")
    Q1 = df['salary_numeric'].quantile(0.25)
    Q3 = df['salary_numeric'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = min(Q3 + 1.5 * IQR, 350)  # Üst sınır 350
    
    # Z-Score yöntemi
    z_scores = np.abs((df['salary_numeric'] - df['salary_numeric'].mean()) / df['salary_numeric'].std())
    upper_bound_z = df['salary_numeric'][z_scores <= 3].max()
    lower_bound_z = df['salary_numeric'][z_scores <= 3].min()
    
    # IQR ve Z-Score sınırlarını birleştir
    final_lower = max(lower_bound, lower_bound_z)
    final_upper = min(upper_bound, upper_bound_z, 350)
    
    df['salary_numeric'] = df['salary_numeric'].clip(lower=final_lower, upper=final_upper)
    
    print(f"   Aykırı değer sınırları: {final_lower:.1f} - {final_upper:.1f}")
    
    # 12. Orijinal Sütunları Kaldırma
    print("12. Orijinal sütunlar kaldırılıyor...")
    columns_to_drop = ['salary_range', 'programming_languages', 'frontend_technologies', 'tools']
    for col in columns_to_drop:
        if col in df.columns:
            df = df.drop(columns=[col])
    
    # 13. Kalite Kontrol
    print("13. Kalite kontrol yapılıyor...")
    print(f"   Final veri boyutu: {df.shape}")
    print(f"   Eksik veri sayısı: {df.isna().sum().sum()}")
    print(f"   Sütun sayısı: {df.shape[1]}")
    
    # 14. Temizlenmiş Veri Setini Kaydetme
    print("14. Temizlenmiş veri seti kaydediliyor...")
    df.to_csv('data/2025_cleaned_data.csv', index=False)
    print("   ✅ 2025_cleaned_data.csv başarıyla oluşturuldu!")
    
    # 15. Özet İstatistikler
    print("\n15. Özet İstatistikler:")
    print(f"   Toplam kayıt sayısı: {len(df)}")
    print(f"   Toplam sütun sayısı: {df.shape[1]}")
    print(f"   Maaş ortalaması: {df['salary_numeric'].mean():.1f} bin TL")
    print(f"   Maaş medyanı: {df['salary_numeric'].median():.1f} bin TL")
    print(f"   Erkek oranı: {(df['gender'] == 0).mean():.1%}")
    print(f"   Yönetici oranı: {df['is_manager'].mean():.1%}")
    
    # Sütun isimlerini göster
    print(f"\n16. Oluşturulan sütunlar ({df.shape[1]} adet):")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")
    
    print("\n✅ Sprint 1 başarıyla tamamlandı!")
    return df

if __name__ == "__main__":
    df_cleaned = main()

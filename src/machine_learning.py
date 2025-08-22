"""
Makine Öğrenmesi Modülü

Bu modül, maaş anketi verisinin makine öğrenmesi analizi için gerekli
fonksiyonları içerir.

Fonksiyonlar:
- prepare_data: Veri hazırlama ve feature engineering
- train_models: Maaş tahmin modelleri eğitimi
- cross_validation: Çapraz doğrulama
- feature_importance: Özellik önem analizi
- clustering: Developer profil kümeleme
- model_evaluation: Model değerlendirme
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import xgboost as xgb
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

# Görselleştirme ayarları
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12


def load_cleaned_data(file_path: str = '../data/cleaned_data.csv') -> pd.DataFrame:
    """
    Temizlenmiş veriyi yükler.
    
    Args:
        file_path: Temizlenmiş veri dosya yolu
        
    Returns:
        pd.DataFrame: Temizlenmiş veri seti
    """
    df = pd.read_csv(file_path)
    print(f"Temizlenmiş veri yüklendi. Boyut: {df.shape}")
    return df


def prepare_data(df: pd.DataFrame, salary_column: str = 'salary_normalized') -> tuple:
    """
    ML modelleri için veri hazırlama.
    
    Args:
        df: Veri seti
        salary_column: Hedef değişken sütunu
        
    Returns:
        tuple: X_train, X_test, y_train, y_test, feature_names
    """
    print("=== VERİ HAZIRLAMA ===")
    
    # Sayısal sütunları seç
    numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Hedef değişkeni çıkar
    if salary_column in numerical_columns:
        numerical_columns.remove(salary_column)
    
    # Timestamp sütununu çıkar
    if 'Timestamp' in numerical_columns:
        numerical_columns.remove('Timestamp')
    
    # Maaş aralığı sütununu çıkar (tahmin için kullanılamaz)
    if 'Aylık ortalama net kaç bin TL alıyorsun?' in numerical_columns:
        numerical_columns.remove('Aylık ortalama net kaç bin TL alıyorsun?')
    
    # Feature matrix oluştur
    X = df[numerical_columns]
    y = df[salary_column]
    
    print(f"Feature sayısı: {len(numerical_columns)}")
    print(f"Örnek sayısı: {len(X)}")
    print(f"Hedef değişken: {salary_column}")
    print(f"Hedef değişken aralığı: {y.min():.1f} - {y.max():.1f}")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Eğitim seti: {X_train.shape[0]} örnek")
    print(f"Test seti: {X_test.shape[0]} örnek")
    
    return X_train, X_test, y_train, y_test, numerical_columns


def train_models(X_train: pd.DataFrame, X_test: pd.DataFrame, 
                y_train: pd.Series, y_test: pd.Series) -> dict:
    """
    Maaş tahmin modellerini eğitir.
    
    Args:
        X_train: Eğitim feature'ları
        X_test: Test feature'ları
        y_train: Eğitim hedef değişkeni
        y_test: Test hedef değişkeni
        
    Returns:
        dict: Eğitilmiş modeller ve performans metrikleri
    """
    print("\n=== MODEL EĞİTİMİ ===")
    
    models = {}
    results = {}
    
    # 1. Linear Regression (Baseline)
    print("1. Linear Regression eğitiliyor...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    
    lr_pred = lr_model.predict(X_test)
    lr_r2 = r2_score(y_test, lr_pred)
    lr_mae = mean_absolute_error(y_test, lr_pred)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
    
    models['linear_regression'] = lr_model
    results['linear_regression'] = {
        'r2': lr_r2,
        'mae': lr_mae,
        'rmse': lr_rmse
    }
    
    print(f"  R²: {lr_r2:.4f}")
    print(f"  MAE: {lr_mae:.2f}")
    print(f"  RMSE: {lr_rmse:.2f}")
    
    # 2. Random Forest
    print("\n2. Random Forest eğitiliyor...")
    rf_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    
    rf_pred = rf_model.predict(X_test)
    rf_r2 = r2_score(y_test, rf_pred)
    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
    
    models['random_forest'] = rf_model
    results['random_forest'] = {
        'r2': rf_r2,
        'mae': rf_mae,
        'rmse': rf_rmse
    }
    
    print(f"  R²: {rf_r2:.4f}")
    print(f"  MAE: {rf_mae:.2f}")
    print(f"  RMSE: {rf_rmse:.2f}")
    
    # 3. XGBoost
    print("\n3. XGBoost eğitiliyor...")
    xgb_model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    )
    xgb_model.fit(X_train, y_train)
    
    xgb_pred = xgb_model.predict(X_test)
    xgb_r2 = r2_score(y_test, xgb_pred)
    xgb_mae = mean_absolute_error(y_test, xgb_pred)
    xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
    
    models['xgboost'] = xgb_model
    results['xgboost'] = {
        'r2': xgb_r2,
        'mae': xgb_mae,
        'rmse': xgb_rmse
    }
    
    print(f"  R²: {xgb_r2:.4f}")
    print(f"  MAE: {xgb_mae:.2f}")
    print(f"  RMSE: {xgb_rmse:.2f}")
    
    return models, results


def cross_validation(X: pd.DataFrame, y: pd.Series, models: dict) -> dict:
    """
    Çapraz doğrulama uygular.
    
    Args:
        X: Feature matrix
        y: Hedef değişken
        models: Eğitilmiş modeller
        
    Returns:
        dict: CV sonuçları
    """
    print("\n=== ÇAPRAZ DOĞRULAMA ===")
    
    cv_results = {}
    
    for name, model in models.items():
        print(f"{name} için 5-katlı CV uygulanıyor...")
        
        # R² CV skorları
        r2_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
        mae_scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_error')
        rmse_scores = cross_val_score(model, X, y, cv=5, scoring='neg_root_mean_squared_error')
        
        cv_results[name] = {
            'r2_mean': r2_scores.mean(),
            'r2_std': r2_scores.std(),
            'mae_mean': -mae_scores.mean(),
            'mae_std': mae_scores.std(),
            'rmse_mean': -rmse_scores.mean(),
            'rmse_std': rmse_scores.std(),
            'r2_scores': r2_scores
        }
        
        print(f"  CV R²: {r2_scores.mean():.4f} (±{r2_scores.std():.4f})")
        print(f"  CV MAE: {-mae_scores.mean():.2f} (±{mae_scores.std():.2f})")
        print(f"  CV RMSE: {-rmse_scores.mean():.2f} (±{rmse_scores.std():.2f})")
    
    return cv_results


def feature_importance_analysis(models: dict, feature_names: list, 
                              output_path: str = '../outputs/tables/') -> dict:
    """
    Feature importance analizi yapar.
    
    Args:
        models: Eğitilmiş modeller
        feature_names: Feature isimleri
        output_path: Çıktı yolu
        
    Returns:
        dict: Feature importance sonuçları
    """
    print("\n=== FEATURE IMPORTANCE ANALİZİ ===")
    
    importance_results = {}
    
    # Klasör oluştur
    os.makedirs(output_path, exist_ok=True)
    
    for name, model in models.items():
        if hasattr(model, 'feature_importances_'):
            # Feature importance al
            importances = model.feature_importances_
            
            # En önemli 10 feature'ı seç
            indices = np.argsort(importances)[::-1][:10]
            
            importance_results[name] = {
                'importances': importances,
                'top_features': [feature_names[i] for i in indices],
                'top_importance_values': [importances[i] for i in indices]
            }
            
            print(f"\n{name} - En Önemli 10 Feature:")
            for i, (feature, importance) in enumerate(zip(
                importance_results[name]['top_features'],
                importance_results[name]['top_importance_values']
            ), 1):
                print(f"  {i:2d}. {feature}: {importance:.4f}")
    
    # Feature importance tablosu oluştur
    all_importances = []
    for name, result in importance_results.items():
        for feature, importance in zip(result['top_features'], result['top_importance_values']):
            all_importances.append({
                'Model': name,
                'Feature': feature,
                'Importance': importance
            })
    
    importance_df = pd.DataFrame(all_importances)
    importance_df.to_csv(f"{output_path}feature_importance.csv", index=False)
    print(f"\nFeature importance tablosu kaydedildi: {output_path}feature_importance.csv")
    
    return importance_results


def developer_clustering(df: pd.DataFrame, n_clusters: int = 4) -> dict:
    """
    Developer profillerini kümeleme.
    
    Args:
        df: Veri seti
        n_clusters: Küme sayısı
        
    Returns:
        dict: Kümeleme sonuçları
    """
    print(f"\n=== DEVELOPER KÜMELEME ({n_clusters} küme) ===")
    
    # Kümeleme için feature'ları seç
    clustering_features = [
        'salary_normalized',
        'Hangi seviyedesin?',
        'Toplam kaç yıllık iş deneyimin var?',
        'Frontend_React',
        'Hangi_JavaScript',
        'Hangi_Python',
        'Hangi_TypeScript',
        'Çalışma şekli'
    ]
    
    # Eksik feature'ları kontrol et
    available_features = [f for f in clustering_features if f in df.columns]
    
    if len(available_features) < 3:
        print("Yeterli feature bulunamadı, varsayılan feature'lar kullanılıyor...")
        available_features = ['salary_normalized', 'Hangi seviyedesin?', 'Toplam kaç yıllık iş deneyimin var?']
    
    # Kümeleme verisi hazırla
    clustering_data = df[available_features].copy()
    
    # Eksik verileri doldur
    clustering_data = clustering_data.fillna(clustering_data.median())
    
    # Standardizasyon
    scaler = StandardScaler()
    clustering_scaled = scaler.fit_transform(clustering_data)
    
    # K-means kümeleme
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(clustering_scaled)
    
    # Sonuçları analiz et
    df_clustered = df.copy()
    df_clustered['cluster'] = cluster_labels
    
    # Her küme için özet istatistikler
    cluster_summary = {}
    for cluster_id in range(n_clusters):
        cluster_data = df_clustered[df_clustered['cluster'] == cluster_id]
        
        cluster_summary[cluster_id] = {
            'size': len(cluster_data),
            'percentage': len(cluster_data) / len(df) * 100,
            'avg_salary': cluster_data['salary_normalized'].mean(),
            'avg_experience': cluster_data['Toplam kaç yıllık iş deneyimin var?'].mean() if 'Toplam kaç yıllık iş deneyimin var?' in cluster_data.columns else 0,
            'react_users': cluster_data['Frontend_React'].sum() if 'Frontend_React' in cluster_data.columns else 0,
            'react_percentage': cluster_data['Frontend_React'].mean() * 100 if 'Frontend_React' in cluster_data.columns else 0
        }
    
    print(f"Kümeleme tamamlandı. {n_clusters} küme oluşturuldu.")
    
    for cluster_id, summary in cluster_summary.items():
        print(f"\nKüme {cluster_id}:")
        print(f"  Boyut: {summary['size']} ({summary['percentage']:.1f}%)")
        print(f"  Ortalama maaş: {summary['avg_salary']:.1f} bin TL")
        if 'Toplam kaç yıllık iş deneyimin var?' in df.columns:
            print(f"  Ortalama deneyim: {summary['avg_experience']:.1f} yıl")
        if 'Frontend_React' in df.columns:
            print(f"  React kullanıcıları: {summary['react_users']} ({summary['react_percentage']:.1f}%)")
    
    return {
        'kmeans_model': kmeans,
        'cluster_labels': cluster_labels,
        'cluster_summary': cluster_summary,
        'features_used': available_features
    }


def model_evaluation(models: dict, results: dict, cv_results: dict, 
                    X_test: pd.DataFrame, y_test: pd.Series,
                    output_path: str = '../outputs/tables/') -> dict:
    """
    Model değerlendirme ve karşılaştırma.
    
    Args:
        models: Eğitilmiş modeller
        results: Test sonuçları
        cv_results: CV sonuçları
        X_test: Test feature'ları
        y_test: Test hedef değişkeni
        output_path: Çıktı yolu
        
    Returns:
        dict: Değerlendirme sonuçları
    """
    print("\n=== MODEL DEĞERLENDİRME ===")
    
    # Model karşılaştırma tablosu
    comparison_data = []
    
    for name in models.keys():
        comparison_data.append({
            'Model': name,
            'Test R²': results[name]['r2'],
            'Test MAE': results[name]['mae'],
            'Test RMSE': results[name]['rmse'],
            'CV R²': cv_results[name]['r2_mean'],
            'CV MAE': cv_results[name]['mae_mean'],
            'CV RMSE': cv_results[name]['rmse_mean']
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df.to_csv(f"{output_path}model_comparison.csv", index=False)
    print(f"Model karşılaştırma tablosu kaydedildi: {output_path}model_comparison.csv")
    
    # En iyi modeli belirle
    best_model_name = max(results.keys(), key=lambda x: results[x]['r2'])
    best_model = models[best_model_name]
    
    print(f"\nEn İyi Model: {best_model_name}")
    print(f"Test R²: {results[best_model_name]['r2']:.4f}")
    print(f"CV R²: {cv_results[best_model_name]['r2_mean']:.4f}")
    
    # Hedef kontrolü
    target_r2 = 0.75
    target_cv_r2 = 0.70
    
    print(f"\nHedef Kontrolü:")
    print(f"Test R² > {target_r2}: {'✅' if results[best_model_name]['r2'] > target_r2 else '❌'} ({results[best_model_name]['r2']:.4f})")
    print(f"CV R² > {target_cv_r2}: {'✅' if cv_results[best_model_name]['r2_mean'] > target_cv_r2 else '❌'} ({cv_results[best_model_name]['r2_mean']:.4f})")
    
    return {
        'comparison_table': comparison_df,
        'best_model_name': best_model_name,
        'best_model': best_model,
        'targets_met': {
            'test_r2': results[best_model_name]['r2'] > target_r2,
            'cv_r2': cv_results[best_model_name]['r2_mean'] > target_cv_r2
        }
    }


def save_models(models: dict, output_path: str = '../models/') -> None:
    """
    Eğitilmiş modelleri kaydeder.
    
    Args:
        models: Eğitilmiş modeller
        output_path: Kayıt yolu
    """
    print(f"\n=== MODELLERİ KAYDETME ===")
    
    os.makedirs(output_path, exist_ok=True)
    
    for name, model in models.items():
        model_path = f"{output_path}{name}.joblib"
        joblib.dump(model, model_path)
        print(f"{name} modeli kaydedildi: {model_path}")


def machine_learning_pipeline(file_path: str = '../data/cleaned_data.csv',
                            output_path: str = '../outputs/') -> dict:
    """
    Tam ML pipeline'ı çalıştırır.
    
    Args:
        file_path: Veri dosya yolu
        output_path: Çıktı yolu
        
    Returns:
        dict: Tüm sonuçlar
    """
    print("=== MAKİNE ÖĞRENMESİ PIPELINE ===")
    
    # 1. Veri yükleme
    df = load_cleaned_data(file_path)
    
    # 2. Veri hazırlama
    X_train, X_test, y_train, y_test, feature_names = prepare_data(df)
    
    # 3. Model eğitimi
    models, results = train_models(X_train, X_test, y_train, y_test)
    
    # 4. Çapraz doğrulama
    cv_results = cross_validation(X_train, y_train, models)
    
    # 5. Feature importance analizi
    importance_results = feature_importance_analysis(models, feature_names, f"{output_path}tables/")
    
    # 6. Developer kümeleme
    clustering_results = developer_clustering(df)
    
    # 7. Model değerlendirme
    evaluation_results = model_evaluation(models, results, cv_results, X_test, y_test, f"{output_path}tables/")
    
    # 8. Modelleri kaydet
    save_models(models, f"{output_path}../models/")
    
    # 9. Özet rapor
    print(f"\n=== ÖZET RAPOR ===")
    print(f"Toplam model sayısı: {len(models)}")
    print(f"En iyi model: {evaluation_results['best_model_name']}")
    print(f"En iyi R²: {results[evaluation_results['best_model_name']]['r2']:.4f}")
    print(f"En iyi CV R²: {cv_results[evaluation_results['best_model_name']]['r2_mean']:.4f}")
    print(f"Küme sayısı: {len(clustering_results['cluster_summary'])}")
    
    return {
        'models': models,
        'results': results,
        'cv_results': cv_results,
        'importance_results': importance_results,
        'clustering_results': clustering_results,
        'evaluation_results': evaluation_results,
        'feature_names': feature_names
    }


if __name__ == "__main__":
    # Test çalıştırması
    results = machine_learning_pipeline()
    print(f"\nMakine öğrenmesi pipeline tamamlandı!")

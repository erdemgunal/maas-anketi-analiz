"""
Streamlit Dashboard for Salary Analysis

Interactive web application for exploring salary analysis results
and making salary predictions.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import os
import sys

# Add src to path for imports
sys.path.append('../src')

# Page config
st.set_page_config(
    page_title="Maaş Analizi Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load cleaned data and models"""
    try:
        df = pd.read_csv('../data/cleaned_data.csv')
        return df
    except FileNotFoundError:
        st.error("Veri dosyası bulunamadı. Lütfen data/cleaned_data.csv dosyasının mevcut olduğundan emin olun.")
        return None

@st.cache_resource
def load_models():
    """Load trained models"""
    models = {}
    model_paths = {
        'XGBoost': '../models/xgboost.joblib',
        'Random Forest': '../models/random_forest.joblib',
        'Linear Regression': '../models/linear_regression.joblib'
    }
    
    for name, path in model_paths.items():
        try:
            models[name] = joblib.load(path)
        except FileNotFoundError:
            st.warning(f"{name} modeli bulunamadı: {path}")
    
    return models

def main():
    # Header
    st.markdown('<h1 class="main-header">💰 Maaş Analizi Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### React Geliştiricileri İçin Kapsamlı İstatistiksel ve Makine Öğrenmesi Analizi")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Load models
    models = load_models()
    
    # Sidebar
    st.sidebar.title("📊 Navigasyon")
    page = st.sidebar.selectbox(
        "Sayfa Seçin",
        ["🏠 Ana Sayfa", "📈 Veri Analizi", "🤖 Makine Öğrenmesi", "💰 Maaş Tahmini", "👥 Profil Analizi"]
    )
    
    if page == "🏠 Ana Sayfa":
        show_homepage(df)
    elif page == "📈 Veri Analizi":
        show_data_analysis(df)
    elif page == "🤖 Makine Öğrenmesi":
        show_machine_learning(df, models)
    elif page == "💰 Maaş Tahmini":
        show_salary_prediction(df, models)
    elif page == "👥 Profil Analizi":
        show_profile_analysis(df)

def show_homepage(df):
    """Show homepage with key metrics and overview"""
    st.header("🏠 Ana Sayfa")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Toplam Katılımcı",
            value=f"{len(df):,}",
            delta="2,820 geliştirici"
        )
    
    with col2:
        avg_salary = df['salary_normalized'].mean()
        st.metric(
            label="Ortalama Maaş",
            value=f"{avg_salary:.1f} bin TL",
            delta="91.2 bin TL"
        )
    
    with col3:
        react_users = df['Frontend_React'].sum() if 'Frontend_React' in df.columns else 0
        react_percentage = (react_users / len(df)) * 100
        st.metric(
            label="React Kullanıcıları",
            value=f"{react_users:,}",
            delta=f"%{react_percentage:.1f}"
        )
    
    with col4:
        gender_gap = df[df['Cinsiyet'] == 0]['salary_normalized'].mean() - df[df['Cinsiyet'] == 1]['salary_normalized'].mean()
        st.metric(
            label="Gender Gap",
            value=f"{gender_gap:.1f} bin TL",
            delta="Erkek-Kadın farkı"
        )
    
    # Summary statistics
    st.subheader("📊 Özet İstatistikler")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Maaş Dağılımı:**")
        salary_stats = {
            'Ortalama': f"{df['salary_normalized'].mean():.2f} bin TL",
            'Medyan': f"{df['salary_normalized'].median():.2f} bin TL",
            'Minimum': f"{df['salary_normalized'].min():.2f} bin TL",
            'Maksimum': f"{df['salary_normalized'].max():.2f} bin TL",
            'Standart Sapma': f"{df['salary_normalized'].std():.2f} bin TL"
        }
        
        for stat, value in salary_stats.items():
            st.write(f"• {stat}: {value}")
    
    with col2:
        st.markdown("**Demografik Dağılım:**")
        if 'Cinsiyet' in df.columns:
            male_count = (df['Cinsiyet'] == 0).sum()
            female_count = (df['Cinsiyet'] == 1).sum()
            st.write(f"• Erkek: {male_count:,} (%{(male_count/len(df)*100):.1f})")
            st.write(f"• Kadın: {female_count:,} (%{(female_count/len(df)*100):.1f})")
        
        if 'Hangi seviyedesin?' in df.columns:
            level_counts = df['Hangi seviyedesin?'].value_counts()
            st.write("**Deneyim Seviyeleri:**")
            for level, count in level_counts.head(3).items():
                st.write(f"• Seviye {level}: {count:,} (%{(count/len(df)*100):.1f})")
    
    # Key findings
    st.subheader("🔍 Ana Bulgular")
    
    findings = [
        "React kullanımı maaş üzerinde beklenmedik şekilde minimal etkiye sahip (-3.96 bin TL)",
        "Remote çalışanlar en yüksek maaşı alıyor (98.58 bin TL)",
        "Gender gap tespit edildi: Erkekler 10.59 bin TL daha fazla kazanıyor",
        "Deneyim seviyesi maaş ile en güçlü korelasyona sahip (0.417)",
        "XGBoost modeli ile %99.07 doğruluk oranında maaş tahmini yapılabiliyor"
    ]
    
    for i, finding in enumerate(findings, 1):
        st.write(f"{i}. {finding}")

def show_data_analysis(df):
    """Show interactive data analysis visualizations"""
    st.header("📈 Veri Analizi")
    
    # Analysis type selection
    analysis_type = st.selectbox(
        "Analiz Türü Seçin",
        ["Maaş Dağılımı", "React vs Non-React", "Cinsiyet Analizi", "Çalışma Şekli", "Korelasyon Analizi"]
    )
    
    if analysis_type == "Maaş Dağılımı":
        st.subheader("💰 Maaş Dağılımı Analizi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            fig = px.histogram(
                df, x='salary_normalized', nbins=30,
                title="Maaş Dağılımı (Histogram)",
                labels={'salary_normalized': 'Maaş (bin TL)', 'count': 'Frekans'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Box plot
            fig = px.box(
                df, y='salary_normalized',
                title="Maaş Dağılımı (Box Plot)",
                labels={'salary_normalized': 'Maaş (bin TL)'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "React vs Non-React":
        st.subheader("⚛️ React vs Non-React Maaş Karşılaştırması")
        
        if 'Frontend_React' in df.columns:
            react_salary = df[df['Frontend_React'] == 1]['salary_normalized']
            non_react_salary = df[df['Frontend_React'] == 0]['salary_normalized']
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Box plot comparison
                fig = px.box(
                    df, x='Frontend_React', y='salary_normalized',
                    title="React Kullanımı vs Maaş",
                    labels={'Frontend_React': 'React (0=Hayır, 1=Evet)', 'salary_normalized': 'Maaş (bin TL)'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Statistics
                st.markdown("**İstatistikler:**")
                st.write(f"• React kullananlar: {react_salary.mean():.1f} bin TL")
                st.write(f"• React kullanmayanlar: {non_react_salary.mean():.1f} bin TL")
                st.write(f"• Fark: {react_salary.mean() - non_react_salary.mean():.1f} bin TL")
                st.write(f"• React kullanıcı sayısı: {len(react_salary):,}")
                st.write(f"• Non-React kullanıcı sayısı: {len(non_react_salary):,}")
    
    elif analysis_type == "Cinsiyet Analizi":
        st.subheader("👥 Cinsiyet Bazlı Maaş Analizi")
        
        if 'Cinsiyet' in df.columns:
            male_salary = df[df['Cinsiyet'] == 0]['salary_normalized']
            female_salary = df[df['Cinsiyet'] == 1]['salary_normalized']
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.box(
                    df, x='Cinsiyet', y='salary_normalized',
                    title="Cinsiyet vs Maaş",
                    labels={'Cinsiyet': 'Cinsiyet (0=Erkek, 1=Kadın)', 'salary_normalized': 'Maaş (bin TL)'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**Gender Gap Analizi:**")
                st.write(f"• Erkek ortalama: {male_salary.mean():.1f} bin TL")
                st.write(f"• Kadın ortalama: {female_salary.mean():.1f} bin TL")
                st.write(f"• Gender gap: {male_salary.mean() - female_salary.mean():.1f} bin TL")
                st.write(f"• Gap yüzdesi: %{((male_salary.mean() - female_salary.mean()) / male_salary.mean() * 100):.1f}")
    
    elif analysis_type == "Çalışma Şekli":
        st.subheader("🏢 Çalışma Şekli Maaş Analizi")
        
        if 'Çalışma şekli' in df.columns:
            fig = px.box(
                df, x='Çalışma şekli', y='salary_normalized',
                title="Çalışma Şekli vs Maaş",
                labels={'Çalışma şekli': 'Çalışma Şekli (0=Remote,1=Hybrid,2=Office)', 'salary_normalized': 'Maaş (bin TL)'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            work_stats = df.groupby('Çalışma şekli')['salary_normalized'].agg(['mean', 'count']).round(1)
            st.markdown("**Çalışma Şekli İstatistikleri:**")
            st.dataframe(work_stats)

def show_machine_learning(df, models):
    """Show machine learning results and model performance"""
    st.header("🤖 Makine Öğrenmesi Sonuçları")
    
    if not models:
        st.warning("Eğitilmiş modeller bulunamadı. Lütfen models/ klasöründeki model dosyalarının mevcut olduğundan emin olun.")
        return
    
    # Model performance comparison
    st.subheader("📊 Model Performans Karşılaştırması")
    
    # Mock performance data (replace with actual if available)
    performance_data = {
        'Model': ['Linear Regression', 'Random Forest', 'XGBoost'],
        'Test R²': [0.3705, 0.9959, 1.0000],
        'CV R²': [0.3761, 0.9731, 0.9907],
        'MAE': [27.18, 0.39, 0.04]
    }
    
    perf_df = pd.DataFrame(performance_data)
    st.dataframe(perf_df, use_container_width=True)
    
    # Performance visualization
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            perf_df, x='Model', y='Test R²',
            title="Model Test R² Karşılaştırması",
            color='Test R²'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            perf_df, x='Model', y='CV R²',
            title="Model CV R² Karşılaştırması",
            color='CV R²'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Feature importance
    st.subheader("🎯 Feature Importance (XGBoost)")
    
    # Mock feature importance data
    feature_importance = {
        'Feature': ['Maaş aralığı', 'Deneyim seviyesi', 'İş deneyimi', 'Şirket lokasyon', 'Cinsiyet'],
        'Importance': [0.7425, 0.1908, 0.0587, 0.0062, 0.0010]
    }
    
    fi_df = pd.DataFrame(feature_importance)
    
    fig = px.bar(
        fi_df, x='Importance', y='Feature', orientation='h',
        title="XGBoost Feature Importance",
        labels={'Importance': 'Önem Skoru', 'Feature': 'Özellik'}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_salary_prediction(df, models):
    """Show salary prediction interface"""
    st.header("💰 Maaş Tahmini")
    
    if not models:
        st.warning("Eğitilmiş modeller bulunamadı.")
        return
    
    st.markdown("### Maaş Tahmin Aracı")
    st.markdown("Aşağıdaki bilgileri girerek maaş tahmini yapabilirsiniz.")
    
    # Input form
    with st.form("salary_prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            experience = st.slider("İş Deneyimi (Yıl)", 0, 20, 5)
            level = st.selectbox("Deneyim Seviyesi", [0, 1, 2], format_func=lambda x: ['Junior', 'Mid', 'Senior'][x])
            gender = st.selectbox("Cinsiyet", [0, 1], format_func=lambda x: ['Erkek', 'Kadın'][x])
            work_type = st.selectbox("Çalışma Şekli", [0, 1, 2], format_func=lambda x: ['Remote', 'Hybrid', 'Office'][x])
        
        with col2:
            react_usage = st.checkbox("React Kullanıyor musunuz?")
            location = st.selectbox("Şirket Lokasyonu", [0, 1, 2, 3], format_func=lambda x: ['Türkiye', 'Avrupa', 'ABD', 'Diğer'][x])
            employment_type = st.selectbox("Çalışma Türü", [0, 1, 2, 3], format_func=lambda x: ['Tam zamanlı', 'Yarı zamanlı', 'Freelance', 'Diğer'][x])
            role = st.selectbox("Rol", [0, 1, 2, 3, 4], format_func=lambda x: ['Frontend', 'Backend', 'Fullstack', 'DevOps', 'Diğer'][x])
        
        submitted = st.form_submit_button("Maaş Tahmini Yap")
    
    if submitted:
        # Create feature vector (simplified - adjust based on actual model features)
        features = {
            'Hangi seviyedesin?': level,
            'Toplam kaç yıllık iş deneyimin var?': experience,
            'Cinsiyet': gender,
            'Çalışma şekli': work_type,
            'Şirket lokasyon': location,
            'Çalışma türü': employment_type,
            'Ne yapıyorsun?': role,
            'Frontend_React': 1 if react_usage else 0
        }
        
        # Convert to DataFrame
        input_df = pd.DataFrame([features])
        
        # Make predictions
        predictions = {}
        for name, model in models.items():
            try:
                pred = model.predict(input_df)[0]
                predictions[name] = pred
            except:
                predictions[name] = None
        
        # Display results
        st.subheader("🎯 Tahmin Sonuçları")
        
        col1, col2, col3 = st.columns(3)
        
        if 'XGBoost' in predictions and predictions['XGBoost'] is not None:
            with col1:
                st.metric(
                    label="XGBoost Tahmini",
                    value=f"{predictions['XGBoost']:.1f} bin TL",
                    delta="En iyi model"
                )
        
        if 'Random Forest' in predictions and predictions['Random Forest'] is not None:
            with col2:
                st.metric(
                    label="Random Forest Tahmini",
                    value=f"{predictions['Random Forest']:.1f} bin TL"
                )
        
        if 'Linear Regression' in predictions and predictions['Linear Regression'] is not None:
            with col3:
                st.metric(
                    label="Linear Regression Tahmini",
                    value=f"{predictions['Linear Regression']:.1f} bin TL"
                )
        
        # Show input summary
        st.subheader("📋 Girilen Bilgiler")
        input_summary = {
            'İş Deneyimi': f"{experience} yıl",
            'Deneyim Seviyesi': ['Junior', 'Mid', 'Senior'][level],
            'Cinsiyet': ['Erkek', 'Kadın'][gender],
            'Çalışma Şekli': ['Remote', 'Hybrid', 'Office'][work_type],
            'React Kullanımı': 'Evet' if react_usage else 'Hayır',
            'Lokasyon': ['Türkiye', 'Avrupa', 'ABD', 'Diğer'][location],
            'Çalışma Türü': ['Tam zamanlı', 'Yarı zamanlı', 'Freelance', 'Diğer'][employment_type],
            'Rol': ['Frontend', 'Backend', 'Fullstack', 'DevOps', 'Diğer'][role]
        }
        
        for key, value in input_summary.items():
            st.write(f"• **{key}:** {value}")

def show_profile_analysis(df):
    """Show developer profile clustering analysis"""
    st.header("👥 Developer Profil Analizi")
    
    st.markdown("### K-Means Kümeleme Sonuçları")
    
    # Mock clustering results
    clusters = {
        'Küme': ['Küme 0', 'Küme 1', 'Küme 2', 'Küme 3'],
        'Boyut': [683, 969, 762, 406],
        'Yüzde': [24.2, 34.4, 27.0, 14.4],
        'Ortalama Maaş': [66.3, 64.4, 128.8, 126.6],
        'Ortalama Deneyim': [5.7, 4.8, 9.3, 8.8],
        'React Kullanımı': [81.0, 4.1, 4.3, 81.0],
        'Profil': [
            'Düşük maaşlı React kullanıcıları',
            'Düşük maaşlı non-React kullanıcıları',
            'Yüksek maaşlı deneyimli kullanıcılar',
            'Yüksek maaşlı React kullanıcıları'
        ]
    }
    
    cluster_df = pd.DataFrame(clusters)
    st.dataframe(cluster_df, use_container_width=True)
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            cluster_df, values='Boyut', names='Küme',
            title="Developer Profil Dağılımı"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            cluster_df, x='Küme', y='Ortalama Maaş',
            title="Küme Ortalama Maaşları",
            color='Ortalama Maaş'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Profile descriptions
    st.subheader("📋 Profil Açıklamaları")
    
    for i, row in cluster_df.iterrows():
        with st.expander(f"{row['Küme']}: {row['Profil']}"):
            st.write(f"**Boyut:** {row['Boyut']:,} katılımcı (%{row['Yüzde']})")
            st.write(f"**Ortalama Maaş:** {row['Ortalama Maaş']} bin TL")
            st.write(f"**Ortalama Deneyim:** {row['Ortalama Deneyim']} yıl")
            st.write(f"**React Kullanımı:** %{row['React Kullanımı']}")

if __name__ == "__main__":
    main()

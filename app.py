"""
Sprint 4: Streamlit Dashboard Uygulaması

Bu uygulama, maaş analizi projesinin interaktif dashboard'unu sağlar:
- Maaş dağılımı görselleştirmeleri
- İnteraktif filtreleme seçenekleri
- İstatistiksel analiz sonuçları
- Teknoloji ROI analizi

Yazar: Erdem Gunal
Tarih: 2024-08-24
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Proje modüllerini import et - sadece gerekli olanları
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# from src.advanced_analysis import AdvancedAnalyzer  # Dashboard'da kullanılmıyor
# from src.statistical_analysis import StatisticalAnalyzer  # Dashboard'da kullanılmıyor

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Maaş Analizi Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
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
    .section-header {
        font-size: 2rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Veriyi yükle ve cache'le"""
    from src.utils import load_data as load_data_utils
    df = load_data_utils("data/cleaned_data.csv")
    return df

@st.cache_data
def load_analysis_results():
    """Analiz sonuçlarını yükle ve cache'le"""
    # İstatistiksel analiz sonuçları
    stats_df = pd.read_csv("tables/statistical_results_summary.csv")
    
    # İleri analiz sonuçları
    advanced_df = pd.read_csv("tables/advanced_analysis_results.csv")
    
    return stats_df, advanced_df

def main():
    """Ana dashboard fonksiyonu"""
    
    # Header
    st.markdown('<h1 class="main-header">💰 Maaş Analizi Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Türkiye Yazılım Geliştiricileri Maaş Analizi - 2024")
    
    # Veriyi yükle
    df = load_data()
    stats_df, advanced_df = load_analysis_results()
    
    # Sidebar - Filtreleme seçenekleri
    st.sidebar.header("🔍 Filtreleme Seçenekleri")
    
    # Cinsiyet filtresi
    gender_filter = st.sidebar.selectbox(
        "Cinsiyet",
        ["Tümü", "Erkek", "Kadın"],
        index=0
    )
    
    # Kariyer seviyesi filtresi
    career_levels = {1: 'Junior', 2: 'Mid', 3: 'Senior'}
    career_filter = st.sidebar.multiselect(
        "Kariyer Seviyesi",
        options=list(career_levels.values()),
        default=list(career_levels.values())
    )
    
    # Çalışma şekli filtresi
    work_types = {0: 'Remote', 1: 'Office', 2: 'Hybrid'}
    work_filter = st.sidebar.multiselect(
        "Çalışma Şekli",
        options=list(work_types.values()),
        default=list(work_types.values())
    )
    
    # Maaş aralığı filtresi
    min_salary = df['ortalama_maas'].min()
    max_salary = df['ortalama_maas'].max()
    salary_range = st.sidebar.slider(
        "Maaş Aralığı (bin TL)",
        min_value=float(min_salary),
        max_value=float(max_salary),
        value=(float(min_salary), float(max_salary))
    )
    
    # Filtreleme uygula
    filtered_df = df.copy()
    
    if gender_filter != "Tümü":
        gender_value = 0 if gender_filter == "Erkek" else 1
        filtered_df = filtered_df[filtered_df['cinsiyet'] == gender_value]
    
    if career_filter:
        career_values = [k for k, v in career_levels.items() if v in career_filter]
        filtered_df = filtered_df[filtered_df['kariyer_seviyesi'].isin(career_values)]
    
    if work_filter:
        work_values = [k for k, v in work_types.items() if v in work_filter]
        filtered_df = filtered_df[filtered_df['calisma_sekli'].isin(work_values)]
    
    filtered_df = filtered_df[
        (filtered_df['ortalama_maas'] >= salary_range[0]) & 
        (filtered_df['ortalama_maas'] <= salary_range[1])
    ]
    
    # Ana metrikler
    st.markdown('<h2 class="section-header">📊 Genel İstatistikler</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Toplam Katılımcı",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df):+,}" if len(filtered_df) != len(df) else None
        )
    
    with col2:
        avg_salary = filtered_df['ortalama_maas'].mean()
        st.metric(
            label="Ortalama Maaş",
            value=f"{avg_salary:.1f} bin TL",
            delta=f"{avg_salary - df['ortalama_maas'].mean():+.1f}" if len(filtered_df) != len(df) else None
        )
    
    with col3:
        median_salary = filtered_df['ortalama_maas'].median()
        st.metric(
            label="Medyan Maaş",
            value=f"{median_salary:.1f} bin TL",
            delta=f"{median_salary - df['ortalama_maas'].median():+.1f}" if len(filtered_df) != len(df) else None
        )
    
    with col4:
        std_salary = filtered_df['ortalama_maas'].std()
        st.metric(
            label="Standart Sapma",
            value=f"{std_salary:.1f} bin TL"
        )
    
    # Maaş dağılımı görselleştirmesi
    st.markdown('<h2 class="section-header">📈 Maaş Dağılımı</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram
        fig_hist = px.histogram(
            filtered_df, 
            x='ortalama_maas',
            nbins=30,
            title="Maaş Dağılımı - Histogram",
            labels={'ortalama_maas': 'Maaş (bin TL)', 'count': 'Geliştirici Sayısı'}
        )
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Box plot
        fig_box = px.box(
            filtered_df,
            y='ortalama_maas',
            title="Maaş Dağılımı - Box Plot",
            labels={'ortalama_maas': 'Maaş (bin TL)'}
        )
        fig_box.update_layout(height=400)
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Karşılaştırma analizleri
    st.markdown('<h2 class="section-header">🔍 Karşılaştırma Analizleri</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cinsiyet karşılaştırması
        from src.utils import get_gender_data
        gender_data = get_gender_data(filtered_df)
        
        if gender_data:
            gender_df = pd.DataFrame(gender_data)
            fig_gender = px.bar(
                gender_df,
                x='Cinsiyet',
                y='Ortalama Maaş',
                title="Cinsiyet ve Maaş Karşılaştırması",
                text='Ortalama Maaş'
            )
            fig_gender.update_traces(texttemplate='%{text:.1f} bin TL', textposition='outside')
            fig_gender.update_layout(height=400)
            st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Kariyer seviyesi karşılaştırması
        from src.utils import get_career_data
        career_data = get_career_data(filtered_df)
        
        if career_data:
            career_df = pd.DataFrame(career_data)
            fig_career = px.bar(
                career_df,
                x='Kariyer Seviyesi',
                y='Ortalama Maaş',
                title="Kariyer Seviyesi ve Maaş Karşılaştırması",
                text='Ortalama Maaş'
            )
            fig_career.update_traces(texttemplate='%{text:.1f} bin TL', textposition='outside')
            fig_career.update_layout(height=400)
            st.plotly_chart(fig_career, use_container_width=True)
    
    # Çalışma şekli ve lokasyon analizi
    st.markdown('<h2 class="section-header">🏢 Çalışma Şekli ve Lokasyon Analizi</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Çalışma şekli karşılaştırması
        from src.utils import get_work_type_data
        work_data = get_work_type_data(filtered_df)
        
        if work_data:
            work_df = pd.DataFrame(work_data)
            fig_work = px.bar(
                work_df,
                x='Çalışma Şekli',
                y='Ortalama Maaş',
                title="Çalışma Şekli ve Maaş Karşılaştırması",
                text='Ortalama Maaş'
            )
            fig_work.update_traces(texttemplate='%{text:.1f} bin TL', textposition='outside')
            fig_work.update_layout(height=400)
            st.plotly_chart(fig_work, use_container_width=True)
    
    with col2:
        # Lokasyon karşılaştırması
        from src.utils import get_location_data
        location_data = get_location_data(filtered_df)
        
        if location_data:
            location_df = pd.DataFrame(location_data)
            fig_location = px.bar(
                location_df,
                x='Lokasyon',
                y='Ortalama Maaş',
                title="Şirket Lokasyonu ve Maaş Karşılaştırması",
                text='Ortalama Maaş'
            )
            fig_location.update_traces(texttemplate='%{text:.1f} bin TL', textposition='outside')
            fig_location.update_layout(height=400)
            st.plotly_chart(fig_location, use_container_width=True)
    
    # Teknoloji analizi
    st.markdown('<h2 class="section-header">💻 Teknoloji Analizi</h2>', unsafe_allow_html=True)
    
    # React vs Non-React analizi
    col1, col2 = st.columns(2)
    
    with col1:
        react_data = []
        react_salary = filtered_df[filtered_df['frontend_react'] == 1]['ortalama_maas']
        non_react_salary = filtered_df[filtered_df['frontend_react'] == 0]['ortalama_maas']
        
        if len(react_salary) > 0:
            react_data.append({
                'Grup': 'React Kullanıcıları',
                'Ortalama Maaş': react_salary.mean(),
                'Katılımcı Sayısı': len(react_salary)
            })
        
        if len(non_react_salary) > 0:
            react_data.append({
                'Grup': 'React Kullanmayanlar',
                'Ortalama Maaş': non_react_salary.mean(),
                'Katılımcı Sayısı': len(non_react_salary)
            })
        
        if react_data:
            react_df = pd.DataFrame(react_data)
            fig_react = px.bar(
                react_df,
                x='Grup',
                y='Ortalama Maaş',
                title="React Kullanımı ve Maaş Karşılaştırması",
                text='Ortalama Maaş'
            )
            fig_react.update_traces(texttemplate='%{text:.1f} bin TL', textposition='outside')
            fig_react.update_layout(height=400)
            st.plotly_chart(fig_react, use_container_width=True)
    
    with col2:
        # En popüler programlama dilleri
        from src.utils import get_programming_language_usage
        lang_usage = get_programming_language_usage(filtered_df, min_usage_rate=5.0)
        
        if lang_usage:
            # En popüler 8 dil
            top_languages = dict(sorted(lang_usage.items(), key=lambda x: x[1], reverse=True)[:8])
            
            fig_lang = px.bar(
                x=list(top_languages.values()),
                y=list(top_languages.keys()),
                orientation='h',
                title="En Popüler Programlama Dilleri",
                labels={'x': 'Kullanım Oranı (%)', 'y': 'Programlama Dili'}
            )
            fig_lang.update_layout(height=400)
            st.plotly_chart(fig_lang, use_container_width=True)
    
    # İstatistiksel analiz sonuçları
    st.markdown('<h2 class="section-header">📊 İstatistiksel Analiz Sonuçları</h2>', unsafe_allow_html=True)
    
    # Anlamlı sonuçları göster
    significant_results = stats_df[stats_df['Significant'] == True]
    
    if len(significant_results) > 0:
        st.success(f"✅ {len(significant_results)} anlamlı istatistiksel sonuç bulundu!")
        
        for _, result in significant_results.iterrows():
            with st.expander(f"🔍 {result['Test']} - {result['Test_Type']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Test İstatistiği", f"{result['Statistic']:.4f}")
                
                with col2:
                    st.metric("P-Değeri", f"{result['P_Value']:.6f}")
                
                with col3:
                    st.metric("Etki Büyüklüğü", f"{result['Effect_Size']:.4f}")
                
                st.info(f"**Yorum:** {result['Interpretation']}")
    
    # İleri analiz sonuçları
    st.markdown('<h2 class="section-header">🚀 İleri Analiz Sonuçları</h2>', unsafe_allow_html=True)
    
    if len(advanced_df) > 0:
        for _, result in advanced_df.iterrows():
            with st.expander(f"🔬 {result['Analysis_Type']} - {result['Test_Name']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Test İstatistiği", f"{result['Statistic']:.4f}")
                
                with col2:
                    st.metric("P-Değeri", f"{result['P_Value']:.6f}")
                
                with col3:
                    st.metric("Anlamlı", "✅ Evet" if result['Significant'] else "❌ Hayır")
                
                st.info(f"**Yorum:** {result['Interpretation']}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>💰 Maaş Analizi Dashboard | Erdem Gunal | 2024</p>
        <p>Bu dashboard, Türkiye'deki yazılım geliştiricilerinin maaş verilerini analiz eder.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

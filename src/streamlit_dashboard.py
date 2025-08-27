"""
Sprint 3: Streamlit Dashboard (English)
Interactive dashboard for the salary analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="2025 Software Salary Analysis",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

LOCATION_NOTE = (
    "Note: Estimated location is inferred from company location and work mode "
    "(Office/Hybrid → company location). Not definitive."
)

@st.cache_data
def load_data():
    """Load and cache the dataset"""
    df = pd.read_csv('data/2025_cleaned_data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def main():
    """Main dashboard function"""

    # Title
    st.title("💰 2025 Software Salary Analysis")
    st.markdown("**Detailed analysis of 2,969 software professionals surveyed on Aug 20-21, 2025**")

    # Data
    df = load_data()

    # Sidebar
    st.sidebar.header("📊 Filters")

    experience_filter = st.sidebar.multiselect(
        "Years of Experience",
        options=sorted(df['experience_years'].dropna().unique()),
        default=sorted(df['experience_years'].dropna().unique())
    )

    seniority_filter = st.sidebar.multiselect(
        "Career Level (IC scale)",
        options=sorted(df['seniority_level_ic'].dropna().unique()),
        default=sorted(df['seniority_level_ic'].dropna().unique())
    )

    work_mode_options = [c.replace('work_mode_', '') for c in df.columns if c.startswith('work_mode_')]
    work_mode_filter = st.sidebar.multiselect(
        "Work Mode",
        options=work_mode_options,
        default=work_mode_options
    )

    # Apply filters
    filtered_df = df.copy()
    if experience_filter:
        filtered_df = filtered_df[filtered_df['experience_years'].isin(experience_filter)]
    if seniority_filter:
        filtered_df = filtered_df[filtered_df['seniority_level_ic'].isin(seniority_filter)]
    if work_mode_filter:
        mask = filtered_df[[f'work_mode_{m}' for m in work_mode_filter]].sum(axis=1) > 0
        filtered_df = filtered_df[mask]

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="📈 Average Salary",
            value=f"{filtered_df['salary_numeric'].mean():.1f}k TL",
            delta=f"{filtered_df['salary_numeric'].mean() - df['salary_numeric'].mean():.1f}k TL"
        )
    with col2:
        st.metric(label="📊 Median Salary", value=f"{filtered_df['salary_numeric'].median():.1f}k TL")
    with col3:
        st.metric(label="👥 Participants", value=f"{len(filtered_df):,}")
    with col4:
        male_ratio = (filtered_df['gender'] == 0).mean() * 100
        st.metric(label="👨 Male Ratio", value=f"{male_ratio:.1f}%")

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Distributions",
        "💼 Career",
        "🌍 Location & Work Mode",
        "⚡ Technology ROI",
        "📈 Stats"
    ])

    with tab1:
        st.header("📊 Salary Distributions")
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(
                filtered_df,
                x='salary_numeric',
                nbins=30,
                title="Salary Distribution",
                labels={'salary_numeric': 'Monthly Net Salary (thousand TL)', 'count': 'Count'}
            )
            fig.add_vline(x=filtered_df['salary_numeric'].mean(), line_dash="dash", line_color="red",
                          annotation_text=f"Avg: {filtered_df['salary_numeric'].mean():.1f}")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.box(
                filtered_df,
                x='gender',
                y='salary_numeric',
                title="Salary by Gender",
                labels={'gender': 'Gender (0=Male, 1=Female)', 'salary_numeric': 'Monthly Net Salary (thousand TL)'}
            )
            fig.update_xaxes(ticktext=['Male', 'Female'], tickvals=[0, 1])
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("💼 Career Analysis")
        fig = px.box(
            filtered_df,
            x='seniority_level_ic',
            y='salary_numeric',
            title="Salary by Career Level (IC)",
            labels={'seniority_level_ic': 'Career Level (0=Mgmt,1=Jr,2=Mid,3=Sr,4=Staff,5=Arch)', 'salary_numeric': 'Monthly Net Salary (thousand TL)'}
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Average Salary by Role (Top 15)")
        role_cols = [c for c in filtered_df.columns if c.startswith('role_')]
        rows = []
        for c in role_cols:
            name = c.replace('role_', '').replace('_', ' ')
            vals = filtered_df.loc[filtered_df[c] == 1, 'salary_numeric']
            if len(vals) > 5:
                rows.append({'Role': name, 'Average Salary': vals.mean(), 'Participants': len(vals)})
        role_df = pd.DataFrame(rows).sort_values('Average Salary', ascending=False).head(15)
        fig = px.bar(role_df, x='Average Salary', y='Role', title="Highest Paying Roles",
                     labels={'Average Salary': 'Monthly Net Salary (thousand TL)'})
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("🌍 Location & Work Mode")
        c1, c2 = st.columns(2)
        with c1:
            data = []
            for m in ['Remote', 'Hybrid', 'Office']:
                col = f'work_mode_{m}'
                if col in filtered_df.columns:
                    subset = filtered_df[filtered_df[col] == 1]
                    if len(subset) > 0:
                        data.append({'Work Mode': m, 'Average Salary': subset['salary_numeric'].mean(), 'Participants': len(subset)})
            mode_df = pd.DataFrame(data)
            fig = px.bar(mode_df, x='Work Mode', y='Average Salary', title="Average Salary by Work Mode",
                         labels={'Average Salary': 'Monthly Net Salary (thousand TL)'} )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            data = []
            for loc in ['Turkiye', 'Avrupa', 'Amerika', 'Yurtdisi_TR_hub']:
                col = f'company_location_{loc}'
                if col in filtered_df.columns:
                    subset = filtered_df[filtered_df[col] == 1]
                    if len(subset) > 0:
                        data.append({'Location': loc.replace('_', ' '), 'Average Salary': subset['salary_numeric'].mean(), 'Participants': len(subset)})
            loc_df = pd.DataFrame(data)
            fig = px.bar(loc_df, x='Location', y='Average Salary', title="Average Salary by Company Location",
                         labels={'Average Salary': 'Monthly Net Salary (thousand TL)'} )
            st.plotly_chart(fig, use_container_width=True)

        st.info(f"ℹ️ {LOCATION_NOTE}")

    with tab4:
        st.header("⚡ Technology ROI")
        st.subheader("Programming Languages")
        lang_cols = [c for c in filtered_df.columns if c.startswith('programming_') and c != 'programming_Hicbiri']
        rows = []
        for c in lang_cols:
            users = filtered_df[filtered_df[c] == 1]['salary_numeric']
            non = filtered_df[filtered_df[c] == 0]['salary_numeric']
            if len(users) > 10 and len(non) > 10:
                rows.append({'Technology': c.replace('programming_', '').replace('_', ' '),
                             'ROI': users.mean() - non.mean(), 'Users': len(users)})
        lang_df = pd.DataFrame(rows).sort_values('ROI', ascending=False)
        fig = px.bar(lang_df.head(15), x='ROI', y='Technology', title="Top Programming Languages by ROI",
                     labels={'ROI': 'Average Salary Difference (thousand TL)'}, color='ROI', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Frontend Technologies")
        fe_cols = [c for c in filtered_df.columns if c.startswith('frontend_') and c != 'frontend_Kullanmiyorum']
        rows = []
        for c in fe_cols:
            users = filtered_df[filtered_df[c] == 1]['salary_numeric']
            non = filtered_df[filtered_df[c] == 0]['salary_numeric']
            if len(users) > 10 and len(non) > 10:
                rows.append({'Technology': c.replace('frontend_', '').replace('_', ' '),
                             'ROI': users.mean() - non.mean(), 'Users': len(users)})
        fe_df = pd.DataFrame(rows).sort_values('ROI', ascending=False)
        fig = px.bar(fe_df, x='ROI', y='Technology', title="Frontend Technologies ROI",
                     labels={'ROI': 'Average Salary Difference (thousand TL)'}, color='ROI', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.header("📈 Statistical Tests")
        # React vs Non-React
        react = filtered_df[filtered_df['frontend_React'] == 1]['salary_numeric'] if 'frontend_React' in filtered_df.columns else pd.Series(dtype=float)
        non_react = filtered_df[filtered_df['frontend_React'] == 0]['salary_numeric'] if 'frontend_React' in filtered_df.columns else pd.Series(dtype=float)
        if len(react) > 0 and len(non_react) > 0:
            _, p = ttest_ind(react, non_react, equal_var=False)
            st.write("**React vs Non-React (t-test):**")
            st.write(f"- React users avg: {react.mean():.1f}k TL")
            st.write(f"- Non-React users avg: {non_react.mean():.1f}k TL")
            st.write(f"- Difference: {react.mean() - non_react.mean():.1f}k TL")
            st.write(f"- p-value: {p:.4f}")
            st.write(f"- Significant: {'✅ Yes' if p < 0.05 else '❌ No'}")
        # Remote vs Office
        remote = filtered_df[filtered_df['work_mode_Remote'] == 1]['salary_numeric'] if 'work_mode_Remote' in filtered_df.columns else pd.Series(dtype=float)
        office = filtered_df[filtered_df['work_mode_Office'] == 1]['salary_numeric'] if 'work_mode_Office' in filtered_df.columns else pd.Series(dtype=float)
        if len(remote) > 0 and len(office) > 0:
            _, p = ttest_ind(remote, office, equal_var=False)
            st.write("**Remote vs Office (t-test):**")
            st.write(f"- Remote avg: {remote.mean():.1f}k TL")
            st.write(f"- Office avg: {office.mean():.1f}k TL")
            st.write(f"- Difference: {remote.mean() - office.mean():.1f}k TL")
            st.write(f"- p-value: {p:.4f}")
            st.write(f"- Significant: {'✅ Yes' if p < 0.05 else '❌ No'}")

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>📊 <strong>2025 Software Salary Analysis</strong> | Data: Aug 20-21, 2025 (2,969 participants)</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

"""
Sprint 2: Core Analyses and Visualizations (English)
Generates required plots: boxplots, bar charts, scatter (career timeline), heatmap (tech/tool vs salary), and Sankey (seniority to role).
All titles/labels are in English. Location-related plots include the mandatory disclaimer.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import ttest_ind, mannwhitneyu, f_oneway, kruskal

sns.set_palette("husl")
plt.rcParams['font.family'] = 'DejaVu Sans'

FIG_DIR = 'figures'
LOCATION_NOTE = "Note: Estimated location is inferred from company location and work mode (Office/Hybrid → company location). Not definitive."

def load_data() -> pd.DataFrame:
    df = pd.read_csv('data/2025_cleaned_data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def ensure_dirs():
    os.makedirs(FIG_DIR, exist_ok=True)

def calculate_effect_size(group1, group2):
    """Calculate Cohen's d effect size"""
    n1, n2 = len(group1), len(group2)
    pooled_std = np.sqrt(((n1 - 1) * group1.var() + (n2 - 1) * group2.var()) / (n1 + n2 - 2))
    return (group1.mean() - group2.mean()) / pooled_std

# ============ BOX PLOTS ============

def boxplots(df: pd.DataFrame):
    print('Creating boxplots...')
    # Seniority vs Salary
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='seniority_level_ic', y='salary_numeric')
    plt.title('Salary Distribution by Career Level', fontsize=14, fontweight='bold')
    plt.xlabel('Career Level (0=Management, 1=Junior, 2=Mid, 3=Senior, 4=Staff, 5=Architect)')
    plt.ylabel('Monthly Net Salary (thousand TL)')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'boxplot_seniority.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Management Level vs Salary (if exists)
    if 'management_level' in df.columns:
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x='management_level', y='salary_numeric')
        plt.title('Salary Distribution by Management Level', fontsize=14, fontweight='bold')
        plt.xlabel('Management Level')
        plt.ylabel('Monthly Net Salary (thousand TL)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, 'boxplot_management_level.png'), dpi=300, bbox_inches='tight')
        plt.close()

    # Work Mode vs Salary
    work_modes = []
    work_labels = []
    for mode in ['Remote', 'Hybrid', 'Office']:
        col = f'work_mode_{mode}'
        if col in df.columns:
            vals = df.loc[df[col] == 1, 'salary_numeric']
            if len(vals) > 0:
                work_modes.append(vals)
                work_labels.append(mode)
    if work_modes:
        plt.figure(figsize=(10, 6))
        plt.boxplot(work_modes, labels=work_labels)
        plt.title('Salary Distribution by Work Mode', fontsize=14, fontweight='bold')
        plt.ylabel('Monthly Net Salary (thousand TL)')
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, 'boxplot_work_mode.png'), dpi=300, bbox_inches='tight')
        plt.close()

    # Company Location vs Salary
    # data_dict mapping for Turkish → English labels
    location_label_map = {
        'Turkiye': 'Türkiye',
        'Avrupa': 'Europe',
        'Amerika': 'America',
        'Yurtdisi_TR_hub': 'Overseas TR hub'
    }
    loc_series = []
    loc_labels = []
    for loc in ['Turkiye', 'Avrupa', 'Amerika', 'Yurtdisi_TR_hub']:
        col = f'company_location_{loc}'
        if col in df.columns:
            vals = df.loc[df[col] == 1, 'salary_numeric']
            if len(vals) > 0:
                loc_series.append(vals)
                loc_labels.append(location_label_map.get(loc, loc.replace('_', ' ')))
    if loc_series:
        plt.figure(figsize=(12, 6))
        plt.boxplot(loc_series, labels=loc_labels)
        plt.title('Salary Distribution by Company Location', fontsize=14, fontweight='bold')
        plt.ylabel('Monthly Net Salary (thousand TL)')
        plt.figtext(0.5, 0.01, LOCATION_NOTE, ha='center', fontsize=9, style='italic')
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, 'boxplot_company_location.png'), dpi=300, bbox_inches='tight')
        plt.close()

    # Gender vs Salary
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x='gender', y='salary_numeric')
    plt.title('Salary Distribution by Gender', fontsize=14, fontweight='bold')
    plt.xlabel('Gender (0=Male, 1=Female)')
    plt.ylabel('Monthly Net Salary (thousand TL)')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'boxplot_gender.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Employment Type vs Salary (if columns exist)
    # data_dict mapping for Turkish → English labels
    employment_label_map = {
        'Freelance': 'Freelance',
        'Kendi_isim': 'Self-employed',
        'Tam_zamanli': 'Full-time',
        'Yari_zamanli': 'Part-time'
    }
    emp_cols = [c for c in df.columns if c.startswith('employment_type_')]
    if emp_cols:
        data = []
        labels = []
        for c in emp_cols:
            vals = df.loc[df[c] == 1, 'salary_numeric']
            if len(vals) > 0:
                data.append(vals)
                raw = c.replace('employment_type_', '')
                labels.append(employment_label_map.get(raw, raw.replace('_', ' ')))
        if data:
            plt.figure(figsize=(12, 6))
            plt.boxplot(data, labels=labels)
            plt.title('Salary Distribution by Employment Type', fontsize=14, fontweight='bold')
            plt.ylabel('Monthly Net Salary (thousand TL)')
            plt.xticks(rotation=20)
            plt.tight_layout()
            plt.savefig(os.path.join(FIG_DIR, 'boxplot_employment_type.png'), dpi=300, bbox_inches='tight')
            plt.close()

# ============ BAR PLOTS (ROI and Roles) ============

def barplots(df: pd.DataFrame):
    print('Creating bar plots (ROI and roles)...')
    # Role average salaries (top 15)
    role_cols = [c for c in df.columns if c.startswith('role_')]
    role_stats = []
    for c in role_cols:
        role_name = c.replace('role_', '').replace('_', ' ')
        vals = df.loc[df[c] == 1, 'salary_numeric']
        if len(vals) >= 5:
            role_stats.append((role_name, float(vals.mean()), int(len(vals))))
    role_stats.sort(key=lambda x: x[1], reverse=True)
    if role_stats:
        names, means, counts = zip(*role_stats[:15])
        plt.figure(figsize=(12, 8))
        bars = plt.barh(names, means, color='skyblue')
        plt.gca().invert_yaxis()
        plt.title('Average Salary by Role (Top 15)', fontsize=14, fontweight='bold')
        plt.xlabel('Average Monthly Net Salary (thousand TL)')
        for i, (bar, m, n) in enumerate(zip(bars, means, counts)):
            plt.text(m + 2, i, f'{m:.1f}\n({n} people)', va='center', fontsize=9)
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, 'barplot_role_salaries.png'), dpi=300, bbox_inches='tight')
        plt.close()

    # Technology ROI (programming_, frontend_, tools_)
    def roi_for_prefix(prefix: str, exclude: set[str], out_name: str, title: str, ylabel: str):
        cols = [c for c in df.columns if c.startswith(prefix) and c not in exclude]
        rows = []
        for c in cols:
            users = df.loc[df[c] == 1, 'salary_numeric']
            non_users = df.loc[df[c] == 0, 'salary_numeric']
            if len(users) >= 10 and len(non_users) >= 10:
                roi = float(users.mean() - non_users.mean())
                rows.append((c.replace(prefix, '').replace('_', ' '), roi, int(len(users))))
        rows.sort(key=lambda x: x[1], reverse=True)
        if rows:
            names, rois, counts = zip(*rows[:15])
            plt.figure(figsize=(12, 8))
            colors = ['green' if r > 0 else 'red' for r in rois]
            bars = plt.barh(names, rois, color=colors)
            plt.gca().invert_yaxis()
            plt.title(title, fontsize=14, fontweight='bold')
            plt.xlabel('Average Salary Difference vs Non-users (thousand TL)')
            plt.ylabel(ylabel)
            for i, (bar, r, n) in enumerate(zip(bars, rois, counts)):
                xoff = 1 if r >= 0 else -1
                halign = 'left' if r >= 0 else 'right'
                plt.text(r + xoff, i, f'{r:.1f}\n({n} users)', va='center', ha=halign, fontsize=9)
            plt.axvline(0, color='black', lw=0.8, alpha=0.3)
            plt.tight_layout()
            plt.savefig(os.path.join(FIG_DIR, out_name), dpi=300, bbox_inches='tight')
            plt.close()

    roi_for_prefix('programming_', {'programming_Hicbiri'}, 'barplot_programming_roi.png', 'Programming Languages Salary ROI', 'Programming Language')
    roi_for_prefix('frontend_', {'frontend_Kullanmiyorum'}, 'barplot_frontend_roi.png', 'Frontend Technologies Salary ROI', 'Frontend Technology')
    roi_for_prefix('tools_', set(), 'barplot_tools_roi.png', 'Tools Salary ROI', 'Tool')

# ============ GENDER-BASED TECHNOLOGY USAGE ============

def gender_technology_usage(df: pd.DataFrame):
    print('Creating gender-based technology usage plots...')
    
    # Programming languages by gender
    lang_cols = [c for c in df.columns if c.startswith('programming_') and c != 'programming_Hicbiri']
    if lang_cols:
        # Top 10 languages by overall usage
        lang_usage = []
        for col in lang_cols:
            usage = df[col].mean()
            lang_usage.append((col.replace('programming_', '').replace('_', ' '), usage))
        lang_usage.sort(key=lambda x: x[1], reverse=True)
        top_langs = [col.replace('programming_', '') for col, _ in lang_usage[:10]]
        
        # Create gender comparison for top languages
        gender_data = []
        for lang in top_langs:
            col = f'programming_{lang}'
            if col in df.columns:
                male_usage = df[df['gender'] == 0][col].mean() * 100
                female_usage = df[df['gender'] == 1][col].mean() * 100
                gender_data.append((lang.replace('_', ' '), male_usage, female_usage))
        
        if gender_data:
            langs, male_pct, female_pct = zip(*gender_data)
            x = np.arange(len(langs))
            width = 0.35
            
            plt.figure(figsize=(14, 8))
            plt.bar(x - width/2, male_pct, width, label='Male', color='skyblue')
            plt.bar(x + width/2, female_pct, width, label='Female', color='lightcoral')
            plt.xlabel('Programming Language')
            plt.ylabel('Usage Percentage (%)')
            plt.title('Programming Language Usage by Gender (Top 10)', fontsize=14, fontweight='bold')
            plt.xticks(x, langs, rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(FIG_DIR, 'barplot_gender_programming.png'), dpi=300, bbox_inches='tight')
            plt.close()
    
    # Frontend technologies by gender
    frontend_cols = [c for c in df.columns if c.startswith('frontend_') and c != 'frontend_Kullanmiyorum']
    if frontend_cols:
        # Top 8 frontend technologies
        frontend_usage = []
        for col in frontend_cols:
            usage = df[col].mean()
            frontend_usage.append((col.replace('frontend_', '').replace('_', ' '), usage))
        frontend_usage.sort(key=lambda x: x[1], reverse=True)
        top_frontend = [col.replace('frontend_', '') for col, _ in frontend_usage[:8]]
        
        # Create gender comparison for top frontend technologies
        gender_data = []
        for tech in top_frontend:
            col = f'frontend_{tech}'
            if col in df.columns:
                male_usage = df[df['gender'] == 0][col].mean() * 100
                female_usage = df[df['gender'] == 1][col].mean() * 100
                gender_data.append((tech.replace('_', ' '), male_usage, female_usage))
        
        if gender_data:
            techs, male_pct, female_pct = zip(*gender_data)
            x = np.arange(len(techs))
            width = 0.35
            
            plt.figure(figsize=(12, 6))
            plt.bar(x - width/2, male_pct, width, label='Male', color='skyblue')
            plt.bar(x + width/2, female_pct, width, label='Female', color='lightcoral')
            plt.xlabel('Frontend Technology')
            plt.ylabel('Usage Percentage (%)')
            plt.title('Frontend Technology Usage by Gender (Top 8)', fontsize=14, fontweight='bold')
            plt.xticks(x, techs, rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(FIG_DIR, 'barplot_gender_frontend.png'), dpi=300, bbox_inches='tight')
            plt.close()

# ============ SCATTER (Career Timeline) ============

def scatter_career_timeline(df: pd.DataFrame):
    print('Creating career timeline scatter...')
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='experience_years', y='salary_numeric', hue='seniority_level_ic', palette='viridis', s=25, edgecolor=None)
    plt.title('Experience vs Salary (colored by Career Level)', fontsize=14, fontweight='bold')
    plt.xlabel('Years of Experience')
    plt.ylabel('Monthly Net Salary (thousand TL)')
    plt.legend(title='Career Level', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'scatter_experience_salary.png'), dpi=300, bbox_inches='tight')
    plt.close()

# ============ HEATMAP (Tech/Tools vs Salary correlation) ============

def heatmap_tech_salary(df: pd.DataFrame):
    print('Creating technology/tool salary heatmap...')
    tech_cols = [c for c in df.columns if c.startswith('programming_') or c.startswith('frontend_') or c.startswith('tools_')]
    if not tech_cols:
        return
    corr_rows = []
    index = []
    for c in tech_cols:
        if df[c].nunique() > 1:
            corr = df[[c, 'salary_numeric']].corr().iloc[0, 1]
            corr_rows.append([corr])
            index.append(c.replace('programming_', '').replace('frontend_', '').replace('tools_', '').replace('_', ' '))
    if not corr_rows:
        return
    mat = np.array(corr_rows)
    plt.figure(figsize=(8, max(6, len(index) * 0.2)))
    sns.heatmap(mat, annot=False, cmap='RdYlGn', center=0, yticklabels=index, xticklabels=['Correlation with Salary'])
    plt.title('Correlation of Technologies/Tools with Salary', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'heatmap_tech_tool_salary.png'), dpi=300, bbox_inches='tight')
    plt.close()

# ============ HOURLY PARTICIPATION (bar + optional role heatmap) ============

def hourly_participation(df: pd.DataFrame):
    print('Creating hourly participation plots...')
    df = df.copy()
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour

    # Average salary by hour bar plot
    hourly = df.groupby('hour', as_index=False).agg(
        avg_salary=('salary_numeric', 'mean'),
        participants=('salary_numeric', 'size')
    )
    plt.figure(figsize=(12, 6))
    sns.barplot(data=hourly, x='hour', y='avg_salary', color='steelblue')
    plt.title('Average Salary by Survey Hour', fontsize=14, fontweight='bold')
    plt.xlabel('Hour of Day (0-23)')
    plt.ylabel('Average Monthly Net Salary (thousand TL)')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'barplot_hourly_avg_salary.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Participants count by hour bar plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=hourly, x='hour', y='participants', color='indianred')
    plt.title('Participants by Survey Hour', fontsize=14, fontweight='bold')
    plt.xlabel('Hour of Day (0-23)')
    plt.ylabel('Number of Participants')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'barplot_hourly_participants.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Optional: Role distribution heatmap by hour (share of each role among participants at that hour)
    role_cols = [c for c in df.columns if c.startswith('role_')]
    if role_cols:
        role_long = []
        for rc in role_cols:
            rname = rc.replace('role_', '').replace('_', ' ')
            tmp = df.groupby('hour')[rc].mean()  # share using 0/1 columns
            role_long.append(tmp.rename(rname))
        role_mat = pd.concat(role_long, axis=1).fillna(0.0)
        # Keep top 12 roles by overall mean share to keep it readable
        top_roles = role_mat.mean().sort_values(ascending=False).head(12).index
        role_mat = role_mat[top_roles]
        plt.figure(figsize=(12, 6))
        sns.heatmap(role_mat.T, cmap='Blues', cbar_kws={'label': 'Share at Hour'})
        plt.title('Role Distribution by Hour (Share)', fontsize=14, fontweight='bold')
        plt.xlabel('Hour of Day (0-23)')
        plt.ylabel('Role')
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, 'heatmap_roles_by_hour.png'), dpi=300, bbox_inches='tight')
        plt.close()

# ============ SANKEY (Career Level → Role distribution) ============

def sankey_seniority_to_role(df: pd.DataFrame):
    print('Creating Sankey diagram (career level to role)...')
    # Build nodes: career levels + roles
    level_map = {
        0: 'Management', 1: 'Junior', 2: 'Mid', 3: 'Senior', 4: 'Staff', 5: 'Architect'
    }
    role_cols = [c for c in df.columns if c.startswith('role_')]
    # Count flows from level to each role
    flows = []  # (level_name, role_name, count)
    for lvl, lvl_name in level_map.items():
        subset = df[df['seniority_level_ic'] == lvl]
        if subset.empty:
            continue
        for rc in role_cols:
            role_name = rc.replace('role_', '').replace('_', ' ')
            count = int((subset[rc] == 1).sum())
            if count > 0:
                flows.append((lvl_name, role_name, count))
    if not flows:
        return

    levels = sorted(list({f[0] for f in flows}), key=lambda x: list(level_map.values()).index(x))
    roles = sorted(list({f[1] for f in flows}))
    nodes = levels + roles
    node_index = {n: i for i, n in enumerate(nodes)}

    source = [node_index[s] for s, _, _ in flows]
    target = [node_index[t] for _, t, _ in flows]
    value = [v for _, _, v in flows]

    fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=18, line=dict(color='black', width=0.5), label=nodes),
        link=dict(source=source, target=target, value=value)
    )])
    fig.update_layout(title_text='Career Level to Role Distribution (Sankey)', font_size=12)

    # Save interactive and attempt static export if kaleido is installed
    html_path = os.path.join(FIG_DIR, 'sankey_career_level_role.html')
    fig.write_html(html_path)
    try:
        fig.write_image(os.path.join(FIG_DIR, 'sankey_career_level_role.png'), scale=2)
    except Exception:
        # Skip static image if engine is missing; HTML is sufficient
        pass

# ============ STATISTICAL TESTS WITH EFFECT SIZES ============

def perform_statistical_tests(df: pd.DataFrame):
    """Perform hypothesis tests with effect sizes"""
    print('Performing statistical tests with effect sizes...')
    
    results = {}
    
    # React vs Non-React
    if 'frontend_React' in df.columns:
        react_salaries = df[df['frontend_React'] == 1]['salary_numeric']
        non_react_salaries = df[df['frontend_React'] == 0]['salary_numeric']
        
        if len(react_salaries) > 10 and len(non_react_salaries) > 10:
            t_stat, p_value = ttest_ind(react_salaries, non_react_salaries, equal_var=False)
            effect_size = calculate_effect_size(react_salaries, non_react_salaries)
            
            results['react_vs_non_react'] = {
                'react_mean': react_salaries.mean(),
                'non_react_mean': non_react_salaries.mean(),
                'mean_diff': react_salaries.mean() - non_react_salaries.mean(),
                'p_value': p_value,
                'effect_size': effect_size,
                'significant': p_value < 0.05,
                'react_count': len(react_salaries),
                'non_react_count': len(non_react_salaries)
            }
    
    # Remote vs Office
    if 'work_mode_Remote' in df.columns and 'work_mode_Office' in df.columns:
        remote_salaries = df[df['work_mode_Remote'] == 1]['salary_numeric']
        office_salaries = df[df['work_mode_Office'] == 1]['salary_numeric']
        
        if len(remote_salaries) > 10 and len(office_salaries) > 10:
            t_stat, p_value = ttest_ind(remote_salaries, office_salaries, equal_var=False)
            effect_size = calculate_effect_size(remote_salaries, office_salaries)
            
            results['remote_vs_office'] = {
                'remote_mean': remote_salaries.mean(),
                'office_mean': office_salaries.mean(),
                'mean_diff': remote_salaries.mean() - office_salaries.mean(),
                'p_value': p_value,
                'effect_size': effect_size,
                'significant': p_value < 0.05,
                'remote_count': len(remote_salaries),
                'office_count': len(office_salaries)
            }
    
    # Europe vs Turkey
    if 'company_location_Avrupa' in df.columns and 'company_location_Turkiye' in df.columns:
        europe_salaries = df[df['company_location_Avrupa'] == 1]['salary_numeric']
        turkey_salaries = df[df['company_location_Turkiye'] == 1]['salary_numeric']
        
        if len(europe_salaries) > 10 and len(turkey_salaries) > 10:
            t_stat, p_value = ttest_ind(europe_salaries, turkey_salaries, equal_var=False)
            effect_size = calculate_effect_size(europe_salaries, turkey_salaries)
            
            results['europe_vs_turkey'] = {
                'europe_mean': europe_salaries.mean(),
                'turkey_mean': turkey_salaries.mean(),
                'mean_diff': europe_salaries.mean() - turkey_salaries.mean(),
                'p_value': p_value,
                'effect_size': effect_size,
                'significant': p_value < 0.05,
                'europe_count': len(europe_salaries),
                'turkey_count': len(turkey_salaries)
            }
    
    # Gender gap
    male_salaries = df[df['gender'] == 0]['salary_numeric']
    female_salaries = df[df['gender'] == 1]['salary_numeric']
    
    if len(male_salaries) > 10 and len(female_salaries) > 10:
        t_stat, p_value = ttest_ind(male_salaries, female_salaries, equal_var=False)
        effect_size = calculate_effect_size(male_salaries, female_salaries)
        
        results['gender_gap'] = {
            'male_mean': male_salaries.mean(),
            'female_mean': female_salaries.mean(),
            'mean_diff': male_salaries.mean() - female_salaries.mean(),
            'p_value': p_value,
            'effect_size': effect_size,
            'significant': p_value < 0.05,
            'male_count': len(male_salaries),
            'female_count': len(female_salaries)
        }
    
    # Print results
    for test_name, result in results.items():
        print(f"\n{test_name.replace('_', ' ').title()}:")
        print(f"  Mean difference: {result['mean_diff']:.1f} thousand TL")
        print(f"  P-value: {result['p_value']:.4f}")
        print(f"  Effect size (Cohen's d): {result['effect_size']:.3f}")
        print(f"  Significant: {result['significant']}")
    
    return results

# ============ MAIN ==========

def main():
    print('Sprint 2 analyses (English) started...')
    ensure_dirs()
    df = load_data()
    print(f'Data loaded: {df.shape}')

    # Perform statistical tests with effect sizes
    test_results = perform_statistical_tests(df)

    # Generate plots
    boxplots(df)
    barplots(df)
    gender_technology_usage(df)
    scatter_career_timeline(df)
    heatmap_tech_salary(df)
    hourly_participation(df)
    sankey_seniority_to_role(df)

    print('✅ Sprint 2 analyses completed. Files saved under figures/.')

if __name__ == '__main__':
    main()

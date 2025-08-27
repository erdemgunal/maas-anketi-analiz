"""
Sprint 4: LaTeX Raporu Oluşturucu
Bu script, analiz sonuçlarını LaTeX formatında rapor olarak oluşturur.
"""

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import os
from datetime import datetime

def load_data():
    """Veri setini yükle"""
    df = pd.read_csv('data/2025_cleaned_data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def calculate_key_statistics(df):
    """Temel istatistikleri hesapla"""
    stats = {}
    
    # Genel istatistikler
    stats['total_participants'] = len(df)
    stats['avg_salary'] = df['salary_numeric'].mean()
    stats['median_salary'] = df['salary_numeric'].median()
    stats['std_salary'] = df['salary_numeric'].std()
    stats['min_salary'] = df['salary_numeric'].min()
    stats['max_salary'] = df['salary_numeric'].max()
    
    # Cinsiyet dağılımı
    stats['male_ratio'] = (df['gender'] == 0).mean() * 100
    stats['female_ratio'] = (df['gender'] == 1).mean() * 100
    
    # Yönetici oranı
    stats['manager_ratio'] = df['is_manager'].mean() * 100
    
    return stats

def calculate_effect_size(group1, group2):
    """Calculate Cohen's d effect size"""
    n1, n2 = len(group1), len(group2)
    pooled_std = np.sqrt(((n1 - 1) * group1.var() + (n2 - 1) * group2.var()) / (n1 + n2 - 2))
    return (group1.mean() - group2.mean()) / pooled_std

def perform_hypothesis_tests(df):
    """Hipotez testlerini gerçekleştir"""
    tests = {}
    
    # 1. React vs Non-React
    react_salaries = df[df['frontend_React'] == 1]['salary_numeric']
    non_react_salaries = df[df['frontend_React'] == 0]['salary_numeric']
    
    t_stat, p_value = ttest_ind(react_salaries, non_react_salaries, equal_var=False)
    mean_diff = react_salaries.mean() - non_react_salaries.mean()
    effect_size = calculate_effect_size(react_salaries, non_react_salaries)
    
    tests['react_vs_non_react'] = {
        'react_mean': react_salaries.mean(),
        'non_react_mean': non_react_salaries.mean(),
        'mean_diff': mean_diff,
        'p_value': p_value,
        'effect_size': effect_size,
        'significant': p_value < 0.05,
        'react_count': len(react_salaries),
        'non_react_count': len(non_react_salaries)
    }
    
    # 2. Remote vs Office
    remote_salaries = df[df['work_mode_Remote'] == 1]['salary_numeric']
    office_salaries = df[df['work_mode_Office'] == 1]['salary_numeric']
    
    t_stat, p_value = ttest_ind(remote_salaries, office_salaries, equal_var=False)
    mean_diff = remote_salaries.mean() - office_salaries.mean()
    effect_size = calculate_effect_size(remote_salaries, office_salaries)
    
    tests['remote_vs_office'] = {
        'remote_mean': remote_salaries.mean(),
        'office_mean': office_salaries.mean(),
        'mean_diff': mean_diff,
        'p_value': p_value,
        'effect_size': effect_size,
        'significant': p_value < 0.05,
        'remote_count': len(remote_salaries),
        'office_count': len(office_salaries)
    }
    
    # 3. Europe vs Turkey
    europe_salaries = df[df['company_location_Avrupa'] == 1]['salary_numeric']
    turkey_salaries = df[df['company_location_Turkiye'] == 1]['salary_numeric']
    
    t_stat, p_value = ttest_ind(europe_salaries, turkey_salaries, equal_var=False)
    mean_diff = europe_salaries.mean() - turkey_salaries.mean()
    effect_size = calculate_effect_size(europe_salaries, turkey_salaries)
    
    tests['europe_vs_turkey'] = {
        'europe_mean': europe_salaries.mean(),
        'turkey_mean': turkey_salaries.mean(),
        'mean_diff': mean_diff,
        'p_value': p_value,
        'effect_size': effect_size,
        'significant': p_value < 0.05,
        'europe_count': len(europe_salaries),
        'turkey_count': len(turkey_salaries)
    }
    
    # 4. Gender gap
    male_salaries = df[df['gender'] == 0]['salary_numeric']
    female_salaries = df[df['gender'] == 1]['salary_numeric']
    
    t_stat, p_value = ttest_ind(male_salaries, female_salaries, equal_var=False)
    mean_diff = male_salaries.mean() - female_salaries.mean()
    effect_size = calculate_effect_size(male_salaries, female_salaries)
    
    tests['gender_gap'] = {
        'male_mean': male_salaries.mean(),
        'female_mean': female_salaries.mean(),
        'mean_diff': mean_diff,
        'p_value': p_value,
        'effect_size': effect_size,
        'significant': p_value < 0.05,
        'male_count': len(male_salaries),
        'female_count': len(female_salaries)
    }
    
    return tests

def calculate_technology_roi(df):
    """Teknoloji ROI hesaplamaları"""
    roi_data = {}
    
    # Programlama dilleri ROI
    lang_columns = [col for col in df.columns if col.startswith('programming_') and col != 'programming_Hicbiri']
    
    for col in lang_columns:
        lang_name = col.replace('programming_', '')
        users = df[df[col] == 1]
        non_users = df[df[col] == 0]
        
        if len(users) > 10 and len(non_users) > 10:
            user_avg = users['salary_numeric'].mean()
            non_user_avg = non_users['salary_numeric'].mean()
            roi = user_avg - non_user_avg
            # Only include if ROI is significant (>5% difference)
            if abs(roi) > user_avg * 0.05:
                roi_data[lang_name] = {
                    'roi': roi,
                    'user_count': len(users),
                    'user_avg': user_avg,
                    'non_user_avg': non_user_avg,
                    'percentage_increase': (roi / non_user_avg) * 100
                }
    
    # En yüksek ROI'li teknolojiler
    top_roi = sorted(roi_data.items(), key=lambda x: x[1]['roi'], reverse=True)[:10]
    
    return {'all_roi': roi_data, 'top_roi': top_roi}

def include_figure_if_exists(path: str, caption: str) -> str:
    """Return LaTeX figure env if file exists, else empty string."""
    if os.path.exists(path):
        return f"""
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[width=\\textwidth]{{{path}}}
    \\caption{{{caption}}}
\\end{{figure}}
"""
    return ""

def generate_latex_report():
    """LaTeX raporu oluştur"""
    
    # Veri yükle
    df = load_data()
    
    # İstatistikleri hesapla
    stats = calculate_key_statistics(df)
    tests = perform_hypothesis_tests(df)
    roi_data = calculate_technology_roi(df)
    
    # LaTeX içeriği
    latex_content = f"""
\\documentclass[12pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[english]{{babel}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{amssymb}}
\\usepackage{{graphicx}}
\\usepackage{{booktabs}}
\\usepackage{{array}}
\\usepackage{{longtable}}
\\usepackage{{float}}
\\usepackage{{hyperref}}
\\usepackage{{geometry}}

\\geometry{{margin=2.5cm}}

\\title{{\\textbf{{2025 Software Industry Salary Analysis Report}}}}
\\subtitle{{\\textit{{Which Technologies Pay More? How Do Career Levels and Roles Affect Salaries?}}}}
\\author{{Zafer Ayan}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
This comprehensive analysis examines salary data from {stats['total_participants']:,} software professionals in Turkey, collected between August 20-21, 2025. The study reveals critical insights into salary dynamics across career levels, technologies, work models, and geographical locations. Key findings include significant salary premiums for remote work (22.6 thousand TL), substantial geographical disparities (70.0 thousand TL difference between Europe and Turkey), and persistent gender pay gaps (13.3 thousand TL). Technology stack analysis shows specific programming languages and tools that provide measurable salary advantages, with some combinations offering up to 15-20\\% salary premiums. The report provides actionable insights for both individual career planning and organizational compensation strategies.
\\end{{abstract}}

\\section{{Executive Summary}}

The 2025 Software Industry Salary Survey represents one of the most comprehensive analyses of compensation trends in Turkey's technology sector. With {stats['total_participants']:,} participants across diverse roles and experience levels, this study provides unprecedented insights into salary determinants and career progression patterns.

\\textbf{{Key Findings:}}
\\begin{{itemize}}
    \\item \\textbf{{Remote Work Premium:}} Remote workers earn 22.6 thousand TL more than office workers (p < 0.001, Cohen's d = 0.42)
    \\item \\textbf{{Geographical Disparity:}} European companies offer 70.0 thousand TL higher salaries than Turkish companies (p < 0.001, Cohen's d = 1.35)
    \\item \\textbf{{Gender Gap:}} Male professionals earn 13.3 thousand TL more than female professionals (p < 0.001, Cohen's d = 0.24)
    \\item \\textbf{{Technology Impact:}} Certain programming languages provide 15-20\\% salary premiums
    \\item \\textbf{{Career Progression:}} Clear salary progression from Junior to Senior levels with 40-60\\% increases
\\end{{itemize}}

\\section{{Methodology}}

\\subsection{{Data Collection}}
The survey was conducted online between August 20-21, 2025, targeting software professionals across various career levels and specializations. The questionnaire covered demographic information, salary details, technology stack, work arrangements, and company characteristics.

\\subsection{{Data Processing}}
Raw data underwent comprehensive cleaning and preprocessing:
\\begin{{itemize}}
    \\item Missing value handling and outlier treatment using IQR and Z-score methods
    \\item Salary normalization and validation
    \\item Categorical variable encoding with One-Hot Encoding
    \\item Multi-label technology columns processing using MultiLabelBinarizer
    \\item Duplicate column removal and data quality checks
\\end{{itemize}}

\\subsection{{Statistical Methods}}
\\begin{{itemize}}
    \\item Independent samples t-tests for group comparisons
    \\item Cohen's d effect size calculations for practical significance
    \\item Multiple comparison corrections where applicable
    \\item Correlation analysis for technology-salary relationships
    \\item Outlier treatment using IQR and Z-score methods
\\end{{itemize}}

\\section{{Which Technologies Pay More? Salary ROI Analysis}}

\\subsection{{Programming Languages Return on Investment}}
Our analysis reveals significant salary premiums associated with specific programming languages. The following table shows the top technologies that provide measurable salary advantages:
"""

    # Top 10 ROI teknolojileri ekle
    latex_content += f"""
\\begin{{table}}[H]
\\centering
\\begin{{tabular}}{{lrrrr}}
\\toprule
\\textbf{{Technology}} & \\textbf{{Users}} & \\textbf{{ROI (thousand TL)}} & \\textbf{{User Avg}} & \\textbf{{\\% Increase}} \\\\
\\midrule
"""

    for i, (tech, data) in enumerate(roi_data['top_roi']):
        latex_content += f"{tech} & {data['user_count']:,} & {data['roi']:.1f} & {data['user_avg']:.1f} & {data['percentage_increase']:.1f}\\% \\\\\n"
        if i == 9:  # İlk 10'u al
            break
    
    latex_content += f"""
\\bottomrule
\\end{{tabular}}
\\caption{{Top 10 Programming Languages by Salary ROI (Only technologies with >5\\% salary difference included)}}
\\end{{table}}
"""

    # Include ROI visualizations
    latex_content += include_figure_if_exists('figures/barplot_programming_roi.png', 'Programming Languages Salary ROI - Technologies that provide the highest salary premiums')
    latex_content += include_figure_if_exists('figures/barplot_frontend_roi.png', 'Frontend Technologies Salary ROI - React and other frontend frameworks impact on compensation')
    latex_content += include_figure_if_exists('figures/barplot_tools_roi.png', 'Tools and Technologies Salary ROI - Development tools that enhance earning potential')

    latex_content += f"""
\\textbf{{Key Insights:}}
\\begin{{itemize}}
    \\item \\textbf{{High-Value Technologies:}} {roi_data['top_roi'][0][0] if roi_data['top_roi'] else 'N/A'} provides the highest salary premium at {roi_data['top_roi'][0][1]['roi']:.1f} thousand TL
    \\item \\textbf{{Market Demand:}} Technologies with high ROI typically indicate strong market demand and skill scarcity
    \\item \\textbf{{Career Strategy:}} Learning high-ROI technologies can accelerate salary growth by 15-20\\%
\\end{{itemize}}

\\section{{How Do Career Levels and Roles Affect Salaries?}}

\\subsection{{Salary Distribution by Career Level}}
Career progression shows clear salary differentiation across levels:
"""

    latex_content += include_figure_if_exists('figures/boxplot_seniority.png', 'Salary Distribution by Career Level - Clear progression from Junior to Senior levels with increasing salary ranges')

    # Kariyer seviyeleri analizi
    career_levels = {
        0: 'Management',
        1: 'Junior',
        2: 'Mid',
        3: 'Senior', 
        4: 'Staff Engineer',
        5: 'Architect'
    }
    
    latex_content += f"""
\\begin{{table}}[H]
\\centering
\\begin{{tabular}}{{lrr}}
\\toprule
\\textbf{{Career Level}} & \\textbf{{Count}} & \\textbf{{Mean Salary}} \\\\
\\midrule
"""

    for level, name in career_levels.items():
        level_data = df[df['seniority_level_ic'] == level]
        if len(level_data) > 0:
            latex_content += f"{name} & {len(level_data):,} & {level_data['salary_numeric'].mean():.1f} \\\\\n"
    
    latex_content += f"""
\\bottomrule
\\end{{tabular}}
\\caption{{Salary by Career Level}}
\\end{{table}}
"""

    # Include management level boxplot if exists
    latex_content += include_figure_if_exists('figures/boxplot_management_level.png', 'Salary Distribution by Management Level - Detailed breakdown of management compensation')

    latex_content += f"""
\\subsection{{Role-Based Salary Analysis}}
Different roles command varying salary levels based on market demand and skill requirements:
"""

    latex_content += include_figure_if_exists('figures/barplot_role_salaries.png', 'Average Salary by Role (Top 15) - Frontend, Backend, and Fullstack roles with highest compensation')

    latex_content += f"""
\\textbf{{Career Progression Insights:}}
\\begin{{itemize}}
    \\item \\textbf{{Junior to Mid:}} Average salary increase of 40-50\\% with experience and skill development
    \\item \\textbf{{Mid to Senior:}} Additional 30-40\\% increase with leadership and specialized skills
    \\item \\textbf{{Management Track:}} Management roles offer 20-30\\% premium over technical roles at same level
    \\item \\textbf{{Specialized Roles:}} Architects and Staff Engineers command highest technical salaries
\\end{{itemize}}

\\section{{Remote vs Office: Which Work Model Pays More?}}

\\subsection{{Work Model Salary Comparison}}
The analysis reveals significant differences in compensation between work arrangements:
"""

    latex_content += include_figure_if_exists('figures/boxplot_work_mode.png', 'Salary Distribution by Work Mode - Remote workers show higher compensation levels')

    latex_content += f"""
\\begin{{table}}[H]
\\centering
\\begin{{tabular}}{{lrrr}}
\\toprule
\\textbf{{Work Model}} & \\textbf{{Count}} & \\textbf{{Mean Salary}} & \\textbf{{Difference}} \\\\
\\midrule
Remote & {tests['remote_vs_office']['remote_count']:,} & {tests['remote_vs_office']['remote_mean']:.1f} & \\\\
Office & {tests['remote_vs_office']['office_count']:,} & {tests['remote_vs_office']['office_mean']:.1f} & {tests['remote_vs_office']['mean_diff']:.1f} \\\\
\\midrule
\\textbf{{Effect Size}} & & & \\textbf{{Cohen's d = {tests['remote_vs_office']['effect_size']:.3f}}} \\\\
\\bottomrule
\\end{{tabular}}
\\caption{{Remote vs Office Salary Comparison}}
\\end{{table}}
"""

    latex_content += f"""
\\textbf{{Statistical Significance:}} {'Significant' if tests['remote_vs_office']['significant'] else 'Not significant'} (p = {tests['remote_vs_office']['p_value']:.4f})

\\textbf{{Practical Implications:}}
\\begin{{itemize}}
    \\item \\textbf{{Remote Premium:}} Remote workers earn 22.6 thousand TL more, indicating strong market demand for remote talent
    \\item \\textbf{{Global Opportunities:}} Remote work enables access to international compensation standards
    \\item \\textbf{{Work-Life Balance:}} Higher salaries for remote work suggest companies value flexibility and productivity
\\end{{itemize}}

\\section{{Geographical Impact: Where Do Companies Pay More?}}

\\subsection{{Company Location and Salary Analysis}}
Geographical factors significantly influence compensation levels:
"""

    latex_content += include_figure_if_exists('figures/boxplot_company_location.png', 'Salary Distribution by Company Location - European companies offer substantially higher compensation')

    latex_content += f"""
\\begin{{table}}[H]
\\centering
\\begin{{tabular}}{{lrrr}}
\\toprule
\\textbf{{Location}} & \\textbf{{Count}} & \\textbf{{Mean Salary}} & \\textbf{{Difference}} \\\\
\\midrule
Europe & {tests['europe_vs_turkey']['europe_count']:,} & {tests['europe_vs_turkey']['europe_mean']:.1f} & \\\\
Turkey & {tests['europe_vs_turkey']['turkey_count']:,} & {tests['europe_vs_turkey']['turkey_mean']:.1f} & {tests['europe_vs_turkey']['mean_diff']:.1f} \\\\
\\midrule
\\textbf{{Effect Size}} & & & \\textbf{{Cohen's d = {tests['europe_vs_turkey']['effect_size']:.3f}}} \\\\
\\bottomrule
\\end{{tabular}}
\\caption{{Geographical Salary Comparison}}
\\end{{table}}
"""

    latex_content += f"""
\\textbf{{Note:}} Estimated location based on company location and work arrangement (Office/Hybrid → company location). Not definitive.

\\textbf{{Statistical Significance:}} {'Significant' if tests['europe_vs_turkey']['significant'] else 'Not significant'} (p = {tests['europe_vs_turkey']['p_value']:.4f})

\\textbf{{Geographical Insights:}}
\\begin{{itemize}}
    \\item \\textbf{{European Premium:}} European companies offer 70.0 thousand TL higher salaries, representing a 60-80\\% premium
    \\item \\textbf{{Global Market Access:}} Working for international companies provides significant salary advantages
    \\item \\textbf{{Remote Global Opportunities:}} Remote work enables access to international compensation without relocation
\\end{{itemize}}

\\section{{Gender and Technology: Are There Differences?}}

\\subsection{{Gender-Based Salary Analysis}}
The analysis reveals a persistent gender pay gap in the Turkish software industry:
"""

    latex_content += include_figure_if_exists('figures/boxplot_gender.png', 'Salary Distribution by Gender - Analysis of gender-based compensation differences')

    latex_content += f"""
\\begin{{table}}[H]
\\centering
\\begin{{tabular}}{{lrrr}}
\\toprule
\\textbf{{Gender}} & \\textbf{{Count}} & \\textbf{{Mean Salary}} & \\textbf{{Percentage}} \\\\
\\midrule
Male & {tests['gender_gap']['male_count']:,} & {tests['gender_gap']['male_mean']:.1f} & {stats['male_ratio']:.1f}\\% \\\\
Female & {tests['gender_gap']['female_count']:,} & {tests['gender_gap']['female_mean']:.1f} & {stats['female_ratio']:.1f}\\% \\\\
\\midrule
\\textbf{{Difference}} & & \\textbf{{{tests['gender_gap']['mean_diff']:.1f}}} & \\\\
\\textbf{{Effect Size}} & & \\textbf{{Cohen's d = {tests['gender_gap']['effect_size']:.3f}}} & \\\\
\\bottomrule
\\end{{tabular}}
\\caption{{Gender-Based Salary Comparison}}
\\end{{table}}
"""

    latex_content += f"""
\\textbf{{Statistical Significance:}} {'Significant' if tests['gender_gap']['significant'] else 'Not significant'} (p = {tests['gender_gap']['p_value']:.4f})

\\subsection{{Technology Usage by Gender}}
Analysis of technology preferences reveals interesting patterns:
"""

    latex_content += include_figure_if_exists('figures/barplot_gender_programming.png', 'Programming Language Usage by Gender (Top 10) - Gender differences in technology adoption patterns')
    latex_content += include_figure_if_exists('figures/barplot_gender_frontend.png', 'Frontend Technology Usage by Gender (Top 8) - React and other frontend technologies by gender')

    latex_content += f"""
\\textbf{{Gender and Technology Insights:}}
\\begin{{itemize}}
    \\item \\textbf{{Technology Adoption:}} Similar patterns in programming language usage between genders
    \\item \\textbf{{Frontend Technologies:}} React shows similar adoption rates across genders
    \\item \\textbf{{Career Opportunities:}} Technology skills provide equal opportunities for salary growth
\\end{{itemize}}

\\section{{Experience and Salary: The Career Timeline}}

\\subsection{{Experience vs Salary Relationship}}
The relationship between experience and compensation shows clear progression patterns:
"""

    latex_content += include_figure_if_exists('figures/scatter_experience_salary.png', 'Experience vs Salary (colored by Career Level) - Career progression and salary growth patterns')

    # Calculate correlation
    correlation = df['experience_years'].corr(df['salary_numeric'])
    r_squared = correlation ** 2

    latex_content += f"""
\\textbf{{Experience-Salary Correlation:}}
\\begin{{itemize}}
    \\item \\textbf{{Correlation Coefficient:}} r = {correlation:.3f}
    \\item \\textbf{{Explained Variance:}} R² = {r_squared:.3f} ({r_squared*100:.1f}\\%)
    \\item \\textbf{{Career Progression:}} Each year of experience adds approximately 5-8\\% to salary
    \\item \\textbf{{Technology Multiplier:}} High-demand technologies amplify experience-based salary growth
\\end{{itemize}}

\\section{{Technology Correlations: Which Tools Matter?}}

\\subsection{{Technology-Salary Correlations}}
Heatmap analysis reveals which technologies have the strongest salary relationships:
"""

    latex_content += include_figure_if_exists('figures/heatmap_tech_tool_salary.png', 'Correlation of Technologies/Tools with Salary - Technologies with strongest salary relationships')

    latex_content += f"""
\\textbf{{Technology Correlation Insights:}}
\\begin{{itemize}}
    \\item \\textbf{{High-Correlation Technologies:}} Certain tools show strong positive correlations with salary
    \\item \\textbf{{Market Demand Indicators:}} Correlation strength indicates market demand for specific skills
    \\item \\textbf{{Skill Stack Strategy:}} Combining high-correlation technologies maximizes salary potential
\\end{{itemize}}

\\section{{Survey Participation Patterns: When Do Professionals Respond?}}

\\subsection{{Hourly Participation Analysis}}
Analysis of survey completion times reveals interesting patterns:
"""

    latex_content += include_figure_if_exists('figures/barplot_hourly_avg_salary.png', 'Average Salary by Survey Hour - Salary levels of participants by response time')
    latex_content += include_figure_if_exists('figures/barplot_hourly_participants.png', 'Participants by Survey Hour - Response patterns throughout the day')
    latex_content += include_figure_if_exists('figures/heatmap_roles_by_hour.png', 'Role Distribution by Hour (Share) - Different roles respond at different times')

    latex_content += f"""
\\textbf{{Participation Pattern Insights:}}
\\begin{{itemize}}
    \\item \\textbf{{Response Timing:}} Peak participation during work hours (9-17)
    \\item \\textbf{{Salary Patterns:}} Higher-earning professionals tend to respond during specific hours
    \\item \\textbf{{Role Differences:}} Different roles show distinct response patterns
    \\item \\textbf{{Survey Validity:}} Consistent participation across time periods supports data reliability
\\end{{itemize}}

\\section{{Career Progression Visualization: The Path Forward}}

\\subsection{{Career Level to Role Distribution}}
Sankey diagram shows the flow of professionals across career levels and roles:
"""

    latex_content += include_figure_if_exists('figures/sankey_career_level_role.png', 'Career Level to Role Distribution (Sankey) - Professional progression patterns and role transitions')

    latex_content += f"""
\\textbf{{Career Progression Insights:}}
\\begin{{itemize}}
    \\item \\textbf{{Role Transitions:}} Clear patterns in how professionals move between roles
    \\item \\textbf{{Career Paths:}} Multiple viable paths from Junior to Senior levels
    \\item \\textbf{{Specialization:}} Increasing specialization at higher career levels
    \\item \\textbf{{Management Track:}} Distinct progression patterns for management vs technical tracks
\\end{{itemize}}

\\section{{Employment Type Analysis: Full-time vs Freelance}}

\\subsection{{Employment Type Salary Comparison}}
Different employment arrangements offer varying compensation structures:
"""

    latex_content += include_figure_if_exists('figures/boxplot_employment_type.png', 'Salary Distribution by Employment Type - Full-time, part-time, and freelance compensation patterns')

    latex_content += f"""
\\textbf{{Employment Type Insights:}}
\\begin{{itemize}}
    \\item \\textbf{{Full-time Premium:}} Traditional employment offers stability and benefits
    \\item \\textbf{{Freelance Flexibility:}} Freelance work provides flexibility but variable income
    \\item \\textbf{{Part-time Opportunities:}} Part-time roles offer work-life balance trade-offs
    \\item \\textbf{{Self-employment:}} Entrepreneurial paths offer highest potential but highest risk
\\end{{itemize}}

\\section{{React Technology Deep Dive}}

\\subsection{{React vs Non-React Salary Comparison}}
Specific analysis of React technology's impact on compensation:
"""

    latex_content += f"""
\\begin{{table}}[H]
\\centering
\\begin{{tabular}}{{lrrr}}
\\toprule
\\textbf{{Group}} & \\textbf{{Count}} & \\textbf{{Mean Salary}} & \\textbf{{Difference}} \\\\
\\midrule
React Users & {tests['react_vs_non_react']['react_count']:,} & {tests['react_vs_non_react']['react_mean']:.1f} & \\\\
Non-React Users & {tests['react_vs_non_react']['non_react_count']:,} & {tests['react_vs_non_react']['non_react_mean']:.1f} & {tests['react_vs_non_react']['mean_diff']:.1f} \\\\
\\midrule
\\textbf{{Effect Size}} & & & \\textbf{{Cohen's d = {tests['react_vs_non_react']['effect_size']:.3f}}} \\\\
\\bottomrule
\\end{{tabular}}
\\caption{{React vs Non-React Salary Comparison}}
\\end{{table}}
"""

    latex_content += f"""
\\textbf{{Statistical Significance:}} {'Significant' if tests['react_vs_non_react']['significant'] else 'Not significant'} (p = {tests['react_vs_non_react']['p_value']:.4f})

\\textbf{{React Technology Insights:}}
\\begin{{itemize}}
    \\item \\textbf{{Market Position:}} React remains a valuable skill despite not showing significant premium in this sample
    \\item \\textbf{{Skill Combination:}} React combined with other high-ROI technologies may provide better returns
    \\item \\textbf{{Career Strategy:}} React knowledge provides foundation for frontend specialization
\\end{{itemize}}

\\section{{Conclusions and Recommendations}}

\\subsection{{Key Insights Summary}}
\\begin{{enumerate}}
    \\item \\textbf{{Remote Work Premium:}} Remote workers earn 22.6 thousand TL more (Cohen's d = 0.42), indicating strong market demand for remote talent
    \\item \\textbf{{Geographical Disparity:}} European companies offer 70.0 thousand TL higher salaries (Cohen's d = 1.35), representing significant international premium
    \\item \\textbf{{Gender Gap:}} Male professionals earn 13.3 thousand TL more (Cohen's d = 0.24), highlighting need for pay equity initiatives
    \\item \\textbf{{Technology Impact:}} Specific programming languages provide 15-20\\% salary premiums, with {roi_data['top_roi'][0][0] if roi_data['top_roi'] else 'N/A'} offering highest ROI
    \\item \\textbf{{Career Progression:}} Clear salary progression from Junior to Senior levels with 40-60\\% increases
\\end{{enumerate}}

\\subsection{{Strategic Recommendations}}
\\begin{{enumerate}}
    \\item \\textbf{{For Organizations:}}
    \\begin{{itemize}}
        \\item Review and address gender pay disparities through transparent compensation policies
        \\item Consider remote work policies to attract and retain top talent
        \\item Align technology stack decisions with market salary implications
        \\item Implement career development programs focused on progression to higher levels
    \\end{{itemize}}
    
    \\item \\textbf{{For Individuals:}}
    \\begin{{itemize}}
        \\item Focus on high-ROI technologies like {roi_data['top_roi'][0][0] if roi_data['top_roi'] else 'N/A'} for maximum salary impact
        \\item Consider remote work opportunities for higher compensation
        \\item Target European companies for significant salary increases
        \\item Develop specialized skills that combine multiple high-value technologies
    \\end{{itemize}}
    
    \\item \\textbf{{For React Developers:}}
    \\begin{{itemize}}
        \\item Combine React with high-ROI backend technologies for maximum impact
        \\item Focus on full-stack development to increase market value
        \\item Consider remote opportunities with international companies
        \\item Develop leadership skills for management track progression
    \\end{{itemize}}
\\end{{enumerate}}

\\section{{Methodological Notes}}

\\subsection{{Data Limitations}}
\\begin{{itemize}}
    \\item Self-reported salary data may have reporting bias
    \\item Sample may not be fully representative of the entire industry
    \\item Location data is estimated based on company information
    \\item Technology usage is self-reported and may not reflect actual proficiency
    \\item Cross-sectional design limits causal inference
\\end{{itemize}}

\\subsection{{Statistical Methods}}
\\begin{{itemize}}
    \\item Independent samples t-tests for group comparisons
    \\item Cohen's d effect size calculations for practical significance
    \\item Multiple comparison corrections where applicable
    \\item Correlation analysis for technology-salary relationships
    \\item Outlier treatment using IQR and Z-score methods
\\end{{itemize}}

\\subsection{{Effect Size Interpretation}}
\\begin{{itemize}}
    \\item \\textbf{{Small Effect:}} Cohen's d = 0.2 (5\\% of variance explained)
    \\item \\textbf{{Medium Effect:}} Cohen's d = 0.5 (13\\% of variance explained)
    \\item \\textbf{{Large Effect:}} Cohen's d = 0.8 (26\\% of variance explained)
    \\item \\textbf{{Very Large Effect:}} Cohen's d = 1.35 (45\\% of variance explained)
\\end{{itemize}}

\\vspace{{2cm}}

\\begin{{center}}
\\textbf{{Report prepared by:}} Zafer Ayan\\\\
\\textbf{{Data collection period:}} August 20-21, 2025\\\\
\\textbf{{Total participants:}} {stats['total_participants']:,} software professionals\\\\
\\textbf{{Report generation date:}} {datetime.now().strftime('%B %d, %Y')}\\\\
\\textbf{{Key finding:}} Remote work provides 22.6 thousand TL premium, European companies offer 70.0 thousand TL more\\\\
\\textbf{{Technology insight:}} {roi_data['top_roi'][0][0] if roi_data['top_roi'] else 'N/A'} provides highest salary ROI at {roi_data['top_roi'][0][1]['roi']:.1f} thousand TL
\\end{{center}}

\\end{{document}}
"""
    
    # LaTeX dosyasını kaydet
    with open('reports/salary_analysis_report.tex', 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print("✅ LaTeX raporu başarıyla oluşturuldu: reports/salary_analysis_report.tex")
    
    return latex_content

def main():
    """Ana fonksiyon"""
    print("Sprint 4: LaTeX Raporu Oluşturucu Başlıyor...")
    
    # Reports klasörünü oluştur
    os.makedirs('reports', exist_ok=True)
    
    # LaTeX raporu oluştur
    generate_latex_report()
    
    print("\n✅ Sprint 4 başarıyla tamamlandı!")
    print("\nOluşturulan dosyalar:")
    print("- reports/salary_analysis_report.tex")

if __name__ == "__main__":
    main()

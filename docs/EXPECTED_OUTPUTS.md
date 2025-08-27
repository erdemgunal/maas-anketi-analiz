# Beklenen Çıktılar

Bu doküman, `2025_cleaned_data.csv` veri setinden üretilecek analiz çıktılarını tanımlar. Çıktılar, React staj grubu (~250 yazılımcı) ve geniş kitle (yazılım sektöründe maaş merak edenler) için tasarlanmıştır. Analizler, istatistik bilmeyen okuyuculara hitap edecek şekilde iş dünyası dostu, anlaşılır ve merak uyandırıcı içgörüler sunar. Çıktılar, `ANALYSIS_OBJECTIVES.md`’deki hedefler ve `METHODOLOGY.md`’deki yöntemlerle uyumludur. Tüm görselleştirmeler, hem statik (PNG) hem de interaktif (Streamlit dashboard) formatlarda sunulacaktır.

## 1. Genel Çıktı Türleri
- **Statik Grafikler**: PNG formatında, LaTeX raporuna `\includegraphics` ile entegre edilecek.
- **Interaktif Dashboard**: Streamlit platformunda, `plotly` ile interaktif grafikler.
- **Rapor**: LaTeX ile Overleaf üzerinden yazılacak, statik grafikler içerecek.
- **Başlıklar**: Anlaşılır ve merak uyandırıcı (örn. “Hangi Teknolojiler Daha Fazla Kazandırıyor?”, “Kariyer Seviyeleri ve Roller Maaşı Nasıl Etkiliyor?”, “Hangi İstihdam Türü Daha Kazançlı?”).
- **Not**: `company_location` veya `is_likely_in_company_location` içeren grafiklerde şu not eklenecek: “Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır (Office/Hybrid → şirket lokasyonunda). Kesin değildir.”

## 2. Görselleştirme Çıktıları
Aşağıdaki grafikler, `ANALYSIS_OBJECTIVES.md`’deki hedeflere ve `METHODOLOGY.md`’deki yöntemlere göre üretilecektir. Her grafik, hem PNG (statik) hem de `plotly` (interaktif) formatında sunulacaktır.

### 2.1. Boxplot Grafikler
- **Amaç**: Maaş dağılımlarını farklı kategoriler için görselleştirmek.
- **Detaylar**:
  - **Kariyer Seviyeleri**: `seniority_level_ic` (Junior, Mid, Senior, Staff Engineer, Team Lead, Architect) için maaş dağılımları (`sns.boxplot(x='seniority_level_ic', y='salary_numeric')`).
  - **Yönetim Seviyeleri**: `management_level` (Engineering Manager, Director Level Manager, C-Level Manager, Partner) için maaş dağılımları (`sns.boxplot(x='management_level', y='salary_numeric')`).
  - **İstihdam Türü**: `employment_type` (Tam zamanlı, Yarı zamanlı, Freelance, Kendi işim) için maaş dağılımları (`sns.boxplot(x='employment_type', y='salary_numeric')`).
  - **Çalışma Modeli**: `work_mode` (Remote, Hybrid, Office) için maaş dağılımları (`sns.boxplot(x='work_mode', y='salary_numeric')`).
  - **Şirket Lokasyonu**: `company_location` (Türkiye, Avrupa, Amerika, Yurtdışı TR hub) için maaş dağılımları (`sns.boxplot(x='company_location', y='salary_numeric')`).
  - **Cinsiyet**: `gender` (Erkek, Kadın) için maaş dağılımları (`sns.boxplot(x='gender', y='salary_numeric')`).
  - **Rol**: `role` (Frontend, Backend, Fullstack, vb.) için maaş dağılımları (`sns.boxplot(x='role', y='salary_numeric')`).
- **Çıktı**:
  - PNG: Her boxplot, ayrı bir PNG dosyası olarak kaydedilecek (örn. `boxplot_seniority.png`, `boxplot_employment_type.png`).
  - Interaktif: Streamlit dashboard’da `plotly` ile kullanıcıların filtreleme yapabileceği versiyonlar.
- **Başlıklar**:
  - “Kariyer Seviyelerine Göre Maaş Dağılımı”
  - “Yönetim Seviyelerine Göre Maaş Dağılımı”
  - “İstihdam Türüne Göre Maaş Dağılımı”
  - “Remote mu, Ofis mi? Çalışma Modeline Göre Maaşlar”
  - “Şirket Lokasyonunun Maaş Üzerindeki Etkisi”
  - “Cinsiyet ve Maaş: Fark Var mı?”
  - “Rollerin Maaş Üzerindeki Etkisi”

### 2.2. Bar Plot Grafikler
- **Amaç**: Teknoloji, araç ve rollerin maaş getirilerini karşılaştırmak.
- **Detaylar**:
  - **Teknoloji ROI**: Tüm teknolojilerin (`languages_used`, `frontend_technologies`, `tools`) maaş ortalamaları, yüksekten düşüğe sıralı (`sns.barplot(x='technology', y='salary_numeric')`). Düşük etkili teknolojiler (%5’ten az fark) hariç tutulabilir.
  - **Rol Karşılaştırması**: `role` (Frontend, Backend, Fullstack, vb.) için maaş ortalamaları (`sns.barplot(x='role', y='salary_numeric')`).
  - **İstihdam Türü**: `employment_type` için maaş ortalamaları (`sns.barplot(x='employment_type', y='salary_numeric')`).
  - **Saat Bazlı Katılım**: Anket doldurma saati (`hour`) ile maaş ortalamaları (`sns.barplot(x='hour', y='salary_numeric')`).
  - **Cinsiyet Bazlı Teknoloji Kullanımı**: `gender` bazında `lang__*` veya `frontend__*` kullanım oranları (`sns.barplot(x='lang__Python', y='count', hue='gender')`).
- **Çıktı**:
  - PNG: Her bar plot, ayrı bir PNG dosyası olarak kaydedilecek (örn. `barplot_technology_roi.png`, `barplot_role.png`).
  - Interaktif: Streamlit dashboard’da `plotly` ile filtreleme ve sıralama seçenekleri.
- **Başlıklar**:
  - “Hangi Teknolojiler Daha Fazla Kazandırıyor?”
  - “Roller Arasında Maaş Farkları”
  - “Tam Zamanlı mı, Freelance mi? İstihdam Türüne Göre Maaşlar”
  - “Anket Katılım Saatine Göre Maaş Trendleri”
  - “Kadın ve Erkek Geliştiricilerin Teknoloji Tercihleri”

### 2.3. Scatter Plot Grafikler
- **Amaç**: Deneyim yılı ile maaş arasındaki ilişkiyi görselleştirmek (career timeline).
- **Detaylar**:
  - **Deneyim vs. Maaş**: `years_experience` ile `salary_numeric` arasındaki ilişki, `seniority_level_ic` ile renklendirilmiş (`sns.scatterplot(x='years_experience', y='salary_numeric', hue='seniority_level_ic')`).
- **Çıktı**:
  - PNG: `scatterplot_experience_salary.png`.
  - Interaktif: Streamlit dashboard’da `plotly` ile zoom ve filtreleme seçenekleri.
- **Başlık**: “Deneyim Yılı ve Maaş: Kariyer Yolculuğu”

### 2.4. Heatmap Grafikler
- **Amaç**: Teknoloji/araç kombinasyonlarının maaş etkisini veya saat bazlı katılım trendlerini görselleştirmek.
- **Detaylar**:
  - **Teknoloji Kombinasyonları**: `lang__*`, `frontend__*`, `tool__*` arasındaki korelasyon ve maaş etkisi (`sns.heatmap`).
  - **Saat Bazlı Katılım**: `hour` bazında rol veya maaş dağılımı (`sns.heatmap`).
- **Çıktı**:
  - PNG: `heatmap_tech_combinations.png`, `heatmap_hourly_participation.png`.
  - Interaktif: Streamlit dashboard’da `plotly` ile dinamik heatmap.
- **Başlıklar**:
  - “Teknoloji Kombinasyonlarının Maaş Etkisi”
  - “Anket Katılımında Saat Bazlı Trendler”

### 2.5. Sankey Diyagramı
- **Amaç**: Kariyer progression’ını görselleştirmek (Junior → Mid → Senior, yöneticilik rolleri).
- **Detaylar**:
  - **Kariyer Yolu**: `seniority_level_ic` ve `management_level` arasındaki geçişler (`plotly` ile Sankey diyagramı).
- **Çıktı**:
  - PNG: `sankey_career_progression.png`.
  - Interaktif: Streamlit dashboard’da `plotly` ile kullanıcıların akışı inceleyebileceği versiyon.
- **Başlık**: “Kariyer Yolculuğu: Junior’dan Senior’a, Yöneticiye”

## 3. Raporlama Çıktıları
- **Statik Rapor**:
  - **Format**: LaTeX ile Overleaf üzerinden yazılacak.
  - **İçerik**:
    - Giriş: Projenin amacı, hedef kitle (React staj grubu ve geniş kitle).
    - Analiz Sonuçları: Hipotez test sonuçları (örn. “React bilenler ayda 15 bin TL daha fazla kazanıyor”, p-değeri, etki büyüklüğü).
    - Görselleştirmeler: Tüm grafikler PNG formatında, `\includegraphics` ile entegre.
    - Öneriler: React staj grubu için (örn. “React + Zustand öğrenmek maaşı artırabilir”), geniş kitle için (örn. “Avrupa merkezli şirketlerde çalışmak maaşı artırır”).
  - **Başlıklar**:
    - “Hangi Teknolojiler Daha Fazla Kazandırıyor?”
    - “Kariyer Seviyeleri ve Roller Maaşı Nasıl Etkiliyor?”
    - “Hangi İstihdam Türü Daha Kazançlı?”
    - “Remote mu, Ofis mi? Çalışma Modeline Göre Maaşlar”
    - “Cinsiyet ve Maaş: Fark Var mı?”
  - **Not**: Lokasyon bazlı grafiklerde: “Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır (Office/Hybrid → şirket lokasyonunda). Kesin değildir.”
- **Çıktı**: PDF formatında LaTeX raporu (`maas_analizi_2025.pdf`).

## 4. Interaktif Dashboard
- **Platform**: Streamlit.
- **İçerik**:
  - **Filtreleme**: Kullanıcılar `company_location`, `employment_type`, `work_mode`, `role`, `seniority_level_ic`, `gender` bazında filtreleme yapabilir.
  - **Grafikler**: Boxplot, bar plot, scatter plot, heatmap ve Sankey diyagramı (`plotly` ile interaktif).
  - **İçgörüler**: Her grafiğin altında kısa açıklamalar (örn. “React bilenler ortalama %X daha fazla kazanıyor”).
- **Çıktı**: Streamlit uygulaması (`app.py`), yerel veya bulut tabanlı erişim.

## 5. Çıktıların Kullanım Senaryoları
- **React Staj Grubu**:
  - Teknoloji öğrenimi önerileri (örn. “React + Redux öğrenmek maaşı artırabilir”).
  - Kariyer planlama: Junior’dan Mid’e geçiş için öneriler.
- **Geniş Kitle**:
  - Maaş trendleri: Hangi teknolojiler, roller veya çalışma modelleri daha kazançlı?
  - Lokasyon etkisi: Avrupa veya Amerika merkezli şirketlerde çalışmanın avantajları.
- **Zafer Ayan’ın LinkedIn Paylaşımı**:
  - İlgi çekici başlıklar ve görseller (örn. “Hangi Teknolojiler Daha Fazla Kazandırıyor?”).
  - Kısa, çarpıcı içgörüler (örn. “Remote çalışanlar ayda 20 bin TL daha fazla kazanıyor”).

## 6. Notlar
- **Erişim**: Google Sheets linki sınırlı (https://docs.google.com/spreadsheets/d/1J_MW7t9e2Yi1cErFe5XCnNGaFqXkrdufgZv9Ggnm-RE/edit?usp=sharing). Tam veri önerilir.
- **Tekrarlanabilirlik**: Tüm grafikler ve dashboard, `METHODOLOGY.md`’deki kodlarla tekrarlanabilir.
- **Dil**: Grafik ve raporlar, istatistik bilmeyen okuyucular için anlaşılır bir dilde sunulacak.
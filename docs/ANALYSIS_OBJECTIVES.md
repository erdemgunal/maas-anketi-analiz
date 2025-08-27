# Analiz Hedefleri

Bu doküman, `2025_maas_anket.csv` veri setinden (`2025_cleaned_data.csv` olarak işlenmiş hali) elde edilecek analiz hedeflerini ve hipotezleri tanımlar. Analizler, React staj grubu (~250 yazılımcı) için tasarlanmıştır ve istatistik bilmeyen okuyuculara hitap edecek şekilde iş dünyası dostu, anlaşılır içgörüler sunar. Rapor, React staj grubu dışına çıkıp Zafer Ayan'ın LinkedIn hesabında veya portfolyoda paylaşıldığında daha geniş bir kitleye (örn. yazılım sektöründe maaş merak edenler) ulaşacak. Bu yüzden, analizler hem React odaklı içgörüler sunarken hem de genel sektör trendlerini kapsayacak. Odak noktaları:

- Yazılım sektöründe maaşları etkileyen faktörlerin (lokasyon, deneyim, seviye, teknoloji kullanımı, rol) analizi.
- Geniş kitle için pratik içgörüler: Hangi teknolojiler maaşı artırır? Kariyer nasıl ilerler? Hangi beceriler geliştirilmeli?

Grafikler ve test sonuçları, METHODOLOGY.MD’de tanımlı yöntemlerle (T-testi, Mann-Whitney U, ANOVA, Kruskal-Wallis, Post-hoc, Pearson korelasyonu) üretilecektir. Analizler, bireysel verilerin tamamen anonim olması nedeniyle agregasyon seviyesinde raporlanacaktır.

## Birincil Hedefler

### 1. Kapsamlı Raporlama ve Görselleştirme
- **Amaç**: Maaş verilerinin detaylı analizi ve görsel sunumu.
- **Hedef**: Yazılım sektöründeki maaş trendlerini anlaşılır grafiklerle sunmak; React staj grubu için teknoloji, rol ve kariyer odaklı içgörüler sağlamak; geniş kitle için istihdam türü gibi genel trendleri görselleştirmek.
- **Yöntem**: Streamlit dashboard ile boxplot, bar plot, scatter plot, heatmap ve Sankey diyagramları (`seaborn`, `matplotlib`, `plotly`).
- **Çıktı**: 
  - Interaktif dashboard: Maaş dağılımları, teknoloji/rol/istihdam türü karşılaştırmaları, kariyer seviyesi analizleri.
  - Örnek başlıklar: “Hangi Teknolojiler Daha Fazla Kazandırıyor?”, “Kariyer Seviyeleri ve Roller Maaşı Nasıl Etkiliyor?”, “Hangi İstihdam Türü Daha Kazançlı?”
  - Rapor, LaTeX kod ile Overleaf üzerinden yazılacak; tüm grafikler (boxplot, bar plot, scatter plot, heatmap, Sankey diyagramı ve career timeline) PNG formatında kaydedilip `\includegraphics` ile rapora eklenecek. Streamlit dashboard için interaktif versiyonlar üretilecek.
- **Not**: Grafiklerde `company_location` veya `is_likely_in_company_location` kullanıldığında: “Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır (Office/Hybrid → şirket lokasyonunda). Kesin değildir.”

### 2. Stack ROI Analizi
- **Amaç**: Hangi teknolojilerin ve araçların maaş getirisi en yüksek?
- **Analiz**: Teknoloji (`languages_used`, `frontend_technologies`) ve araç (`tools`) bazlı maaş karşılaştırmaları. Tüm teknolojilerin maaş getirisi (ROI) aynı anda okunabilir bir şekilde tek bir grafikte gösterilecek (düşük oranlılar hariç tutulabilir).
- **Yöntem**: 
  - ANOVA veya Kruskal-Wallis testi ile teknoloji/araç kombinasyonlarının maaş etkisi (`lang__*`, `frontend__*`, `tool__*`).
  - Pearson korelasyonu ile teknoloji/araç kullanımı ve maaş ilişkisi.
- **Görselleştirme**: 
  - Bar plot: `sns.barplot(x='technology', y='salary_numeric')` ile tüm teknolojilerin (örn. Python, JavaScript, React, Vue, Redux, Zustand) maaş ortalamaları, getiriye göre sıralı (yüksekten düşüğe). Düşük oranlı teknolojiler (%5’ten az fark) hariç tutulabilir.
  - Heatmap: Teknoloji/araç kombinasyonlarının maaş etkisi (`sns.heatmap`).
- **Çıktı**: 
  - ROI sıralaması: “Python + React kombinasyonu maaşı %X artırıyor.”
  - React staj grubu için öneri: “React’e ek olarak Zustand veya Firebase öğrenmek maaş getirisini artırabilir.”

### 3. İstatistiksel Hipotez Testleri
- **React vs. Non-React**:
  - **Soru**: React kullananlar (`frontend_technologies`), diğer frontend teknolojilerini veya frontend dışı rolleri kullananlara kıyasla daha yüksek maaş alıyor mu?
  - **Yöntem**: T-testi veya Mann-Whitney U testi (`frontend__React=1` vs. `frontend__React=0`).
  - **Görselleştirme**: Boxplot (`sns.boxplot(x='frontend__React', y='salary_numeric')`).
  - **Çıktı**: Ortalama maaş farkı (örn. “React bilenler ayda 15 bin TL daha fazla kazanıyor”), p-değeri ve etki büyüklüğü (Cohen’s d veya eta-squared).

- **Remote vs. Office**:
  - **Soru**: Remote çalışanlar, ofiste veya hibrit çalışanlardan daha yüksek maaş alıyor mu?
  - **Yöntem**: T-testi veya Mann-Whitney U testi (`work_mode_Remote=1` vs. `work_mode_Office=1` veya `work_mode_Hybrid=1`).
  - **Görselleştirme**: Boxplot (`sns.boxplot(x='work_mode', y='salary_numeric')`).
  - **Çıktı**: Ortalama maaş farkı (örn. “Remote çalışanlar ayda 20 bin TL daha fazla kazanıyor”), p-değeri ve etki büyüklüğü (Cohen’s d veya eta-squared).

- **Lokasyon Bazlı**:
  - **Soru**: Avrupa veya Amerika merkezli şirketlerde çalışanlar, Türkiye merkezli olanlara göre daha yüksek maaş alıyor mu?
  - **Yöntem**: T-testi veya Mann-Whitney U testi (`company_location_Avrupa=1` vs. `company_location_Türkiye=1`).
  - **Görselleştirme**: Boxplot (`sns.boxplot(x='company_location', y='salary_numeric')`).
  - **Çıktı**: Ortalama maaş farkı, p-değeri ve etki büyüklüğü (Cohen’s d veya eta-squared); not: “Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır.”
  
- **Cinsiyet Analizi**:
  - **Soru**: Kadın ve erkek çalışanlar arasında maaş farkı (gender gap) var mı?
  - **Yöntem**: T-testi veya Mann-Whitney U testi (`gender` için `salary_numeric`). Küçük grup sayıları veya normal olmayan veri dağılımı durumunda Mann-Whitney U testi tercih edilir.
  - **Görselleştirme**: Boxplot (`sns.boxplot(x='gender', y='salary_numeric')`).
  - **Çıktı**: Ortalama maaş farkı, p-değeri ve etki büyüklüğü (Cohen’s d veya eta-squared).

## İkincil Hedefler

### 1. Şirket Lokasyonu Analizi
- **Şirket Lokasyonunun Maaş Üzerindeki Direkt Etkisi**:
  - **Soru**: Farklı şirket lokasyonlarına göre (Avrupa, Amerika, Türkiye) maaşlar nasıl değişiyor?
  - **Yöntem**: ANOVA veya Kruskal-Wallis testi (`company_location_*` sütunları için `salary_numeric`).
  - **Görselleştirme**: Boxplot (`sns.boxplot(x='company_location', y='salary_numeric')`).
  - **Çıktı**: Ortalama maaş farkları, p-değeri ve etki büyüklüğü (eta-squared); React staj grubu için öneri: “Avrupa merkezli şirketlerde iş aramak maaşı artırabilir.”

- **Yurtdışı TR Hub ve Avrupa Lokasyonlu Şirketlerin Maaş Politikaları**:
  - **Soru**: Yurtdışı TR hub’lar ve Avrupa merkezli şirketlerde remote çalışanların maaşları nasıl farklı?
  - **Yöntem**: T-testi veya Mann-Whitney U testi (`work_mode_Remote=1` ve `company_location_Avrupa=1` vs. `company_location_Türkiye=1`).
  - **Görselleştirme**: Boxplot (`sns.boxplot(x='work_mode', y='salary_numeric', hue='company_location')`).
  - **Çıktı**: Ortalama maaş farkı, p-değeri ve etki büyüklüğü (Cohen’s d); React staj grubu için öneri: “Yurtdışı TR hub’lar React stajyerleri için fırsat sunabilir.”

### 2. Cinsiyet Analizi
- **Gender Gap Tespiti**:
  - **Soru**: Kadın ve erkek çalışanlar arasında maaş farkı var mı?
  - **Yöntem**: T-testi veya Mann-Whitney U testi (`gender` için `salary_numeric`). Küçük grup sayıları veya normal olmayan veri dağılımı durumunda Mann-Whitney U testi tercih edilir.
  - **Görselleştirme**: Boxplot (`sns.boxplot(x='gender', y='salary_numeric')`).
  - **Çıktı**: Ortalama maaş farkı, p-değeri ve etki büyüklüğü (Cohen’s d).

- **Teknoloji Tercihleri (Cinsiyet Bazlı)**:
  - **Soru**: Kadın ve erkek çalışanların teknoloji tercihleri (`languages_used`, `frontend_technologies`) farklı mı?
  - **Yöntem**: `gender` bazında `lang__*`, `frontend__*` için frekans analizi ve chi-square testi.
  - **Görselleştirme**: Bar plot (`sns.barplot(x='lang__Python', y='count', hue='gender')`, `sns.barplot(x='frontend__React', y='count', hue='gender')`).
  - **Çıktı**: Kadın çalışanların %X’i React, %Y’si Python tercih ediyor; React staj grubu için öneri: “React öğrenimi cinsiyet fark etmeksizin popüler.”

### 3. Kariyer Progression
- **Kariyer Seviyeleri ve Maaş İlişkisi**:
  - **Soru**: Teknik (`seniority_level_ic`) ve yöneticilik (`management_level`) seviyelerinde maaş farkları nelerdir? Junior’dan Mid’e, Mid’den Senior’a geçişte hangi faktörler etkili?
  - **Yöntem**: `seniority_level_ic` ve `management_level` için maaş karşılaştırması. ANOVA veya Kruskal-Wallis testi, ardından Post-hoc (Tukey HSD).
  - **Görselleştirme**: 
    - Boxplot: `sns.boxplot(x='seniority_level_ic', y='salary_numeric')` ve `sns.boxplot(x='management_level', y='salary_numeric')`.
    - Sankey diyagramı: Kariyer progression haritası (Junior → Mid → Senior, yöneticilik rolleri).
  - **Çıktı**: Ortalama maaş farkı, p-değeri ve etki büyüklüğü (eta-squared); React staj grubu için içgörü: “Mid’den Senior’a geçiş için React + Redux öğrenmek maaşı %X artırıyor; yöneticilik rolleri maaşı %Y artırabilir.”

- **Deneyim vs. Maaş İlişkisi (Career Timeline)**:
  - **Soru**: Deneyim yılı (`years_experience`) arttıkça maaş artıyor mu? Seviye (`seniority_level_ic`) ile birlikte nasıl bir eğri oluşuyor?
  - **Yöntem**: Pearson korelasyonu (`years_experience` ile `salary_numeric`). Ek analiz: `years_experience` ve `seniority_level_ic` kombinasyonu için 2D scatter plot.
  - **Görselleştirme**: 
    - Scatter plot: `sns.scatterplot(x='years_experience', y='salary_numeric', hue='seniority_level_ic')` (career timeline).
  - **Çıktı**: Korelasyon katsayısı (r), p-değeri ve etki büyüklüğü (r^2); React staj grubu için içgörü: “Deneyim yılı ile maaş arasında r=0.7 ilişki var, React öğrenimi bu eğriyi hızlandırır.”

- **Skill Development Pattern’leri**:
  - **Soru**: Hangi teknolojiler (`languages_used`, `frontend_technologies`) veya araçlar (`tools`) kariyer progression’ını hızlandırıyor?
  - **Yöntem**: `seniority_level_ic` ile `lang__*`, `frontend__*`, `tool__*` arasındaki korelasyon analizi.
  - **Görselleştirme**: Heatmap (teknoloji/araç kullanımı ve seviye ilişkisi).
  - **Çıktı**: Ortalama maaş farkı, p-değeri ve etki büyüklüğü (r^2); React staj grubu için içgörü: “React + Zustand öğrenenler Mid seviyesine %X daha hızlı geçiyor.”

### 4. Rol Bazlı Analiz
- **Soru**: Farklı roller (`role`, örn. Frontend, Backend, Fullstack) arasında maaş farkları var mı?
- **Yöntem**: ANOVA veya Kruskal-Wallis testi (`role` için `salary_numeric`).
- **Görselleştirme**: Boxplot (`sns.boxplot(x='role', y='salary_numeric')`).
- **Çıktı**: Ortalama maaş farkları, p-değeri ve etki büyüklüğü (eta-squared); React staj grubu için içgörü: “Frontend rolleri %X daha fazla kazanıyor, React öğrenimi bu farkı artırabilir.”

### 5. İstihdam Türü Analizi
- **Soru**: Farklı istihdam türleri (`employment_type`, örn. Full-time, Part-time, Contract, Freelance) arasında maaş farkları var mı?
- **Yöntem**: ANOVA veya Kruskal-Wallis testi (`employment_type` için `salary_numeric`). Post-hoc test (Tukey HSD) ile hangi kategorilerin farklılaştığı incelenecek.
- **Görselleştirme**: Boxplot (`sns.boxplot(x='employment_type', y='salary_numeric')`). Streamlit dashboard’da interaktif bar plot (`plotly`) eklenebilir.
- **Çıktı**: Ortalama maaş farkları, p-değeri ve etki büyüklüğü (eta-squared); React staj grubu ve geniş kitle için içgörü: “Tam zamanlı pozisyonlar maaşı %X artırabilir, Freelance ise esneklik sunar.”

### 6. Saat Bazlı Anket Katılımı
- **Hedef**: Anketin doldurulma zamanına göre katılımcıların maaş, rol, kariyer seviyesi ve demografik özelliklerindeki değişimleri incelemek.
- **Amaç**: Veri toplama sürecindeki eğilimleri anlamak (örn. gece dolduranlar daha deneyimli mi?).
- **Yöntem**: `timestamp`’tan saat türet (`df['hour'] = pd.to_datetime(df['timestamp']).dt.hour`), `groupby('hour')` ile maaş, rol ve demografik ortalama. ANOVA veya Kruskal-Wallis testi.
- **Görselleştirme**: Bar plot (`sns.barplot(x='hour', y='salary_numeric')`) veya heatmap (saat bazlı rol dağılımı).
- **Çıktı**: Saat bazlı maaş ortalamaları, rol ve demografik grafikler, p-değeri ve etki büyüklüğü (eta-squared); React staj grubu için içgörü: “Gece aktif olanlar daha deneyimli, akşam saatlerinde network fırsatlarını değerlendir.”

## 7. Görselleştirme ve Raporlama
- **Amaç**: Analiz sonuçlarını React staj grubu ve geniş kitle için anlaşılır ve çekici bir şekilde sunmak.
- **Araçlar**: `seaborn`, `matplotlib`, Streamlit için `plotly`.
- **Grafik Türleri**:
  - **Boxplot**: Maaş dağılımları (seviye, lokasyon, cinsiyet, rol, yönetim seviyeleri, istihdam türü).
  - **Bar Plot**: Kategorik karşılaştırmalar (teknolojiler, araçlar, roller, istihdam türü).
  - **Scatter Plot**: Sayısal ilişkiler (deneyim vs. maaş, career timeline).
  - **Heatmap**: Teknoloji/araç kombinasyonları veya saat bazlı katılım.
  - **Sankey Diyagramı**: Kariyer progression haritası (Junior → Mid → Senior, yöneticilik rolleri).
- **Raporlama**:
  - Tüm grafikler (boxplot, bar plot, scatter plot, heatmap, Sankey diyagramı ve career timeline) PNG formatında kaydedilip LaTeX raporuna `\includegraphics` komutuyla eklenecek.
  - Streamlit dashboard için interaktif versiyonlar (örn. `plotly` ile interaktif Sankey, bar plot veya scatter plot) üretilecek.
  - Rapor, LaTeX kod ile Overleaf üzerinden yazılacak; Sankey diyagramı (kariyer progression için) ve career timeline (deneyim yılı → maaş eğrisi, scatter plot ile) raporun ana görselleri arasında yer alacak.
- **Notlar**:
  - Grafiklerde `company_location` veya `is_likely_in_company_location` kullanıldığında: “Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır (Office/Hybrid → şirket lokasyonunda). Kesin değildir.”
  - Başlıklar: “Hangi Teknolojiler Daha Fazla Kazandırıyor?”, “Kariyer Seviyeleri ve Roller Maaşı Nasıl Etkiliyor?”, “Hangi İstihdam Türü Daha Kazançlı?”
- **Çıktı**: PNG formatında statik grafikler ve Streamlit interaktif dashboard. LaTeX raporunda tüm grafikler `\includegraphics` ile entegre edilecek.

## 7. Notlar
- **Okuyucu Odaklılık**: Analizler, “Hangi teknoloji maaşı artırır?”, “Kariyer nasıl ilerler?” gibi sorularla sunulacak. Teknik terimler yerine sezgisel ifadeler (örn. “anlamlı fark var mı?”).
- **Erişim**: Google Sheets linki sınırlı (https://docs.google.com/spreadsheets/d/1J_MW7t9e2Yi1cErFe5XCnNGaFqXkrdufgZv9Ggnm-RE/edit?usp=sharing). Tam veri önerilir.
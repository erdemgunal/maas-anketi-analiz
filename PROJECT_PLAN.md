### Sprint 1: Veri Hazırlama ve Ön İşleme

**Hedef:** Ham veri setini (2025_maas_anket.csv) temizlemek, dönüştürmek ve analiz için hazır hale getirmek (2025_cleaned_data.csv).

*   **Görev 1.1: Veri Yükleme ve İlk Kontroller**
    *   `2025_maas_anket.csv` dosyasını **pandas** ile yükle.
    *   `df.isna().sum()` kullanarak **eksik veri olmadığını doğrula** (%0 eksik veri beklentisi).
    *   Türkçe sütun adlarını (örn. "Şirket lokasyon") İngilizce kanonik adlara (örn. "company_location") çevir.
    *   `df.dtypes` ile veri tiplerini kontrol et.
*   **Görev 1.2: Maaş Normalizasyonu (`salary_numeric` Oluşturma)**
    *   `salary_range` sütunundaki aralıkları (örn. "61-70") midpoint'e (örn. 65.5) çevir.
    *   "300+" gibi üst sınırı açık aralıklar için sabit bir değer (örn. 350) ata.
    *   Yeni sayısal sütun `salary_numeric` oluştur.
*   **Görev 1.3: Çoklu Seçim Parsing (Multi-Hot Encoding)**
    *   `programming_languages`, `frontend_technologies`, `tools` sütunlarındaki virgülle ayrılmış değerleri `sklearn.preprocessing.MultiLabelBinarizer` kullanarak binary (0/1) sütunlara dönüştür.
    *   Yeni sütun adları `lang__Python`, `frontend__React`, `tool__Redux` formatında olmalı.
*   **Görev 1.4: Kategorik ve Sıralı Kodlama**
    *   `company_location`, `employment_type`, `work_mode`, `role` için **One-Hot Encoding** (`pd.get_dummies`) uygula.
    *   `experience_years` sütununu ordinal olarak sayısal değerlere dönüştür (örn. "11-15" → 13, "30+" → 30).
    *   `level` sütunundan **`seniority_level_ic`** (ordinal: Junior=1, Mid=2, ..., Architect=6) ve **`management_level`** (One-Hot) sütunlarını türet.
    *   Yönetim rolleri için **`is_manager`** (binary: 1=yönetici, 0=değil) bayrağını oluştur.
    *   `gender` sütununu binary (Erkek=0, Kadın=1) olarak kodla.
*   **Görev 1.5: Çalışan Lokasyon Tahmini (`is_likely_in_company_location` Oluşturma)**
    *   `company_location` ve `work_mode` sütunlarını kullanarak, **çalışanın şirket lokasyonunda olma ihtimalini** gösteren `is_likely_in_company_location` (binary) sütunu oluştur.
    *   Kural: `company_location`'a eşit `work_mode` "Office" veya "Hybrid" ise `1`, aksi takdirde `0`.
*   **Görev 1.6: Aykırı Değer İşleme**
    *   `salary_numeric` sütununda IQR yöntemiyle **aykırı değerleri tespit et ve sınırlandır** (örn. üst sınır 350 bin TL).
*   **Görev 1.7: Temizlenmiş Veri Setini Kaydet**
    *   Tüm işleme adımlarından sonra elde edilen veri setini `2025_cleaned_data.csv` olarak kaydet.
    *   Bu dosya, gelecek sprint'lerdeki analizler için ana veri kaynağı olacaktır.

---

### Sprint 2: Temel Analizler ve Görselleştirmeler

**Hedef:** Birincil analiz hedeflerini gerçekleştirmek ve ilk statik/interaktif grafikleri oluşturmak.

*   **Görev 2.1: Birincil Hipotez Testleri**
    *   **React vs. Non-React Maaş Farkı**: React kullananlar ile diğerleri arasında maaş farkı olup olmadığını test et (T-testi/Mann-Whitney U).
    *   **Remote vs. Office Maaş Farkı**: Remote çalışanlar ile ofis/hibrit çalışanlar arasında maaş farkı olup olmadığını test et (T-testi/Mann-Whitney U).
    *   **Lokasyon Bazlı Maaş Farkı**: Avrupa/Amerika merkezli şirketlerde çalışanlar ile Türkiye merkezli olanlar arasında maaş farkı olup olmadığını test et (T-testi/Mann-Whitney U).
    *   **Cinsiyet Bazlı Maaş Farkı (Gender Gap)**: Kadın ve erkek çalışanlar arasında maaş farkı olup olmadığını test et (T-testi/Mann-Whitney U).
    *   Her test için **ortalama maaş farkını, p-değerini ve etki büyüklüğünü** (Cohen's d veya eta-squared) kaydet.
*   **Görev 2.2: Kapsamlı Boxplot Görselleştirmeleri**
    *   Aşağıdaki kategoriler için `salary_numeric` dağılımlarını gösteren **boxplot grafikleri** oluştur:
        *   **Kariyer Seviyeleri** (`seniority_level_ic`)
        *   **Yönetim Seviyeleri** (`management_level`)
        *   **İstihdam Türü** (`employment_type`)
        *   **Çalışma Modeli** (`work_mode`)
        *   **Şirket Lokasyonu** (`company_location`)
        *   **Cinsiyet** (`gender`)
        *   **Rol** (`role`)
    *   Her grafiğin hem **statik (PNG)** hem de **interaktif (Plotly)** versiyonlarını üret.
    *   Lokasyon bazlı grafiklerde **"Tahmini lokasyon..." uyarı notunu** ekle.
*   **Görev 2.3: Stack ROI Bar Plot Görselleştirmeleri**
    *   `languages_used`, `frontend_technologies` ve `tools` sütunlarındaki **tüm teknolojilerin ortalama maaş getirilerini** gösteren bar plotlar oluştur.
    *   Grafikleri getiriye göre yüksekten düşüğe sırala ve düşük oranlı teknolojileri (%5'ten az fark) hariç tutabilirsin.
    *   Hem **statik (PNG)** hem de **interaktif (Plotly)** versiyonlarını üret.
*   **Görev 2.4: Rol Bazlı Bar Plot Görselleştirmeleri**
    *   Farklı roller (`role`) arasındaki **ortalama maaş farklarını** gösteren bar plotlar oluştur.
    *   Hem **statik (PNG)** hem de **interaktif (Plotly)** versiyonlarını üret.

---

### Sprint 3: Gelişmiş Analizler ve Görselleştirmeler

**Hedef:** İkincil analiz hedeflerini gerçekleştirmek, kariyer ilerlemesi ve beceri gelişimi gibi daha derin içgörüler sunan görselleştirmeler oluşturmak.

*   **Görev 3.1: Şirket Lokasyonu İleri Analizleri**
    *   **Farklı Şirket Lokasyonlarına Göre Maaş Değişimi**: `company_location` sütunları için `salary_numeric` ile ANOVA veya Kruskal-Wallis testi uygula.
    *   **Yurtdışı TR Hub ve Avrupa Lokasyonlu Remote Çalışanların Maaş Politikaları**: `work_mode_Remote=1` ve `company_location_Avrupa=1` ile `company_location_Türkiye=1` kombinasyonları arasında maaş farkı testi yap (T-testi/Mann-Whitney U).
    *   Sonuçları (ortalama farklar, p-değeri, etki büyüklüğü) kaydet.
*   **Görev 3.2: Cinsiyet Bazlı Teknoloji Tercihleri Analizi**
    *   `gender` bazında `languages_used` ve `frontend_technologies` kullanım oranlarını frekans analizi ve chi-square testi ile incele.
    *   Kadın ve erkek çalışanların teknoloji tercihlerini gösteren **bar plotları** (örn. `sns.barplot(x='lang__Python', y='count', hue='gender')`) oluştur (PNG ve Plotly).
*   **Görev 3.3: Kariyer Progression & Timeline Analizi ve Görselleştirmeler**
    *   **Kariyer Seviyeleri ve Maaş İlişkisi**: Teknik (`seniority_level_ic`) ve yöneticilik (`management_level`) seviyelerinde maaş farklarını incele (ANOVA/Kruskal-Wallis ve Post-hoc testleri).
    *   **Deneyim vs. Maaş İlişkisi**: `years_experience` ile `salary_numeric` arasındaki Pearson korelasyonunu hesapla.
    *   **Deneyim vs. Maaş Scatter Plot**: `years_experience` ile `salary_numeric` ilişkisini, `seniority_level_ic` ile renklendirilmiş bir **scatter plot** olarak görselleştir (PNG ve Plotly).
    *   **Kariyer Progression Sankey Diyagramı**: Junior → Mid → Senior ve yöneticilik rolleri arasındaki geçişleri gösteren bir **Sankey diyagramı** oluştur (PNG ve Plotly).
*   **Görev 3.4: Skill Development Pattern'leri Analizi (Heatmap)**
    *   Hangi teknolojilerin (`languages_used`, `frontend_technologies`) veya araçların (`tools`) kariyer ilerlemesini (`seniority_level_ic`) hızlandırdığını korelasyon analizi ile incele.
    *   Teknoloji/araç kullanımı ve seviye arasındaki ilişkiyi gösteren bir **heatmap** oluştur (PNG ve Plotly).
*   **Görev 3.5: İstihdam Türü Analizi ve Görselleştirme**
    *   Farklı istihdam türleri (`employment_type`) arasında maaş farkı olup olmadığını test et (ANOVA/Kruskal-Wallis ve Post-hoc testleri).
    *   `employment_type` için maaş dağılımını gösteren **bar plot** oluştur (PNG ve Plotly).
*   **Görev 3.6: Saat Bazlı Anket Katılımı Analizi ve Görselleştirme**
    *   `timestamp` sütunundan anket doldurma saatini (`hour`) türet.
    *   Saat bazında maaş ortalamaları, rol ve demografik özelliklerdeki değişimleri incele (groupby('hour') ve ANOVA/Kruskal-Wallis).
    *   Saat bazlı maaş ortalamalarını gösteren **bar plot** (PNG ve Plotly) ve saat bazlı rol dağılımını gösteren **heatmap** (PNG ve Plotly) oluştur.

---

### Sprint 4: Raporlama ve Dashboard Geliştirme

**Hedef:** Tüm analiz ve görselleştirmeleri nihai LaTeX raporuna ve interaktif Streamlit dashboard'a entegre etmek.

*   **Görev 4.1: Statik LaTeX Rapor Taslağı Oluşturma**
    *   Projenin amacı, hedef kitle (React staj grubu ve geniş kitle), metodoloji, bulgular ve öneriler bölümlerini içeren LaTeX rapor yapısını Overleaf üzerinden oluştur.
    *   Raporun dili İngilizce olacak.
*   **Görev 4.2: Tüm Statik Grafikleri Rapora Entegre Etme**
    *   Sprint 2 ve 3'te üretilen tüm **PNG formatındaki grafikleri** (`\includegraphics` komutuyla) LaTeX raporuna ekle.
    *   Her grafiğe **anlaşılır ve merak uyandırıcı başlıklar** (örn. "Hangi Teknolojiler Daha Fazla Kazandırıyor?") ekle.
    *   Lokasyon içeren tüm grafiklerde **uyarı notunu** (`"Tahmini lokasyon..."`) zorunlu olarak ekle.
*   **Görev 4.3: Hipotez Test Sonuçlarını Rapora Yazma**
    *   Sprint 2 ve 3'te yapılan tüm hipotez testlerinin sonuçlarını (ortalama farklar, p-değerleri, etki büyüklükleri) **iş dünyası dostu, sezgisel bir dille** rapora entegre et.
    *   Örn. "React bilenler ayda 15 bin TL daha fazla kazanıyor" gibi ifadeler kullan.
*   **Görev 4.4: İçgörüler ve Öneriler Bölümünü Yazma**
    *   **React staj grubu için spesifik, uygulanabilir öneriler** ekle (örn. "React'e ek olarak Zustand öğrenmek maaş getirisini artırabilir").
    *   **Geniş kitle için genel sektör trendleri ve kariyer içgörüleri** ekle (örn. "Avrupa merkezli şirketlerde iş aramak maaşı artırabilir").
*   **Görev 4.5: Streamlit Dashboard Yapısını Oluşturma**
    *   `app.py` dosyasını oluşturarak temel Streamlit uygulamasını kur.
    *   `company_location`, `employment_type`, `work_mode`, `role`, `seniority_level_ic`, `gender` gibi sütunlar için **interaktif filtreleme** mekanizmaları entegre et.
*   **Görev 4.6: İnteraktif Grafikleri Dashboard'a Entegre Etme**
    *   Sprint 2 ve 3'te üretilen tüm **Plotly tabanlı interaktif grafikleri** (boxplot, bar plot, scatter plot, heatmap, Sankey) Streamlit dashboard'a ekle.
    *   Her grafiğin altına **kısa, anlaşılır içgörü özetleri** ekle (örn. "Remote çalışanlar ortalama %X daha fazla kazanıyor").
*   **Görev 4.7: Dashboard Performans Optimizasyonu**
    *   Dashboard'ın 2,970 satırlık veri setiyle **2 saniyeden daha kısa sürede yüklendiğini** doğrula.
    *   Filtreleme ve grafik etkileşimlerinin hızlı ve akıcı çalıştığından emin ol.

---

### Sprint 5: Kalite Kontrol, Test ve Yaygınlaştırma

**Hedef:** Projenin tüm başarı kriterlerini karşıladığını doğrulamak, kullanıcı testlerini tamamlamak ve çıktıları paylaşım için hazırlamak.

*   **Görev 5.1: Veri Kalitesi ve Encoding Doğrulaması**
    *   `2025_cleaned_data.csv` dosyasının **eksik veri içermediğini** ve tüm encoding adımlarının **doğru uygulandığını** (`df.isna().sum()`, `df.shape` kontrolleri) teyit et.
    *   Aykırı değer yönetiminin belirlenen sınırlar dahilinde çalıştığını kontrol et.
*   **Görev 5.2: Analiz Doğruluğu ve İçgörü Güvenilirliği Doğrulaması**
    *   Tüm istatistiksel testlerin (T-testi, ANOVA vb.) **METHODOLOGY.md'deki kılavuzlara uygun yapıldığını** ve sonuçlarının (p-değerleri, etki büyüklükleri) doğru raporlandığını kontrol et.
    *   Test varsayımlarının (örn. normallik, homojenlik) karşılandığını doğrula (Shapiro-Wilk, Levene testi).
*   **Görev 5.3: Görselleştirme Kalitesi Kontrolü**
    *   Tüm grafiklerin (en az 10 PNG ve 5+ interaktif) üretildiğini, **net başlıklar ve etiketler** içerdiğini kontrol et.
    *   Lokasyon notunun (`company_location` veya `is_likely_in_company_location` içeren grafiklerde) **tüm ilgili yerlerde bulunduğunu** doğrula.
*   **Görev 5.4: Kullanıcı Testleri (Rapor ve Dashboard)**
    *   En az **6 kullanıcı (3 React stajyeri, 3 sektör profesyoneli)** ile LaTeX raporunun ve Streamlit dashboard'ın **anlaşılırlık ve kullanılabilirliğini** test et.
    *   Raporda ve dashboard'da sunulan öneri/içgörülerin **%80+ faydalı bulunduğunu** doğrula.
*   **Görev 5.5: Portfolyo ve LinkedIn Paylaşım Hazırlığı**
    *   LaTeX raporunun PDF çıktısının (Overleaf üzerinden) **estetik ve profesyonel bir görünüme** sahip olduğunu kontrol et.
    *   Streamlit dashboard'ın **mobil uyumluluğunu** test et.
    *   LinkedIn'de paylaşım için **en az 1 çarpıcı grafik** (örn. "Hangi Teknolojiler Daha Fazla Kazandırıyor?") ve başlık seç.
*   **Görev 5.6: Kod Tekrarlanabilirliği ve Dokümantasyon**
    *   Tüm analiz ve görselleştirme kodlarının (Jupyter Notebook veya Python script'leri) **belgelenmiş, yorumlu ve tekrarlanabilir** olduğunu teyit et.
*   **Görev 5.7: Proje Yaygınlaştırma**
    *   Streamlit dashboard'u **yerel veya bulut tabanlı** olarak yayına al.
    *   Nihai LaTeX raporunu PDF formatında (`maas_analizi_2025.pdf`) oluştur.
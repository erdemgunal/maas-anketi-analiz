# Product Requirements Document (PRD)  
## Proje: 2025 Yazılım Sektörü Maaş Analizi

---

### 1. Genel Tanım
Bu proje, 20-21 Ağustos 2025’te toplanan `2025_maas_anket.csv` verisinden (n=2,970) hareketle yazılım sektöründe maaş dinamiklerini incelemeyi amaçlar.  
Hedef kitle ikiye ayrılır:  
- **React Staj Grubu (~250 yazılımcı)** → Eğitim ve kariyer planlama içgörüleri.  
- **Geniş Kitle (sektör meraklıları, LinkedIn paylaşımları)** → Genel maaş trendleri, teknoloji ROI, çalışma modelleri.  

Çıktılar; statik rapor (LaTeX), interaktif dashboard (Streamlit) ve görsel özetlerden oluşacaktır.

---

### 2. Hedefler
- **Kapsamlı raporlama ve görselleştirme** (maaş dağılımları, roller, teknolojiler, lokasyon etkisi).  
- **Stack ROI analizi** (hangi dil, framework veya tool maaşı artırıyor?).  
- **İstatistiksel hipotez testleri** (React vs. non-React, Remote vs. Office, Lokasyon farkları, Gender gap).  
- **Kariyer progression & timeline** (deneyim yılı vs. maaş, seviyeler arası geçişler).  
- **Erişilebilir raporlama**: İstatistik bilmeyen okuyuculara hitap eden, iş dünyası dostu dil.  

---

### 3. Veri
- **Kaynak**: `2025_maas_anket.csv` (Google Sheets export).  
- **Boyut**: 2,970 satır.  
- **Temizlenmiş veri**: `2025_cleaned_data.csv`.  
- **Ana sütunlar (kanonik adlar)**  
  - `timestamp` (datetime) ← *Timestamp*  
  - `company_location` (categorical) ← *Şirket lokasyon*  
  - `employment_type` (categorical) ← *Çalışma türü*  
  - `work_mode` (categorical) ← *Çalışma şekli*  
  - `gender` (categorical) ← *Cinsiyet*  
  - `years_experience` (numeric/ordinal) ← *Toplam kaç yıllık iş deneyimin var?*  
  - `seniority_level_ic` (ordinal, 1–6) ← *Hangi seviyedesin?* (IC: Junior→Architect)  
  - `management_level` (categorical) ← *Yönetim seviyeleri* (Engineering Manager, Director, C-Level, Partner)  
  - `is_manager` (binary) ← türetilmiş (yönetim seviyesi varsa 1, yoksa 0)  
  - `role` (categorical) ← *Ne yapıyorsun?* (Frontend, Backend, Fullstack, …)  
  - `languages_used` (multi-categorical) ← *Hangi programlama dillerini kullanıyorsun*  
  - `frontend_technologies` (multi-categorical) ← *Frontend yazıyorsan hangilerini kullanıyorsun*  
  - `tools` (multi-categorical) ← *Hangi tool’ları kullanıyorsun*  
  - `salary_range` (ordinal) ← *Aylık ortalama net kaç bin TL alıyorsun?*  
  - `salary_numeric` (numeric) ← `salary_range` orta noktası (örn. 61–70 → 65.5; 300+ → 350)

- **Ön işleme / Encoding**  
  - `timestamp`: `pd.to_datetime`; türevler → `year`, `month`, `day`, `hour`.  
  - `years_experience`: aralıklar orta nokta ile sayısala (örn. 11–15 → 13, 30+ → 30).  
  - `seniority_level_ic`: ordinal eşleme (Junior=1, Mid=2, Senior=3, Staff=4, TeamLead=5, Architect=6).  
  - `management_level`: One-Hot; `is_manager` bayrağı türetilir.  
  - `company_location`, `employment_type`, `work_mode`, `role`: One-Hot (`pd.get_dummies`).  
  - `languages_used`, `frontend_technologies`, `tools`: `MultiLabelBinarizer`  
    - sütun adları: `lang__Python`, `lang__JavaScript`, `frontend__React`, `tool__Redux`, …  
  - `salary_range` → `salary_numeric`: orta nokta haritalaması; üst sınır `300+` → `350` (capping).  
  - **Tahmini lokasyon**: `is_likely_in_company_location`  
    - Kurallar:  
      - Şirket Lokasyon ∈ {Türkiye, Avrupa, Amerika}  
      - Çalışma Şekli = Office → 1  
      - Çalışma Şekli = Hybrid → 1  
      - Çalışma Şekli = Remote → 0  
      - Şirket Lokasyon = Yurtdışı TR hub  
        - Çalışma Şekli = Remote → 0 (Türkiye’de olabilir ama net değil)  
        - Çalışma Şekli = Hybrid veya Office → 0 (aykırı değer say → direkt dışarıda bırak)  
    - Raporlarda şu uyarı zorunlu: *“Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır. Kesin değildir.”*


---

### 4. Metodoloji
- **İstatistiksel yöntemler**: T-testi, Mann-Whitney U, ANOVA, Kruskal-Wallis, Post-hoc (Tukey HSD), Pearson korelasyonu.  
- **Veri işleme**: Aykırı değer kontrolü (IQR/Z-score), salary capping (350k).  
- **Kodlama araçları**: `pandas`, `sklearn`, `scipy`, `statsmodels`.  
- **Görselleştirme**: `seaborn`, `matplotlib`, `plotly` (Streamlit için).  
- **Not**: Lokasyon içeren tüm grafiklerde şu ibare zorunlu:  
  _“Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır (Office/Hybrid → şirket lokasyonunda). Kesin değildir.”_

---

### 5. Beklenen Çıktılar
#### 5.1 Statik Grafikler (PNG, LaTeX’e entegre)
- **Boxplot**: Seviye, yönetim, istihdam türü, çalışma modeli, lokasyon, cinsiyet, rol.  
- **Bar Plot**: Teknoloji ROI, rol, istihdam türü, saat bazlı maaş trendleri, cinsiyet bazlı teknoloji tercihleri.  
- **Scatter Plot**: Deneyim yılı vs. maaş (kariyer timeline).  
- **Heatmap**: Teknoloji/araç kombinasyonlarının maaş etkisi, saat bazlı katılım, korelasyon ısı haritası, Work Type x Location maaş matrisi.  
- **Sankey Diyagramı**: Kariyer progression (Junior → Mid → Senior → Yöneticilik).  
- **Line Plot**: Career Progression - Salary Growth (`is_likely_in_company_location == 1` filtresiyle Türkiye/Avrupa/Amerika için Junior→Mid→Senior maaş gelişimi).  
- **Violin Plot**: Skill Diversity (dil+frontend+tool çeşitliliği) ile maaş dağılımı.  

---

#### 5.2 Rapor (PDF, LaTeX / Overleaf)
- **Bölümler**: Giriş, Yöntem, Bulgular, Öneriler.  
- **Başlık örnekleri**:  
  - “Hangi Teknolojiler Daha Fazla Kazandırıyor?”  
  - “Kariyer Seviyeleri ve Roller Maaşı Nasıl Etkiliyor?”  
  - “Hangi İstihdam Türü Daha Kazançlı?”  
- **İçerik**: Hipotez test sonuçları, p-değerleri, etki büyüklükleri (Cohen’s d, eta-squared).  
- **Öneriler**: React staj grubu için teknoloji öğrenimi tavsiyeleri, geniş kitle için lokasyon & çalışma modeli trendleri.  

---

#### 5.3 Interaktif Dashboard (Streamlit + Plotly)
- **Filtreler**: `company_location`, `employment_type`, `work_mode`, `role`, `seniority_level_ic`, `gender`.  
- **Grafikler**: Boxplot, bar plot, scatter plot, heatmap, Sankey.  
- **Kullanıcı deneyimi**: Grafiğin altında kısa, iş dünyası dostu özet (örn. “Remote çalışanlar ortalama %X daha fazla kazanıyor”).  

---

### 6. Başarı Kriterleri
- Veri temizleme sonrası `2025_cleaned_data.csv` eksiksiz, doğru encode edilmiş olacak.  
- Tüm grafikler hem PNG hem interaktif versiyon olarak üretilecek.  
- Rapor, istatistik bilmeyen okuyucuların da anlayacağı dilde olacak.  
- React staj grubu için doğrudan kullanılabilir öneriler (örn. “React + Zustand öğrenmek maaşı artırır”).  
- LinkedIn paylaşımı için ilgi çekici başlık ve grafikler üretilecek.  

---

### 7. Kullanım Senaryoları
- **React Staj Grubu** → Eğitim modüllerinde “hangi teknolojiyi öğrenmeliyim” sorusuna yanıt.  
- **Sektör Profesyonelleri** → Kariyer progression, istihdam türü ve lokasyon bazlı trendleri inceleme.  
- **LinkedIn & Portfolyo Paylaşımı** → İlgi çekici grafik ve başlıklarla kitle çekmek.  

---

### 📚 DOKÜMANTASYON İNDEKSİ (DOCUMENTATION INDEX)

#### 📊 Veri ve Analiz Dokümanları
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Detaylı proje özeti ve kapsamı  
- **[DATASET_SPECIFICATIONS.md](DATASET_SPECIFICATIONS.md)** - Veri seti detayları ve yapısı  
- **[ANALYSIS_OBJECTIVES.md](ANALYSIS_OBJECTIVES.md)** - Analiz hedefleri ve kategorileri  
- **[METHODOLOGY.md](METHODOLOGY.md)** - Metodoloji ve teknik detaylar  

#### 🛠️ Teknik Dokümanlar
- **[EXPECTED_OUTPUTS.md](EXPECTED_OUTPUTS.md)** - Beklenen çıktılar ve formatlar  
- **[SUCCESS_CRITERIA.md](SUCCESS_CRITERIA.md)** - Başarı kriterleri ve değerlendirme  
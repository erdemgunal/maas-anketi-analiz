**Proje Hedefi:** React staj grubuna değer katacak, bilimsel metodlarla hazırlanmış kapsamlı bir maaş analizi raporu üretmek.

İşte sprint bazlı detaylı görevlendirmelerimiz:

---

### **Sprint 0: Proje Başlangıcı ve Planlama (0.5 Saat - Geliştirici ve PM)**

Bu aşama, projenin genel kapsamını anlamak ve sprint'ler öncesi gerekli kurulumları yapmak içindir.

*   **Görev 0.1: Dokümantasyon İncelemesi ve Anlama**
    *   `PRD.MD`, `PROJECT_OVERVIEW.md`, `ANALYSIS_OBJECTIVES.md`, `DATASET_SPECIFICATIONS.md` ve `WORKFLOW.md` belgelerini detaylıca okuyarak projenin hedeflerini, veri yapısını ve iş akışını anla.
    *   **Çıktı:** Proje hedeflerine dair ortak bir anlayış.
*   **Görev 0.2: Geliştirme Ortamı Kurulumu**
    *   Python 3.8+ sürümünün kurulu olduğundan emin ol.
    *   `venv` veya `conda` kullanarak bir sanal ortam oluştur.
    *   Gerekli Python kütüphanelerini (pandas, numpy, scikit-learn, matplotlib, seaborn, plotly, streamlit vb.) kur.
    *   **Çıktı:** Proje için hazır, izole geliştirme ortamı.
*   **Görev 0.3: Dosya Yapısını Oluşturma**
    *   `FILE_STRUCTURE.md` belgesine uygun olarak ana klasör ve alt klasör yapılarını oluştur (Data, src, Notebooks, Outputs, Reports, Dashboard vb.).
    *   **Çıktı:** Düzenli ve standartlara uygun proje dosya yapısı.

---

### **Sprint 1: Veri Hazırlama ve Ön İşleme (2 Saat)**

Bu sprint, ham veriyi temiz, tutarlı ve analiz edilebilir bir formata getirmeyi amaçlar.

*   **Görev 1.1: Ham Veriyi Yükleme ve İlk Keşifsel Analiz (EDA)**
    *   `maas_anketi.csv` dosyasını pandas DataFrame olarak yükle.
    *   `01_exploratory_data_analysis.ipynb` dosyasında ilk 5 satırı görüntüle, sütun adlarını ve veri tiplerini kontrol et.
    *   Temel istatistiksel özetleri (mean, median, count vb.) çıkar.
    *   **Çıktı:** Verinin genel yapısının anlaşılması, `01_exploratory_data_analysis.ipynb` notebook'una başlangıç.
*   **Görev 1.2: Veri Kalitesi Değerlendirmesi ve Eksik Veri İşleme**
    *   Her sütundaki eksik veri oranlarını (`Completeness < %5` hedefi) belirle.
    *   Eksik veriler için uygun imputation stratejilerini uygula (`DATASET_SPECIFICATIONS.md` ve `METHODOLOGY.md` referans alınacak).
    *   **Çıktı:** Eksik veri raporu, `cleaned_data.csv` için temel temizlik.
*   **Görev 1.3: Maaş Normalizasyonu ve Outlier Tespiti**
    *   "Aylık ortalama net kaç bin TL alıyorsun?" sütunundaki aralık değerlerini sayısal ortalamaya çevir (örn: "61-70" → 65).
    *   IQR veya Z-Score metodu kullanarak aykırı değerleri (outliers) tespit et ve ele al (`Outlier oranı < %3` hedefi).
    *   **Çıktı:** Sayısal maaş sütunu, aykırı değerlerden arındırılmış veri.
*   **Görev 1.4: Teknoloji Ayrıştırma ve Kategorik Kodlama (Feature Engineering)**
    *   Virgülle ayrılmış teknoloji sütunlarını (örn: "Hangi programlama dillerini kullanıyorsun") ayrı binary (dummy) değişkenlere böl.
    *   String deneyim değerlerini sayısal değerlere dönüştür (örn: "11-15" → 13).
    *   Diğer kategorik sütunları (örn: "Cinsiyet", "Şirket lokasyon") Label Encoding veya One-Hot Encoding ile kodla.
    *   **Çıktı:** `cleaned_data.csv` (temizlenmiş ve işlenmiş veri).
    *   **Tanım Kriteri:** Tüm veri işleme adımları `data_cleaning.py` dosyasında belgelenmiş ve `cleaned_data.csv` oluşturulmuş olmalı. `Completeness < %5` ve `Outlier oranı < %3` hedefleri sağlanmalı.

---

### **Sprint 2: İstatistiksel Analiz (3 Saat)**

Bu sprint, belirlenen hipotezleri test ederek ve deskriptif istatistikler üreterek veri hakkında derinlemesine içgörüler elde etmeyi hedefler.

*   **Görev 2.1: Deskriptif İstatistikler ve Temel Grafikler**
    *   Yaş, deneyim, maaş gibi temel demografik ve maaş bilgilerinin dağılımını analiz et.
    *   Ortalama, medyan, standart sapma gibi deskriptif istatistikleri hesapla.
    *   **Çıktı:** Temel analiz grafikleri için ilk 5 PNG grafik (`figures/` klasörüne).
*   **Görev 2.2: Hipotez Testlerinin Uygulanması**
    *   **React vs non-React:** React kullanan ve kullanmayan geliştiriciler arasındaki maaş farkını analiz et (t-test).
    *   **Remote vs Office:** Uzaktan, hibrit ve ofis çalışma şekillerinin maaş üzerindeki etkisini incele (ANOVA).
    *   **Lokasyon bazlı:** Türkiye içindeki şehirler ve Avrupa gibi coğrafi lokasyonların maaş farklarını analiz et.
    *   **Cinsiyet analizi:** Cinsiyet bazlı maaş farklarını tespit et (`Gender gap tespiti`).
    *   **Çıktı:** İstatistiksel test sonuç tabloları (`tables/` klasörüne). `statistical_analysis.py` dosyasına ilgili test fonksiyonlarını ekle.
*   **Görev 2.3: Korelasyon Analizi**
    *   Deneyim, teknoloji kullanımı ve maaş arasındaki ilişkileri belirle.
    *   **Çıktı:** Korelasyon matrisi görselleştirmesi (`figures/` klasörüne).
*   **Görev 2.4: Güven Aralıkları ve Etki Büyüklüğü Hesaplamaları**
    *   Her anlamlı istatistiksel test için %95 güven aralıklarını hesapla.
    *   Cohen's d ve eta-squared gibi etki büyüklüğü metriklerini raporla.
    *   **Tanım Kriteri:** En az 5 anlamlı hipotez testi (p < 0.05) yapılmış, etki büyüklükleri ve güven aralıkları hesaplanmış olmalı. Sonuçlar `02_statistical_tests.ipynb` notebook'unda ve `statistical_analysis.py`'de belgelenmiş olmalı.

---

### **Sprint 3: Makine Öğrenmesi Modelleri (2 Saat)**

Bu sprint, maaş tahmin modelini geliştirmeyi ve geliştirici profillerini kümelemeyi hedefler.

*   **Görev 3.1: Maaş Tahmin Modeli Eğitimi**
    *   `machine_learning.py` dosyasında Random Forest ve XGBoost regresyon modellerini uygula.
    *   Veriyi %80 eğitim, %20 test seti olarak böl.
    *   Modelleri eğit ve ilk tahminleri yap.
    *   **Amaç:** R² > 0.75 açıklama gücüne ulaşmak.
    *   **Çıktı:** Eğitilmiş modeller (`models/` klasörüne kaydedilecek).
*   **Görev 3.2: Model Değerlendirme ve Çapraz Doğrulama**
    *   Modellerin performansını R², MAE, RMSE gibi metriklerle değerlendir.
    *   5-katlı çapraz doğrulama (5-fold CV) uygulayarak modelin genellenebilirliğini kontrol et (CV R² > 0.70 hedefi).
    *   **Çıktı:** Model performans raporu (tablo olarak).
*   **Görev 3.3: Feature Importance Analizi**
    *   Maaş tahmini üzerinde en etkili olan 10 özelliği (feature) belirle.
    *   **Çıktı:** Feature importance sıralaması (tablo veya grafik olarak).
*   **Görev 3.4: Developer Profil Clustering (K-means)**
    *   K-means algoritmasını kullanarak 3-5 farklı geliştirici persona grubu oluştur.
    *   Her grubun karakteristik özelliklerini (teknoloji tercihleri, deneyim, ortalama maaş vb.) analiz et.
    *   **Çıktı:** Kümeleme sonuçları ve her grubun profili.
    *   **Tanım Kriteri:** Maaş tahmin modelinin R² > 0.75 hedefini karşılaması, feature importance analizinin yapılması ve 3-5 developer profili oluşturulmuş olması. Tüm ML süreçleri `03_machine_learning.ipynb` notebook'unda ve `machine_learning.py`'de belgelenmiş olmalı.

---

### **Sprint 4: Görselleştirme (2 Saat)**

Bu sprint, analiz sonuçlarını etkili ve anlaşılır grafikler aracılığıyla sunmayı hedefler.

*   **Görev 4.1: 20+ Grafik Oluşturma ve Kategorizasyon**
    *   `visualizations.py` dosyasını kullanarak belirlenen analiz kategorilerine (temel, teknoloji, kariyer, ML, ek) uygun en az 20 adet PNG grafik oluştur.
    *   Örnek grafik türleri: Histogram, Bar Chart, Box Plot, Scatter Plot, Korelasyon Matrisi.
    *   **Çıktı:** `figures/` klasöründe 20+ PNG grafik dosyası.
*   **Görev 4.2: Yayın Kalitesinde Formatlama ve Kalite Kontrol**
    *   Tüm grafiklerin **300 DPI çözünürlükte, 12x8 inç boyutunda ve PNG formatında** olmasını sağla.
    *   `VISUAL_STANDARDS.md` belgesindeki **tutarlı renk paleti**, Arial/Helvetica fontları (minimum 10pt) ve başlık/etiket standartlarını uygula.
    *   Grafiklerin renk körü dostu ve yeterli kontrast oranına sahip olduğundan emin ol.
    *   **Çıktı:** Yüksek kaliteli, profesyonel standartlara uygun grafikler.
    *   **Tanım Kriteri:** `figures/` klasöründe en az 20 adet, `publication quality` (yayın kalitesinde) ve `VISUAL_STANDARDS.md`'ye uygun formatlanmış PNG grafik bulunmalı.

---

### **Sprint 5: Raporlama ve Dağıtım (1 Saat)**

Bu son sprint, projenin çıktılarını bir araya getirerek raporu tamamlamayı ve interaktif dashboard'u devreye almayı amaçlar.

*   **Görev 5.1: LaTeX Raporunun Derlenmesi ve Final PDF Oluşturma**
    *   `latex_report/` klasöründeki LaTeX kaynak dosyalarını kullanarak **15-20 sayfalık bilimsel raporu** derle.
    *   Raporun `APA Format`'a uygun olduğundan, tüm figürlerin numaralandırılmış ve başlıklandırılmış olduğundan emin ol.
    *   **Executive Summary** (2 sayfa), Giriş, Metodoloji, Sonuçlar, Tartışma, Sonuç ve Referanslar bölümlerini tamamla.
    *   **Çıktı:** `final_report.pdf` dosyası (`Reports/` klasöründe).
*   **Görev 5.2: Streamlit Dashboard Uygulamasının Geliştirilmesi ve Dağıtımı**
    *   `app.py` dosyasında Streamlit web uygulamasını geliştir.
    *   Uygulamanın **interaktif grafikler, filtreleme seçenekleri, maaş tahmin aracı ve karşılaştırma modülleri** içermesini sağla.
    *   Uygulamayı yerel olarak `localhost:8501` adresinde çalışacak şekilde dağıt.
    *   **Çıktı:** Çalışır durumda bir Streamlit dashboard'u.
*   **Görev 5.3: Proje Metadata ve Diğer Çıktıların Düzenlenmesi**
    *   Proje metadata ve konfigürasyon dosyalarını kontrol et.
    *   Tüm çıktıların (grafikler, tablolar, modeller) ilgili klasörlerde düzenli olduğundan emin ol.
    *   **Çıktı:** Tüm proje çıktılarının eksiksiz ve düzenli teslimi.
    *   **Tanım Kriteri:** 15-20 sayfalık `final_report.pdf` dosyasının hazır olması, interaktif Streamlit dashboard'un çalışır durumda olması ve tüm eğitilmiş modellerin `models/` klasöründe bulunması.

---

### **Genel Proje Başarı ve Kalite Kontrolü:**

Her sprint sonunda ve projenin sonunda aşağıdaki kriterler kontrol edilecektir:

*   **Model Performansı:** Maaş tahmin modeli için **R² > 0.75**.
*   **İstatistiksel Anlamlılık:** Tüm hipotez testleri için **p < 0.05**.
*   **Veri Kullanımı:** Anket verisinin tamamının (n=2970) kullanılması ve eksik veri oranının **<%5** olması.
*   **Görsel Kalite:** En az **20 adet yayın kalitesinde** (300 DPI) profesyonel grafik.
*   **İçerik:** React staj grubuna yönelik **pratik kariyer önerileri** sunulması, **teknoloji ROI analizi** ve **küresel benchmark karşılaştırması**.
*   **Kod Kalitesi:** `CODING_GUIDELINES.md`'ye (Single Responsibility, DRY, KISS, Clean Code, Type Hints, Error Handling) uygunluk.
*   **Zaman Kısıtı:** Tüm projenin **10 saat içinde** tamamlanması.

Bu detaylı görevlendirmelerle, sıkı zaman çizelgemize rağmen projemizi başarıyla tamamlayacağımıza inanıyorum! İyi çalışmalar dilerim.
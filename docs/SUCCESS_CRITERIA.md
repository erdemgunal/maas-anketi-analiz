# Başarı Kriterleri

Bu belge, 2025 Yazılım Endüstrisi Maaş Analizi projesinin başarı kriterlerini tanımlamaktadır. Kriterler, projenin hedeflerine (`ANALYSIS_OBJECTIVES.md`), veri işleme gereksinimlerine (`DATASET_SPECIFICATIONS.md`, `METHODOLOGY.md`), beklenen çıktılara (`EXPECTED_OUTPUTS.md`), ürün gereksinimlerine (`PRD.md`) ve teknik yığına (TECHNICAL_STACK.md) uygun olup olmadığını değerlendirir. Proje, React stajyer grubu (~250 geliştirici) ve daha geniş bir kitle (ör. yazılım endüstrisi meraklıları, LinkedIn takipçileri) için tasarlanmıştır.

## 1. Genel Başarı Kriterleri
Projenin başarısı, aşağıdaki ana kategorilerde değerlendirilecektir:
- **Veri Kalitesi**: Temizlenmiş veri seti (`2025_cleaned_data.csv`) eksiksiz ve doğru olmalı.
- **Analiz Doğruluğu**: İstatistiksel testler ve içgörüler güvenilir olmalı.
- **Görselleştirme Kalitesi**: Grafikler ve dashboard anlaşılır, estetik ve işlevsel olmalı.
- **Kullanıcı Deneyimi (UX)**: Rapor ve dashboard, istatistik bilmeyen kullanıcılar için sezgisel olmalı.
- **Etkileşim ve Paylaşım**: LinkedIn paylaşımı ve portfolyo için çarpıcı, paylaşılabilir çıktılar üretilmeli.
- **Milestone kontrolleri**: Önemli proje aşamaları zamanında tamamlanmalı ve kalite standartlarını karşılamalıdır.
- **Bilimsel Titizlik**: Analizler metodolojik olarak sağlam ve tekrarlanabilir olmalıdır.

## 2. Detaylı Kriterler
### 2.1. Veri Kalitesi
- **Eksiksiz Veri**:
  - **Kriter**: `2025_cleaned_data.csv`’de eksik veri oranı %0 olmalı.
  - **Ölçüm**: `df.isna().sum()` ile kontrol, tüm sütunlar için 0 dönmeli.
  - **Referans**: `DATASET_SPECIFICATIONS.md`’deki veri işleme gereksinimleri.
- **Doğru Encoding**:
  - **Kriter**: `programming_languages`, `frontend_technologies`, `tools` için `MultiLabelBinarizer`, `company_location`, `employment_type`, `work_mode`, `role`, `management_level` için one-hot encoding, `salary_numeric` için maaş normalizasyonu doğru uygulanmalı.
  - **Ölçüm**: Örnek veri (n=100) ile encoding sonuçları manuel doğrulama (örn. `programming_Python` sütunu doğru etiketlenmeli).
  - **Referans**: `DATASET_SPECIFICATIONS.md`’deki encoding önerileri.
- **Aykırı Değer Yönetimi**:
  - **Kriter**: `salary_numeric` için IQR yöntemiyle aykırı değerler sınırlandırılmalı (üst sınır: 350k TL).
  - **Ölçüm**: `Q1 - 1.5*IQR` ve `Q3 + 1.5*IQR` dışındaki değerler kontrol edilip raporlanmalı.
  - **Referans**: `METHODOLOGY.md`’deki aykırı değer kontrolü.

### 2.2. Analiz Doğruluğu
- **İstatistiksel Testler**:
  - **Kriter**: T-testi, Mann-Whitney U, ANOVA, Kruskal-Wallis ve Post-hoc testler (Tukey HSD) doğru uygulanmalı, p-değerleri <0.05 için anlamlı sonuçlar raporlanmalı.
  - **Ölçüm**: Test sonuçları (örn. `p_value`, Cohen’s d, eta-squared) `METHODOLOGY.md`’deki yöntemlerle uyumlu olmalı; en az 5 hipotez testi (React vs. non-React, Remote vs. Office, vb.) tamamlanmalı.
  - **Referans**: `ANALYSIS_OBJECTIVES.md`’deki hipotezler.
- **İçgörü Güvenilirliği**:
  - **Kriter**: İçgörüler (örn. “React bilenler %X daha fazla kazanıyor”) istatistiksel testlerle desteklenmeli.
  - **Ölçüm**: Her içgörü için p-değeri ve etki büyüklüğü raporlanmalı (örn. LaTeX raporda).
  - **Referans**: `EXPECTED_OUTPUTS.md`’deki rapor içeriği.

### 2.3. Görselleştirme Kalitesi
- **Grafik Üretimi**:
  - **Kriter**: Tüm grafikler (boxplot, bar plot, scatter plot, heatmap, Sankey diyagramı) hem PNG hem interaktif (`plotly`) formatta üretilmeli.
  - **Ölçüm**: En az 17 PNG dosyası (mevcutlara ek 7 yeni grafik: Career Progression line, Top Tech Combinations by Role, Korelasyon Isı Haritası, Work Type x Location heatmap, Work Arrangement by Role stacked bar, Skill Diversity violin, ayrıca gerektiğinde türev varyantlar) ve Streamlit dashboard’da 7+ yeni interaktif grafik.
  - **Referans**: `EXPECTED_OUTPUTS.md`’deki grafik tanımları.
- **Netlik**:
  - **Kriter**: Grafikler, istatistik bilmeyen kullanıcılar için anlaşılır başlıklar ve etiketler içermeli (örn. “Hangi Teknolojiler Daha Fazla Kazandırıyor?”).
  - **Referans**: `PRD.md`’deki başlıklar.
- **Lokasyon Notu**:
  - **Kriter**: `company_location` veya `is_likely_in_company_location` içeren grafiklerde şu not zorunlu: “Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır (Office/Hybrid → şirket lokasyonunda). Kesin değildir.”
  - **Ölçüm**: Tüm ilgili grafiklerde notun varlığı kontrol edilmeli.
  - **Referans**: `DATASET_SPECIFICATIONS.md` ve `EXPECTED_OUTPUTS.md`.
  - **Ek Not**: Career Progression line grafiğinde `is_likely_in_company_location == 1` filtresi uygulandığı belirtilmelidir.

### 2.4. Kullanıcı Deneyimi (UX)
- **Rapor Anlaşılırlığı**:
  - **Kriter**: LaTeX raporu (`maas_analizi_2025.pdf`), istatistik bilgisi olmayan kullanıcıların da anlayabileceği, iş dünyasına uygun bir İngilizce ile yazılmalıdır.
  - **Referans**: `PRD.md`’deki rapor bölümleri.
- **Dashboard Kullanılabilirliği**:
  - **Kriter**: Streamlit dashboard, sezgisel filtreleme (`company_location`, `employment_type`, vb.) ve hızlı yükleme (<2 saniye) sunmalı.
  - **Ölçüm**: 2,970 satırlık veriyle yükleme süresi testi, filtreleme için ortalama gezinme süresi <5 dakika.
  - **Referans**: `PRD.md`’deki dashboard özellikleri.
- **Öneriler**:
  - **Kriter**: React staj grubu için en az 3 kullanılabilir öneri (örn. “React + Zustand öğrenmek maaşı %X artırır”), geniş kitle için 5+ içgörü (örn. “Avrupa merkezli şirketler %X daha fazla ödüyor”).
  - **Ölçüm**: Rapor ve dashboard’da öneri/içgörü sayısı.
  - **Referans**: `ANALYSIS_OBJECTIVES.md` ve `PRD.md`.

### 2.5. Milestone kontrolleri
- **Veri Hazırlama**:
  - **Kriter**: `2025_cleaned_data.csv`, proje milestone 1'e kadar tüm ön işleme adımları (normalleştirme, kodlama, aykırı değerlerin işlenmesi) tamamlanmış olarak.
  - **Ölçüm**: Veri kümesini `pandas` kontrolleriyle (ör. kodlamadan sonra sütunlar için `df.shape == (2970, 50+)`) ve eksik değer olmadan doğrulayın
  - **Referans**: `DATASET_SPECIFICATIONS.md`, `METHODOLOGY.md`.
- **Analiz Tamamlama**:
  - **Kriter**: 2. milestone da oluşturulan tüm istatistiksel testler (5+ hipotez) ve içgörüler.
  - **Ölçüm**: Jupyter Notebook veya komut dosyasında belgelenen test sonuçlarını (p değerleri, etki büyüklükleri) onaylayın.
  - **Referans**: `METHODOLOGY.md`, `ANALYSIS_OBJECTIVES.md`.
- **Görselleştirme Teslimi**:
  - **Kriter**: 3. aşamada üretilen tüm grafikler (10+ PNG, 5+ etkileşimli).
  - **Ölçüm**: `/docs/figures` içindeki PNG dosyalarını ve Streamlit kontrol panelindeki etkileşimli grafikleri doğrulayın.
  - **Referans**: `EXPECTED_OUTPUTS.md`.
- **Rapor ve Kontrol Paneli Sonlandırma**:
  - **Kriter**: LaTeX raporu (`maas_analizi_2025.pdf`) ve Streamlit kontrol paneli (`app.py`) milestone 4 ile sonlandırılır.
  - **Ölçüm**: Overleaf'te PDF derlemesini ve kontrol paneli işlevselliğini (filtreler, yükleme süresi <2 saniye) onaylayın.
  - **Referans**: `PRD.md`, `TECHNICAL_STACK.md`.
- **Kullanıcı Test**:
  - **Kriter**:  Kullanıcı testi milestone 5'e kadar tamamlanmış, %80+ netlik ve kullanılabilirlik derecesi.
  - **Ölçüm**: Anket veya görüşmeler yoluyla geri bildirim toplanır.
  - **Referans**: `PRD.md`.

### 2.6. Bilimsel Titizlik
- **Metodolojik Doğruluk**:
  - **Kriter**: İstatistiksel testler (T-testi, ANOVA vb.) `METHODOLOGY.md` kılavuzuna uygun olmalı ve doğru varsayımlara dayanmalıdır (ör. T-testi için normallik, ANOVA için homojenlik).
  - **Ölçüm**: Test varsayımlarını doğrulayın (ör. normallik için Shapiro-Wilk, homojenlik için Levene testi) ve sonuçları raporlayın.
  - **Referans**: `METHODOLOGY.md`.
- **Metodolojik Doğruluk**:
  - **Kriter**: Tüm analizler ve görselleştirmeler, belgelenmiş kod kullanılarak tekrarlanabilir olmalıdır.
  - **Ölçüm**: `2025_cleaned_data.csv` dosyasındaki tüm çıktıları yeniden üreten, yorumlu kod içeren Jupyter Notebook veya Python komut dosyası sağlayın.
  - **Referans**: `TECHNICAL_STACK.md`.
- **Şeffaflık**:
  - **Kriter**: Tüm içgörüler istatistiksel kanıtlar (p-değeri, etki büyüklüğü) ve sınırlamalar (ör. konum tahmini) içermelidir.
  - **Ölçüm**: Rapor ve gösterge tablosunda p değerlerinin, etki büyüklüklerinin ve notların (ör. konum notu) dahil edildiğini doğrulayın.
  - **Referans**: `EXPECTED_OUTPUTS.md`, `DATASET_SPECIFICATIONS.md`.


## 3. Değerlendirme Yöntemleri
- **Veri Kontrolü**: `pandas` ile veri kalitesi testleri (`df.isna().sum()`, encoding doğrulama).
- **İstatistiksel Doğrulama**: Test sonuçlarının `METHODOLOGY.md`’deki yöntemlerle uyumu, p-değerleri ve etki büyüklükleri kontrolü.
- **Performans Testi**: Streamlit dashboard’ın yükleme süresi (2,970 satırlık veriyle <2 saniye).
- **Etkileşim Takibi**: LinkedIn paylaşımı sonrası etkileşim sayısı (beğeni, yorum, paylaşım).

## 4. Notlar
- **Erişim**: Google Sheets linki sınırlı (https://docs.google.com/spreadsheets/d/1J_MW7t9e2Yi1cErFe5XCnNGaFqXkrdufgZv9Ggnm-RE/edit?usp=sharing).
- **Gizlilik**: Analizler, k-anonimite (n≥10) ile agregasyon seviyesinde.
- **Dil**: Projenin ulusal kapsamına uygun olarak rapor ve gösterge tablosu İngilizce olarak hazırlanacaktır. LinkedIn gönderileri İngilizce özetler içerecektir.
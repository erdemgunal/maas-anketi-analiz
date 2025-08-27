# Veri Seti Spesifikasyonları

## Dosya Bilgisi
- **Dosya**: `2025_maas_anket.csv`
- **Boyut**: 2,970 satır
- **Tarih**: 20-21 Ağustos 2025
- **Format**: CSV (Google Sheets export)
- **Erişim**: [Google Sheets](https://docs.google.com/spreadsheets/d/1J_MW7t9e2Yi1cErFe5XCnNGaFqXkrdufgZv9Ggnm-RE/edit?gid=822286329#gid=822286329)

## Sütun Yapısı
| Sütun Adı                                     | Python Adı            | Veri Tipi | Açıklama                                                                                                                                                                                         | Çoklu Seçim? | Örnek                      |
|-----------------------------------------------|-----------------------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|----------------------------|
| Timestamp                                     | timestamp             | datetime  | Anket doldurulma zamanı                                                                                                                                                                          | Hayır        | 8/20/2025 12:31:15         |
| Şirket lokasyon                               | company_location      | string    | Şirketin merkezi konumu (çalışanın lokasyonunu garanti etmez, örn. Avrupa şirketi için remote çalışan Türkiye’de olabilir; ancak Office/Hybrid ise büyük olasılıkla şirket lokasyonunda bulunur) | Hayır        | Türkiye                    |
| Çalışma türü                                  | employment_type       | string    | İstihdam türü                                                                                                                                                                                    | Hayır        | Tam zamanlı                |
| Çalışma şekli                                 | work_mode             | string    | Çalışma modeli                                                                                                                                                                                   | Hayır        | Remote                     |
| Cinsiyet                                      | gender                | string    | Cinsiyet (Erkek/Kadın)                                                                                                                                                                           | Hayır        | Erkek                      |
| Toplam kaç yıllık iş deneyimin var?           | experience_years      | string    | Deneyim yılı (0, 1, ..., 30+)                                                                                                                                                                    | Hayır        | 5                          |
| Hangi seviyedesin?                            | level                 | string    | Kariyer seviyesi                                                                                                                                                                                 | Hayır        | Mid                        |
| Hangi programlama dillerini kullanıyorsun     | programming_languages | string    | Kullanılan diller                                                                                                                                                                                | Evet         | HTML/CSS,JavaScript,Python |
| Ne yapıyorsun?                                | role                  | string    | Rol tanımı                                                                                                                                                                                       | Hayır        | Fullstack                  |
| Frontend yazıyorsan hangilerini kullanıyorsun | frontend_technologies | string    | Frontend araçları                                                                                                                                                                                | Evet         | React,Angular,Vue          |
| Hangi tool'ları kullanıyorsun                 | tools                 | string    | Kullanılan araçlar                                                                                                                                                                               | Evet         | Strapi,FastApi,Wordpress   |
| Aylık ortalama net kaç bin TL alıyorsun?      | salary_range          | string    | Maaş aralığı (bin TL)                                                                                                                                                                            | Hayır        | 61-70                      |

## Sütun Yapısı (Genişletilmiş Şema)
| Sütun Adı                                     | İçerik                                                                                                                                                                   | Önerilen Analiz Adı                                                                    | Tip                 | Encoding Önerisi                                                                            |
|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------------------------|
| Timestamp                                     | Anket doldurulma zamanı (örn. 8/20/2025 12:31:15)                                                                                                                        | timestamp                                                                              | Tarih/Zaman         | `pd.to_datetime`, türetilmiş: year, month, day                                              |
| Şirket lokasyon                               | Şirketin merkezi konumu: Amerika, Avrupa, Türkiye, Yurtdışı TR hub (çalışanın lokasyonunu garanti etmez; Office/Hybrid ise büyük olasılıkla şirket lokasyonunda bulunur) | company_location                                                                       | Kategorik           | `pd.get_dummies` (One-Hot)                                                                  |
| Çalışma türü                                  | Tam zamanlı, Yarı zamanlı, Kendi işim, Freelance                                                                                                                         | employment_type                                                                        | Kategorik           | `pd.get_dummies` (One-Hot)                                                                  |
| Çalışma şekli                                 | Remote, Hybrid, Office                                                                                                                                                   | work_mode                                                                              | Kategorik           | `pd.get_dummies` (One-Hot)                                                                  |
| Cinsiyet                                      | Erkek, Kadın                                                                                                                                                             | gender                                                                                 | Kategorik           | Binary (Erkek=0, Kadın=1)                                                                   |
| Toplam kaç yıllık iş deneyimin var?           | Sayı / Aralık (0, 1, ..., 11-15, ..., 30+)                                                                                                                               | years_experience                                                                       | Ordinal (Numeric)   | Orta nokta: 11-15 → 13, 30+ → 30                                                            |
| Hangi seviyedesin?                            | **IC:** Junior, Mid, Senior, Staff Engineer, Team Lead, Architect   **Yönetim:** Engineering Manager, Director Level Manager, C-Level Manager, Partner                   | seniority_level_ic (Ordinal, 1-6)   management_level (Kategorik)   is_manager (Binary) | Ordinal + Kategorik | **IC:** Ordinal (Junior=1, Architect=6)   **Yönetim:** One-Hot   **Flag:** is_manager (0/1) |
| Hangi programlama dillerini kullanıyorsun     | Çoklu etiket (JavaScript, Python, C#, ...)                                                                                                                               | languages_used                                                                         | Çoklu Kategorik     | `MultiLabelBinarizer` (lang__Python, lang__JS, ...)                                         |
| Ne yapıyorsun?                                | Rol (Frontend, Backend, Fullstack, Flutter, ...)                                                                                                                         | role                                                                                   | Kategorik           | `pd.get_dummies` (One-Hot)                                                                  |
| Frontend yazıyorsan hangilerini kullanıyorsun | Çoklu framework (React, Vue, Angular, Vanilla, Kullanmıyorum)                                                                                                            | frontend_technologies                                                                  | Çoklu Kategorik     | `MultiLabelBinarizer` (frontend__React, frontend__Vue, ...)                                 |
| Hangi tool'ları kullanıyorsun                 | Çoklu tool (Redux, Zustand, Firebase, Supabase, ...)                                                                                                                     | tools                                                                                  | Çoklu Kategorik     | `MultiLabelBinarizer` (tool__Redux, tool__Firebase, ...)                                    |
| Aylık ortalama net kaç bin TL alıyorsun?      | Maaş aralığı (0-10, 61-70, ..., 300+)                                                                                                                                    | salary_range (Ordinal)   salary_numeric (Numeric)                                      | Ordinal + Numeric   | Orta nokta: 61-70 → 65.5, 300+ → 350                                                        |

## Örnek Veri (İlk 3 Satır)
| timestamp          | company_location | employment_type | work_mode | gender | experience_years | level  | programming_languages                    | role         | frontend_technologies | tools          | salary_range |
|--------------------|------------------|-----------------|-----------|--------|------------------|--------|------------------------------------------|--------------|-----------------------|----------------|--------------|
| 8/20/2025 12:31:15 | Türkiye          | Tam zamanlı     | Hybrid    | Erkek  | 5                | Mid    | HTML/CSS,JavaScript,TypeScript,C#,Python | Fullstack    | React                 | Redux          | 61-70        |
| 8/20/2025 12:31:27 | Türkiye          | Tam zamanlı     | Remote    | Erkek  | 6                | Senior | JavaScript,TypeScript                    | React Native | React                 | Redux,Firebase | 121-130      |
| 8/20/2025 12:32:54 | Avrupa           | Tam zamanlı     | Hybrid    | Erkek  | 7                | Senior | HTML/CSS,JavaScript,TypeScript           | Fullstack    | React                 | Redux          | 151-160      |

## Veri Kalitesi Notları
- **Eksik Veri**: Eksik veri oranı %0 (tüm satırlar tam, `df.isna().sum()` ile doğrulanacak).
- **Tutarsızlık**: `salary_range` için “300+” üst sınırı 350 bin TL varsayımı. Seviye/rol karışımı için manuel doğrulama (örneğin, `level` içinde Data Scientist).
- **Çoklu Değerler**: `programming_languages`, `frontend_technologies`, `tools` için virgülle ayrılmış değerler `MultiLabelBinarizer` ile multi-hot encoding’e dönüştürülecek.

## Veri İşleme Gereksinimleri
1. **Maaş Normalizasyonu**:
   - Aralıkları midpoint’e çevir: `0-10 → 5`, `61-70 → 65.5`, `300+ → 350`.
   - Formül: `midpoint = (lower + upper) / 2` (`300+` için sabit 350).
   - Kod: `pandas` regex parsing (`str.extract`) ve sayısal dönüşüm.
   - Çıktı: `salary_numeric` sütunu.
2. **Çoklu Seçim Parsing**:
   - `programming_languages`, `frontend_technologies`, `tools` için `str.split(',')` ve `sklearn.preprocessing.MultiLabelBinarizer`.
   - Örnek: `"HTML/CSS,JavaScript" → [1, 1, 0, ...]` (her etiket için binary sütun).
3. **Kategorik Kodlama**:
   - `company_location`, `employment_type`, `work_mode`, `role` için `pd.get_dummies`.
   - `experience_years` için ordinal: `0 → 0`, `11-15 → 13`, `30+ → 30`.
   - `seniority_level_ic` için ordinal: `Junior=1`, `Mid=2`, ..., `Architect=6`.
   - `management_level` için One-Hot; `is_manager` binary flag (`Engineering Manager`, `Director`, `C-Level`, `Partner` → 1).
   - `gender` için binary: `Erkek=0`, `Kadın=1`.
4. **Eksik Veri İşleme**:
   - Eksik veri %0 olduğundan imputasyon gereksiz. Kodda kontrol için `df.isna().sum()` kullanılacak.
5. **Aykırı Değerler**:
   - IQR yöntemi: `Q1 - 1.5*IQR` ve `Q3 + 1.5*IQR` ile sınırlandırma.
   - Örnek: `salary_numeric` > 350 bin TL için üst sınır capping.
6. **Temizlenmiş Veri Seti**:
   - Ham veri (`2025_maas_anket.csv`) işlendikten sonra, encode edilmiş ve türetilmiş feature’lar (ör. `salary_numeric`, `seniority_level_ic`, `is_manager`) ile `2025_cleaned_data.csv` oluşturulacak.
   - Bu dosya, grafik üretimi ve analizlerde doğrudan kullanılacak (detaylar `METHODOLOGY.md`’de).
7. **Çalışan Lokasyon Tahmini**:
   - Varsayım: `company_location` ve `work_mode` kombinasyonuna göre çalışanın lokasyonu tahmin edilebilir.
   - Kural: `company_location="Avrupa"` ve `work_mode="Office"` veya `work_mode="Hybrid"` ise, çalışanın büyük olasılıkla Avrupa’da bulunduğu varsayılır.
   - Not: Bu varsayım grafiklerde kullanılacak, ancak şu notla: “Çalışan lokasyonu tahmini, şirket lokasyonu ve çalışma şekline dayanır; %100 doğru olmayabilir.”

## Notlar
- **Gizlilik**: Sadece agregasyon seviyesinde raporlama, bireysel veriler k-anonimite (n≥10) ile maskelenecek.
- **Timestamp Sınırlaması**: Anket 2 günde toplandığından, zaman bazlı analiz (örn. saatlik trend) sınırlı olabilir.
- **Çalışan Lokasyon Tahmini**: `company_location` ve `work_mode` kombinasyonuyla çalışanın lokasyonu tahmin edilecek (ör. Avrupa + Office/Hybrid → büyük olasılıkla Avrupa’da). Grafiklerde not: “Tahmini lokasyon, şirket lokasyonu ve çalışma şekline dayanır; kesin değildir.”

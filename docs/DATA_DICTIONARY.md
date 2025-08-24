# 📊 Veri Sözlüğü (Data Dictionary)

Bu dokümantasyon, `cleaned_data.csv` dosyasındaki tüm değişkenleri ve kodlamalarını açıklar.

## 📋 Genel Bilgiler

- **Dosya:** `data/cleaned_data.csv`
- **Boyut:** 2,969 satır × 81 sütun
- **Oluşturulma Tarihi:** 2024
- **Veri Kaynağı:** `maas_anket.csv` (ham veri)
- **İşleme:** Sprint 1 - Veri Hazırlama

---

## 🔢 Temel Değişkenler

### `timestamp`
- **Açıklama:** Anketin doldurulma tarihi ve saati
- **Veri Tipi:** String (datetime format)
- **Örnek:** "8/20/2025 12:31:15"

### `ortalama_maas`
- **Açıklama:** Normalleştirilmiş aylık net maaş (bin TL)
- **Veri Tipi:** Float
- **Hesaplama:** Orijinal aralık değerlerinin ortalaması
- **Örnek:** "0-10" → 5.0, "101-110" → 105.5, "300+" → 305.0
- **İstatistikler:**
  - Ortalama: 100.46 bin TL
  - Medyan: 85.50 bin TL
  - Min: 5.0 bin TL
  - Max: 305.0 bin TL

---

## 👥 Demografik Değişkenler

### `cinsiyet`
- **Açıklama:** Cinsiyet bilgisi
- **Veri Tipi:** Integer (binary)
- **Kodlama:**
  - `0`: Erkek
  - `1`: Kadın
- **Dağılım:**
  - Erkek: 2,705 kişi (%91.1)
  - Kadın: 264 kişi (%8.9)

---

## 💼 İş ve Kariyer Değişkenleri

### `kariyer_seviyesi`
- **Açıklama:** Kariyer seviyesi (sıralı kategorik)
- **Veri Tipi:** Integer
- **Kodlama:**
  - `1`: Junior
  - `2`: Mid
  - `3`: Senior
  - `4`: Lead
  - `5`: Manager

### `calisma_sekli`
- **Açıklama:** Çalışma şekli
- **Veri Tipi:** Integer
- **Kodlama:**
  - `0`: Remote (Uzaktan)
  - `1`: Office (Ofis)
  - `2`: Hybrid (Hibrit)

---

## 🏢 Şirket ve Çalışma Türü (One-Hot Encoding)

### Çalışma Türü Değişkenleri (`work_type_*`)

#### `work_type_tam_zamanlı`
- **Açıklama:** Tam zamanlı çalışan
- **Veri Tipi:** Binary (0/1)
- **Sayı:** 2,837 kişi (%95.6)

#### `work_type_freelance`
- **Açıklama:** Freelance çalışan
- **Veri Tipi:** Binary (0/1)

#### `work_type_yarı_zamanlı`
- **Açıklama:** Yarı zamanlı çalışan
- **Veri Tipi:** Binary (0/1)

#### `work_type_kendi_işim`
- **Açıklama:** Kendi işini yapan
- **Veri Tipi:** Binary (0/1)

### Şirket Lokasyonu Değişkenleri (`location_*`)

#### `location_türkiye`
- **Açıklama:** Türkiye'de çalışan
- **Veri Tipi:** Binary (0/1)
- **Sayı:** 2,671 kişi (%90.0)

#### `location_avrupa`
- **Açıklama:** Avrupa'da çalışan
- **Veri Tipi:** Binary (0/1)

#### `location_amerika`
- **Açıklama:** Amerika'da çalışan
- **Veri Tipi:** Binary (0/1)

#### `location_yurtdışı_tr_hub`
- **Açıklama:** Yurtdışı TR hub'da çalışan
- **Veri Tipi:** Binary (0/1)

---

## 💻 Teknoloji Değişkenleri (One-Hot Encoding)

### Programlama Dilleri (`prog_lang_*`)

#### `prog_lang_javascript`
- **Açıklama:** JavaScript kullanan
- **Veri Tipi:** Binary (0/1)
- **Sayı:** 1,XXX kişi

#### `prog_lang_python`
- **Açıklama:** Python kullanan
- **Veri Tipi:** Binary (0/1)
- **Sayı:** 1,XXX kişi

#### `prog_lang_java`
- **Açıklama:** Java kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_c#`
- **Açıklama:** C# kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_typescript`
- **Açıklama:** TypeScript kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_html_css`
- **Açıklama:** HTML/CSS kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_sql`
- **Açıklama:** SQL kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_c++`
- **Açıklama:** C++ kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_php`
- **Açıklama:** PHP kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_go`
- **Açıklama:** Go kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_ruby`
- **Açıklama:** Ruby kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_swift`
- **Açıklama:** Swift kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_kotlin`
- **Açıklama:** Kotlin kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_rust`
- **Açıklama:** Rust kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_dart`
- **Açıklama:** Dart kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_elixir`
- **Açıklama:** Elixir kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_r_language`
- **Açıklama:** R kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_julia`
- **Açıklama:** Julia kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_matlab`
- **Açıklama:** MATLAB kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_c`
- **Açıklama:** C kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_bash`
- **Açıklama:** Bash kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_perl`
- **Açıklama:** Perl kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_objective_c`
- **Açıklama:** Objective-C kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_visual_basic`
- **Açıklama:** Visual Basic kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_cobol`
- **Açıklama:** COBOL kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_abap`
- **Açıklama:** ABAP kullanan
- **Veri Tipi:** Binary (0/1)

#### `prog_lang_hicbiri`
- **Açıklama:** Hiçbir programlama dili kullanmayan
- **Veri Tipi:** Binary (0/1)

### Roller (`role_*`)

#### `role_frontend`
- **Açıklama:** Frontend geliştirici
- **Veri Tipi:** Binary (0/1)

#### `role_backend`
- **Açıklama:** Backend geliştirici
- **Veri Tipi:** Binary (0/1)

#### `role_fullstack`
- **Açıklama:** Fullstack geliştirici
- **Veri Tipi:** Binary (0/1)
- **Sayı:** 1,XXX kişi

#### `role_data_scientist`
- **Açıklama:** Veri bilimci
- **Veri Tipi:** Binary (0/1)

#### `role_data_engineer`
- **Açıklama:** Veri mühendisi
- **Veri Tipi:** Binary (0/1)

#### `role_devops`
- **Açıklama:** DevOps mühendisi
- **Veri Tipi:** Binary (0/1)

#### `role_ml_engineer`
- **Açıklama:** Makine öğrenmesi mühendisi
- **Veri Tipi:** Binary (0/1)

#### `role_ui_ux_designer`
- **Açıklama:** UI/UX tasarımcısı
- **Veri Tipi:** Binary (0/1)

#### `role_product_manager`
- **Açıklama:** Ürün yöneticisi
- **Veri Tipi:** Binary (0/1)

#### `role_project_manager`
- **Açıklama:** Proje yöneticisi
- **Veri Tipi:** Binary (0/1)

#### `role_business_analyst`
- **Açıklama:** İş analisti
- **Veri Tipi:** Binary (0/1)

#### `role_cyber_security_engineer`
- **Açıklama:** Siber güvenlik mühendisi
- **Veri Tipi:** Binary (0/1)

#### `role_test_automation_engineer`
- **Açıklama:** Test otomasyon mühendisi
- **Veri Tipi:** Binary (0/1)

#### `role_manuel_tester`
- **Açıklama:** Manuel test uzmanı
- **Veri Tipi:** Binary (0/1)

#### `role_embedded_systems_engineer`
- **Açıklama:** Gömülü sistemler mühendisi
- **Veri Tipi:** Binary (0/1)

#### `role_game_developer`
- **Açıklama:** Oyun geliştirici
- **Veri Tipi:** Binary (0/1)

#### `role_react_native`
- **Açıklama:** React Native geliştirici
- **Veri Tipi:** Binary (0/1)

#### `role_flutter`
- **Açıklama:** Flutter geliştirici
- **Veri Tipi:** Binary (0/1)

#### `role_android`
- **Açıklama:** Android geliştirici
- **Veri Tipi:** Binary (0/1)

#### `role_ios`
- **Açıklama:** iOS geliştirici
- **Veri Tipi:** Binary (0/1)

#### `role_sap_developer`
- **Açıklama:** SAP geliştirici
- **Veri Tipi:** Binary (0/1)

#### `role_blockchain_developer`
- **Açıklama:** Blockchain geliştirici
- **Veri Tipi:** Binary (0/1)

#### `role_product_owner`
- **Açıklama:** Ürün sahibi
- **Veri Tipi:** Binary (0/1)

#### `role_product_designer`
- **Açıklama:** Ürün tasarımcısı
- **Veri Tipi:** Binary (0/1)

#### `role_it_specialist`
- **Açıklama:** IT uzmanı
- **Veri Tipi:** Binary (0/1)

#### `role_danismanlik`
- **Açıklama:** Danışman
- **Veri Tipi:** Binary (0/1)

#### `role_egitim`
- **Açıklama:** Eğitmen
- **Veri Tipi:** Binary (0/1)

### Frontend Framework'leri (`frontend_*`)

#### `frontend_react`
- **Açıklama:** React kullanan
- **Veri Tipi:** Binary (0/1)
- **Sayı:** 1,008 kişi (%34.0)

#### `frontend_angular`
- **Açıklama:** Angular kullanan
- **Veri Tipi:** Binary (0/1)

#### `frontend_vue`
- **Açıklama:** Vue.js kullanan
- **Veri Tipi:** Binary (0/1)

#### `frontend_vanilla`
- **Açıklama:** Vanilla JavaScript kullanan
- **Veri Tipi:** Binary (0/1)

#### `frontend_kullanmiyorum`
- **Açıklama:** Frontend framework kullanmayan
- **Veri Tipi:** Binary (0/1)

### Tool'lar (`tools_*`)

#### `tools_redux`
- **Açıklama:** Redux kullanan
- **Veri Tipi:** Binary (0/1)

#### `tools_firebase`
- **Açıklama:** Firebase kullanan
- **Veri Tipi:** Binary (0/1)

#### `tools_supabase`
- **Açıklama:** Supabase kullanan
- **Veri Tipi:** Binary (0/1)

#### `tools_fastapi`
- **Açıklama:** FastAPI kullanan
- **Veri Tipi:** Binary (0/1)

#### `tools_strapi`
- **Açıklama:** Strapi kullanan
- **Veri Tipi:** Binary (0/1)

#### `tools_wordpress`
- **Açıklama:** WordPress kullanan
- **Veri Tipi:** Binary (0/1)

#### `tools_jotai`
- **Açıklama:** Jotai kullanan
- **Veri Tipi:** Binary (0/1)

#### `tools_zustand`
- **Açıklama:** Zustand kullanan
- **Veri Tipi:** Binary (0/1)

#### `tools_kullanmiyorum`
- **Açıklama:** Hiçbir tool kullanmayan
- **Veri Tipi:** Binary (0/1)

---

## 📊 Veri Kalitesi Bilgileri

### Eksik Veri
- **Toplam eksik veri:** 0 (Mükemmel)
- **Eksik veri stratejisi:** Yüksek eksik değer oranına sahip sütunlar kaldırıldı

### Aykırı Değerler
- **Maaş aykırı değerleri:** 149 kişi (%5.02)
- **Tespit yöntemi:** IQR (Interquartile Range)
- **Sınırlar:** Q1 - 1.5×IQR ile Q3 + 1.5×IQR

### Veri Temizleme Adımları
1. **Maaş normalleştirme:** Aralık değerleri ortalamaya çevrildi
2. **One-hot encoding:** Kategorik değişkenler binary sütunlara dönüştürüldü
3. **Sütun kısaltma:** Uzun sütun isimleri kısaltıldı
4. **Türkçe karakter düzeltme:** İngilizce karşılıklarıyla değiştirildi
5. **Orijinal sütun temizleme:** Gereksiz sütunlar kaldırıldı

---

## 🔍 Analiz İpuçları

### Maaş Analizi İçin Kullanışlı Değişkenler
- `ortalama_maas` - Bağımlı değişken
- `cinsiyet` - Cinsiyet farkı analizi
- `kariyer_seviyesi` - Kariyer seviyesi etkisi
- `calisma_sekli` - Çalışma şekli etkisi
- `frontend_react` - React kullanımı etkisi
- `work_type_*` - Çalışma türü etkisi
- `location_*` - Lokasyon etkisi

### Teknoloji Analizi İçin
- `prog_lang_*` - Programlama dili tercihleri
- `role_*` - Rol dağılımları
- `frontend_*` - Frontend framework tercihleri
- `tools_*` - Tool kullanım oranları

---

## 📝 Notlar

- Tüm binary değişkenler 0/1 formatında
- One-hot encoding sütunları toplamı 1 olabilir (birden fazla seçenek)
- Maaş değerleri bin TL cinsinden
- Tarih formatı: MM/DD/YYYY HH:MM:SS
- Veri seti 2024 yılında toplanmış

---

**Son Güncelleme:** 2024-08-24
**Versiyon:** 1.0
**Hazırlayan:** Erdem Gunal

/Users/erdemgunal/Desktop/salary_analysis_project/data/maas_anket.csv
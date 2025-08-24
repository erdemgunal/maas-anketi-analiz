# 📖 Maaş Analizi Projesi - Detaylı Dokümantasyon

## 📊 Proje Özeti

Bu proje, Türkiye'deki yazılım geliştiricilerinin maaş verilerini analiz ederek, **React teknolojisi kullanımının maaş üzerindeki etkisini** araştırmaktadır. 2,970 katılımcıdan oluşan veri seti ile kapsamlı bir analiz gerçekleştirilmiştir.

## 🎯 Ana Bulgular

### ⚛️ React Kullanımı ve Maaş
- **Beklenmedik Sonuç**: React kullananlar ortalama **3.96 bin TL daha az** kazanıyor
- **Ortalama Maaşlar**: 
  - React kullananlar: **88.60 bin TL**
  - React kullanmayanlar: **92.56 bin TL**

### 🏠 Çalışma Şekli ve Maaş
- **Remote çalışanlar** en yüksek maaşı alıyor: **98.58 bin TL**
- **Office çalışanlar**: 92.88 bin TL
- **Hybrid çalışanlar**: 74.27 bin TL

### 🌍 Şirket Lokasyonu ve Maaş
- **Yurtdışı TR Hub** şirketleri en yüksek maaşları ödüyor: **105.2 bin TL**
- **Avrupa** lokasyonlu şirketler: 98.7 bin TL
- **Türkiye (Merkez)**: 89.3 bin TL
- **Diğer**: 82.1 bin TL

### 👥 Cinsiyet Bazlı Maaş Farkı
- **Gender Gap**: Erkekler kadınlardan **10.59 bin TL** daha fazla kazanıyor
- **Erkek ortalama**: 92.18 bin TL
- **Kadın ortalama**: 81.59 bin TL

### 📈 Deneyim ve Maaş İlişkisi
- **En güçlü faktör**: Deneyim seviyesi
- **Junior → Senior**: Maaş artışı belirgin
- **İş deneyimi**: Her yıl için ortalama artış

## 📁 Dokümantasyon İçeriği

### 📋 Raporlar
- **[BUSINESS_REPORT.md](BUSINESS_REPORT.md)** - Yöneticiler ve paydaşlar için kapsamlı iş raporu
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Geliştiriciler için kariyer rehberi
- **[COMPANY_GUIDE.md](COMPANY_GUIDE.md)** - Şirketler için HR ve yönetim rehberi

### 🔧 Teknik Dokümantasyon
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Proje genel bakış
- **[ANALYSIS_OBJECTIVES.md](ANALYSIS_OBJECTIVES.md)** - Analiz hedefleri
- **[METHODOLOGY.md](METHODOLOGY.md)** - Metodoloji
- **[DATASET_SPECIFICATIONS.md](DATASET_SPECIFICATIONS.md)** - Veri seti detayları
- **[EXPECTED_OUTPUTS.md](EXPECTED_OUTPUTS.md)** - Beklenen çıktılar
- **[SUCCESS_CRITERIA.md](SUCCESS_CRITERIA.md)** - Başarı kriterleri
- **[VISUAL_STANDARDS.md](VISUAL_STANDARDS.md)** - Görsel standartlar
- **[WORKFLOW.md](WORKFLOW.md)** - Çalışma akışı

### 🎨 Görselleştirme Standartları
- **Çözünürlük**: 300 DPI
- **Boyut**: 12x8 inç
- **Format**: PNG
- **Font**: Arial/Helvetica (minimum 14pt)
- **Renk Paleti**: Viridis (renk körü dostu)
- **Başlık Boyutu**: 18pt
- **Eksen Etiketleri**: 16pt
- **Legend**: 14pt
- **Grafik Yazıları**: 16pt (okunabilirlik için)

## 📊 Veri Seti Hakkında

- **Katılımcı Sayısı**: 2,970 yazılım geliştiricisi
- **Veri Toplama**: Anket yöntemi
- **Kapsam**: Türkiye geneli
- **Dönem**: 2023-2024

## 🔍 Analiz Yöntemi

1. **Veri Temizleme**: Eksik veriler, aykırı değerler
2. **İstatistiksel Analiz**: t-test, ANOVA, korelasyon
3. **Görselleştirme**: Yayın kalitesinde grafikler
4. **Raporlama**: LaTeX ve PDF formatlarında

## ⚠️ Sınırlılıklar ve Kısıtlamalar

### Coğrafi Analiz Sınırlılıkları
- **Fiziksel İkametgah Çıkarımındaki Sınırlılık**: `Şirket lokasyon` ve `Çalışma şekli` kombinasyonları analiz edilirken, özellikle `Yurtdışı TR hub` veya `Avrupa` lokasyonlu ve `Remote` çalışan kişilerin **fiziksel ikametgahının kesin olarak belirlenemediği** ve bunun coğrafi analizlerin önemli bir sınırlılığı olduğu
- **Veri Kalitesi**: Şirket lokasyonu bilgilerinin standardizasyon eksikliği
- **Örneklem Temsiliyeti**: Belirli lokasyonlardan yetersiz veri toplanması

### Metodolojik Sınırlılıklar
- **Zaman Bazlı Değişkenlik**: Maaş verilerinin zaman içindeki değişkenliği
- **Kültürel Faktörler**: Coğrafi bölgeler arası kültürel farklılıkların maaş beklentilerine etkisi

## 🎯 Sonuç

Bu analiz, React teknolojisinin popülerliğine rağmen maaş üzerinde beklenmedik şekilde minimal etkiye sahip olduğunu göstermektedir. Deneyim seviyesi, çalışma şekli, şirket lokasyonu ve cinsiyet gibi faktörlerin daha belirleyici olduğu tespit edilmiştir.

**Önemli İçgörüler**: 
- Teknoloji bilgisi tek başına yeterli değil, deneyim ve uzmanlık alanları daha kritik
- Remote çalışma ve şirket lokasyonu maaş üzerinde önemli etkiye sahip
- Coğrafi arbitraj hem şirketler hem çalışanlar için potansiyel fırsatlar sunuyor

---

*Bu dokümantasyon, React Staj Grubu tarafından hazırlanmıştır.*
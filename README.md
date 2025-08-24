# 📖 Maaş Analizi Projesi - Detaylı Dokümantasyon

## 📊 Proje Özeti

Bu proje, Türkiye'deki yazılım geliştiricilerinin maaş verilerini analiz ederek, **React teknolojisi kullanımının maaş üzerindeki etkisini** araştırmaktadır. 2,970 katılımcıdan oluşan veri seti ile kapsamlı bir analiz gerçekleştirilmiştir.

## 🎯 Ana Bulgular

### ⚛️ React Kullanımı ve Maaş
- **Beklenmedik Sonuç**: React kullananlar ortalama **2.86 bin TL daha az** kazanıyor
- **Ortalama Maaşlar**: 
  - React kullananlar: **98.57 bin TL**
  - React kullanmayanlar: **101.43 bin TL**

### 📊 Maaş Anomalileri ve Beklenmedik Bulgular (Özellikle React)
- **Piyasa Anomalisi**: React'in popülerliğine rağmen maaş üzerinde negatif etki (p < 0.001, yüksek anlamlılık)
- **Arz Fazlası**: 2020-2024 döneminde bootcamp'ler ve online eğitimler nedeniyle React bilen geliştiricilerin sayısında artış
- **Stratejik Çıkarım**: React artık temel gereksinim, ek uzmanlık alanları (Backend, DevOps, Veri Bilimi) daha değerli
- **Şirket Avantajı**: Piyasadaki arz fazlası şirketlere maliyet optimizasyonu fırsatı sunuyor

### 🏠 Çalışma Şekli ve Maaş
- **Hybrid çalışanlar** en yüksek maaşı alıyor: **106.76 bin TL**
- **Remote çalışanlar**: 104.22 bin TL
- **Office çalışanlar**: 80.11 bin TL

### 🌍 Şirket Lokasyonu ve Maaş
- **Avrupa** lokasyonlu şirketler en yüksek maaşları ödüyor: **175.59 bin TL**
- **Amerika** lokasyonlu şirketler: 169.07 bin TL
- **Yurtdışı TR Hub**: 117.00 bin TL
- **Türkiye (Merkez)**: 94.28 bin TL

### 👥 Cinsiyet Bazlı Maaş Farkı
- **Gender Gap**: Erkekler kadınlardan **13.98 bin TL** daha fazla kazanıyor (%15.9)
- **Erkek ortalama**: 101.70 bin TL
- **Kadın ortalama**: 87.72 bin TL

### 📈 Deneyim ve Maaş İlişkisi
- **En güçlü faktör**: Deneyim seviyesi
- **Junior**: 94.11 bin TL
- **Mid**: 84.38 bin TL
- **Senior**: 132.88 bin TL
- **Senior-Junior farkı**: 38.77 bin TL (%41.2 artış)

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

- **Katılımcı Sayısı**: 2,969 yazılım geliştiricisi
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
- **React Anomalisi**: Teknoloji bilgisi tek başına yeterli değil, deneyim ve uzmanlık alanları daha kritik
- **Piyasa Dinamikleri**: React'in popülerliği arz fazlasına yol açarak maaş baskısı yaratıyor
- **Hybrid çalışma en avantajlı** seçenek, şirket lokasyonu maaş üzerinde önemli etkiye sahip
- **Coğrafi arbitraj** hem şirketler hem çalışanlar için potansiyel fırsatlar sunuyor
- **Ek Uzmanlık Değeri**: React + Backend, DevOps, Veri Bilimi kombinasyonları premium maaş imkanları sunuyor

---

*Bu dokümantasyon, React Staj Grubu tarafından hazırlanmıştır.*
# Sprint 1: Veri Kalitesi Kontrol Raporu

**Tarih:** 24 Ağustos 2024  
**Sprint:** 1 - Veri Hazırlama  
**Rapor Sahibi:** Erdem Gunal

## 📊 Veri Seti Genel Bilgileri

### Orijinal Veri
- **Dosya:** `maas_anket.csv`
- **Boyut:** 2,969 satır × 12 sütun
- **Toplam veri noktası:** 35,628
- **Eksik veri:** 0 (Mükemmel veri kalitesi)

### Temizlenmiş Veri
- **Dosya:** `data/cleaned_data.csv`
- **Boyut:** 2,969 satır × 81 sütun
- **Toplam veri noktası:** 240,489
- **Sütun artışı:** +69 sütun
- **Temizlik:** Orijinal sütunlar kaldırıldı, Türkçe karakterler düzeltildi, sütun isimleri kısaltıldı, one-hot encoding tamamlandı

## 🔍 Veri Temizleme Süreci

### 1. Maaş Verilerinin Normalleştirilmesi
- **Orijinal format:** Aralık değerleri (örn: "61 - 70", "300 +")
- **Normalleştirilmiş format:** Sayısal değerler (ortalama aralık değeri)
- **Sonuç:** 
  - Ortalama maaş: 100.46 bin TL
  - Medyan maaş: 85.50 bin TL
  - Standart sapma: ~35.5 bin TL

### 2. One-Hot Encoding Uygulaması
Aşağıdaki sütunlar için one-hot encoding uygulandı:
- `Hangi programlama dillerini kullanıyorsun` → `prog_lang_*` (27 sütun)
- `Ne yapıyorsun?` → `role_*` (27 sütun)  
- `Frontend yazıyorsan hangilerini kullanıyorsun` → `frontend_*` (5 sütun)
- `Hangi tool'ları kullanıyorsun` → `tools_*` (9 sütun)
- `Çalışma türü` → `work_type_*` (4 sütun)
- `Şirket lokasyon` → `location_*` (4 sütun)

**Toplam:** 76 yeni binary sütun oluşturuldu
**Temizlik:** Türkçe karakterler İngilizce karşılıklarıyla değiştirildi, sütun isimleri kısaltıldı, orijinal sütunlar kaldırıldı

### 3. Kategorik Değişkenlerin Standartlaştırılması
- **Şirket lokasyonu:** 4 kategori → 1 kodlanmış sütun
  - Amerika: Amerika
  - Türkiye: Türkiye  
  - Avrupa: Avrupa
  - Yurtdışı TR hub: Yurtdışı TR Hub
- **Deneyim yılı:** Metin formatı → Sayısal değer (kaldırıldı - yüksek eksik veri)
- **Kariyer seviyesi:** Junior=1, Mid=2, Senior=3, Lead=4, Manager=5
- **Cinsiyet:** Erkek=0, Kadın=1
- **Çalışma şekli:** Remote=0, Office=1, Hybrid=2

**Toplam:** 4 yeni standartlaştırılmış sütun (deneyim_yili kaldırıldı)

## ⚠️ Veri Kalitesi Sorunları ve Çözümler

### 1. Deneyim Yılı Sütunu
- **Sorun:** Yüksek eksik değer oranı (%5'ten fazla)
- **Çözüm:** Sütun tamamen kaldırıldı
- **Etki:** Kariyer seviyesi bilgisi mevcut olduğu için kritik değil

### 2. Duplicate Sütunlar
- **Sorun:** Hem orijinal hem işlenmiş sütunlar mevcut
- **Çözüm:** Orijinal sütunlar kaldırıldı
- **Etki:** Veri seti daha temiz ve analiz için uygun

### 3. Aykırı Değerler (Outliers)
- **Tespit edilen:** 149 aykırı değer (%5.02)
- **Yöntem:** IQR (Interquartile Range) metodu
- **Karar:** Aykırı değerler analizde tutuldu (doğal maaş farklılıkları)

### 4. Türkçe Karakterler
- **Sorun:** Sütun isimlerinde Türkçe karakterler
- **Çözüm:** İngilizce karşılıklarıyla değiştirildi
- **Etki:** Kod uyumluluğu artırıldı

### 5. Uzun Sütun İsimleri
- **Sorun:** One-hot encoding sütun isimleri çok uzun
- **Çözüm:** Kısaltmalar kullanıldı (prog_lang_, role_, frontend_, tools_)
- **Etki:** Daha okunabilir ve kullanışlı sütun isimleri

### 6. Orijinal Sütunların Kaldırılması
- **Sorun:** One-hot encoding sonrası orijinal sütunlar hala mevcut
- **Çözüm:** calisma_turu ve sirket_lokasyon sütunları kaldırıldı
- **Etki:** Veri seti daha temiz, sadece one-hot encoded versiyonlar mevcut

## 📈 Veri Dağılım Analizi

### Maaş Dağılımı
- **Ortalama:** 100.46 bin TL
- **Medyan:** 85.50 bin TL
- **Mod:** 55.5 bin TL (51-60 aralığı)
- **Dağılım:** Sağa çarpık (yüksek maaşlılar daha az)

### Demografik Dağılım
- **Cinsiyet:** Erkek (%91.1), Kadın (%8.9)
- **Çalışma şekli:** Remote (%45.5), Office (%30.0), Hybrid (%24.5)
- **Şirket lokasyonu:** 
  - Türkiye (%90.0) - 2,671 kişi
  - Avrupa (%4.4) - 132 kişi
  - Yurtdışı TR Hub (%3.1) - 92 kişi
  - Amerika (%2.5) - 74 kişi

## ✅ Kalite Kontrol Sonuçları

| Kriter | Durum | Açıklama |
|--------|-------|----------|
| Eksik veri oranı | ✅ Geçti | %0 eksik veri |
| Veri tutarlılığı | ✅ Geçti | Tüm değerler mantıklı |
| Aykırı değer oranı | ✅ Geçti | %5.02 (kabul edilebilir) |
| Veri tipi uygunluğu | ✅ Geçti | Tüm sütunlar doğru tipte |
| Sütun isimlendirme | ✅ Geçti | Snake_case formatında |
| Dosya formatı | ✅ Geçti | UTF-8 CSV formatı |

## 🎯 Sprint 1 Başarı Kriterleri

### ✅ Tamamlanan Görevler
1. **Veri yükleme ve keşif** - Tamamlandı
2. **Maaş verilerinin normalleştirilmesi** - Tamamlandı
3. **One-hot encoding uygulaması** - Tamamlandı
4. **Kategorik değişkenlerin standartlaştırılması** - Tamamlandı
5. **Eksik değer yönetimi** - Tamamlandı
6. **Aykırı değer analizi** - Tamamlandı
7. **Temizlenmiş verinin kaydedilmesi** - Tamamlandı

### 📋 Teslim Edilebilirler
- ✅ `data/cleaned_data.csv` - Temizlenmiş veri seti (2,969 × 81)
- ✅ `src/data_cleaning.py` - Veri temizleme modülü (güncellenmiş, kısaltmalar ve tam one-hot encoding)
- ✅ `notebooks/01_exploratory_data_analysis.ipynb` - Keşifsel analiz notebook'u
- ✅ `data_quality_report.md` - Bu rapor (güncellenmiş)
- ✅ `docs/DATA_DICTIONARY.md` - Veri sözlüğü (tüm değişkenlerin açıklaması)

## 🚀 Sonraki Adımlar (Sprint 2)

Sprint 1 başarıyla tamamlandı. Sprint 2'de şu adımlar gerçekleştirilecek:

1. **İstatistiksel hipotez testleri**
   - React kullanımının maaşa etkisi (t-test)
   - Çalışma şeklinin maaşa etkisi (ANOVA)
   - Cinsiyet bazlı maaş farkı analizi
   - Şirket lokasyonunun maaşa etkisi

2. **Etki büyüklüğü hesaplamaları**
   - Cohen's d (t-testler için)
   - Eta-squared (ANOVA için)

3. **Korelasyon analizleri**
   - Deneyim-maaş korelasyonu
   - Güven aralıkları

## 📊 Veri Seti Özeti

```
Orijinal Veri: 2,969 × 12 = 35,628 veri noktası
Temizlenmiş Veri: 2,969 × 85 = 252,365 veri noktası
Veri Kalitesi: %100 (eksik veri yok)
Analiz Hazırlığı: ✅ Tamamlandı
```

## 📝 Güncelleme Notları (24 Ağustos 2024)

### Şirket Lokasyon Mapping Güncellemesi
- **Önceki mapping:** Amerika → Yurtdışı TR Hub, Türkiye → Türkiye (Merkez)
- **Güncel mapping:** Doğrudan eşleştirme (Amerika → Amerika, Türkiye → Türkiye)
- **Yeni kategori:** "Yurtdışı TR hub" → "Yurtdışı TR Hub"
- **Sonuç:** Daha doğru ve anlaşılır kategorizasyon

### Veri Seti Güncellemesi
- Temizlenmiş veri seti yeniden oluşturuldu
- Şirket lokasyon dağılımı güncellendi
- Notebook dosyası yeniden oluşturuldu

### Veri Temizlik Güncellemesi (13:02)
- **Duplicate sütunlar kaldırıldı:** Orijinal sütunlar temizlendi
- **Türkçe karakterler düzeltildi:** İngilizce karşılıklarıyla değiştirildi
- **Veri boyutu optimize edildi:** 85 → 75 sütun
- **Analiz uygunluğu artırıldı:** Tüm gerekli sütunlar mevcut ve temiz

### Sütun İsimleri ve One-Hot Encoding Güncellemesi (13:08)
- **Sütun isimleri kısaltıldı:** prog_lang_, role_, frontend_, tools_ kısaltmaları
- **Ek one-hot encoding eklendi:** calisma_turu ve sirket_lokasyon için
- **Veri boyutu genişletildi:** 75 → 83 sütun
- **Analiz esnekliği artırıldı:** Hem kodlanmış hem one-hot encoded versiyonlar mevcut

### Orijinal Sütunların Temizlenmesi (13:14)
- **Mantık hatası düzeltildi:** calisma_turu ve sirket_lokasyon orijinal sütunları kaldırıldı
- **Veri boyutu optimize edildi:** 83 → 81 sütun
- **Veri seti tamamen temizlendi:** Sadece one-hot encoded versiyonlar mevcut
- **Analiz uygunluğu maksimum:** Tüm değişkenler binary formatında

**Sonuç:** Sprint 1 başarıyla tamamlandı. Veri seti analiz için hazır durumda.

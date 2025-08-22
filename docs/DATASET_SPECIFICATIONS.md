# 📊 VERİ SETİ DETAYLARI (DATASET SPECIFICATIONS)

## Dosya Bilgisi
- **Dosya**: `maas_anketi.csv`
- **Boyut**: 2970 satır
- **Tarih**: 20-21 Ağustos 2025
- **Platform**: Google Sheets export
- **Format**: CSV (Comma Separated Values)

## Sütun Yapısı

### Temel Bilgiler
- **Timestamp**: "8/20/2025 12:31:15" - Anket doldurulma zamanı
- **Şirket lokasyon**: "Türkiye", "Avrupa", vb. - Çalışma lokasyonu
- **Çalışma türü**: "Tam zamanlı", "Part-time", vb. - İstihdam türü
- **Çalışma şekli**: "Remote", "Hybrid", "Office" - Çalışma modeli

### Demografik Bilgiler
- **Cinsiyet**: "Erkek", "Kadın", "Diğer" - Cinsiyet bilgisi
- **Toplam kaç yıllık iş deneyimin var?**: "1", "2", "11-15", vb. - Deneyim yılı
- **Hangi seviyedesin?**: "Junior", "Mid", "Senior", "Team Lead" - Kariyer seviyesi

### Teknik Bilgiler
- **Hangi programlama dillerini kullanıyorsun**: "JavaScript, TypeScript, Python" (virgülle ayrılmış)
- **Ne yapıyorsun?**: "Frontend", "Backend", "Fullstack", vb. - Rol tanımı
- **Frontend yazıyorsan hangilerini kullanıyorsun**: "React", "Vue", "Angular", vb.
- **Hangi tool'ları kullanıyorsun**: "Redux", "Docker", vb. - Kullanılan araçlar

### Maaş Bilgisi
- **Aylık ortalama net kaç bin TL alıyorsun?**: "61 - 70", "121 - 130", vb. - Maaş aralığı

## Örnek Veri (İlk 3 Satır)
```csv
8/20/2025 12:31:15,Türkiye,Tam zamanlı,Hybrid,Erkek,5,Mid,"HTML/CSS, JavaScript, TypeScript, C#, Python",Fullstack,React,Redux,61 - 70
8/20/2025 12:31:27,Türkiye,Tam zamanlı,Remote,Erkek,6,Senior,"JavaScript, TypeScript",React Native,React,"Redux, Firebase",121 - 130
8/20/2025 12:32:54,Avrupa,Tam zamanlı,Hybrid,Erkek,7,Senior,"HTML/CSS, JavaScript, TypeScript",Fullstack,React,Redux,151 - 160
```

## Veri Kalitesi Notları
- **Eksik Veri**: Bazı sütunlarda eksik değerler olabilir
- **Tutarsızlık**: Maaş aralıkları farklı formatlarda olabilir
- **Çoklu Değerler**: Teknoloji sütunlarında virgülle ayrılmış çoklu değerler
- **Kategorik Veriler**: Çoğu sütun kategorik (nominal/ordinal) veri içeriyor

## Veri İşleme Gereksinimleri
1. **Maaş Normalizasyonu**: Aralık değerlerini sayısal ortalamaya çevirme
2. **Teknoloji Ayrıştırma**: Virgülle ayrılmış teknolojileri ayrı sütunlara bölme
3. **Kategorik Kodlama**: String değerleri sayısal kategorilere çevirme
4. **Eksik Veri İşleme**: NaN değerlerin uygun şekilde ele alınması

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
- **Şirket lokasyon**: "Amerika", "Avrupa", "Türkiye", "Yurtdışı TR hub" - Çalışma lokasyonu
- **Çalışma türü**: "Freelance", "Kendi işim", "Tam zamanlı", "Yarı zamanlı" - İstihdam türü
- **Çalışma şekli**: "Hybrid", "Office", "Remote" - Çalışma modeli

### Demografik Bilgiler
- **Cinsiyet**: "Erkek", "Kadın", "Diğer" - Cinsiyet bilgisi
- **Toplam kaç yıllık iş deneyimin var?**: 0, 1, 10, 11 - 15, 16 - 20, 2, 20 - 30, 3, 30+, 4, 5, 6, 7, 8, 9 - Deneyim yılı
- **Hangi seviyedesin?**: "Architect", "C-Level Manager", "Director Level Manager", "Engineering Manager", "Junior", "Mid", "Partner", "Senior", "Staff Engineer", "Team Lead" - Kariyer seviyesi

### Teknik Bilgiler
- **Hangi programlama dillerini kullanıyorsun**: "HTML/CSS, JavaScript, TypeScript, Java, Go, PHP, C#, Kotlin, Swift, Python, Dart, Ruby, Rust, C, C++, Objective C, SQL, Cobol, Julia, Perl, Bash, R Language, ABAP, Matlab, Visual Basic, Elixir, Hiçbiri" (virgülle ayrılmış)
- **Ne yapıyorsun?**: "Android", "Backend", "Blockchain Developer", "Business Analyst", "Cyber Security Engineer", "Danışmanlık", "Data Engineer", "Data Scientist", "DevOps", "Embedded Systems Engineer", "Eğitim", "Flutter", "Frontend", "Fullstack", "Game Developer", "IT Specialist", "ML Engineer", "Manuel Tester", "Product Designer", "Product Manager", "Product Owner", "Project Manager", "React Native", "SAP Developer", "Test Automation Engineer", "UI/UX Designer", "iOS" - Rol tanımı
- **Frontend yazıyorsan hangilerini kullanıyorsun**: "React", "Angular", "Vue", "Vanilla", "Kullanmıyorum"
- **Hangi tool'ları kullanıyorsun**: "Strapi", "FastApi", "Wordpress", "Redux", "Zustand", "Jotai", "Supabase", "Firebase", "Kullanmıyorum" - Kullanılan araçlar

### Maaş Bilgisi
- **Aylık ortalama net kaç bin TL alıyorsun?**: "0 - 10", "101 - 110", "11 - 20", "111 - 120", "121 - 130", "131 - 140", "141 - 150", "151 - 160", "161 - 170", "171 - 180", "191 - 200", "201 - 210", "21 - 30", "211 - 220", "221 - 230", "231 - 240", "241 - 250", "251 - 260", "261 - 270", "271 - 280", "281 - 290", "291 - 300", "300 +", "31 - 40", "41 - 50", "51 - 60", "61 - 70", "71 - 80", "81 - 90", "91 - 100" - Maaş aralığı

## Örnek Veri (İlk 3 Satır)
```csv
8/20/2025 12:31:15,Türkiye,Tam zamanlı,Hybrid,Erkek,5,Mid,"HTML/CSS, JavaScript, TypeScript, C#, Python",Fullstack,React,Redux,61 - 70
8/20/2025 12:31:27,Türkiye,Tam zamanlı,Remote,Erkek,6,Senior,"JavaScript, TypeScript",React Native,React,"Redux, Firebase",121 - 130
8/20/2025 12:32:54,Avrupa,Tam zamanlı,Hybrid,Erkek,7,Senior,"HTML/CSS, JavaScript, TypeScript",Fullstack,React,Redux,151 - 160
8/20/2025 12:33:08,Türkiye,Tam zamanlı,Remote,Erkek,5,Mid,C#,Backend,Kullanmıyorum,Kullanmıyorum,81 - 90
8/20/2025 12:34:03,Türkiye,Tam zamanlı,Remote,Erkek,10,Senior,"HTML/CSS, JavaScript, TypeScript",Frontend,React,Zustand,121 - 130
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

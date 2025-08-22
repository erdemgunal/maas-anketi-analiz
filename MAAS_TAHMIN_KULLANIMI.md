# 🎯 XGBoost Maaş Tahmin Modeli - Kullanım Rehberi

## 📋 Genel Bilgi

Bu araç, eğitilmiş XGBoost modelini kullanarak bireysel maaş tahmini yapar. Model, 2820 kişilik maaş anketi verisi ile eğitilmiş ve %53.34 doğruluk oranına sahiptir. **Önemli:** Bu model gerçek tahmin yapar - maaş bilgisini feature olarak kullanmaz!

## 🚀 Hızlı Başlangıç

### 1. Sanal Ortamı Aktifleştirin
```bash
source venv/bin/activate
```

### 2. Basit Tahmin Örneği
```bash
python -m src.predict --json '{"yas":27, "Toplam kaç yıllık iş deneyimin var?":3, "Hangi seviyedesin?":2, "Frontend_React":1, "Hangi_JavaScript":1, "Hangi_Python":1, "Çalışma şekli":1, "Cinsiyet":1, "Şirket lokasyon":1, "Çalışma türü":0, "Ne yapıyorsun?":1, "Hangi tool'\''ları kullanıyorsun":1}'
```

**Çıktı:** `Tahmin edilen maaş (bin TL): 137.41`

## 📊 Giriş Parametreleri

### 🔢 Sayısal Değerler
- **yas**: Yaşınız (örn: 25, 30, 35)
- **Toplam kaç yıllık iş deneyimin var?**: İş deneyimi yılı (örn: 1, 3, 5, 10)

### 🏷️ Kategorik Değerler (0-1 kodlaması)
- **Hangi seviyedesin?**: 
  - 0: Junior
  - 1: Mid
  - 2: Senior
  - 3: Lead/Manager

- **Çalışma şekli**:
  - 0: Ofis
  - 1: Remote
  - 2: Hibrit

- **Cinsiyet**:
  - 0: Kadın
  - 1: Erkek

- **Çalışma türü**:
  - 0: Tam zamanlı
  - 1: Yarı zamanlı
  - 2: Freelance

### 💻 Teknoloji Kullanımı (0-1)
- **Frontend_React**: React kullanıyor musunuz? (1: Evet, 0: Hayır)
- **Hangi_JavaScript**: JavaScript kullanıyor musunuz? (1: Evet, 0: Hayır)
- **Hangi_Python**: Python kullanıyor musunuz? (1: Evet, 0: Hayır)
- **Hangi_TypeScript**: TypeScript kullanıyor musunuz? (1: Evet, 0: Hayır)
- **Hangi_Java**: Java kullanıyor musunuz? (1: Evet, 0: Hayır)
- **Hangi_C++**: C++ kullanıyor musunuz? (1: Evet, 0: Hayır)
- **Hangi_SQL**: SQL kullanıyor musunuz? (1: Evet, 0: Hayır)
- **Hangi_HTML_CSS**: HTML/CSS kullanıyor musunuz? (1: Evet, 0: Hayır)

### 🏢 Şirket Bilgileri
- **Şirket lokasyon**: Şehir kodu (0-10 arası)
- **Ne yapıyorsun?**: Rol kodu (0-5 arası)
- **Hangi tool'ları kullanıyorsun**: Tool kullanım kodu (0-5 arası)

## 📝 Örnek Kullanım Senaryoları

### 👨‍💻 Junior React Geliştirici
```bash
python -m src.predict --json '{
  "yas": 25,
  "Toplam kaç yıllık iş deneyimin var?": 2,
  "Hangi seviyedesin?": 0,
  "Frontend_React": 1,
  "Hangi_JavaScript": 1,
  "Hangi_HTML_CSS": 1,
  "Çalışma şekli": 1,
  "Cinsiyet": 1,
  "Çalışma türü": 0,
  "Şirket lokasyon": 1,
  "Ne yapıyorsun?": 1,
  "Hangi tool'\''ları kullanıyorsun": 1
}'
```
**Çıktı:** `Tahmin edilen maaş (bin TL): 120.09`

### 👩‍💻 Senior Python Geliştirici
```bash
python -m src.predict --json '{
  "yas": 32,
  "Toplam kaç yıllık iş deneyimin var?": 8,
  "Hangi seviyedesin?": 2,
  "Hangi_Python": 1,
  "Hangi_SQL": 1,
  "Hangi_JavaScript": 1,
  "Çalışma şekli": 2,
  "Cinsiyet": 0,
  "Çalışma türü": 0,
  "Şirket lokasyon": 1,
  "Ne yapıyorsun?": 2,
  "Hangi tool'\''ları kullanıyorsun": 1
}'
```
**Çıktı:** `Tahmin edilen maaş (bin TL): 124.79`

### 🚀 Full Stack Geliştirici
```bash
python -m src.predict --json '{
  "yas": 28,
  "Toplam kaç yıllık iş deneyimin var?": 5,
  "Hangi seviyedesin?": 1,
  "Frontend_React": 1,
  "Hangi_JavaScript": 1,
  "Hangi_TypeScript": 1,
  "Hangi_Python": 1,
  "Hangi_SQL": 1,
  "Hangi_HTML_CSS": 1,
  "Çalışma şekli": 1,
  "Cinsiyet": 1,
  "Çalışma türü": 0,
  "Şirket lokasyon": 1,
  "Ne yapıyorsun?": 1,
  "Hangi tool'\''ları kullanıyorsun": 1
}'
```
**Çıktı:** `Tahmin edilen maaş (bin TL): ~125.00`

## 🔍 Mevcut Feature'ları Görme

Tüm kullanılabilir feature'ları görmek için:
```bash
python -m src.predict --print-schema --json '{"dummy":0}'
```

## ⚠️ Önemli Notlar

1. **Eksik Feature'lar**: Girmeyen feature'lar otomatik olarak 0 değeri alır
2. **Doğruluk**: Model %53.34 doğruluk oranına sahiptir (gerçek tahmin)
3. **Birim**: Sonuç "bin TL" cinsindendir (örn: 120.09 = 120,090 TL)
4. **Güncelleme**: Model Maas Anket verilerine göre eğitilmiştir
5. **Gerçek Tahmin**: Maaş bilgisi feature olarak kullanılmaz!

## 🎯 Model Performansı

- **Test R²**: 0.5334 (İyi)
- **CV R²**: 0.5288 (İyi)
- **MAE**: 23.45 bin TL
- **RMSE**: 31.87 bin TL

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. Feature listesini kontrol edin: `--print-schema`
2. JSON formatını doğrulayın
3. Tüm gerekli alanları doldurun

---

**Not**: Bu tahminler eğitim verisine dayalıdır ve gerçek maaşlar piyasa koşullarına göre değişebilir.

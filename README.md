# 2025 Yazılım Sektörü Maaş Analizi Projesi

Bu klasör, **2025 Yazılım Sektörü Maaş Analizi** projesinin tüm dokümantasyonunu içermektedir.

Bu proje, 20-21 Ağustos 2025 tarihleri arasında **2.969 yazılım uzmanından** toplanan maaş verilerini analiz eder. Zafer Ayan'ın 2025 Yazılım Sektörü Maaş Anketi verilerine dayalı olarak hazırlanmıştır.

**Veri Kaynağı:** [LinkedIn Post](https://www.linkedin.com/posts/zaferayan_geleneksel-maa%C5%9F-anketi-buyrun-httpslnkdin-activity-7363866008664629248-7YcQ) | [Medium Makalesi](https://zaferayan.medium.com/2025-a%C4%9Fustos-detayl%C4%B1-maa%C5%9F-anketi-98446d71920a)

## Ana Bulgular

| Kategori | Bulgu | Detay |
|----------|-------|-------|
| **Uzaktan Çalışma** | +22.6k TL | Uzaktan çalışanlar ofisten %28.8 daha fazla kazanıyor |
| **Coğrafi Fark** | +70.0k TL | Avrupalı şirketler Türk şirketlerinden %75.3 daha fazla ödüyor |
| **Cinsiyet Farkı** | +13.3k TL | Erkekler kadınlardan %15.4 daha fazla kazanıyor |
| **Kariyer Artışı** | +137% | Junior'dan Senior'a maaş artışı |
| **Teknoloji ROI** | +70.7% | Rust kullanıcıları en yüksek primi alıyor |

## Hızlı Başlangıç

```bash
# Depoyu klonlayın
git clone https://github.com/erdemgunal/salary_analysis_project.git
cd salary_analysis_project

# Sanal ortam oluşturun
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Analizi çalıştırın
python src/sprint2_analysis.py

# Dashboard'u başlatın
streamlit run src/streamlit_dashboard.py
```

## Proje Yapısı

```
salary_analysis_project/
├── data/                    # Ham ve işlenmiş veriler
├── src/                     # Analiz kodları
├── figures/                 # Görselleştirmeler
├── reports/                 # LaTeX rapor
├── docs/                    # Proje belgeleri
└── README.md               # Bu dosya
```

## Önemli Görselleştirmeler

- **Kariyer Seviyesi Analizi**: Junior → Senior maaş artışı
- **Teknoloji ROI**: Hangi teknolojiler daha fazla ödüyor
- **Coğrafi Karşılaştırma**: Ülke bazında maaş farkları
- **Çalışma Modu**: Remote vs Office maaş karşılaştırması
- **Cinsiyet Analizi**: Ücret eşitliği incelemesi

## Etkileşimli Dashboard

**🔗 Canlı Dashboard:** [maas-anketi.streamlit.app](http://maas-anketi.streamlit.app)

## Gelecek Özellikler

- **Maaş Tahmin Modeli**: Kullanıcının profil bilgilerine göre (rol, deneyim, teknoloji, lokasyon vb.) beklenen maaşı tahmin eden bir makine öğrenimi modeli (örn. XGBoost/LightGBM). Dashboard entegrasyonu ve model performans raporlaması planlanmaktadır.
 - **2025 vs 2024 Karşılaştırması**: 2025 verisinin 2024 verisiyle karşılaştırmalı analizi (ortalama maaş, dağılım, ROI ve çalışma modu bazında). Yıl etkisi için normalizasyon ve istatistiksel anlamlılık testleri (örn. t-test, etki büyüklüğü) dahil edilecektir.

### Özellikler:
- Gerçek zamanlı filtreleme
- Etkileşimli grafikler
- İstatistiksel testler
- Kariyer önerileri

## İstatistiksel Metodoloji

- **Örneklem:** 2,969 profesyonel
- **Veri Toplama:** 20-21 Ağustos 2025 (2 gün)
- **Testler:** t-test, Cohen's d, korelasyon analizi
- **Anlamlılık:** p < 0.001 seviyesinde

## Teknoloji ROI Analizi

### En Yüksek Kazandıran Teknolojiler:
1. **Rust**: +69.4k TL (%71.0 artış)
2. **Objective-C**: +63.1k TL (%64.8 artış)
3. **Go**: +39.1k TL (%40.8 artış)
4. **Kotlin**: +32.2k TL (%33.5 artış)

### Frontend Teknolojileri:
- **Vue.js**: +8.3k TL (%8.5 artış)
- **React**: -3.3k TL (%3.3 azalış) - Pazar doygunluğu

## Kariyer Seviyeleri

| Seviye | Ortalama Maaş | Katılımcı |
|--------|---------------|-----------|
| Staff Engineer | 193.0k TL | 16 |
| Architect | 188.4k TL | 52 |
| Management | 184.8k TL | 83 |
| Team Lead | 150.5k TL | 175 |
| Senior | 130.8k TL | 772 |
| Mid | 84.1k TL | 1,138 |
| Junior | 55.1k TL | 733 |

## Coğrafi Etki

| Şirket Lokasyonu | Ortalama Maaş | Türkiye'ye Göre |
|-------|---------------|-----------------|
| Avrupa | 162.9k TL | +75.3% |
| Amerika | 154.4k TL | +66.2% |
| Yurtdışı Tr Hub | 113.2k TL | +21.9% |
| Türkiye | 92.9k TL | - |

## Çalışma Modları

| Mod | Ortalama Maaş | Ofis'e Göre |
|-----|---------------|-------------|
| Hibrit | 105.0k TL | +33.6% |
| Uzaktan | 101.2k TL | +28.8% |
| Ofis | 78.6k TL | - |

## Önemli Notlar

- **Veri Sınırlaması:** 2 günlük anket penceresi
- **Konum Tahmini:** Şirket bilgilerine dayalı
- **Kendi Beyanı:** Maaş ve teknoloji kullanımı
- **Örneklem:** 2,969 profesyonel

## Raporlar

- **LaTeX Rapor:** `reports/salary_analysis_report.tex`
- **PDF Çıktısı:** `maas_analizi_2025.pdf`
- **Jupyter Notebooks:** `notebooks/` klasörü

## Katkı

Bu proje geliştirmelere açıktır. Yeni özellikler, hata düzeltmeleri veya dokümantasyon iyileştirmeleri için katkılarınızı memnuniyetle karşılıyoruz. Veri gizliliği ve etik kurallara uygun kullanım önemlidir.

### Nasıl Katkıda Bulunulur (Adım Adım)

1. Depoyu forklayın ve yerel ortamınıza klonlayın
   ```bash
   git clone https://github.com/erdemgunal/salary_analysis_project.git
   cd salary_analysis_project
   git remote add upstream https://github.com/erdemgunal/salary_analysis_project.git
   ```
2. Geliştirme ortamını hazırlayın
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Yeni bir dal (branch) oluşturun
   ```bash
   git checkout -b feat/kisa-ozet-branch-adi
   ```
4. Analizleri ve dashboard'u çalıştırarak doğrulayın
   ```bash
   python src/sprint2_analysis.py
   streamlit run src/streamlit_dashboard.py
   ```
5. Notebooks üzerinde çalışıyorsanız çıktıların (grafikler, .pkl) tutarlı üretildiğini doğrulayın
   - Üretilen görseller `figures/` altına kaydedilmelidir
   - Büyük verileri repoya eklemeyin; gerekiyorsa `data/` için indirme talimatı ekleyin
6. Kod stili ve kalite kontrolleri
   ```bash
   # (Varsa) basit format ve linter komutlarınızı çalıştırın
   # örn: ruff/flake8/isort/black kullanılabilir
   ```
7. Anlamlı commit mesajları yazın ve dalınızı gönderin
   ```bash
   git add -A
   git commit -m "feat: X analizi için Y görselleştirmesi eklendi"
   git push origin feat/kisa-ozet-branch-adi
   ```
8. Pull Request (PR) açın
   - Değişiklik özeti, motivasyon ve doğrulama adımlarını yazın
   - İlgili görselleri ve çıktı örneklerini ekleyin
   - Gerekliyse `README.md` ve `docs/` güncellemelerini dahil edin

### Rehber İlkeler

- Açıklayıcı değişken/işlev adları ve tekrar kullanılabilir fonksiyonlar tercih edin
- Görseller ve raporlar ilgili klasörlerde konumlandırılmalı (`figures/`, `reports/`)
- Yeni özellikler için kısa bir bölümle `README.md` veya `docs/` güncellemesi yapın

### Maaş Tahmin Modeline Katkı

- Plan: ML tabanlı tahmin (örn. XGBoost/LightGBM), metrikler: MAE/RMSE/R²
- Beklenenler:
  - `src/` altında modüler bir `salary_prediction.py` veya benzeri yapı
  - Eğitim/validasyon bölünmesi ve çapraz doğrulama
  - Model kartı/dokümantasyonu ve dashboard entegrasyonu (inference)
  - Çıktıların açıklanabilirliği için SHAP/feature importance
  
Önerilerinizi ve sorularınızı Issue olarak açabilirsiniz. Küçük değişiklikler için doğrudan PR gönderebilirsiniz.

## İletişim

**Rapor Hazırlayan:** Hakkı Günal  
**Veri Kaynağı:** Zafer Ayan  
**Tarih:** Ağustos 2025

---

**Canlı Dashboard:** [maas-anketi.streamlit.app](http://maas-anketi.streamlit.app)  
**Toplam Katılımcı:** 2,969 yazılım uzmanı  
**Anket Dönemi:** 20-21 Ağustos 2025
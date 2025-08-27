# 2025 Yazılım Sektörü Maaş Analizi Projesi

## Projeye Genel Bakış

Bu kapsamlı analiz, 20-21 Ağustos 2025 tarihleri arasında Türkiye'deki 2.969 yazılım uzmanından toplanan maaş verilerini incelemektedir. Çalışma, kariyer seviyeleri, teknolojiler, çalışma modelleri ve coğrafi konumlar genelinde maaş dinamiklerine ilişkin önemli bilgiler ortaya koyarak, hem bireysel kariyer planlaması hem de kurumsal ücretlendirme stratejileri için eyleme geçirilebilir içgörüler sunmaktadır.

## Önemli Bulgular

### Önemli Keşifler
- **Uzaktan Çalışma Primi**: Uzaktan çalışanlar, ofis çalışanlarından 22,6 bin TL daha fazla kazanıyor (Cohen's d = 0,42)
- **Coğrafi Eşitsizlik**: Avrupalı şirketler, Türk şirketlerinden 70,0 bin TL daha yüksek maaşlar sunuyor (Cohen's d = 1,35)
- **Cinsiyet Uçurumu**: Erkek profesyoneller, kadın profesyonellerden 13,3 bin TL daha fazla kazanıyor (Cohen's d = 0,24)
- **Teknolojinin Etkisi**: Belirli programlama dilleri %15-20 maaş primi sağlıyor
- **Kariyer Gelişimi**: Junior seviyeden Senior seviyeye %40-60 artışla net maaş artışı

### 📊 İstatistiksel Anlamlılık
Tüm önemli bulgular istatistiksel olarak anlamlıdır (p < 0,001) ve etki büyüklükleri küçükten çok büyük arasında değişmektedir, bu da hem istatistiksel hem de pratik anlamlılığı göstermektedir.

## Proje Yapısı

```
salary_analysis_project/
├── data/
│   ├── 2025_maas_anket.csv          # Ham anket verileri
│   └── 2025_cleaned_data.csv        # İşlenmiş ve temizlenmiş veriler
├── src/
│   ├── data_preprocessing.py        # Sprint 1: Veri temizleme ve ön işleme
│   ├── sprint2_analysis.py          # Sprint 2: Temel analizler ve görselleştirmeler
│   ├── streamlit_dashboard.py       # Sprint 3: Etkileşimli gösterge tablosu
│   └── latex_report_generator.py    # Sprint 4: LaTeX rapor oluşturma
├── figures/                         # Oluşturulan görselleştirmeler (PNG/HTML)
├── reports/
│   └── salary_analysis_report.tex   # LaTeX rapor kaynağı
├── docs/                           # Proje belgeleri
└── README.md                       # Bu dosya
```
## Kurulum ve Yükleme

### Ön Koşullar
- Python 3.8+
- pip paket yöneticisi

### Yükleme
```bash
# Depoyu kopyalayın
git clone <depo-url>
cd salary_analysis_project

# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı etkinleştirin
source venv/bin/activate  # Windows'ta: venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### Analizi Çalıştırma
```bash
# Sanal ortamı etkinleştirin
source venv/bin/activate

# Veri ön işlemeyi çalıştırın (Sprint 1)
python src/data_preprocessing.py

# Temel analizleri çalıştırın (Sprint 2)
python src/sprint2_analysis.py

# LaTeX raporu oluşturun (Sprint 4)
python src/latex_report_generator.py

# Etkileşimli gösterge tablosunu başlatın (Sprint 3)
streamlit run src/streamlit_dashboard.py
```

## Önemli Görselleştirmeler

### Maaş Dağılımı Analizi
- **Kariyer Seviyesi Kutulu Grafikler**: Junior seviyeden Senior seviyeye maaş artışı
- **Çalışma Modu Karşılaştırması**: Uzaktan çalışma ve ofis maaş dağılımları
- **Coğrafi Analiz**: Şirketin konumunun ücretlere etkisi
- **Cinsiyet Analizi**: Cinsiyete dayalı maaş farkları

### Teknoloji ROI Analizi
- **Programlama Dilleri**: Farklı diller için maaş primleri
- **Ön Uç Teknolojileri**: React ve diğer çerçevelerin etkisi
- **Geliştirme Araçları**: Çeşitli araçlar için yatırım getirisi analizi
- **Teknoloji Korelasyonları**: Teknoloji-maaş ilişkilerinin ısı haritası

### Gelişmiş Analitik
- **Kariyer Zaman Çizelgesi**: Deneyim ve maaş dağılım grafikleri
- **Sankey Diyagramları**: Kariyer gelişiminin görselleştirilmesi
- **Saatlik Katılım**: Anket yanıt kalıpları
- **Cinsiyete Göre Teknoloji Kullanımı**: Cinsiyete göre teknoloji benimseme

## Etkileşimli Kontrol Paneli Özellikleri

### Filtreleme Özellikleri
- **Demografik Bilgiler**: Cinsiyet, deneyim seviyesi, kariyer aşaması
- **Çalışma Düzenlemeleri**: Uzaktan, hibrit, ofis çalışması
- **Coğrafi**: Şirketin konumu ve çalışma yeri
- **Teknoloji Yığını**: Programlama dilleri, çerçeveler, araçlar

### Etkileşimli Görselleştirmeler
- **Dinamik Kutu Grafikleri**: Gerçek zamanlı filtreleme ve karşılaştırma
- **Etkileşimli Çubuk Grafikler**: Fareyle üzerine gelindiğinde ayrıntıları görünen teknoloji ROI'si
- **Sankey Diyagramları**: Kariyer ilerleme akışları
- **Dağılım Grafikleri**: Deneyim-maaş ilişkileri

### Önemli Bilgiler Paneli
- **İstatistiksel Testler**: P değerleri ve etki büyüklükleri
- **Pratik Önemi**: Cohen'in d yorumları
- **Pazar Eğilimleri**: Teknoloji talep göstergeleri
- **Kariyer Önerileri**: Uygulanabilir tavsiyeler

## İstatistiksel Metodoloji

### Hipotez Testi
- **Bağımsız Örneklem t-testleri**: Grup karşılaştırmaları
- **Etki Büyüklüğü Hesaplamaları**: Pratik önem için Cohen's d
- **Çoklu Karşılaştırma Düzeltmeleri**: Uygulanabilir olduğu durumlarda
- **Korelasyon Analizi**: Teknoloji-maaş ilişkileri

### Veri Kalitesi
- **Aykırı Değerlerin İşlenmesi**: IQR ve Z-skor yöntemleri
- **Eksik Değerlerin İşlenmesi**: Kapsamlı imputasyon stratejileri
- **Veri Doğrulama**: Kalite kontrolleri ve tutarlılık doğrulaması
- **Çoklu Etiket İşleme**: Teknoloji yığını kodlaması

## Kategoriye Göre Önemli Bulgular

### Uzaktan Çalışma Analizi
- Uzaktan çalışanlar için **22,6 bin TL prim**
- Uzaktan çalışan yeteneklere yönelik **güçlü pazar talebi**
- Taşınma gerektirmeyen **küresel fırsatlar**
- İşverenler tarafından değer verilen **iş-yaşam dengesi**

### Coğrafi Etki
- Avrupa ve Türkiye arasında **70,0 bin TL fark**
- Avrupa şirketleri için **%60-80 prim**
- Uzaktan çalışma yoluyla **uluslararası pazara erişim**
- Ulaşılabilir **küresel ücret standartları**

### Cinsiyet ve Teknoloji
- **13,3 bin TL cinsiyet farkı** (Cohen's d = 0,24)
- Cinsiyetler arasında **benzer teknoloji benimseme** modelleri
- Teknoloji becerileri sayesinde **eşit fırsatlar**
- **Ücret eşitliği** girişimlerine ihtiyaç

### Teknoloji Yığını ROI
- Yüksek talep gören teknolojiler için **%15-20 maaş primi**
- Nadir beceriler için **pazar odaklı ücretlendirme**
- Maksimum etki için **beceri kombinasyonu stratejileri**
- Teknoloji seçimleri sayesinde **kariyer hızlandırma**

## Rapor Çıktıları

### LaTeX Raporu
- İstatistiksel titizlikle **kapsamlı analiz**
- Yayınlamaya uygun **profesyonel biçimlendirme**
- Farklı hedef kitleler için **uygulanabilir içgörüler**
- Etki büyüklükleri ile **metodolojik şeffaflık**

### Hedef Kitleler
- **React Stajyer Grubu**: Teknolojiye özgü içgörüler ve kariyer rehberliği
- **Yazılım Uzmanları**: Maaş eğilimleri ve kariyer planlama
- **Kuruluşlar**: Ücretlendirme stratejisi ve yetenekleri elde tutma
- **Araştırmacılar**: İstatistiksel metodoloji ve veri analizi

### Kontrol Paneli Özellikleri
- **Gerçek zamanlı filtreleme** ve keşif
- Plotly ile **etkileşimli görselleştirmeler**
- Etki büyüklükleri ile **istatistiksel özetler**
- Verilere dayalı **kariyer önerileri**

## Teknik Yığın

### Temel Teknolojiler
- **Python 3.8+**: Birincil analiz dili
- **Pandas**: Veri işleme ve analiz
- **NumPy**: Sayısal hesaplamalar
- **SciPy**: İstatistiksel testler ve etki büyüklükleri

### Görselleştirme
- **Matplotlib**: Statik görselleştirmeler
- **Seaborn**: İstatistiksel grafikler
- **Plotly**: Etkileşimli görselleştirmeler
- **Streamlit**: Kontrol paneli çerçevesi

### Raporlama
- **LaTeX**: Profesyonel rapor oluşturma
- **Overleaf**: Bulut tabanlı LaTeX derleme
- **Markdown**: Belgeleme ve README

## Dokümantasyon

### Proje Dokümantasyonu
- **ANALYSIS_OBJECTIVES.md**: Ayrıntılı analiz hedefleri ve hipotezler
- **METHODOLOGY.md**: İstatistiksel yöntemler ve veri işleme
- **DATASET_SPECIFICATIONS.md**: Veri yapısı ve değişkenler
- **EXPECTED_OUTPUTS.md**: Görselleştirme ve raporlama gereksinimleri
- **SUCCESS_CRITERIA.md**: Proje kabul kriterleri
- **TECHNICAL_STACK.md**: Teknoloji gereksinimleri ve kurulum
- **PRD.md**: Ürün gereksinimleri belgesi
- **SHARE_STRATEGY.md**: Dağıtım ve paylaşım yönergeleri

### Analiz Kapsamı
- **Kariyer Gelişimi**: Junior ve Senior maaş modelleri
- **Teknoloji ROI**: Programlama dilleri ve araçlarının etkisi
- **Çalışma Modelleri**: Uzaktan çalışma ve ofis çalışması ücretleri
- **Coğrafi Faktörler**: Konuma bağlı maaş farklılıkları
- **Cinsiyet Analizi**: Ücret eşitliği ve teknoloji benimseme
- **Deneyimin Etkisi**: Kariyer zaman çizelgesi ve maaş artışı
- **İstihdam Türleri**: Tam zamanlı ve serbest çalışma modelleri

## Kullanım Senaryoları

### Bireysel Geliştiriciler İçin
- **Kariyer Planlama**: Maksimum yatırım getirisi için öğrenilmesi gereken teknolojiler
- **Maaş Müzakeresi**: Piyasa karşılaştırmaları ve ücret eğilimleri
- **İş Arama**: Daha yüksek maaş için hedef şirketler ve konumlar
- **Beceri Geliştirme**: Kariyer gelişimi için odaklanılması gereken alanlar

### Kuruluşlar için
- **Ücretlendirme Stratejisi**: Piyasa ile uyumlu maaş yapıları
- **Yetenek Tutma**: Uzaktan çalışma politikaları ve avantajları
- **Teknoloji Yatırımı**: Beceri geliştirme öncelikleri
- **Çeşitlilik Girişimleri**: Cinsiyetler arası ücret farkı analizi ve çözümleri

### React Geliştiricileri için
- **Teknoloji Yığını**: React + yüksek ROI arka uç kombinasyonları
- **Kariyer Yolu**: Ön uçtan tam yığına ilerleme
- **Uzaktan Çalışma Fırsatları**: Uluslararası ücret erişimi
- **Liderlik Gelişimi**: Yönetim kariyeri hazırlığı

## Önemli Notlar

### Veri Sınırlamaları
- **Kendi beyanına dayalı veriler**: Potansiyel raporlama önyargısı
- **Örnek temsil gücü**: Tüm sektörü yansıtmayabilir
- **Konum tahmini**: Şirket bilgilerine dayalı
- **Teknoloji yeterliliği**: Kendi beyanına dayalı kullanım ile gerçek beceriler

### Konum Feragatnamesi
*“Şirketin konumu ve çalışma düzenine (Ofis/Hibrit → şirketin konumu) dayalı tahmini konum. Kesin değildir.”*

### Gizlilik ve Etik
- **Anonimleştirilmiş veriler**: Bireysel kimlik bilgisi içermez
- **Toplu raporlama**: Yalnızca grup düzeyinde içgörüler
- **Etik analiz**: Bireysel vakalara değil, sektör trendlerine odaklanma
- **Şeffaf metodoloji**: Yöntemlerin ve sınırlamaların tam olarak açıklanması

## Katkı

Bu proje, açık dokümantasyon ve kabul kriterleri ile sprint tabanlı bir geliştirme yaklaşımını takip etmektedir. Tüm analizler, tekrarlanabilir ve istatistiksel olarak titiz olacak şekilde tasarlanmıştır.

## Lisans

Bu proje, eğitim ve araştırma amaçlı tasarlanmıştır. Bulguları kullanırken veri gizliliği ve etik kurallara uyunuz.

---

**Rapor hazırlayan**: Zafer Ayan  
**Veri toplama dönemi**: 20-21 Ağustos 2025  
**Toplam katılımcı sayısı**: 2.969 yazılım uzmanı  
**Önemli içgörü**: Uzaktan çalışma 22,6 bin TL prim sağlıyor, Avrupalı şirketler 70,0 bin TL daha fazla teklif ediyor
- Anket katılımcılarının verdiği “Hangi seviyedesin?” cevapları, doğrudan tek bir sıralı yapı içinde değerlendirilemeyecek kadar farklı türden rolleri içermektedir. Bu nedenle, analiz sürecinde öncelikle seviyeler iki ana kategoriye ayrılmıştır: **Individual Contributor (IC) seviyeleri** ve **Managerial / Ownership seviyeleri**. IC kategorisi teknik odaklı kariyer basamaklarını (Junior, Mid, Senior, Staff Engineer, Team Lead, Architect) kapsarken, Managerial / Ownership kategorisi yönetim veya iş ortaklığı rolleri (Engineering Manager, Director Level Manager, C-Level Manager, Partner) altında toplanmıştır.

Individual Contributor seviyeleri, kariyer ilerleyişine uygun olacak şekilde **ordinal değişken** olarak yeniden kodlanmıştır. Burada Junior en düşük değer (1) olacak şekilde sıralama yapılmış, Mid (2), Senior (3), Staff Engineer (4), Team Lead (5) ve Architect (6) şeklinde devam eden bir yapıya dönüştürülmüştür. Bu sayısal kodlama sayesinde kıdem ile maaş arasındaki ilişkiyi doğrudan incelemek mümkün hale gelmiştir.

Managerial ve Ownership roller ise farklı bir doğaya sahip olduklarından ordinal değil, **kategorik değişken** olarak ele alınmıştır. Engineering Manager, Director, C-Level ve Partner için ayrı kategoriler oluşturulmuş ve **One-Hot encoding** yöntemi kullanılmıştır. Ayrıca, teknik seviyelerle yönetsel seviyeleri birbirinden ayırmak amacıyla ek olarak bir **is\_manager** ikili (binary) değişkeni tanımlanmıştır. Bu değişken sayesinde bir katılımcının yönetimsel veya sahiplik rolünde olup olmadığı basit bir şekilde işaretlenebilmiştir.

Raporlama aşamasında, Individual Contributor seviyeleri **tek bir ordinal eksen üzerinde** değerlendirilmiş, böylece Junior’dan Architect’e kadar maaşların nasıl değiştiği görsel olarak kolaylıkla sunulabilmiştir. Yönetim ve sahiplik rollerinin maaş dağılımları ise ayrı bir kategorik karşılaştırma olarak ele alınmıştır. Bu yöntem, hem kariyer basamaklarının doğal ilerleyişini hem de yönetsel rollerin etkisini analize dahil ederek daha sağlıklı ve okunabilir sonuçlar ortaya koymuştur.


- Çalışan lokasyonu tahmini, şirket lokasyonu ve çalışma şekline dayanır; %100 doğru olmayabilir. calisma sekli hybrid veya office ise buyuk bir ihtimal sirket lokasyonu

- kadin erkek maas analizinde "Mann-Whitney" grafigi

- cleaned_data.csv dosyasi icerisinde kolon isimleri "Staff Engineer" seviyesi icin "management_Staff Engineer" seklinde yaziliyor. veya "SAP Developer" rolu icin "role_SAP Developer" seklinde aralarinda bosluklari bu sekilde birakacak miyiz? veya "Objective C" icin "lang__Objective C" bunun disinda turkce karakterler icin nasil bir yol izlememiz gerekiyor sirket lokasyonu "Yurtdışı TR hub" icin "company_location_Yurtdışı TR hub" seklinde kullaniliyor. hem aralari acik hemde turkce. buna gore PROJECT_PLAN yi ve ilgili dokumantasyonlari guncelleyelim

- cleaned_data nin tutarlili cok onemli



ai modeline saglanan veriler ile bu yorumlar yapilacaktir. '''
*   **Kariyer Gelişimi İçgörülerinin Eksikliği (Skill Development)**:
    *   `ANALYSIS_OBJECTIVES.md`, hangi teknolojilerin kariyer ilerlemesini hızlandırdığına dair içgörüler ("React + Zustand öğrenenler Mid seviyesine %X daha hızlı geçiyor") beklemektedir.
    *   Bu türden bir analiz veya içgörü **rapor metninde yer almamaktadır**.

*   **React Staj Grubu için Spesifik Önerilerin Yetersizliği**:
    *   Projenin temel hedeflerinden biri, **React staj grubuna yönelik somut, eyleme dönüştürülebilir tavsiyeler** sunmaktır. Örneğin, "React’e ek olarak Zustand veya Firebase öğrenmek maaş getirisini artırabilir" veya "Mid’den Senior’a geçiş için React + Redux öğrenmek maaşı %X artırıyor" gibi öneriler beklenmektedir.
    *   Mevcut rapordaki "Recommendations" bölümü oldukça geneldir ve React staj grubuna özel teknoloji öğrenimi veya kariyer ilerlemesi tavsiyeleri **içermemektedir**. Bu, ana hedef kitle için önemli bir eksikliktir.
    '''


2. "Mid’den Senior’a geçiş için React + Redux öğrenmek maaşı %X artırıyor" yorumu için gerekenler:
Bu yorumu yapabilmek için, Kariyer Gelişimi (Career Progression), Skill Development Pattern’ları ve Kariyer Seviyeleri ve Maaş İlişkisi analizlerine ihtiyaç duyarız.
• Gerekli Veri Sütunları:
    ◦ salary_numeric: Maaş bilgisi.
    ◦ seniority_level_ic: Teknik kariyer seviyeleri (Junior, Mid, Senior, Staff Engineer, Team Lead, Architect). Bu sütun, ordinal olarak kodlanmış olmalıdır (örn. Junior=1, Mid=2, Senior=3).
    ◦ management_level: Yönetim seviyeleri (Engineering Manager, Director Level Manager, C-Level Manager, Partner).
    ◦ frontend_technologies: React gibi frontend teknolojileri.
    ◦ tools: Redux gibi araçlar.
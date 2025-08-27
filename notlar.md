- Anket katılımcılarının verdiği “Hangi seviyedesin?” cevapları, doğrudan tek bir sıralı yapı içinde değerlendirilemeyecek kadar farklı türden rolleri içermektedir. Bu nedenle, analiz sürecinde öncelikle seviyeler iki ana kategoriye ayrılmıştır: **Individual Contributor (IC) seviyeleri** ve **Managerial / Ownership seviyeleri**. IC kategorisi teknik odaklı kariyer basamaklarını (Junior, Mid, Senior, Staff Engineer, Team Lead, Architect) kapsarken, Managerial / Ownership kategorisi yönetim veya iş ortaklığı rolleri (Engineering Manager, Director Level Manager, C-Level Manager, Partner) altında toplanmıştır.

Individual Contributor seviyeleri, kariyer ilerleyişine uygun olacak şekilde **ordinal değişken** olarak yeniden kodlanmıştır. Burada Junior en düşük değer (1) olacak şekilde sıralama yapılmış, Mid (2), Senior (3), Staff Engineer (4), Team Lead (5) ve Architect (6) şeklinde devam eden bir yapıya dönüştürülmüştür. Bu sayısal kodlama sayesinde kıdem ile maaş arasındaki ilişkiyi doğrudan incelemek mümkün hale gelmiştir.

Managerial ve Ownership roller ise farklı bir doğaya sahip olduklarından ordinal değil, **kategorik değişken** olarak ele alınmıştır. Engineering Manager, Director, C-Level ve Partner için ayrı kategoriler oluşturulmuş ve **One-Hot encoding** yöntemi kullanılmıştır. Ayrıca, teknik seviyelerle yönetsel seviyeleri birbirinden ayırmak amacıyla ek olarak bir **is\_manager** ikili (binary) değişkeni tanımlanmıştır. Bu değişken sayesinde bir katılımcının yönetimsel veya sahiplik rolünde olup olmadığı basit bir şekilde işaretlenebilmiştir.

Raporlama aşamasında, Individual Contributor seviyeleri **tek bir ordinal eksen üzerinde** değerlendirilmiş, böylece Junior’dan Architect’e kadar maaşların nasıl değiştiği görsel olarak kolaylıkla sunulabilmiştir. Yönetim ve sahiplik rollerinin maaş dağılımları ise ayrı bir kategorik karşılaştırma olarak ele alınmıştır. Bu yöntem, hem kariyer basamaklarının doğal ilerleyişini hem de yönetsel rollerin etkisini analize dahil ederek daha sağlıklı ve okunabilir sonuçlar ortaya koymuştur.


- Çalışan lokasyonu tahmini, şirket lokasyonu ve çalışma şekline dayanır; %100 doğru olmayabilir. calisma sekli hybrid veya office ise buyuk bir ihtimal sirket lokasyonu

- kadin erkek maas analizinde "Mann-Whitney" grafigi





ANALYSIS_OBJECTIVES.MD: Analiz hedeflerini (ör. React vs. non-React maaş farkı, remote vs. office) netleştirmek için.
METHODOLOGY.MD:
# Contested Logistics — Yüksek Lisans Bitirme Tezi Konu Araştırması

**Tarih:** 18 Ekim 2026 · **Kapsam:** YZ + sistem mühendisliği temelli, gerçek veriyle doğrulanabilir YL tez konusu seçimi
**Not:** Bu bir sistematik literatür taraması değil, konu seçimi için hedefli bir keşif taramasıdır (≈40 kaynak tarandı, 20'si birincil). K1 seçilirse 60–80 kaynaklık sistematik tarama ayrıca yapılmalı.

---

## 0. Yönetici özeti

**Önerilen ana konu (K1):** *Sensör-kesintili ortamda kapalı çevrim kontestasyon lojistiği — GNSS/iletişim bozulması altında durum kestirimi, dayanıklı sevkiyat kararı ve "bilginin değeri" analizi.*

Tek cümlelik gerekçe: Literatür ikiye ayrılmış durumda — bir yanda **ağ dayanıklılığı / interdiction oyunları** (ağı tam görüyor varsayıyor), öbür yanda **GNSS karıştırma ve karanlık gemi tespiti** (tespit ediyor ama lojistik kararına bağlamıyor). İkisini kapalı çevrimde birleştiren, üstelik 2023–2026 gerçek açık verisiyle yeniden oynatılarak doğrulanan bir çalışma açık literatürde yok. Bu boşluk, tam olarak "YZ + sistem mühendisliği" tezi tanımına düşüyor.

**Sıralama:** K1 (ana öneri) → K2 (deniz görünürlüğü, en güçlü veri) → K3 (insani koridor, en kolay yayın) → K6 (Boğazlar, en düşük risk) → K4 / K5 (yüksek risk, yüksek özgünlük).

---

## 1. Alan nedir, neden tam şimdi

"Contested logistics", rakibin lojistik zincirini **görsel, elektronik, siber ve kinetik** yollarla kesebildiği ortamda ikmal yapma problemidir. 2022 sonrası doktrin dili değişti: artık istisna değil, varsayılan durum.

Kanıt niteliğindeki gelişmeler:

- **ABD DLA beyaz kitabı (Nisan 2025):** "US military logistics no longer uncontested in Europe" — Avrupa'daki ikmal hattının artık rakipsiz olmadığı resmen kabul edildi.
- **DLA "Modern Contested Logistics Truths" (Aralık 2025):** müşterek lojistik yaklaşımlarını bu kabule göre yeniden yazıyor.
- **NATO JSEC (Ulm, 2019'dan beri):** ittifakın ilk kez lojistik *komutanlığı* var; ana görevi kıta içi intikal ve ikmal koridorları.
- **Ukrayna saha kanıtı — HEDGEHOG 2025:** yaklaşık 10 Ukraynalı drone operatörü, NATO zırhlı kuvvetinin hareketini simülasyonda tıkadı (ABD Kara Harp Okulu *War Room*). Yani "kontestasyon" artık taburun değil, **10 kişinin** yapabildiği bir şey.
- **Kızıldeniz / Bab el-Mandeb 2023–2026:** rota değişimi ~3.500 deniz mili uzama, en az 14 gün ek transit (St. Louis Fed); liman tıkanıklığının "histerezis" etkisi (deniz lojistiği dergisi, 2026).
- **Baltık GNSS karıştırma:** 2023–2026 arasında tırmanış; Bornholm izleme istasyonu 2026'da 30 vaka kaydetti (2025'in tamamı 16); GNSS bozulması artık gemi ve uçuş seyrüseferini bozuyor (GPS Solutions, 2026).
- **Tayvan:** CSIS "Lights Out" abluka oyunu (Temmuz 2025) — lojistik stok ve abluka dayanıklılığı merkezî tartışma.
- **NATO STO S&T Trends 2025–2045:** lojistik/ikmal dayanıklılığı öncelikli teknoloji başlıkları arasında.

**Çıkarım:** Alan sıcak, ama akademik üretim ağırlıklı olarak *senaryo simülasyonu* ve *ağ topolojisi* düzeyinde. **Ölçümün kendisi (sensör kesintisi, veri gecikmesi, belirsizlik) modelin parametresi bile değil, çoğu zaman.** Tezin açılacağı yer burası.

---

## 2. Bugüne kadar ne yapıldı — ve her çalışmanın bıraktığı boşluk

| # | Çalışma | Ne yapıyor | Varsayımı | Bıraktığı boşluk |
|---|---|---|---|---|
| 1 | Chung vd., 2025 — *Contested logistics: Resilience of strategic highways and railways* (arXiv:2507.18470) | ABD stratejik karayolu/demiryolu ağını GIS + ağ bilimi ile modelliyor, bozulma senaryolarında dayanıklılık ölçüyor | Ağ durumu tam gözleniyor; statik topoloji | Karar katmanı yok; sensör/iletişim kesintisi yok; "hangi ek ölçüm ne kazandırır" sorusu yok |
| 2 | Farina vd., 2024 — *Contested Logistics Games* (GameSec; arXiv:2408.13057) | İki kişilik sıfır toplamlı oyun; Blue rota seçer, Red keser; MILP en-iyi-yanıt + double oracle | Her iki taraf da ağı ve kesme sonuçlarını tam biliyor; talep sentetik (Mariupol–Rostov demiryolu senaryosu) | Kısmi gözlem yok; tespit gecikmesi yok; gerçek veriyle kalibrasyon yok |
| 3 | Strinsky, 2023 — Clemson YL tezi, *Multi-Commodity Flow Models for Logistic Operations within a Contested Environment* | Kontestasyon altında çok-ürünlü akış optimizasyonu | Deterministik kapasite/kesinti | Belirsizlik ve ölçüm kısıtı yok |
| 4 | Cantrell vd., AIAA SciTech 2025 — *Digital Twins for Sustainment-Oriented Wargaming* + NDIA/DRIVE atölyesi (GaTech CLOUDS) | İkmal odaklı harp oyunu için dijital ikiz; sortie üretimine lojistik kısıt etkisi | Model doğruluğu veriyle kalibre değil; senaryo kurgusal | Kalibrasyon ve belirsizlik yayılımı eksik; açık veri yok |
| 5 | Stanford CS224R 2025 projesi — DRL ile Indo-Pasifik 5 üs kaynak dağıtımı | Derin RL ile maliyet ~%20 düşüşü | Ders projesi, hakemli değil; sentetik talep/gecikme | Baseline disiplini ve gerçek veri yok |
| 6 | RAND RRA1722-3 — *Limits of AI for Warfighters: Predictive Maintenance* | Hava kuvvetleri RSP (30 günlük yedek paket) için arıza tahmininin sınırları | Veri kalitesi ve etiket gürültüsü sorunlu | Kontestasyon (tedarikçi kaybı, hat kesintisi) modelde yok |
| 7 | NPS/DAIR tezleri (2025–2026) — ör. US-2 kontestasyon mühendisliği, Class 1 gün-sayısı | Tek platform/tek sınıf ikmal analizi | Tekil vaka, kapalı veri | Genellenebilir çerçeve ve açık tekrar üretilebilirlik yok |
| 8 | arXiv:2509.13600 — ADS-B ile düşük maliyetli GNSS karıştırma izleme; gpsjam.org (CC-BY, günlük H3 harita) | Uçak seyrüsefer doğruluk raporlarından karıştırma haritası | Tespit katmanı; ham veri yayınlanmıyor (18.10.2026 itibarıyla `/data/*.csv` 404) | **Lojistik kararına bağlanmamış**; kendi hattını kurma zorunluluğu |
| 9 | xView3 (SERDP), DarkVesselNet (arXiv:2606.00445), OpenSARShip | SAR + AIS ile karanlık gemi tespiti | Tespit odaklı, ticari/balıkçılık bağlamı | Askerî/insani sevkiyat gecikmesi kestirimi yok |
| 10 | Logistics Cluster Ukrayna üç aylık raporları (2026), OCHA Gazze sitrep'leri, ACLED | Konvoy, tonaj, olay verisi | Betimsel raporlama | Öngörüsel model ve karar desteği yok — bu veri **modele** hiç girmemiş |

### Literatürdeki 5 boşluk (tezin satacağı yer)

1. **Ölçüm kısıtı modelin içinde değil.** GNSS/iletişim/AIS kesintisi "gürültü parametresi" olarak geçiştirilmiş; *kestirilecek bir durum* olarak ele alınmamış. Oysa kontestasyonda asıl problem "ağ nerede kesildi" değil, "**kesildiğini ne kadar gecikmeyle ve hangi güvenle biliyorum**".
2. **Tespit ile karar ayrı gövdeler.** Karıştırma/karanlık gemi tespiti (AI/RS topluluğu) ile sevkiyat planlama (OR/IE topluluğu) birbirini okumuyor. **Kapalı çevrim yok.**
3. **Gerçek veriyle retrospektif doğrulama yok.** Neredeyse tüm modeller sentetik talep + kurgusal senaryo. 2023–2026 arasında üç doğal deney yaşandı (Kızıldeniz, Baltık GNSS, Ukrayna demiryolu/liman vuruşları) ve bu veriler **açık**.
4. **Bilginin değeri (VoI) sorulmamış.** "Bir SAR geçişi, bir İHA keşif sortisi, bir GPS-dışı seyrüsefer terminali ne kadar lojistik performans satın alır?" — bu bir sistem mühendisliği trade study'sidir ve literatürde yok.
5. **Türkiye/Doğu Akdeniz–Karadeniz ekseni açık literatürde yok.** Boğazlar rejimi, Mersin/İskenderun/Trabzon hub rolleri, NATO güney kanadı ikmal koridorları — modellemeye konu olmamış.

---

## 3. Altı tez konusu önerisi

Her öneri aynı şablonla: soru → özgünlük → YZ katmanı → sistem mühendisliği katmanı → veri → değerlendirme → süre/risk → çıktı.

---

### K1 — (ANA ÖNERİ) Sensör-kesintili ortamda kapalı çevrim kontestasyon lojistiği

**Araştırma sorusu:** Bir lojistik ağın durumu GNSS karıştırma, iletişim kesintisi ve gecikmeli/kırpılmış raporlama altında kısmen gözlenirken, *belirsizliği kalibre edilmiş biçimde taşıyan* bir kestirim→karar döngüsü, tam gözlem varsayan baseline'lara göre karar kalitesini ne kadar artırır ve ek ölçümün (SAR geçişi, İHA keşif, alternatif PNT) marjinal değeri nedir?

**Özgünlük:** Boşluk 1 + 2 + 3 + 4'ü aynı çerçevede kapatır. Yöntem olarak da yeni: klasik "dayanıklı optimizasyon" belirsizlik kümesini dışarıdan verir; burada belirsizlik **ölçüm modelinden türetiliyor** ve karar onunla birlikte evriliyor.

**YZ katmanı:**
- Bayesçi durum kestirimi (parçacık filtresi / faktör grafiği) — düğüm-kenar tıkanma durumu, kesinti olayları
- Değişim-noktası tespiti (CUSUM / Bayesçi online changepoint) ile "kesinti başladı" alarmı; gecikme-güven eğrisi
- Gradyan artırmalı sınıflandırıcı ile GNSS bozulma olayı tespiti (ADS-B seyrüsefer doğruluk raporlarından türetilmiş etiketlerle)
- **Conformal prediction** ile kalibre edilmiş aralıklar (dağılım varsayımı olmadan kapsama garantisi)
- Karşılaştırma: dayanıklı optimizasyon (iki aşamalı, CVaR) vs. PPO tabanlı politika — aynı kestirim katmanı üstünde

**Sistem mühendisliği katmanı:**
- SysML/MBSE ile "algıla–kestir–karar ver–uygula" mimarisi, gereksinim izlenebilirliği (ör. "kesinti tespit gecikmesi ≤ 6 saat, %90 kapsama")
- Deney tasarımı (faktöriyel/DoE) ile sensör yoğunluğu × bozulma şiddeti × talep oynaklığı uzayının taranması
- **VoI trade study:** ek ölçüm birim maliyeti başına lojistik performans kazancı → sensör yatırım kararı kuralı
- V&V: simülasyon + gerçek veri yeniden oynatma (replay) ile iki katmanlı doğrulama

**Veri (18.10.2026 itibarıyla erişim test edildi):**
- **OpenSky Network** — canlı state vector sorgusu çalıştı (İstanbul FIR üzerinden veri döndü). ADS-B seyrüsefer doğruluk alanları ile karıştırma göstergesi türetilebilir.
- **IMF PortWatch** — günlük liman/boğaz verisi çalıştı, son kayıt **11.10.2026**.
- **T.C. Ulaştırma Bakanlığı denizcilik istatistikleri** — Boğazlar gemi geçiş XLS'i HTTP 200 (çeyreklik, gemi tipine göre).
- **ACLED** — ücretsiz kayıt, ticari olmayan kullanım, dışa açık materyalde "transformative" şartı.
- **Sentinel-1 SAR** — Copernicus ile ücretsiz; gemide/limanda gözlem.
- **gpsjam.org** — CC-BY günlük H3 harita (ham veri yok → kendi ADS-B hattını kurmak gerekir; bu da tezin bir çıktısı olabilir).
- Retrospektif pencereler: Kızıldeniz 2023-11→2026, Baltık GNSS 2025-01→2026-10, Ukrayna demiryolu/liman vuruşları 2022-2026.

**Değerlendirme (dürüst metrikler):**
- Kestirim: CRPS, kalibrasyon eğrisi, ampirik kapsama oranı (hedef %90 ise ölçülen ne?)
- Karar: tam-gözlem baseline'ına göre **karar pişmanlığı (regret)**, hizmet düzeyi, gecikmeli teslim oranı
- **Önceden ilan edilen başarısızlık ölçütü:** Gerçek bozulma pencerelerinde pişmanlık azalması %15'in altındaysa, "kapalı çevrim kazanç sağlar" iddiası düşer. Bunu tezin başında yazılı ilan etmek, iyimserlik baskısını kırar.

**Süre:** 8 ay (veri hattı 1,5 ay | kestirim 2 ay | karar 2 ay | VoI + yazım 2,5 ay). **Risk:** orta-yüksek (ADS-B'den etiket türetme emek ister; PortWatch 7 gün gecikmeli).
**Çıktı:** JDMS / IEEE Systems Journal / Reliability Engineering & System Safety; SAVTEK + SIU bildirileri; açık kaynak tekrar üretilebilir hat.

---

### K2 — Denizde kontestasyonun görünürlüğü: AIS boşluğu + SAR + GNSS bozulması füzyonu ile sevkiyat gecikmesi kestirimi

**Soru:** AIS boşlukları, SAR tespitleri ve GNSS karıştırma haritası birleştirilerek bir sevkiyatın gecikmesi/riski, geminin kendi raporuna hiç güvenmeden ne doğrulukla önceden kestirilebilir?
**Özgünlük:** Boşluk 2'yi (tespit→karar) deniz tarafında kapatır; "dark vessel" literatürünü ticari/askerî sevkiyat gecikmesine bağlar.
**YZ:** Çok modlu füzyon, zayıf etiketleme (weak supervision), sekans modelleri (TCN/Transformer), anomali tespiti; belirsizlik için derin topluluklar.
**SE:** Veri hattı mimarisi, gecikme/maliyet ödünleşimi, operasyonel kullanılabilirlik gereksinimleri, doğrulama için olay kataloğu.
**Veri:** GFW API (CC BY-NC 4.0, akademik ücretsiz), aisstream.io (ücretsiz anahtar, canlı AIS), Sentinel-1, xView3 (başvuru), PortWatch.
**Değerlendirme:** Bab el-Mandeb 2024–2026 rota değişimlerinde geriye dönük isabet; tespit edilen "karanlık" seferlerin gerçek olaylarla eşleşmesi.
**Süre/risk:** 8 ay; SAR işleme öğrenme eğrisi dik, GFW lisansı ticari kullanıma kapalı.
**Çıktı:** Remote Sensing / Ocean Engineering / IEEE JSTARS.

---

### K3 — Kontestasyon altında insani lojistik koridoru dayanıklılığı (Ukrayna + Gazze)

**Soru:** İnsani koridorlarda konvoy/tonaj verisi ve olay kayıtlarından, koridorun *hangi kesiminde* ve *ne kadar sonra* tıkanacağı öngörülebilir mi; kısmi gözlem altında hangi yeniden yönlendirme politikası teslim oranını en çok artırır?
**Özgünlük:** Askerî literatürün "kapalı veri" duvarına takılmayan, yayına tamamen açık, etik olarak temiz bir kontestasyon çalışması. Logistics Cluster/OCHA verisi bugüne kadar **modele** sokulmamış (boşluk 3 ve 5).
**YZ:** Raporlardan olay çıkarımı (NLP/LLM + insan doğrulaması), eksik veride talep kestirimi, dayanıklı yönlendirme.
**SE:** Karar destek mimarisi; teslim oranı / yardıma erişim süresi / eşitlik metrikleri; senaryo yeniden oynatma protokolü.
**Veri:** Logistics Cluster Ukrayna üç aylık raporları (ör. 2026 Ocak–Mart: 14 konvoy, 142 ton, 20 zor erişilir nokta), OCHA Gazze sitrep'leri (ör. Haziran 2026: Zikim kapanışı, konvoyların Kerem Şalom'a yönlendirilmesi), ACLED, PortWatch (İskenderun/Mersin).
**Süre/risk:** 8 ay; düşük teknik risk, orta veri temizleme yükü; etik kurul ve "insani veri" hassasiyeti.
**Çıktı:** Disasters, Journal of Humanitarian Logistics and Supply Chain Management; savunma dışı dergilerde yayın şansı yüksek.

---

### K4 — Kontestasyon altında mühimmat/yedek parça: kesintili talep tahmini + varlık kaybı senaryolarında dayanıklı stok politikası

**Soru:** Tedarikçi kaybı ve transit kesintisi altında, kesintili (intermittent) talepli kalemler için hangi stok politikası hazırlık (readiness) kaybını en aza indirir?
**Özgünlük:** NPS/RAND hattı kesintili talep tahminini çözmüş; **kontestasyona özgü tedarikçi/hat kaybı** boyutu eklenmemiş.
**YZ:** Kesintili talep için ML karşılaştırması (Croston, LightGBM, N-BEATS), belirsizlik kümesi kestirimi.
**SE:** Hazırlık-tabanlı stok (RSP) tasarımı, çok kademeli ağ, maliyet/hazırlık trade study'si.
**Veri:** ⚠ Büyük ölçüde sentetik; gerçek askerî tüketim verisi açık değil. Havacılık MRO açık verileri kısmi ikame sağlar. **Gerçek veri şartı olan bir tez için en zayıf seçenek.**
**Süre/risk:** 7 ay; veri gerçekliği düşük → "gerçek veri" ilkesiyle çelişir.

---

### K5 — LLM destekli lojistik harekât planı (COA) üretimi: kalibre edilmiş güven ve değerlendirme protokolü

**Soru:** LLM'lerin ürettiği ikmal COA'ları, uzman insan COA'larına göre ne kadar uygulanabilir; model güveni ile gerçek başarı arasındaki kalibrasyon bozukluğu ölçülebilir mi?
**Özgünlük:** Yüksek — ama tezin katkısı "model" değil **değerlendirme protokolü** olmalı (insan vs. makine harp oyunu literatürü, arXiv:2403.03407, bunun önünü açtı).
**YZ:** LLM ajanları, RAG ile doktrin erişimi, kalibrasyon (verbalized confidence vs. gerçek isabet), otomatik hakem (adjudicator) tasarımı.
**SE:** Değerlendirme çerçevesi, ölçüm geçerliliği, tekrarlanabilirlik, insan-otomasyon etkileşimi gereksinimleri.
**Veri:** ⚠ Gerçek lojistik verisi yok; açık harp oyunu transkriptleri ve senaryolar sınırlı → **uydurma riski en yüksek konu**. Ayrıca etik/eskalasyon tartışması zorunlu.
**Süre/risk:** 6 ay; yüksek özgünlük, yüksek "boş tez" riski. Ancak bir yan katkı olarak K1'e eklenebilir ("karar açıklaması" katmanı).

---

### K6 — Boğazlar ve Doğu Akdeniz lojistik koridorunun kontestasyon dayanıklılığı (Türkiye odaklı)

**Soru:** İstanbul/Çanakkale Boğazları ve Mersin–İskenderun–Trabzon hub'ları üzerinden işleyen bir ikmal koridorunda, seyir rejimi kısıtları ve bölgesel kesintiler altında throughput dayanıklılığı nedir; hangi yedeklilik yatırımı en verimli?
**Özgünlük:** Orta (chokepoint literatürü var) ama **Türkiye verisiyle ve Türkiye'nin NATO ikmal rolü bağlamında** yapılmış açık çalışma yok. Yayın ve kurum ilgisi şansı yüksek.
**YZ:** Talep/geçiş anomalisi tespiti, kısa vadeli throughput tahmini, senaryo üretimi.
**SE:** Koridor mimarisi, kapasite/yedeklilik trade study'si, kriz yönetimi gereksinimleri.
**Veri (doğrulandı):** UAB Boğazlar gemi geçiş istatistikleri (çeyreklik XLS, gemi tipi bazında), PortWatch günlük boğaz verisi, ACLED, AIS.
**Süre/risk:** 7 ay; düşük risk, orta özgünlük. K1'in "gerçek vaka" bölümü olarak da kullanılabilir.

---

## 4. Karşılaştırma (1–5)

| Konu | Özgünlük | Veri gerçekliği | YZ derinliği | SE derinliği | 8 ayda bitirme | Yayın/şeffaflık | **Toplam** |
|---|---|---|---|---|---|---|---|
| **K1** Kapalı çevrim, sensör-kesintili | 5 | 4 | 4 | 5 | 3 | 5 | **26** |
| **K2** Deniz görünürlüğü füzyonu | 4 | 5 | 5 | 3 | 4 | 4 | **25** |
| **K3** İnsani koridor | 4 | 4 | 4 | 4 | 4 | 5 | **25** |
| **K6** Boğazlar / Doğu Akdeniz | 3 | 5 | 3 | 4 | 5 | 4 | **24** |
| **K4** Mühimmat/yedek parça | 3 | 2 | 4 | 4 | 4 | 4 | **21** |
| **K5** LLM COA değerlendirmesi | 5 | 2 | 5 | 4 | 2 | 3 | **21** |

Okuma: K1 en yüksek toplam ama en zor; K6 en güvenli; K2 en iyi veri/YZ dengesi. **K1 + K6 birleşimi** (K1 çerçevesi, K6 vaka çalışması) tek tezde savunulabilir ve kapsamı gerçekçi kılar.

---

## 5. K1 için tez iskeleti

**Olası başlıklar**
- TR: *Sensör kesintisi altında kontestasyon lojistiği: kalibre edilmiş belirsizlikle kapalı çevrim sevkiyat planlama ve bilginin değeri*
- EN: *Measurement-Aware Contested Logistics: Closed-Loop Sustainment Planning under GNSS and Communications Denial with Calibrated Uncertainty*

**Araştırma soruları**
1. Kısmi gözlem altında ağ kesinti durumu, kalibre edilmiş bir olasılık dağılımıyla ne doğrulukta kestirilebilir? (kapsama + gecikme)
2. Bu dağılımı karar katmanına taşımak, tam-gözlem baseline'ına göre karar pişmanlığını ne kadar azaltır?
3. Ek ölçümün (SAR geçişi / İHA keşfi / alternatif PNT) marjinal lojistik değeri nedir ve bu değer kesinti şiddetine nasıl bağlıdır?

**Beklenen katkılar**
1. Ölçüm-kısıtlı kontestasyon lojistiği için kapalı çevrim çerçeve (kestirim → karar → VoI) — iki ayrı literatürü birleştirir.
2. 2023–2026 gerçek açık verisiyle yeniden oynatma **benchmark'ı** ve tekrar üretilebilir açık hat (kod + veri lisansları).
3. VoI tabanlı sensör yatırım kuralı — sistem mühendisliği trade study'si olarak savunulabilir çıktı.

**Savunulabilirlik (falsifiability)**
- Kapsama hedefi %90 ilan edilir; ölçülen kapsama %80'in altındaysa kestirim katmanı "kalibre değil" kabul edilir ve yöntem revize edilir.
- Pişmanlık azalması <%15 ise kapalı çevrimin kazancı iddia edilmez; sonuç "negatif bulgu" olarak yayınlanır (bu da değerli).

**YZ ↔ SE eşlemesi**

| Katman | Yöntem/artefakt |
|---|---|
| Algı | ADS-B/AIS/SAR ham verisi, olay etiketleme |
| Kestirim | Parçacık filtresi, online changepoint, conformal prediction |
| Karar | İki aşamalı dayanıklı optimizasyon (CVaR) vs. PPO |
| Doğrulama | Retrospektif replay + 4 haftalık ileri gölge koşu (gecikme kayıtlı) |
| Sistem | SysML mimari, gereksinim izlenebilirliği, DoE, VoI trade study |

---

## 6. Sekiz aylık plan (K1)

| Ay | İş | Kapı (gate) |
|---|---|---|
| 1 | Sistematik tarama (60–80 kaynak), veri lisansları, etik kurul, SysML taslak | Veri hattı POC: PortWatch + OpenSky + UAB XLS tek notebook'ta birleşti |
| 2 | Olay kataloğu (Kızıldeniz, Baltık, Ukrayna), etiketleme protokolü | Etiketli olay seti: ≥150 olay, iki kişi bağımsız kodlama, κ ≥ 0,7 |
| 3 | Kestirim katmanı v1 (parçacık filtresi), kapsama ölçümü | Kalibrasyon eğrisi raporlandı; kapsama ≥ %85 |
| 4 | Changepoint + bozulma tespiti; baseline'lar | Tespit gecikmesi medyanı ≤ 6 saat |
| 5 | Karar katmanı: dayanıklı optimizasyon + RL; replay | Baseline'a karşı pişmanlık ölçüldü |
| 6 | VoI deneyleri (DoE), sensör yatırım eğrisi | VoI eğrisi + duyarlılık analizi |
| 7 | 4 haftalık ileri gölge koşu (günlük açık veri, gecikmeler kayıtlı) | Gölge koşu raporu: tahmin vs. gerçekleşen |
| 8 | Tez yazımı, açık kod paketi, makale taslağı | Savunma + arXiv/GitHub sürümü |

---

## 7. Veri ve lisans durumu (18 Ekim 2026'da test edildi)

| Kaynak | Durum | Lisans/kısıt | Not |
|---|---|---|---|
| IMF PortWatch | ✅ çalışıyor (son kayıt 11.10.2026) | Açık, anahtarsız ArcGIS REST | 2.065 liman + 28 boğaz, günlük |
| OpenSky Network | ✅ canlı sorgu döndü | Ücretsiz, kayıt; akademik kullanım | ADS-B state vector |
| T.C. UAB Boğaz istatistikleri | ✅ XLS HTTP 200 | Kamuya açık | Çeyreklik, gemi tipi bazında |
| ACLED | ✅ erişilebilir | Ücretsiz; **ticari olmayan**, dışa açık kullanımda "transformative" şartı | Olay verisi |
| Global Fishing Watch API | ✅ | CC BY-NC 4.0, günlük/aylık kota | Ticari kullanıma kapalı |
| aisstream.io | ✅ | Ücretsiz API anahtarı, canlı AIS | Gerçek zamanlı hat |
| Sentinel-1/2 | ✅ | Copernicus, ücretsiz | SAR/optik |
| gpsjam.org | ⚠ harita var, **ham veri yok** (`/data/*.csv` 404) | CC-BY (harita) | Kendi ADS-B hattını kurmak gerekir |
| airplanes.live API | ⚠ bugün 403 | Ücretsiz katman, UA/referer kısıtı | OpenSky alternatifi |
| ADS-B Exchange | 💰 ücretli (~aylık 10–30 USD) | Ticari | Gerekmiyor, opsiyonel |
| Marine Cadastre AIS | ✅ | Ücretsiz | Yalnız ABD suları |
| xView3-SAR | ⚠ başvuru gerekiyor | Araştırma amaçlı | Karanlık gemi etiketleri |
| Logistics Cluster / OCHA | ✅ | Açık PDF/CSV | Konvoy, tonaj, kesişim |

**Bütçe:** Tezin tamamı 0–30 USD/ay ile yürütülebilir. Ücretli tek kalem, isteğe bağlı ADS-B Exchange. Planet Labs gibi ticari optik **gerekmez** — Sentinel çözünürlüğü bu ölçek için yeterli.

---

## 8. Riskler ve dürüstlük notları

1. **Sınıflandırma riski.** SSB/ASELSAN/HAVELSAN/STM gibi bir sponsorla yürütülen tezlerde yayın kısıtı gelebilir. Açık veri + açık yöntem hattı, hem yayını hem tekrar üretilebilirliği korur. Sponsor görüşmesinde "yayın hakkı" ilk soru olmalı.
2. **"Gerçek veri" ile "gerçek zamanlı" aynı şey değil.** PortWatch ~7 gün gecikmeli, ACLED olayları geriye dönük revize edilir. Her veri setinin gecikmesi tezde tablo olarak yazılmalı; "gerçek zamanlı" ifadesi kullanılmamalı.
3. **Kendi etiketini kendin üretme tuzağı.** ADS-B'den türetilen "karıştırma var" etiketi, gpsjam'in eşik tanımına bağlıdır. Eşik duyarlılığı raporlanmazsa sonuçlar kırılgan olur.
4. **YÖK tez taraması yapılamadı.** `tez.yok.gov.tr` arama ucu oturum/akış gerektirdiği için bu araştırmada programatik sorgu başarısız oldu (HTTP 200 ama sonuç tablosu dönmedi). Öneri: elle şu anahtar kelimelerle tarayın — "kontestasyon lojistiği", "askerî lojistik optimizasyon", "tedarik zinciri dayanıklılığı yapay zeka", "GNSS bozulması", "AIS karanlık gemi", "insani lojistik optimizasyon", "çok kademeli stok yapay sinir ağı". Aynı tarama İngilizce olarak NPS DAIR, DTIC ve ProQuest'te de yapılmalı.
5. **Kapsam şişmesi.** K1 tek başına üç katman (algı, kestirim, karar) + VoI içeriyor. Gerçekçi kesim: **karar katmanında RL'i ikincil** tutmak, birincil katkıyı kestirim + dayanıklı optimizasyon + VoI üçlüsüne vermek.
6. **Danışman/kurum eşleşmesi doğrulanmalı.** MSÜ Alparslan Savunma Bilimleri Enstitüsü, İTÜ/ODTÜ/Gebze Teknik/TOBB ETÜ endüstri ve sistem mühendisliği programları bu profildeki tezleri kabul ediyor; ancak program bazında "YZ + lojistik" danışmanı olup olmadığı ayrıca teyit edilmeli (bu araştırmada doğrulanmadı).

---

## 9. Bu hafta yapılacak 5 şey

1. **Danışman filtresi:** 3 program belirle; son 3 yılda "lojistik/optimizasyon/YZ" yayını olan 5 hoca listele.
2. **YÖK + NPS DAIR taraması:** yukarıdaki anahtar kelimelerle; çıkan 5 tezin "sonuç/öneriler" bölümünü oku, boşluk cümlelerini not et.
3. **İki günlük fizibilite:** PortWatch + OpenSky + UAB XLS'i tek notebook'ta birleştir; Bab el-Mandeb ve İstanbul Boğazı için 30 günlük zaman serisi çiz. Bu, tez önerisinin "veri var" kanıtı olur.
4. **Bir sayfalık öneri:** K1 için problem–boşluk–soru–yöntem–veri–başarısızlık ölçütü.
5. **Takvim:** SAVTEK, SIU, ASYU ve INCOSE Türkiye bildiri tarihlerini not et; ilk bildiri 6. ayda çıkacak şekilde planla.

---

### Kaynaklar (birincil)

- Chung, Sardak, Kitsak, Jin, Linkov (2025). *Contested logistics: Resilience of strategic highways and railways.* arXiv:2507.18470
- Farina vd. (2024). *Contested Logistics Games.* GameSec 2024. arXiv:2408.13057
- Strinsky (2023). *Multi-Commodity Flow Models for Logistic Operations within a Contested Environment.* Clemson YL tezi
- Cantrell vd. (2025). *Digital Twins for Sustainment-Oriented Wargaming.* AIAA SciTech 2025
- RAND (2024). *Understanding the Limits of AI for Warfighters, Vol. 3: Predictive Maintenance.* RRA1722-3
- DLA (2025). *Contested logistics white paper* ve *Modern Contested Logistics Truths*
- NATO STO (2025). *Science & Technology Trends 2025–2045*
- UK Army War College *War Room* (2025). *HEDGEHOG 2025: Prickly Logistics*
- CSIS (2025). *Lights Out: Wargaming a Chinese Blockade of Taiwan*
- St. Louis Fed (2024). *Global Trade Implications of Red Sea Shipping Disruptions*
- arXiv:2509.13600 — ADS-B tabanlı GNSS karıştırma izleme
- arXiv:2606.00445 — DarkVesselNet; xView3-SAR (NeurIPS 2022 Datasets)
- GPS Solutions (2026) — Baltık GNSS karıştırma/emitter tespiti
- Logistics Cluster Ukrayna üç aylık raporları (2026); OCHA Gazze sitrep'leri (2025–2026)

---

## Ek A — Gerçeklik filtresi (18.10.2026 eki)

Kullanıcı kısıtı netleşti: tez **kesin olarak contested logistics** üzerine olacak, ama **bire bir gerçek dünya karşılığı** ve **tutarlılık** şart. Bu, özgünlükten ayrı bir eksendir: bir konu özgün olabilir, doğrulanacak gerçeği olmayabilir. Ölçüt, bozulma zincirinin beş halkasının da açık veride gözlenebilmesi:

**olay** (fiziksel/siyasi müdahale) → **tespit** (ölçüm) → **ağ durumu** (throughput, stok, gecikme) → **karar** (yeniden yönlendirme/ikmal) → **sonuç** (gerçekleşen gecikme, kayıp, teslim oranı)

| Konu | Olay | Tespit | Ağ durumu | Karar | Sonuç | Zincir |
|---|---|---|---|---|---|---|
| K1 — kapalı çevrim, Karadeniz koridoru | ✓ ACLED/FIRMS/OSM | ✓ ADS-B, SAR | ✓ PortWatch, AIS, UAB | ✓ rota/liman seçimi | ✓ gerçekleşen transit | **TAM** |
| K3 — insani koridor (Ukrayna/Gazze) | ✓ OCHA/ACLED | ~ kısmi | ✓ konvoy/tonaj | ✓ konvoy planı | ✓ teslim kaydı (gecikmeli) | **GÜÇLÜ** |
| K6 — Boğazlar / Doğu Akdeniz koridoru | ~ rejim kısıtı | ✓ UAB, AIS | ✓ çeyreklik geçiş | ✓ | ~ | **GÜÇLÜ** |
| K2 — deniz görünürlüğü (AIS+SAR) | ✓ | ✓ | ✓ | ~ | ✓ | **KISMİ** |
| K4 — mühimmat/yedek parça stok | ✗ | ✗ | ✗ | ✗ | ✗ | **YOK** |
| K5 — LLM COA değerlendirmesi | ✗ | ✗ | ✗ | ~ | ✗ | **YOK** |

**Sonuç:** "Bire bir karşılık" şartı K1'i (Karadeniz odaklı) ve K3'ü öne çıkarır; K4/K5 bu şartla elenir — sentetik oldukları için değil, **doğrulanacak gerçekleri olmadığı** için.

### Gerçeklik sözleşmesi (tezin içine konacak 4 kural)

1. **Her sayı için kaynak + zaman damgası + gecikme + lisans.** Tablo hâlinde, tez ekinde. Gecikmesi bilinmeyen veri "gerçek zamanlı" sayılmaz.
2. **Senaryo etiketi zorunlu.** Her senaryo ya *olay-türevli* (gerçekleşmiş bir olaydan türetilmiş) ya da *sentetik* etiketlenir; iki tür aynı tabloda karışmaz. (Aksi hâlde sentetik varsayım sessizce gerçekmiş gibi okunur.)
3. **Zamanda ileriye bölme.** Eğitim ≤ T, test > T; aynı olay iki tarafta yer alamaz. Olay kimliği (event ID) tek ve değişmez.
4. **Çelişki raporlanır, seçilmez.** İki kaynak aynı olay için farklı tarih/tonaj veriyorsa (ACLED revizyonu tipik), hangisinin esas alındığı ve farkın ne olduğu yazılır.

### Su projesinden aktarım — ne geçer, ne geçmez

LeakDB tarafındaki kazanım gerçek: **sensör kesintisi altında konumlandırma + kalibre edilmiş aday kümesi + dürüst değerlendirme**. Lojistiğe aktarılan tam olarak bu üçlüdür; aktarılmayan hidrolik modeldir.

| LeakDB | Contested logistics | Aktarım |
|---|---|---|
| Düğüm/eğri = boru, kaçak konumu | Düğüm/kenar = liman, hat, boğaz; kesinti konumu | ✓ aynı sınıf problem |
| Basınç/debi ölçümünden kestirim | AIS/PortWatch/ADS-B'den durum kestirimi | ~ gözlem modeli **yeniden türetilmeli** |
| Sensör kesintisi senaryoları | GNSS/iletişim kaybı senaryoları | ✓ doğrudan |
| Aday kümesi + güven aralığı | Kesinti aday kenar kümesi + güven | ✓ |
| Kalibrasyon (kapsama) testi | Aynı test, aynı protokol | ✓ ama **ayrı ayrı raporlanır** |

**Aktarım iddiası test edilir, varsayılmaz:** aynı kalibrasyon protokolü iki veri setinde ayrı ayrı koşulur. Su tarafında %90 hedefe yaklaşıp lojistik tarafında yaklaşmıyorsa, bu bir bulgudur ve yazılır — "aynı yöntem, farklı gözlenebilirlik" tezin en dürüst cümlesi olur.

### Somut öneri sıralaması (gerçeklik filtresi sonrası)

1. **A — Karadeniz koridoru, kapalı çevrim** (K1'in gerçeklik filtresinden geçmiş hâli): Reni/İzmail/Odesa/Constanța + Boğazlar; olaylar ACLED/FIRMS, trafik PortWatch/AIS/UAB, GNSS ADS-B. Zincirin tamamı gözlenir; tez "gerçek olay → model → gerçekleşen sonuç" üçlüsünü gösterebilir. **Önerim bu.**
2. **B — Kızıldeniz rota kayması** (K2'nin gerçeklik hâli): en güçlü veri, en zayıf "askerî karar" tarafı; karar verici ticari aktör.
3. **C — İnsani koridor** (K3): en kolay savunma ve yayın; en düşük savaş-oyunu iddiası.
4. Boğazlar (K6) tek başına tez değil, A'nın vaka bölümü olarak en güçlü hâlinde.

**Ön koşul (2 gün):** A'ya geçmeden önce zincirin veriyle gerçekten kapandığı gösterilmeli — aynı koridorda (i) en az 3 belgelenmiş kesinti olayı, (ii) olay öncesi/sonrası 30 günlük kesintisiz throughput serisi, (iii) olay günlerinde gözlenebilir GNSS/ADS-B bozulması. Üçü de yoksa konu A değil, B veya C'ye inilir.

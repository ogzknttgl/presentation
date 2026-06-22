# News HTML Generator

Bu proje, resmi haber brifingi formatındaki `.docx` dosyalarını kapalı ağda çalışabilecek modern bir HTML arayüzüne dönüştürür.

## Beklenen içerik düzeni

Her haber bloğu şu akışla okunur:

1. `Sayın Başkanım,` gibi hitap satırı
2. Haber metni
3. Kaynak bağlantısı
4. `Arz ederim.` gibi kapanış satırı

Aynı dokümanda birden fazla haber bloğu bulunabilir.

Generator, hitap ve kapanış satırlarını veri sınırı olarak kullanır; fakat HTML çıktısında bu satırları göstermez.

## Kapalı Ağ Tasarımı

- Tüm stil ve davranış tek HTML dosyasına gömülür.
- Harici font, CDN, JavaScript paketi veya ağ isteği kullanılmaz.
- Arayüzde yerel arama filtresi ve `Yazdir veya PDF Al` düğmesi bulunur.
- Birlesik bulten modunda sol tarafta kurum ve anahtar kelime filtreleri bulunur.
- HTML, internet erişimi olmadan doğrudan açılabilir.

## Akilli Zenginlestirme Katmani

- Haber metni anahtar kelimelere gore otomatik etiketlenir.
- Her kart icin tema adi, onem skoru ve mini bar infografikleri uretilir.
- Ilk cumlelerden `One Cikanlar` ozeti cikarilir.
- Bu sistem tamamen kural tabanlidir; ag erisimi veya harici model gerektirmez.

## Kullanım

Tek bir `.docx` dosyasini HTML'e cevirmek icin:

```bash
python3 -m src.news_html_generator input.docx output.html --title "Yapay Zeka Gündemi"
```

Bir klasordeki tum `.docx` dosyalarini tek bir birlesik HTML bultene cevirmek icin:

```bash
python3 -m src.news_html_generator ./input-docx-folder ./combined-output.html --title "Birlesik Teknoloji Gundemi"
```

Bu modda:

- tum haberler tek sayfada birlestirilir
- sol panelden kurum bazli filtreleme yapilabilir
- anahtar kelime ve genel search ayni sayfada birlikte calisir

Bir klasordeki tum `.docx` dosyalarindan intranet paketi uretmek icin:

```bash
python3 -m src.news_html_generator ./input-docx-folder ./intranet-site-output --site-title "Intranet Haber Merkezi"
```

Bu modda su dosyalar olusur:

- `index.html`: tum bultenleri listeleyen giris sayfasi
- `manifest.json`: parse stratejileri, uyarilar ve ozet metadata
- her `.docx` icin ayri `.html` bulten dosyasi

## Test

```bash
python3 -m unittest tests/test_generator.py -v
```

## Agent ile Kod Yazmadan Kullanim

Bu projeyi bir "ust akil agent" arkasina koyabilirsiniz. Agent'in gorevi kod yazmak degil, kullanicidan gelen `.docx` dosyalarini dogru klasore almak, generator komutunu calistirmak, HTML ciktisini kontrol etmek ve intranet yayin klasorune koymaktir.

### Onerilen klasor yapisi

```text
news-html-generator-project/
  inbox-docx/              # kullanicinin veya agent'in yeni DOCX dosyalarini koydugu klasor
  published-html/          # tek HTML ciktilari
  published-intranet/      # index.html + manifest.json + ayri bulten HTML paketleri
```

`inbox-docx/`, `published-html/` ve `published-intranet/` klasorleri yoksa agent olusturabilir.

### Agent'a verilecek ana talimat

Agent'a su gorev tanimi verilebilir:

```text
Sen bu projenin operasyon agent'isin. Kullanicidan DOCX dosyalari veya DOCX klasoru aldiginda kod degistirme. Dosyalari inbox-docx klasorune koy, sonra asagidaki komutlardan uygun olani calistir.

Tek HTML istenirse:
python3 -m src.news_html_generator ./inbox-docx ./published-html/newsroom.html --title "Haftalik Haber Portali"

Intranet paketi istenirse:
python3 -m src.news_html_generator ./inbox-docx ./published-intranet --site-title "Intranet Haber Merkezi"

Komut tamamlandiktan sonra sunlari kontrol et:
- HTML dosyasi olustu mu?
- Icerikte haber kartlari gorunuyor mu?
- Sol filtre panelinde kurum, tema, bolge, kategori ve kaynak kirilimlari var mi?
- Arama ve filtreleme icin inline JavaScript HTML icine gomulu mu?
- Dis CDN, font veya harici JavaScript baglantisi yok mu?

Sorun yoksa kullaniciya ciktinin yolunu bildir. Kod degistirme gerekiyorsa once sorunu acikla, sonra testleri calistir:
python3 -m unittest tests/test_generator.py -v
```

### Agent entegrasyon secenekleri

1. **Codex / ChatGPT agent ile manuel operasyon**

   Kullanicilar DOCX dosyalarini agent'a verir. Agent dosyalari `inbox-docx/` altina koyar, generator komutunu calistirir ve uretilen HTML yolunu bildirir. Bu en hizli entegrasyondur.

2. **Intranet portal arkasinda basit is akisi**

   Bir intranet formu DOCX dosyalarini sunucuda `inbox-docx/` klasorune kaydeder. Agent veya bir job su komutu calistirir:

   ```bash
   python3 -m src.news_html_generator ./inbox-docx ./published-intranet --site-title "Intranet Haber Merkezi"
   ```

   Web sunucusu `published-intranet/index.html` dosyasini yayinlar.

3. **Planli veya tetiklemeli calisma**

   Dosya klasore dustugunde ya da belirli saatlerde agent su akisi calistirir:

   ```bash
   python3 -m src.news_html_generator ./inbox-docx ./published-html/newsroom.html --title "Haftalik Haber Portali"
   python3 -m unittest tests/test_generator.py -v
   ```

   Test zorunlu degildir, fakat kod degisikligi yapildigi her durumda calistirilmalidir.

### Agent'in karar kurallari

- Kullanici tek sayfa isterse cikti `.html` dosyasi olmalidir.
- Kullanici intranet paketi isterse cikti klasor olmalidir; bu durumda `index.html`, `manifest.json` ve her DOCX icin ayri HTML olusur.
- Agent DOCX icerigini elle duzeltmemelidir.
- Agent harici API veya internet gerektiren bir islem eklememelidir.
- Agent uretilen HTML'i intranet uyumlu kabul etmeden once dis varlik baglantisi olmadigini kontrol etmelidir.
- Agent kod degisikligi yaparsa mutlaka `python3 -m unittest tests/test_generator.py -v` calistirmalidir.

### Beklenen kullanici deneyimi

Kullanici sadece sunu soyler:

```text
Bu haftanin DOCX dosyalarindan intranet haber portali uret.
```

Agent su isi yapar:

1. DOCX dosyalarini `inbox-docx/` altina koyar.
2. Intranet veya tek HTML komutunu calistirir.
3. Ciktinin olustugunu dogrular.
4. Kullaniciya HTML veya intranet klasoru yolunu bildirir.

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

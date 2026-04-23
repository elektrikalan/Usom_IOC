
USOM IOC Downloader

Açıklama :

Bu script, USOM API'si üzerinden kullanıcı tarafından belirlenen
tarih aralığındaki IOC (Indicator of Compromise) verilerini çeker.

Çekilen veriler:

- Zararlı Domain adresleri
- Zararlı IP adresleri

Tarih Aralığı:
Kullanıcıdan alınan;

- Gün
- Ay
- Yıl

bilgilerine göre geriye dönük sorgulama yapar.
Varsayılan olarak:

- 6 Ay
- 0 Yıl
- 0 Gün

olarak çalışır.

Özellikler:

✔ Otomatik sayfalama

✔ Duplicate temizleme

✔ Domain normalize etme (lowercase)

✔ IP adreslerini sıralı kaydetme

✔ TXT çıktı üretme

✔ Timeout / exception handling

✔ Kullanıcı tanımlı tarih aralığı desteği


Requirements:

pip install requests python-dateutil

Kullanım:

python usom_ioc_downloader.py

Çıktı:

- domainlist.txt
- iplist.txt


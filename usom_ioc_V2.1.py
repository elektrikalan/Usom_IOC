"""
===========================================================
USOM IOC Downloader (Domain + IP)
===========================================================

Author      : Ahmet Genç
Created     : 23.04.2026
Updated     : 28.04.2026
Version     : 2.1

Description :
Bu script, USOM API'si üzerinden kullanıcı tarafından belirlenen tarih aralığındaki IOC (Indicator of Compromise) verilerini çeker. 
Oluşturulan dosyalar domainlist.txt ve iplist.txt olarak kaydedilir.
Dosyaya ekleme yapmaz, var olan dosyayı günceller.

Çekilen veriler:
- Zararlı Domain adresleri
- Zararlı IP adresleri

Tarih Aralığı:
- Dakika
- Saat
- Gün
- Ay
- Yıl 

bilgilerine göre geriye dönük sorgulama yapar.

Özellikler:
✔ Otomatik sayfalama (pageCount kontrolü ile)
✔ Duplicate temizleme
✔ Domain normalize etme (lowercase)
✔ IP adreslerini sıralı kaydetme
✔ TXT çıktı üretme
✔ Timeout / exception handling
✔ Kullanıcı tanımlı tarih aralığı desteği (dakika, saat, gün, ay, yıl)
✔ UTC zaman dilimi desteği (API UTC ile çalışır, ekrana TR saati gösterilir)

Outputs:
- domainlist.txt
- iplist.txt

Requirements:
pip install requests python-dateutil ipaddress datetime

Usage:
python usom_ioc_V1.2.py

Changelog (V1.2):
- Saat ve dakika bazında sorgulama desteği eklendi
- UTC zaman dilimi uyumu sağlandı (API UTC kullanıyor)
- Ekranda hem TR saati hem UTC sorgu bilgisi gösteriliyor
- Sayfalama pageCount ile kontrol ediliyor (sonsuz döngü düzeltildi)
- Timeout süresi 10s → 30s olarak artırıldı

===========================================================
"""


import requests
import ipaddress
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta

    ####SABITLER####
# Tarih aralığı
bugun = datetime.now(timezone.utc)  # API UTC zaman dilimi kullanıyor

zaman_geri = bugun - relativedelta(
    years=0,
    months=0,
    days=1,
    hours=0,
    minutes=0
)

bugun_str = bugun.strftime("%Y-%m-%d %H:%M:%S")
zaman_geri_str = zaman_geri.strftime("%Y-%m-%d %H:%M:%S")

# Gösterimde yerel saat (UTC+3) bilgisi de verilsin
utc_offset = timedelta(hours=3)
yerel_bugun = bugun + utc_offset
yerel_geri  = zaman_geri + utc_offset

print(f"Şu anki zaman (TR): {yerel_bugun.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Geri tarih    (TR): {yerel_geri.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"[API sorgusu UTC ]: {zaman_geri_str} → {bugun_str}")

toplam_kayit = 0

    ####FONKSİYONLAR####    

def ioc(ioc_type):
    """
    ioc_type: 'domain' veya 'ip'
    API sayfa başına 20 kayıt döndürür.
    pageCount bilgisi ile toplam sayfa sayısı kontrol edilir.
    """
    page = 1
    unique_data = set()
    total_pages = None

    while True:
        url = (
            f"https://www.usom.gov.tr/api/address/index"
            f"?type={ioc_type}"
            f"&date_gte={zaman_geri_str}"
            f"&date_lte={bugun_str}"
            f"&page={page}"
        )

        try:
            response = requests.get(url, timeout=30)

            if response.status_code != 200:
                print(f"[{ioc_type}] Hata: {response.status_code}")
                break

            data = response.json()
            models = data.get("models", [])

            # İlk sayfada toplam sayfa sayısını al
            if total_pages is None:
                total_pages = data.get("pageCount", 0)
                total_count = data.get("totalCount", 0)
                print(f"[{ioc_type}] Toplam {total_count} kayıt, {total_pages} sayfa bulundu.")

            if not models:
                break

            for item in models:
                value = item.get("url")
                if value:
                    if ioc_type == "domain":
                        unique_data.add(value.strip().lower())
                    else:
                        unique_data.add(value.strip())

            print(f"[{ioc_type}] Sayfa {page}/{total_pages} → {len(models)} kayıt")

            # Son sayfaya ulaştıysak dur
            if page >= total_pages:
                break

            page += 1

        except requests.exceptions.RequestException as e:
            print(f"[{ioc_type}] Exception: {e}")
            break

    return unique_data


def dosya_kaydet(filename, data, is_ip=False):
    with open(filename, "w", encoding="utf-8") as f:
        if is_ip:
            sorted_data = sorted(data, key=ipaddress.ip_address)
        else:
            sorted_data = sorted(data)

        for item in sorted_data:
            f.write(item + "\n")


def main():
    print("Domain IOC çekiliyor...")
    domains = ioc("domain")

    print("\nIP IOC çekiliyor...")
    ips = ioc("ip")

    print("\nDosyalar yazılıyor...")

    dosya_kaydet("domainlist.txt", domains)
    dosya_kaydet("iplist.txt", ips, is_ip=True)

    print("\nTamamlandı.")
    print(f"Toplam Domain: {len(domains)}")
    print(f"Toplam IP: {len(ips)}")


if __name__ == "__main__":
    main()

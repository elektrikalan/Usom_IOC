"""
===========================================================
USOM IOC Downloader (Domain + IP)
===========================================================

Author      : Ahmet Genç
Created     : 23.04.2026
Version     : 1.0

Description :
Bu script, USOM API'si üzerinden son 6 aya ait IOC verilerini çeker.

Çekilen veriler:
- Zararlı Domain adresleri
- Zararlı IP adresleri

Özellikler:
✔ Otomatik sayfalama
✔ Duplicate temizleme
✔ TXT çıktı
✔ Timeout / exception handling

Outputs:
- domainlist.txt
- iplist.txt

===========================================================
"""


import requests
import ipaddress
from datetime import date
from dateutil.relativedelta import relativedelta

    ####SABITLER####
# Tarih aralığı
bugun = date.today()
alti_ay_once = bugun - relativedelta(months=1)

toplam_kayit = 0

    ####FONKSİYONLAR####    

def ioc(ioc_type):
    """
    ioc_type: 'domain' veya 'ip'
    """
    page = 1
    unique_data = set()

    while True:
        url = (
            f"https://www.usom.gov.tr/api/address/index"
            f"?type={ioc_type}"
            f"&date_gte={alti_ay_once}"
            f"&date_lte={bugun}"
            f"&page={page}"
        )

        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                print(f"[{ioc_type}] Hata: {response.status_code}")
                break

            data = response.json()
            models = data.get("models", [])

            if not models:
                print(f"[{ioc_type}] Tüm sayfalar çekildi.")
                break

            for item in models:
                value = item.get("url")
                if value:
                    if ioc_type == "domain":
                        unique_data.add(value.strip().lower())
                    else:
                        unique_data.add(value.strip())

            print(f"[{ioc_type}] Sayfa {page} → {len(models)} kayıt")

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
import requests
from datetime import date
from dateutil.relativedelta import relativedelta

# Tarih aralığı
bugun = date.today()
alti_ay_once = bugun - relativedelta(months=6)

page = 1
toplam_kayit = 0

with open("domainlist.txt", "w", encoding="utf-8") as dosya:
    while True:
        url = (
            f"https://www.usom.gov.tr/api/address/index"
            f"?type=ip"
            f"&date_gte={alti_ay_once}"
            f"&date_lte={bugun}"
            f"&page={page}"
        )

        print(f"{page}. sayfa çekiliyor...")

        response = requests.get(url)

        if response.status_code != 200:
            print(f"Hata oluştu! Status Code: {response.status_code}")
            break

        data = response.json()

        models = data.get("models", [])

        # Veri bittiyse çık
        if not models:
            print("Tüm sayfalar çekildi.")
            break

        for item in models:
            domain = item.get("url")
            if domain:
                dosya.write(domain + "\n")
                toplam_kayit += 1

        print(f"{page}. sayfadan {len(models)} kayıt alındı.")

        page += 1

print(f"\nToplam çekilen kayıt: {toplam_kayit}")
print(f"Tarih aralığı: {alti_ay_once} - {bugun}")
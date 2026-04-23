import requests
from datetime import date
import ipaddress
from dateutil.relativedelta import relativedelta

# Tarih aralığı
bugun = date.today()
alti_ay_once = bugun - relativedelta(months=6)

page = 1
unique_ips = set()

while True:
    url = (
        f"https://www.usom.gov.tr/api/address/index"
        f"?type=ip"
        f"&date_gte={alti_ay_once}"
        f"&date_lte={bugun}"
        f"&page={page}"
    )

    #print(f"{page}. sayfa çekiliyor...")
    try:

        response = requests.get(url,timeout=100)

        if response.status_code != 200:
            #print(f"Hata oluştu! Status Code: {response.status_code}")
            break

        data = response.json()
        models = data.get("models", [])

        # Veri bittiyse çık
        if not models:
            #print("Tüm sayfalar çekildi.")
            break

        for item in models:
            ip = item.get("url")
            if ip:
                unique_ips.add(ip.strip())

        #print(f"{page}. sayfadan {len(models)} kayıt alındı.")
        #print(f"Şu anki unique kayıt sayısı: {len(unique_ips)}")

        page += 1
    except requests.exceptions.RequestException as e:
        #print(f"Hata oluştu: {e}")
        break

# Dosyaya yaz
with open("iplist.txt", "w", encoding="utf-8") as dosya:
    for ip in sorted(unique_ips, key=ipaddress.ip_address):
        dosya.write(ip + "\n")

#print(f"\nToplam unique ip sayısı: {len(unique_ips)}")
#print(f"Tarih aralığı: {alti_ay_once} - {bugun}")
#print("Liste iplist.txt dosyasına kaydedildi.")
import requests
from datetime import date
from dateutil.relativedelta import relativedelta

# Tarih aralığı
bugun = date.today()
alti_ay_once = bugun - relativedelta(months=6)

page = 1
unique_domains = set()

while True:
    url = (
        f"https://www.usom.gov.tr/api/address/index"
        f"?type=domain"
        f"&date_gte={alti_ay_once}"
        f"&date_lte={bugun}"
        f"&page={page}"
    )

    #print(f"{page}. sayfa çekiliyor...")

    response = requests.get(url)

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
        domain = item.get("url")
        if domain:
            unique_domains.add(domain.strip().lower())

    #print(f"{page}. sayfadan {len(models)} kayıt alındı.")
    #print(f"Şu anki unique kayıt sayısı: {len(unique_domains)}")

    page += 1

# Dosyaya yaz
with open("domainlist.txt", "w", encoding="utf-8") as dosya:
    for domain in sorted(unique_domains):
        dosya.write(domain + "\n")

#print(f"\nToplam unique domain sayısı: {len(unique_domains)}")
#print(f"Tarih aralığı: {alti_ay_once} - {bugun}")
#print("Liste domainlist.txt dosyasına kaydedildi.")
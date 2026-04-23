import requests
import json
from datetime import date
from dateutil.relativedelta import relativedelta

kacgungeri = input("Kaç gün geriye gidilsin: ")
kackaygeri = input("Kaç ay geriye gidilsin: ")
kacyilgeri = input("Kaç yıl geriye gidilsin: ")
istenensayfasayisi = input("Kaç sayfa çekilsin: ")

bugun = date.today()

gerigidilentarih = bugun - relativedelta(
    days=int(kacgungeri),
    months=int(kackaygeri),
    years=int(kacyilgeri)
)

with open("domainlist.txt", "w", encoding="utf-8") as dosya:
    for page in range(1, int(istenensayfasayisi) + 1):
        url = f"https://www.usom.gov.tr/api/address/index?type=domain&date_gte={gerigidilentarih}&date_lte={bugun}&page={page}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            for i in data.get("models", []):
                dosya.write(i["url"] + "\n")

            print(f"{page}. sayfa çekildi.")
        else:
            print(f"Hata oluştu: {response.status_code}")
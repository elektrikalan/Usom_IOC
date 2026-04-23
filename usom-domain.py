from datetime import timedelta
from os import write
import requests
import json 
import time
import sys
import os
from os import listdir
from os.path import isfile, join
from datetime import date, datetime




kacgungeri = input("Kaç gün geriye gidilsin: ")
kackaygeri = input("Kaç ay geriye gidilsin: ")
kacyilgeri = input("Kaç yıl geriye gidilsin: ")
bugun = date.today()


from dateutil.relativedelta import relativedelta

gerigidilentarih = bugun - relativedelta(
    days=int(kacgungeri),
    months=int(kackaygeri),
    years=int(kacyilgeri)
)

#gerigidilentarih = bugun - timedelta(days=int(kacgungeri), months=int(kackaygeri), years=int(kacyilgeri))
istenensayfasayisi = input("Kaç sayfa çekilsin: ")


url = f"https://www.usom.gov.tr/api/address/index?type=domain&date_gte={gerigidilentarih}&date_lte={bugun}&page={istenensayfasayisi}"

payload = {}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)
data = json.loads(response.text)
dosya = open("domainlist.txt" ,"a")
for i in data["models"]:
    dosya.write(i["url"] + "\n")
dosya.close()
print(bugun)
print(gerigidilentarih)
print(istenensayfasayisi)
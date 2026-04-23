"""
===========================================================
USOM IOC Downloader
===========================================================

Author      : Ahmet Genç
Role        : Cyber Security Researcher / Analyst
Created     : 23.04.2026
Version     : 1.0

Description :
Bu script, USOM API'si üzerinden son 6 aya ait IOC verilerini çeker. Zaman bilgisini değiştirmek isterseniz ilgili zaman aralıklarını girebilirsiniz.

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

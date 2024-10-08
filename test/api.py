import requests
import json 

#https://www.mirkvartir.ru/estateoffercard/getphone/?id=312591258&key=OvEfYB5qmXXgoqWADWDaoiNr4MTtRhxPgufzbaXlUM1JonKq+asPHcmrhqAFnILN

r = requests.get('https://www.mirkvartir.ru/estateoffercard/getphone/?id=312591258&key=OvEfYB5qmXXgoqWADWDaoiNr4MTtRhxPgufzbaXlUM1JonKq+asPHcmrhqAFnILN', headers={
    "Host": "www.mirkvartir.ru",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cookie": "activeMain=ekaterinburg",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
})
raw = r.json()
print(raw["contactCardViewModel"]["fixedDescriptionBottomLine"])
print(raw["contactCardViewModel"]["phones"][0])
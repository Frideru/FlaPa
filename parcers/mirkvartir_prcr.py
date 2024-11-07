import requests
from   bs4 import BeautifulSoup
import csv
import re

# main_link = "https://www.mirkvartir.ru/312591258/"
# main_link = "https://www.mirkvartir.ru/313375186/"
# main_link = "https://www.mirkvartir.ru/313375187/"
# main_link = "https://www.mirkvartir.ru/312591257/"
# main_link = "https://www.mirkvartir.ru/313375157/"
# main_link = "https://www.mirkvartir.ru/313345157/"
# main_link = "https://www.mirkvartir.ru/313345151/"
# main_link = "https://www.mirkvartir.ru/312345151/"
main_link = input("enter mirkvartir link ex.(https://www.mirkvartir.ru/313375186/)\n--> ")

flat_number = re.findall(r'\d*\d', main_link)[0]
api_link = f'https://www.mirkvartir.ru/estateoffercard/getphone/?id={flat_number}&key=OvEfYB5qmXXgoqWADWDaoiNr4MTtRhxPgufzbaXlUM1JonKq+asPHcmrhqAFnILN'

header = {
    "Host":            "www.mirkvartir.ru",
    "User-Agent":      "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection":      "keep-alive",
    "Cookie":          "activeMain=ekaterinburg",
    "Sec-Fetch-Dest":  "document",
    "Sec-Fetch-Mode":  "navigate",
    "Sec-Fetch-Site":  "cross-site",
}

r_site = requests.get(main_link, headers=header)
r_api  = requests.get(api_link, headers=header)

raw  = r_api.json()
soup = BeautifulSoup (r_site.text, 'html.parser')
iff  = soup.find_all("div", class_="sc-kjwnom dOPiKV")

if(len(re.findall(r'ул.\s\w*\,\s\d*.\d*|\w*\sул.\,\s\d*.\d*|ул.\s\w*\s\(\w*\.\s\w*\)\,\s\d*.\d*|ул.\s\w*\s\w*\s\w*\,\s\d*.\d*', raw["contactCardViewModel"]["fixedDescriptionBottomLine"])) == 0):
    addr_S  = raw["contactCardViewModel"]["fixedDescriptionBottomLine"]
    addr_FN = "undefind"
else:
    addr_F  = re.findall(r'ул.\s\w*\,\s\d*.\d*|\w*\sул.\,\s\d*.\d*|ул.\s\w*\s\(\w*\.\s\w*\)\,\s\d*.\d*|ул.\s\w*\s\w*\s\w*\,\s\d*.\d*', raw["contactCardViewModel"]["fixedDescriptionBottomLine"])[0]
    addr_S  = re.findall(r'\w{3,}\s\(.\.\s\w{3,}\)|^\w{3,}|[a-zA-Zа-я-А-Я]{3,}|\w{2,}\s\w{4,}\s\w{4,}', addr_F)[0]
    addr_FN = re.findall(r'\d*.\d*$', addr_F)[0].strip()

full_info_json = {
    "rooms":               iff[0].get_text(),
    "full_space":          iff[1].get_text(),
    "kitchen_space":       iff[2].get_text(),
    "flat_height":         re.findall(r'\d*\d', iff[3].get_text())[0],
    "flats":               re.findall(r'\d*\d', iff[3].get_text())[1],
    "price":               iff[4].get_text(),
    "address_street":      addr_S,
    "address_flat_number": addr_FN,
    "phone":               raw["contactCardViewModel"]["phones"][0],
    "link":                'https://www.mirkvartir.ru/312591258/'
}

with open('flat_club.csv', 'a', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # spamwriter.writerow(
    #     ['Улица']     + 
    #     ['№ Дома']    + 
    #     ['Год']       + 
    #     ['Ссылка']    + 
    #     ['Этаж']      + 
    #     ['Этажей']    + 
    #     ['Общая']     + 
    #     ['Кухня']     + 
    #     ['Комната']   + 
    #     ['Потолок']   + 
    #     ['Ремонт']    + 
    #     ['Стоимость'] + 
    #     ['Телефон']   + 
    #     ['Имя']
    # )
    spamwriter.writerow(
        [full_info_json['address_street']]      + 
        [full_info_json['address_flat_number']] + 
        ["0"]                                   + 
        [full_info_json['link']]                + 
        [full_info_json['flat_height']]         + 
        [full_info_json['flats']]               + 
        [full_info_json['full_space']]          + 
        [full_info_json['kitchen_space']]       + 
        ["0"]                                   + 
        ["0"]                                   + 
        ["0"]                                   + 
        [full_info_json['price']]               + 
        [full_info_json['phone']]               + 
        ["0"]
    )

print("OK!")

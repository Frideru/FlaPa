import requests
from   bs4 import BeautifulSoup
import csv
import re
import json

#main_link = 'https://www.mirkvartir.ru/319529218/' #Комнаты
#main_link = 'https://www.mirkvartir.ru/316178961/' #Комната
#main_link = 'https://www.mirkvartir.ru/329549152/' #Много параметров
#main_link = 'https://www.mirkvartir.ru/332092973/'
main_link = 'https://www.mirkvartir.ru/333880056/'

def MirKvartir(link):
    flat_number = re.findall(r'\d*\d', link)[0]
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

    r_site = requests.get(link, headers=header)
    r_api  = requests.get(api_link, headers=header)

    api  = r_api.json()
    soup = BeautifulSoup (r_site.text, 'html.parser')

    info_blocks = soup.find_all("div", class_="sc-jqbzwb juivVv")
    block_value = soup.find_all("div", class_="sc-kjwnom dOPiKV")
    block_descr = soup.find_all("div", class_="sc-sxcbzv bZiYbk")

    find_rooms  = soup.find_all("div", class_="noabbr sc-sxcbzv bZiYbk")
    find_params = soup.find_all("div", class_="sc-sxcbzv bZiYbk")
    find_price  = soup.find_all("div", class_="price m-all")

# ------------
# --- Цена ---
# ------------
    price = find_price[0].get_text().strip().replace(r'руб.', '').replace('\u2009', '')

# ----------------------------
# --- Номер телефона и имя ---
# ----------------------------
    phone = api["contactCardViewModel"]["phones"][0]
    name  = api["contactCardViewModel"]["rawCompanyName"] if 'rawCompanyName' in api["contactCardViewModel"] else api["contactCardViewModel"]["contactName"]

# -------------------------------
# --- Комнаты, Площади, Этажи ---
# -------------------------------
    rooms         = block_value[0].get_text()
    full_space    = "undefined"
    kitchen_space = "undefined"
    floor         = "undefined"
    floors        = "undefined"
    build_age     = "undefined"
    count         = 1

    for desc in block_descr:
        if len(re.findall(r'общая площадь', desc.get_text().lower())) != 0:
            full_space = block_value[count].get_text()
        elif len(re.findall(r'площадь кухни', desc.get_text().lower())) != 0:
            kitchen_space = block_value[count].get_text()
        elif len(re.findall(r'этаж', desc.get_text().lower())) != 0:
            fl     = re.findall(r'(^\d{1,})|(\d{1,}$)', block_value[count].get_text())
            floor  = fl[0][0]
            floors = fl[1][1]
        elif len(re.findall(r'год постройки', desc.get_text().lower())) != 0:
            build_age = block_value[count].get_text()
        count = count + 1

# --------------------------------------
# --- Адрес (Номер и название улицы) ---
# --------------------------------------
    if(len(re.findall(r'ул.\s\w*\,\s\d*.\d*|\w*\sул.\,\s\d*.\d*|ул.\s\w*\s\(\w*\.\s\w*\)\,\s\d*.\d*|ул.\s\w*\s\w*\s\w*\,\s\d*.\d*', api["contactCardViewModel"]["fixedDescriptionBottomLine"])) == 0):
        street_name  = api["contactCardViewModel"]["fixedDescriptionBottomLine"]
        house_number = "undefined"
    else:
        parsed_address  = re.findall(r'ул.\s\w*\,\s\d*.\d*|\w*\sул.\,\s\d*.\d*|ул.\s\w*\s\(\w*\.\s\w*\)\,\s\d*.\d*|ул.\s\w*\s\w*\s\w*\,\s\d*.\d*', api["contactCardViewModel"]["fixedDescriptionBottomLine"])[0]
        street_name  = re.findall(r'\w{3,}\s\(.\.\s\w{3,}\)|^\w{3,}|[a-zA-Zа-я-А-Я]{3,}|\w{2,}\s\w{4,}\s\w{4,}', parsed_address)[0]
        house_number = re.findall(r'\d*.\d*$', parsed_address)[0].strip()

# -----------------
# --- Результат ---
# -----------------
    full_info_json = {
        "rooms"         : rooms,
        "full_space"    : full_space,
        "build_age"     : build_age,
        "kitchen_space" : kitchen_space,
        "floors"        : floors, 
        "floor"         : floor,  
        "price"         : price, 
        "street_name"   : street_name,
        "house_number"  : house_number,
        "phone"         : phone,
        "link"          : link,
        "name"          : name
    }

    with open('./data.csv', 'a', newline='') as csvfile:
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
            [full_info_json['street_name']]   + 
            [full_info_json['house_number']]  +
            [full_info_json['build_age']]     +
            [full_info_json['link']]          + 
            [full_info_json['floors']]        + 
            [full_info_json['floor']]         + 
            [full_info_json['full_space']]    + 
            [full_info_json['kitchen_space']] + 
            ["0"]                             + 
            ["0"]                             + 
            ["0"]                             + 
            [full_info_json['price']]         + 
            [full_info_json['phone']]         + 
            [full_info_json['name']]
        )
    print("OK!")
    return "OK!"

# MirKvartir(main_link)

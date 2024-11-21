import requests
from   bs4 import BeautifulSoup
import csv
import re
import json

# main_link = "https://www.mirkvartir.ru/312591258/"
# main_link = "https://www.mirkvartir.ru/313375186/"
# main_link = "https://www.mirkvartir.ru/313375187/"
# main_link = "https://www.mirkvartir.ru/312591257/"
# main_link = "https://www.mirkvartir.ru/313375157/"
# main_link = "https://www.mirkvartir.ru/313345157/"
# main_link = "https://www.mirkvartir.ru/313345151/"
# main_link = "https://www.mirkvartir.ru/312345151/"
# main_link = input("enter mirkvartir link ex.(https://www.mirkvartir.ru/313375186/)\n--> ")

#main_link = 'https://www.mirkvartir.ru/319529218/' #Комнаты
main_link = 'https://www.mirkvartir.ru/316178961/' #Комната
#main_link = 'https://www.mirkvartir.ru/329549152/' #Много параметров


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

api  = r_api.json()
soup = BeautifulSoup (r_site.text, 'html.parser')
iff  = soup.find_all("div", class_="sc-kjwnom dOPiKV")
desc = soup.find_all("div", class_="sc-jqbzwb juivVv")

find_rooms  = soup.find_all("div", class_="noabbr sc-sxcbzv bZiYbk")
find_params = soup.find_all("div", class_="sc-sxcbzv bZiYbk")
find_price  = soup.find_all("div", class_="price m-all")

price = find_price[0].get_text().strip().replace(r'руб.', '')
phone = api["contactCardViewModel"]["phones"][0]

print("=== IFF ===")
for i in iff:
    print(i.get_text())
print("=== DESC ===")
for i in desc:
    print(i.get_text())

array = [1,2,3,4,5]

rooms         = 1
full_space    = 1
kitchen_space = 1
floor         = 1
floors        = 1

for i in 

if(len(re.findall(r'ул.\s\w*\,\s\d*.\d*|\w*\sул.\,\s\d*.\d*|ул.\s\w*\s\(\w*\.\s\w*\)\,\s\d*.\d*|ул.\s\w*\s\w*\s\w*\,\s\d*.\d*', api["contactCardViewModel"]["fixedDescriptionBottomLine"])) == 0):
    street_name  = api["contactCardViewModel"]["fixedDescriptionBottomLine"]
    house_number = "undefind"
else:
    parsed_address  = re.findall(r'ул.\s\w*\,\s\d*.\d*|\w*\sул.\,\s\d*.\d*|ул.\s\w*\s\(\w*\.\s\w*\)\,\s\d*.\d*|ул.\s\w*\s\w*\s\w*\,\s\d*.\d*', api["contactCardViewModel"]["fixedDescriptionBottomLine"])[0]
    street_name  = re.findall(r'\w{3,}\s\(.\.\s\w{3,}\)|^\w{3,}|[a-zA-Zа-я-А-Я]{3,}|\w{2,}\s\w{4,}\s\w{4,}', parsed_address)[0]
    house_number = re.findall(r'\d*.\d*$', parsed_address)[0].strip()

full_info_json = {
    "rooms"         : rooms,
    "full_space"    : full_space,
    "kitchen_space" : kitchen_space,
    "floors"        : floors, #re.findall(r'\d*\d', iff[3].get_text())[0] if len(iff) > 3 else "0",
    "floor"         : floor,  #re.findall(r'\d*\d', iff[3].get_text())[1] if len(iff) > 3 else "0",
    "price"         : price,
    "street_name"   : street_name,
    "house_number"  : house_number,
    "phone"         : phone,
    "link"          : main_link
}

#print(full_info_json)

# with open('flat_club.csv', 'a', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     # spamwriter.writerow(
#     #     ['Улица']     + 
#     #     ['№ Дома']    + 
#     #     ['Год']       + 
#     #     ['Ссылка']    + 
#     #     ['Этаж']      + 
#     #     ['Этажей']    + 
#     #     ['Общая']     + 
#     #     ['Кухня']     + 
#     #     ['Комната']   + 
#     #     ['Потолок']   + 
#     #     ['Ремонт']    + 
#     #     ['Стоимость'] + 
#     #     ['Телефон']   + 
#     #     ['Имя']
#     # )
#     spamwriter.writerow(
#         [full_info_json['street_name']]   + 
#         [full_info_json['house_number']]  +
#         ["0"]                             + 
#         [full_info_json['link']]          + 
#         [full_info_json['floors']]        + 
#         [full_info_json['floor']]         + 
#         [full_info_json['full_space']]    + 
#         [full_info_json['kitchen_space']] + 
#         ["0"]                             + 
#         ["0"]                             + 
#         ["0"]                             + 
#         [full_info_json['price']]         + 
#         [full_info_json['phone']]         + 
#         ["0"]
#     )
#
print("OK!")

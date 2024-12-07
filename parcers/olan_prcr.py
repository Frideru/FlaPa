import requests
from   bs4 import BeautifulSoup
import csv
import re
import json

street_name, house_number, build_age, floor, floors, full_space, kitchen_space, room_space, ceiling_height, repair_type, price, phone, name = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

link = "https://ekaterinburg.olan.ru/sale-flat/secondary/three-rooms/128231622-79-0-m-etazh-8-19-16999000-rub-ul-bazhova-68"

def Olan(link):
    global street_name, house_number, build_age, floor, floors, full_space, kitchen_space, room_space, ceiling_height, repair_type, price, phone, name
    result = requests.get(link)
    soup   = BeautifulSoup (result.text, 'html.parser')

    find_name = soup.find("span", class_="apartment-desc__owner")
    find_name = find_name.find("noindex")
    name      = find_name.get_text().strip()

    find_info = soup.find_all("div", class_="apartment-desc__item")
    for i in find_info:
        if(len(re.findall(r'этаж:', i.get_text().lower())) != 0):
            floor = i.get_text().replace("этаж: ", "")
        elif(len(re.findall(r'этажей:', i.get_text().lower())) != 0):
            floors = i.get_text().replace("этажей: ", "")
        elif(len(re.findall(r'площадь', i.get_text().lower())) != 0):
            full_space = i.get_text().replace("площадь: ", "")
        elif(len(re.findall(r'адрес', i.get_text().lower())) != 0):
            street_name = i.get_text().replace("адрес: ", "")

    full_info_json = {
        "street_name"   : street_name,
        "house_number"  : house_number,
        "build_age"     : build_age,
        "link"          : link,
        "floor"         : floor,  
        "floors"        : floors, 
        "full_space"    : full_space,
        "kitchen_space" : kitchen_space,
        "room_space"    : room_space,
        "ceiling_height": ceiling_height,
        "repair_type"   : repair_type,
        "price"         : price, 
        "phone"         : phone,
        "name"          : name
    }

    print(full_info_json)

    # with open('./data.csv', 'a', newline='') as csvfile:
    #     spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     spamwriter.writerow(
    #         [full_info_json['street_name']]   +
    #         [full_info_json['house_number']]  +
    #         [full_info_json['build_age']]     +
    #         [full_info_json['link']]          +
    #         [full_info_json['floor']]         +
    #         [full_info_json['floors']]        +
    #         [full_info_json['full_space']]    +
    #         [full_info_json['kitchen_space']] +
    #         [full_info_json['room_space']]    +
    #         [full_info_json['ceiling_height']]+
    #         [full_info_json['repair_type']]   +
    #         [full_info_json['price']]         +
    #         [full_info_json['phone']]         +
    #         [full_info_json['name']]
    #     )
    # print("OK!")
    # return "OK!"

Olan(link)

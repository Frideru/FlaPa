import requests
from   bs4 import BeautifulSoup
import csv
import re
import json

street_name, house_number, build_age, floor, floors, full_space, kitchen_space, room_space, ceiling_height, repair_type, price, phone, name = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
#link = "https://upn.ru/obekty/kvartira-60382696"
#link = "https://upn.ru/obekty/kvartira-60409445"
#link = "https://upn.ru/obekty/kvartira-60409688"

def Upn(link):
    global street_name, house_number, build_age, floor, floors, full_space, kitchen_space, room_space, ceiling_height, repair_type, price, phone, name
    result = requests.get(link)
    soup  = BeautifulSoup (result.text, 'html.parser')

    find_info   = soup.find("div", class_="block-characteristics-objects")
    find_names  = find_info.find_all("span", class_="gray3-color width-percent-50")
    find_values = find_info.find_all("span", class_="black-color width-50")
    
    find_price = soup.find("div", class_="display-inline margin-right-8")
    price      = re.findall(r'\d*\s*\d*\s\d+',find_price.get_text())[0].replace(" ", "")

    find_name = soup.find_all("div", class_="agency-name d-flex")
    find_name = re.findall(r'[А-Я][а-я]{1,}\s[А-Я][а-я]{1,}|[А-Я][а-я]{1,}', str(find_name))
    name = find_name[len(find_name) - 1]

    find_phone = soup.find("div", class_="pressed-buttons")
    find_phone = find_phone.find("a")
    phone      = find_phone["href"].replace(r'tel:', "")

    count = 0
    for name_d in find_names:
        des = name_d.get_text()
        if(len(re.findall(r'год постройки', des.lower())) != 0):
            build_age = find_values[count].get_text().replace(" год", "")
        elif(len(re.findall(r'общая площадь', des.lower())) != 0):
            full_space = find_values[count].get_text().replace(" м2", "")
        elif(len(re.findall(r'жилая площадь', des.lower())) != 0):
            room_space = find_values[count].get_text().replace(" м2", "")
        elif(len(re.findall(r'площадь кухни', des.lower())) != 0):
            kitchen_space = find_values[count].get_text().replace(" м2", "")
        elif(len(re.findall(r'этаж/этажность', des.lower())) != 0):
            fl     = find_values[count].get_text()
            floor  = re.findall(r'^\d*', fl)[0]
            floors = re.findall(r'\d*$', fl)[0]
        elif(len(re.findall(r'ремонт', des.lower())) != 0):
            repair_type = find_values[count].get_text()
        count += 1

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

    with open('./data.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(
            [full_info_json['street_name']]   +
            [full_info_json['house_number']]  +
            [full_info_json['build_age']]     +
            [full_info_json['link']]          +
            [full_info_json['floor']]         +
            [full_info_json['floors']]        +
            [full_info_json['full_space']]    +
            [full_info_json['kitchen_space']] +
            [full_info_json['room_space']]    +
            [full_info_json['ceiling_height']]+
            [full_info_json['repair_type']]   +
            [full_info_json['price']]         +
            [full_info_json['phone']]         +
            [full_info_json['name']]
        )
    print("OK!")
    return "OK!"

#Upn(link)

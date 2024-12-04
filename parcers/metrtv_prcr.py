import requests
from   bs4 import BeautifulSoup
import csv
import re

#link = "https://www.metrtv.ru/prodaga_i_arenda/sell/flat/693548"
street_name, house_number, build_age, floor, floors, full_space, kitchen_space, room_space, ceiling_height, repair_type, price, phone, name = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

def MetrTv(link):
    request = requests.get(link)
    soup    = BeautifulSoup(request.text, 'html5lib')

    find_info  = soup.find("table")
    find_descr = find_info.find_all("td", class_="l")
    find_value = find_info.find_all("td", class_="r")
    
    find_seller = soup.find("div", class_="saler saler-longbar")
    find_name   = find_seller.find("p")
    name        = re.findall(r'—\s[а-яА-Я]*\s?[а-яА-Я]*', find_name.get_text().strip())[0].replace("—", "").strip()
    
    link_id    = re.findall(r'[0-9]{1,}', link)
    find_phone = requests.get(f'https://www.metrtv.ru/phoneclick_counter.php?adId={link_id[0]}')
    phone      = find_phone.json()["phone_number"]

    find_address = soup.find_all("span", itemprop="name")
    address      = find_address[5].get_text()
    house_number = re.findall(r'\d*$', address)[0]
    street_name  = re.findall(r'^(\d{1,}\s\w*\s?\w*|\w*\s?\w*)', address)[0]

    count = 0
    for description in find_descr:
        des = description.get_text().replace(":", "")
        if(len(re.findall(r'общая площадь', des.lower())) != 0):
            full_space = find_value[count].get_text()
        elif(len(re.findall(r'жилая площадь', des.lower())) != 0):
            room_space = find_value[count].get_text()
        elif(len(re.findall(r'площадь кухни', des.lower())) != 0):
            kitchen_space = find_value[count].get_text()
        elif(len(re.findall(r'этаж/этажность дома', des.lower())) != 0):
            value  = re.findall(r'\d\d?', find_value[count].get_text().strip())
            floor  = value[0]
            floors = value[1]
        elif(len(re.findall(r'отделка', des.lower())) != 0):
            repair_type = find_value[count].get_text()
        elif(len(re.findall(r'год постройки', des.lower())) != 0):
            build_age = find_value[count].get_text()
        elif(len(re.findall(r'цена', des.lower())) != 0):
            price = find_value[count].get_text().strip()
            price = re.findall(r'[0-9]{1,}\s\d\d\d\s\d\d\d', price)
            price = price[0].replace(" ", "")

        count = count + 1

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

# MetrTv(link)

import requests
from   bs4 import BeautifulSoup
import csv
import re

#Улица
#№ Дома
#Год
#Ссылка
#Этаж
#Этажей
#Общая
#Кухня
#Комната
#Потолок
#Ремонт
#Стоимость
#Телефон
#Имя

#link = "https://sverdlovsk.move.ru/objects/prodaetsya_3-komnatnaya_kvartira_ploschadyu_558_kvm_sverdlovskaya_oblast_ekaterinburg_6923998097/"
#link = "https://sverdlovsk.move.ru/objects/prodaetsya_2-komnatnaya_kvartira_ploschadyu_424_kvm_sverdlovskaya_oblast_ekaterinburg_9266216694/"
street_name, house_number, build_age, floor, floors, full_space, kitchen_space, room_space, ceiling_height, repair_type, price, phone, name = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

def MoveRu(link):
    global street_name, house_number, build_age, floor, floors, full_space, kitchen_space, room_space, ceiling_height, repair_type, price, phone, name
    request = requests.get(link)
    soup    = BeautifulSoup(request.text, 'html5lib')

    find_info  = soup.find_all("ul", class_="object-info__details-table")
    find_names = soup.find_all("div", class_="object-info__details-table_property_name")
    find_value = soup.find_all("div", class_="object-info__details-table_property_value")

    find_name  = soup.find("div", class_="block-user__name")
    find_phone = soup.find("p", class_="block-user__show-telephone_number")
    phone      = find_phone.get_text()
    name       = find_name.get_text()

    count = 0
    for name_d in find_names:
        des = name_d.get_text().replace(":", "")
        if(len(re.findall(r'адрес', des.lower())) != 0):
            address = re.findall(r'(ул\s\d?\s?\w*\w*?\s?\w*?\s\w*)|([0-9]{1,})', find_value[count].get_text().strip())
            street_name  = address[0][0].replace("ул", "").strip()
            house_number = address[1][1].strip()
        elif(len(re.findall(r'\sэтаж\s', des.lower())) != 0):
            floor  = re.findall(r'^\d*', find_value[count].get_text())[0]
            floors = re.findall(r'\d{1,}$', find_value[count].get_text())[0]
        elif(len(re.findall(r'общая площадь', des.lower())) != 0):
            full_space = find_value[count].get_text().replace(" м²", "")
        elif(len(re.findall(r'площадь кухни', des.lower())) != 0):
            kitchen_space = find_value[count].get_text().replace(" м²", "")
        elif(len(re.findall(r'жилая площадь', des.lower())) != 0):
            room_space = find_value[count].get_text().replace(" м²", "")
        elif(len(re.findall(r'высота потолков', des.lower())) != 0):
            ceiling_height = find_value[count].get_text()
        elif(len(re.findall(r'ремонт', des.lower())) != 0):
            repair_type = find_value[count].get_text()
        elif(len(re.findall(r'Цена', des)) != 0):
            price = find_value[count].get_text()

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

#MoveRu(link)

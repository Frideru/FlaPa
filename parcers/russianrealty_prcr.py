import requests
from   bs4 import BeautifulSoup
import csv
import re

#main_link = 'https://ekaterinburg.russianrealty.ru/prodazha-kvartiry-452108487-1-komnatnaya-Ekaterinburg-ulitsa-Stepana-Razina-Chkalovskaya/'
#main_link = 'https://ekaterinburg.russianrealty.ru/prodazha-kvartiry-442460908-3-komnatnaya-Ekaterinburg-ulitsa-Stepana-Razina-Chkalovskaya/'
main_link = 'https://www.russianrealty.ru/prodazha-kvartiry-260787057-4-komnatnaya-Moskva-pereulok-Banny-Prospekt-mira/'
def Russianrealty(link):
    r                   = requests.get(link)
    soup                = BeautifulSoup(r.text, 'html5lib')
    find_rooms          = soup.find_all("h1", itemprop="name")
    find_price          = soup.find_all("strong", class_="price-total")
    find_flat_character = soup.find_all("td")
    find_floors         = soup.find("div", class_="col-lg-4 col-md-6 col-sm-12 desc-list")
    find_floors         = find_floors.find("li")
    find_address        = soup.find_all("span", class_="street-address")
    find_contacts       = soup.find_all("div", class_="list-contact vcard")
    
    # Комнаты
    rooms = re.findall(r'\s\d\-', find_rooms[0].get_text())[0].replace(' ', '')
    rooms = rooms.replace('-', '')

    # Цена
    price = re.findall(r'\d*\s\d*\s\d*', find_price[0].get_text())[0].replace(' ', '')
    
    # Размер комнат
    flat_characters = []
    for i in find_flat_character:
        flat_characters.append(i.get_text())

    # Этажи
    floors = re.findall(r'[0-9]{1,}', find_floors.get_text())

    # Адрес
    address = find_address[0].get_text().replace(r'Адрес: ', '')
    address = re.search(r'\b(ул\.|пер\.)\s+([^\d]+)\s+(\d+[^,\s]*)\b', address)
    street  = address.group(2).replace(',', '')
    number  = address.group(3)

    # Контакты
    name = soup.find("strong", class_="fn agent")
    name = name.get_text()
    #phone =

    full_info_json = {
        "rooms":               rooms,
        "full_space":          flat_characters[0],
        "kitchen_space":       flat_characters[2],
        "room_space":          flat_characters[1],
        "floors":              floors[0],
        "floor":               floors[1],
        "price":               price,
        "address_street":      street,
        "address_flat_number": number,
        "phone":               '',
        "name":                name,
        "remont":              '0',
        "link":                link
    }
    print(full_info_json)
    print("oki test!")
    # with open('../data.csv', 'a', newline='') as csvfile:
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
    #         [full_info_json['address_street']]      + 
    #         [full_info_json['address_flat_number']] + 
    #         ["0"]                                   + 
    #         [full_info_json['link']]                + 
    #         [full_info_json['floors']]              + 
    #         [full_info_json['floor']]               + 
    #         [full_info_json['full_space']]          + 
    #         [full_info_json['kitchen_space']]       + 
    #         [full_info_json['room_space']]          + 
    #         ["0"]                                   + 
    #         [full_info_json['remont']]              + 
    #         [full_info_json['price']]               + 
    #         [full_info_json['phone']]               + 
    #         [full_info_json['name']]
    #     )

        # print("OK!")
        # return "OK!"

Russianrealty(main_link)

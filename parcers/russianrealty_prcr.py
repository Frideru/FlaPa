import requests
from   bs4 import BeautifulSoup
import csv
import re

#main_link = 'https://ekaterinburg.russianrealty.ru/prodazha-kvartiry-452108487-1-komnatnaya-Ekaterinburg-ulitsa-Stepana-Razina-Chkalovskaya/'
main_link = 'https://ekaterinburg.russianrealty.ru/prodazha-kvartiry-442460908-3-komnatnaya-Ekaterinburg-ulitsa-Stepana-Razina-Chkalovskaya/'
def Russianrealty(link):
    r                   = requests.get(link)
    soup                = BeautifulSoup(r.text, 'html5lib')
    find_price          = soup.find_all("strong", class_="price-total")
    find_flat_character = soup.find_all("td")
    find_address        = soup.find_all("span", class_="street-address")

    print(re.findall(r'\d*\s\d*\s\d*', find_price[0].get_text())[0].replace(' ', ''))
    for i in find_flat_character:
        print(i.get_text())

    for i in find_address:
        print(i.get_text().replace(r'Адрес: ', ''))

    full_info_json = {
        "rooms":               '',
        "full_space":          '',
        "kitchen_space":       '',
        "room_space":          '',
        "flat_height":         '',
        "flats":               '',
        "price":               '',
        "address_street":      '',
        "address_flat_number": '',
        "phone":               '',
        "name":                '',
        "remont":              '',
        "link":                ''
    }


# with open('../flat_club.csv', 'a', newline='') as csvfile:
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
#         [full_info_json['flat_height']]         + 
#         [full_info_json['flats']]               + 
#         [full_info_json['full_space']]          + 
#         [full_info_json['kitchen_space']]       + 
#         [full_info_json['room_space']]          + 
#         ["0"]                                   + 
#         [full_info_json['remont']]              + 
#         [full_info_json['price']]               + 
#         [full_info_json['phone']]               + 
#         [full_info_json['name']]
#     )

    print("OK!")

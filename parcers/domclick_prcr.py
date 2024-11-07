import requests
from   bs4 import BeautifulSoup
import csv
import re
import time

# olan_link = 'https://ekaterinburg.olan.ru/sale-flat/one-room/114031530-45-0-m-etazh-6-15-8500000-rub-ul-bazhova-ekaterinburg-munitsipalnoe-obrazovanie'

# main_link = input("enter mirkvartir link ex.(https://www.mirkvartir.ru/313375186/)\n--> ")

#GET PHONE NUMBER
main_link = 'https://ekaterinburg.domclick.ru/card/sale__flat__1578505738?appmetrica_tracking_id=748334322586582078&referrer=reattribution%3D1&utm_campaign=vitrina_frk_jan-dec2022_20211200028_fid_free_sale_online&utm_medium=card&utm_source=2gis&utm_term=1578505738'
# main_link = 'https://ekaterinburg.domclick.ru/card/sale__flat__2056970632'
get_number = re.findall(r'\/\w*__\w*__\d*', main_link)[0]
get_number = re.findall(r'\d*$', get_number)[0]

get_phone_link = f'https://offer-card.domclick.ru/api/v3/offers/phone/{get_number}'
get_token_link = f'https://offer-card.domclick.ru/api/v3/public_request/{get_number}'

get_token_link_header = {
    "Host":            "offer-card.domclick.ru",
    "User-Agent":      "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept":          "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer":         "https://ekaterinburg.domclick.ru/",
    "Origin":          "https://ekaterinburg.domclick.ru",
    "Connection":      "keep-alive",
    "Cookie":          "qrator_jsr=v2.0.1730958783.970.5ee6803cZwb3oZD9|HCoWW0g8q9yvVpax|oWIXfZMk2zznaNiloLreZvtvyNxpdyGnDI+LAkFmF+7dzYstC7ylT/wnb6Wu+N2sLQyanwuy2oXYoX6AGkfw4Q==-2am2WY7dH7ePj1ei3n7l1r3woFw=-00; ns_session=a81de1f5-0cf7-494a-aa1a-914879523dd7; qrator_ssid2=v2.0.1730958784.338.5ee6803cN79LPF1l|5zs7vaXK1Daxg4vg|z2yotVkm7jwN0PejCmPhW7Bk0KTDoQCN7HUhaJc/lg8YKvlnCzivhFYotegypoUPzgzBl0UTOZWOs3iwDhO1iQ==-OGN0W7/jb8BZXd9mkpHGKZX2/ag=; qrator_jsid2=v2.0.1730958783.970.5ee6803cZwb3oZD9|kmFPeTGvMgq1sD5U|jDrjhC42g4KU/f6Jo/xGOPL…ue; logoSuffix=; regionName=0d475b79-88de-4054-818c-37d8f9d0d440:%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3; _visitId=ba3ef9c7-7bb8-40c7-ba42-6dbfcccdc945-887c3e444c005759; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; _sa=SA1.aeffbe58-9928-40e5-ba9a-e429792c2d0a.1730958791; _sas=SA1.aeffbe58-9928-40e5-ba9a-e429792c2d0a.1730958791.1730958791",
    "Sec-Fetch-Dest":  "empty",
    "Sec-Fetch-Mode":  "cors",
    "Sec-Fetch-Site":  "same-site"
}

r_token = requests.get(get_token_link, headers=get_token_link_header)
print(r_token)
token   = r_token.json()['result']['token']

get_phone_link_header = {
    "Host":               "offer-card.domclick.ru",
    "User-Agent":         "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept":             "application/json, text/plain, */*",
    "Accept-Language":    "en-US,en;q=0.5",
    "Accept-Encoding":    "gzip, deflate, br",
    "Referer":            "https://ekaterinburg.domclick.ru/",
    "research-api-token": f'{token}',
    "Origin":             "https://ekaterinburg.domclick.ru",
    "Connection":         "keep-alive",
    "Cookie":             "ns_session=813382d8-0cca-4b57-9783-2562ecd40bc1; ftgl_cookie_id=ba202698a83b70f7b94b55a2d6e9bc3f; currentRegionGuid=962c3758-8514-4c8f-91fe-aa465d78e56f; currentLocalityGuid=0d475b79-88de-4054-818c-37d8f9d0d440; rent-experiment=false; logoSuffix=; RETENTION_COOKIES_NAME=54c39e9b9044410f9acfd73e0a30ad40:WzKcZT-ludN8iMdTKEZF1lAtT7g; sessionId=c4eaa2e7bd454539b11b118b46d689d1:JG0GtBq9AO-S_AzwPl_TbJ7DewU; UNIQ_SESSION_ID=88909ef999ce432f991898d73eccf894:5Ful5CISAeg313OnCZf3E3Nt3xQ; regionName=0d475b79-88de-4054-818c-37d8f9d0d440:%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3; _sa=SA1.b011a8d8-2ee5-4512-9649-50836b3c9dd0.1711597785; regionAlert=1; dtCookie=v_4_srv_7_sn_B503EC1C773551CA00D99475DFFC8502_perc_100000_ol_0_mul_1_app-3Aca312da39d5a5d07_1_app-3A6ea6d147da1fb68a_1_rcs-3Acss_0; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; qrator_ssid=1714120909.550.ngZxXW1uuOacNFhU-9enn4bma98dn7c08hvcmhg3rn823gp2e; qrator_jsid=1714120943.341.QFj0b9VUpNkDl0ea-mjgdn0arifjb54nj400lu7kq2ke80gfu",
    "Sec-Fetch-Dest":     "empty",
    "Sec-Fetch-Mode":     "cors",
    "Sec-Fetch-Site":     "same-site"
}
r_phone = requests.get(get_phone_link, headers=get_phone_link_header)


#PARSE THE SITE
get_parce_header = {
    "Host":            "ekaterinburg.domclick.ru",
    "User-Agent":      "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection":      "keep-alive",
    "Cookie":          "ns_session=813382d8-0cca-4b57-9783-2562ecd40bc1; ftgl_cookie_id=ba202698a83b70f7b94b55a2d6e9bc3f; currentRegionGuid=962c3758-8514-4c8f-91fe-aa465d78e56f; currentLocalityGuid=0d475b79-88de-4054-818c-37d8f9d0d440; logoSuffix=; RETENTION_COOKIES_NAME=54c39e9b9044410f9acfd73e0a30ad40:WzKcZT-ludN8iMdTKEZF1lAtT7g; sessionId=c4eaa2e7bd454539b11b118b46d689d1:JG0GtBq9AO-S_AzwPl_TbJ7DewU; UNIQ_SESSION_ID=88909ef999ce432f991898d73eccf894:5Ful5CISAeg313OnCZf3E3Nt3xQ; regionName=0d475b79-88de-4054-818c-37d8f9d0d440:%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3; _sa=SA1.b011a8d8-2ee5-4512-9649-50836b3c9dd0.1711597785; regionAlert=1; dtCookie=v_4_srv_7_sn_B503EC1C773551CA00D99475DFFC8502_perc_100000_ol_0_mul_1_app-3Aca312da39d5a5d07_1_app-3A6ea6d147da1fb68a_1_rcs-3Acss_0; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; qrator_ssid=1714187591.260.yl2HdazNqknLfm0g-cufi92o3qh3g4depdh3q2u7a9oh0mrkc; qrator_jsid=1714187590.857.14fc282zI3ao25tV-tifc2eul1allf3vc9057800949aq0i79; is-lotto-banner-hidden=true; rent-experiment=false; _visitId=240fc726-37b0-4e76-826e-1e52d0d07501-887c3e444c005759",
    "Sec-Fetch-Dest":  "document",
    "Sec-Fetch-Mode":  "navigate",
    "Sec-Fetch-Site":  "cross-site"
}
r_parce        = requests.get(main_link, headers=get_parce_header)
soup           = BeautifulSoup(r_parce.text, 'html5lib')
find_main_info = soup.find_all("div", class_="adkhV")
find_price     = soup.find("div", class_="ZS0ck")
find_address   = soup.find_all("span", class_="ItUnT")
find_remont    = soup.find_all("li", class_="_cGv6")
find_name      = soup.find("a", class_="YmqEJ")
if(find_name == None):
    find_name = False

address        = re.findall(r'улица\s\w*\,\s\d*.\d*|\w*\sулица\,\s\d*.\d*|улица\s\w*\s\(\w*\.\s\w*\)\,\s\d*.\d*|улица\s\w*\s\w*\s\w*\,\s\d*.\d*', find_address[0].get_text())[0];
address_street = re.findall(r'\s[a-zA-Zа-яА-Я]{3,}', address)[0];
address_number = re.findall(r'\d*$', address.strip())[0];

full_info_json = {
    "rooms":               '',
    "full_space":          find_main_info[0].get_text(),
    "kitchen_space":       find_main_info[2].get_text(),
    "room_space":          find_main_info[1].get_text(),
    "flat_height":         re.findall(r'^\d*', find_main_info[3].get_text())[0],
    "flats":               re.findall(r'\d*$', find_main_info[3].get_text())[0],
    "price":               re.findall(r'\d*\s\d*\s\d*', find_price.get_text())[0].replace(' ', ''),
    "address_street":      address_street.strip(),
    "address_flat_number": address_number,
    "phone":               r_phone.json()['result']['phone'],
    "name":                find_name.get_text() if find_name else "0",
    "remont":              '',
    "link":                main_link,
}

for i in find_remont: 
    if(len(re.findall(r'Ремонт', i.get_text())) != 0):
        remont = re.findall(r'\w*$', i.get_text())[0]
        full_info_json['remont'] = remont
    elif(len(re.findall(r'Комнат', i.get_text())) != 0):
        komnat = re.findall(r'\d*$', i.get_text())[0]
        full_info_json['rooms'] = komnat


with open('../flat_club.csv', 'a', newline='') as csvfile:
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
        [full_info_json['room_space']]          + 
        ["0"]                                   + 
        [full_info_json['remont']]              + 
        [full_info_json['price']]               + 
        [full_info_json['phone']]               + 
        [full_info_json['name']]
    )


time.sleep(1)
print("OK!")

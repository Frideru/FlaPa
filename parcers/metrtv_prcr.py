import requests
from   bs4 import BeautifulSoup
import csv
import re

link = "https://www.metrtv.ru/prodaga_i_arenda/sell/flat/693548"

request = requests.get(link)
soup    = BeautifulSoup(request.text, 'html5lib')

find_info = soup.find_all("tr")
for i in find_info:
    print(i.get_text())

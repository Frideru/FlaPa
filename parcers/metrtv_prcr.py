import requests
from   bs4 import BeautifulSoup
import csv
import re

link = "https://www.metrtv.ru/prodaga_i_arenda/sell/flat/693548"
r          = requests.get(link)
soup       = BeautifulSoup(r.text, 'html5lib')
find_rooms = soup.find_all("h1", itemprop="name")


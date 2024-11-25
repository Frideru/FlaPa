import requests
from   bs4 import BeautifulSoup
import csv
import re

r                   = requests.get(link)
soup                = BeautifulSoup(r.text, 'html5lib')
find_rooms          = soup.find_all("h1", itemprop="name")


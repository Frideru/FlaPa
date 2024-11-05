import re

links = [
    "https://ekaterinburg.domclick.ru/card/sale__flat__1578505738?appmetrica_tracking_id=748334322586582078&referrer=reattribution%3D1&utm_campaign=vitrina_frk_jan-dec2022_20211200028_fid_free_sale_online&utm_medium=card&utm_source=2gis&utm_term=1578505738",
    "https://www.mirkvartir.ru/312345151/",
    "https://ekaterinburg.russianrealty.ru/prodazha-kvartiry-452108487-1-komnatnaya-Ekaterinburg-ulitsa-Stepana-Razina-Chkalovskaya/",
    "http://ror.soso.lol",
    "https://ya.ru",
    "https://google.com/search",
    "http://dom.google.com/hiu/ror"
]

pattern = r'https?://([a-zA-Z]*)?\.?(domclick|mirkvartir|russianrealty)\.[a-z]{,3}\/[a-zA-Z]*'
for link in links:
    #link = link.strip()
    #print(link)
    t = re.findall(pattern, link)
    if re.findall(pattern, link):
        print(link)
    else:
        print(t)

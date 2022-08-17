import requests
from bs4 import BeautifulSoup
import WebScraping as W

User_name="닥닥"
user_HTML = BeautifulSoup(requests.get(f'https://maple.gg/u/{User_name}').text, "html.parser")

a=user_HTML.find_all("div", {"class": "pt-3 pb-2 pb-sm-3"})


print(a[0])

b=W.UserChar("닥닥")
print(b.get_TheSeed())
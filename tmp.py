import requests
from bs4 import BeautifulSoup
import WebScraping as W

User_name="바늘킹"
user_HTML = BeautifulSoup(requests.get(f'https://maple.gg/u/{User_name}').text, "html.parser")

a=user_HTML


print(a)

b=W.UserChar("닥닥")
print(b.get_TheSeed())
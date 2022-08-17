import requests
from bs4 import BeautifulSoup
import WebScraping as W

User_name="닥닥"
user_HTML = BeautifulSoup(requests.get(f'https://maple.gg/u/{User_name}').text, "html.parser")

a=user_HTML.select("#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(4) > section > footer > div.user-summary-date > span")
print(a[0].string)

b=W.UserChar("루델팡")
print(b.get_achievement())
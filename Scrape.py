import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Scrape:
    def __init__(self):
        self.headers = {
            "User-Agent": UserAgent().random
          }
        
    def scrape(self, search):
        result = requests.get(url=f"https://feebee.com.tw/s/?q={search}", headers=self.headers)
        soup = BeautifulSoup(result.text, "lxml")
        
        options = soup.findAll("h3",class_="large")
        price = soup.findAll("span",class_="price ellipsis xlarge")
        link = soup.findAll("a",class_="campaign_link campaign_link_buy")
        
        lst = ""
        for i in range(3):
            lst += f"商品名稱: {options[i].getText()}\n"
            lst += f"價格: {price[i].getText()}\n"
            lst += f"購買連結: {link[i].get('href')}\n"
            
        return lst

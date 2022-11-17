import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class scrape:
    def __init__(self):
        self.headers = {
            "User-Agent": UserAgent().random
          }
        
    def scrape(self, search):
        result = requests.get(url=f"https://feebee.com.tw/s/?q={search}", headers=self.headers)
        soup = BeautifulSoup(result.text)
        
        options = soup.findAll("h3",class_="large")
        price = soup.findAll("span",class_="price ellipsis xlarge")
        link = soup.findAll("a",class_="campaign_link campaign_link_buy")
        
        lst = ""
        for i in range(3):
            lst += f"商品名稱: {options[i].getText()}\n"
            lst += f"價格: {price[i].getText()}\n"
            lst += f"購買連結: {link[i].get('href')}\n"
            
        return lst
    
    def news(self):
        url = "https://technews.tw/"
        result = requests.get(url=url, headers=self.headers)
        soup = BeautifulSoup(result.text)
        div = soup.find(id="content") 

        news_list=[]
        for article in div.find_all("article")[:3]:
            target = { 
                "title": "",
                "img_url": "",
                "role": "",
                "news_url": ""
                }
            h1 = article.find("h1", class_="entry-title")
            span = article.find_all("span", class_="body")[0]
            div = article.find("div", class_="img")
            div_a = div.find("a").get('href')
            div_img = div.find("img").get('src')
            target["title"] = h1.text
            target["news_url"] = div_a
            target["role"] = span.text 
            target["img_url"] = div_img
            news_list.append(target)
        
        return news_list

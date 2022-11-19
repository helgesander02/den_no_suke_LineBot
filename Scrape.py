import requests
from bs4 import BeautifulSoup

class scrape:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320"
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
            target["title"] = article.find("h1", class_="entry-title").text
            target["role"] = article.find_all("span", class_="body")[0].text
            target["news_url"] = article.find("div", class_="img").find("a").get('href')
            target["img_url"] = article.find("div", class_="img").find("img").get('src')
            news_list.append(target)
        
        return news_list

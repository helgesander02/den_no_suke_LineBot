from flask import Flask, request, abort

from channel import keys
from Scrape import scrape

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import random

app = Flask(__name__)

line_bot_api = LineBotApi(keys['Chennel_access_token'])
handler = WebhookHandler(keys['Channel_secret'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = str(event.message.text)
    if msg == "隨機一組數字":
        x = random.randrange(100)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(x)))
        
    elif msg == "熱銷商品比價GO":
        goods_list = ["滑鼠", "鍵盤", "喇叭", "耳機", "麥克風", "電競椅", "辦公椅", "繪圖板", "office軟體",
              "電競螢幕", "網路攝影機", "電腦機殼", "固態硬碟", "傳統硬碟", "顯示卡", "CPU", "主機板", "記憶體", "電源供應器",
              "風扇", "外接硬碟", "電腦機殼", "UPS", "記憶卡", "隨身碟", "Nintendo Switch", "PlayStation 5", "Xbox", "手把控制器",
              "羅技", "雷蛇", "HyperX", "路由器", "橋接器", "交換器", "光碟機", "華碩", "ROG", "曜越", "海盜船", "酷媽", "藍芽耳機",
              "Turtle Beach", "鐵三角", "微星", "賽德斯", "威剛", "樹梅派", "Arduino", "ESP32"]
        x = random.randrange(50)
        user_input = goods_list[x]
        myScrape = scrape()
        output = myScrape.scrape(user_input)       
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(output)))
    
    elif msg == "最新新聞追追追":
        myScrape = scrape()
        news_list = myScrape.news()
        carousel_template_message = TemplateSendMessage(
             alt_text='最新新聞推薦',
             template=CarouselTemplate(
                 columns=[
                     CarouselColumn(
                         thumbnail_image_url=news_list[0]["img_url"],
                         title=news_list[0]["title"],#title
                         text=f'作者:{news_list[0]["role"]}',#作者
                         actions=[
                             URIAction(
                                 label='馬上查看',
                                 uri=news_list[0]["news_url"]#文章連結
                             )
                         ]
                     ),
                     CarouselColumn(
                         thumbnail_image_url=news_list[1]["img_url"],
                         title=news_list[1]["title"],
                         text=f'作者:{news_list[1]["role"]}',
                         actions=[
                             URIAction(
                                 label='馬上查看',
                                 uri=news_list[1]["news_url"]
                             )
                         ]
                     ),
                     CarouselColumn(
                         thumbnail_image_url=news_list[2]["img_url"],
                         title=news_list[2]["title"],
                         text=f'作者:{news_list[2]["role"]}',
                         actions=[
                             URIAction(
                                 label='馬上查看',
                                 uri=news_list[2]["news_url"]
                             )
                         ]
                     )
                 ]
             )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
        
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        
if __name__ == "__main__":
    app.run()

from flask import Flask, request, abort

import os
from pyChatGPT import ChatGPT
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

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

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
    if msg == "餵食電之助":
        name = line_bot_api.get_profile(str(event.source.userId))
        #x = random.randrange(100)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=name))
        
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
        
        #line_bot_api.reply_message(
            #event.reply_token,
            #TextSendMessage(text="根據問題深度需要1至3分鐘才會回答"))
        
        session_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..PvSL4cZdtVx0jxcf.pP-5BydOd3QrNrGh6BScYDSLhMIcGpKXq3JhB7z7bwf7XhmeHP1FiM9uWhOz1swJ2em9YKBX29VQhljoID9eeez57yk9GJO-M3SvwNQYYVpfWzz7fIun5tS-OnOWw2zbMpJ6u_ffnAdZWEKaSJXquMKgU-qJo1H80Ohwn-qkvN_8vX-CzYoFkR0RIPqyRL0VVdCPVpwHnBgBAfo4Lp4iJFiyBR2IF9LjFWosgOy-hJFYJxRDiWvR1CjOqfuc9tb7PaYUhAmday42MZtSZWsfGw-rweLiE1zLbkRiIQNSxxdyi9cmaYtSHChvSSEK0WlKGlVVTtMZdfKwuO9BGWNfe8-udwBHHGpEYXm0ZDzshv5nTbg7pUPFCnA4ILMG1gOuK5jCZl73CtuR6D1MGoxBK6G702mmiVjMNmzGxFVNrEBU6vw590swE0YOVfQ0HMySVeQUhKxXrAZN5JR36Z5oM7YczAB7Jq6cXGKPz4u0dVZTx0sb7FZYP1BS0isAftvFaxIa2C4aFJ9gcbOmJWAYXEv4JehcHi8LgMSrag62VojVOQ2xuvywbreWUlgdukK7w5MCkFEtj6kIeUZ4M-6H6tfkDZQgroEsjuwr_-Q3_emnk00BVeZn6D81jkEE1GWj_vIAjzpJUJf3fFBsVVE8zGO_UKGoXDJn3OBWWTo9V_vGi8BPadFFNrZiyv-OriL8cjithcUn88CudME5sfGNfiMg9IqxUFtJXms9CRES9MVrqcIqMuJ6ocLHx7efUMRzcWYFArfdg5BX0kdNUgq6fy-bM2X2uas3qRNHgfm7tiVigefIy0D9P5aN_SPOfWpUGedJZpuEtypJj8i8woahwhZWDhJYnk5LjqQj2qvyEiOLXQ22ezAfOJkgRaXtkdPNGNdu52txgm72hBZS1q6K38alxhufuUJ13xz7Cs19uhnhuKRhVFfFMKrmpJrZdagCn_xX6O6T2oR7MggX3Rb-0RdlOUt2ba9IcAdVXooz6F6Q1JxHQnG0y9jVdyHGJ8Uo5fNrARbAoJJta_lb3Lljwz_FSpVkwebffV3W3s5O80a8wVlHmZ1AkwtKK0-shdgRhelL1kg3bEXdIM_IekELfZtcAi-rQFg_gmdYDs9c1Z1g3cU7BqjVjtq6BCtpU3anuN2A7Uu-0L94ZzWtaQSfrby7ALLGeX_to5ENPGA-3XPVN8_r-EGfUI5vUs9oPu9XBUl_Pr1sjRUmmrXp7jZzg9-l7OUJB8ZQR6y9vH1o_4k1WdFtBsNF7Kn96y8yQeM9gfhw0axrmLEv1npxdFsI56uJGTiSzBVtDygsBPHBBNP3GcvaF0C5x2tO9YTxNJOC41zuNlhOASpq8zVNEt8KHQiwCHMNLQVYGw_J-WcWRZCSUnrlXVi_TuOnUJuY5EBGY1S86AC3lqdy3-mE8iAPefBzq67KmrdjXHts8L-1OheZBZPp6Mr3GazHqGaYKCuN2WYo7dkPjUrwGVSjXmV_f8zgvwprB59_d4VXeHT3Z4OnF3ADsXh4XgU2H4cG76c9LIWUo5tZEnKdMr4vnnnJ6OXtz6Azvxde4yNLjUzaS9zW3L_CrRI7GCtG_gUg3J0l7-o67sMTzWRZUeUX6Ssgge9mb96-Hd_vPlQyCC1cBovr9Lbdre85VIVyNQqhgRWxeIh3fc3GGOinP-cMgch6IOB2WQzjOuioVcW6orRavDSci0nAhE9EQ-tPjnnQ_5rKiDfCAfBZg604VWjNWiaSZnwR0AqGo9QmHu1vqgCYj0ERG2k3WMltSLje_PjZnK8SIZwlvqBiil6bBr85_wBhL5AtnNXOIgjc55FSWRSBVPi8mGA4yiA737yiPb6QutfqI3CjqUsF1lA4U82SnGXaS_cC21Urk3ww4pSuCCqEiO8L8UkQXyjIAga-1d2QuNkKFULAPFIjgQcDXN7jVGvFk3f-IlRvjp7vTYJ7lQqXVBTEXw9mg8IkpUCpGfOV4ACejwOF6Lxj08CnPz_6h_9Qc14cX2I-62AGaB0lYrRv6sOvD3QxuvpQVNy1DHcF8wMiEcr_dp0nV10HyqXmnyu39up2OSIvNQt-V50UWUcVWIquw35WoSEYsFFqYj7LNACH1oQIQFsS2wuquEP57TRk5J-lmuiuQhenjc5lR0HhZscTioXhIx5HvRPwVhjbT2dbGHpIJUQj9iwAzyDYfNwkVhftQ9EVQndtZhgiQjmdhq3ZtvKxt0SHBLnfgcEDig6s9SAe_q6DuYSi.C2d9LRY76viR41MKo4YQOA"
        api = ChatGPT(session_token)
        rp = api.send_message(msg)
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = rp['message']))
        
if __name__ == "__main__":
    app.run()

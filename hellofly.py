from flask import Flask, request, abort

from channel import keys

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

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
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
        
if __name__ == "__main__":
    app.run()

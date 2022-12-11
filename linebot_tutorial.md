<h1>建立與Render的連線</h1>
<h2>Render網站</h2>
<img src="https://github.com/helgesander02/linebot_flask/blob/main/img/%E5%BB%BA%E7%AB%8B%E6%AA%94%E6%A1%88.jpg" with="300" heigh="150"></img>
<p>在文字方塊裡面加入 https://github.com/helgesander02/linebot_flask/blob/main/render.yaml ，按continue開始建立。</p>
<h2>render.yaml內容</h2>
<img src="https://github.com/helgesander02/linebot_flask/blob/main/img/%E5%85%A7%E5%AE%B9.jpg" with="300" heigh="150"></img>
<p>name : 這是建立在Render裡 Web Service 名稱。</p>
<p>repo : 這是連結LineBot專案 GitHub連結。</p>
<p>buildCommand : 這是在雲端安裝套件，通常都寫在requirements.txt裡面。</p>
<p>startCommand : 這是Web與LineBot的連線</p>
<h1>LineBot</h1>
<h2>官網</h2>
<p>https://developers.line.biz/en/</p>
<h2>LineAPI2Render</h2>
<img src="https://github.com/helgesander02/linebot_flask/blob/main/img/token.jpg" with="300" heigh="150"></img>
<p>LINE_CHANNEL_ACCESS_TOKEN</p>
<img src="https://github.com/helgesander02/linebot_flask/blob/main/img/secret.jpg" with="300" heigh="150"></img>
<p>LINE_CHANNEL_SECRET</p>
<h2>環境變數</h2>
<img src="https://github.com/helgesander02/linebot_flask/blob/main/img/%E5%BB%BA%E7%AB%8BWebService.jpg" with="300" heigh="150"></img>
<p>Service Group Name填入名字</p>
<p>將兩個Key填入LINE_CHANNEL_ACCESS_TOKEN與LINE_CHANNEL_SECRET的Value</p>
<p>把環境變數輸入到LineBot_API</p>
<p>line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))</p>
<p>handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))</p>
<h2>設定</h2>
<img src="https://github.com/helgesander02/linebot_flask/blob/main/img/URL.png" with="300" heigh="150"></img>
<p>最後把Render產出的網址貼到Webhook URL加上/callback就能測試LineBot了</p>
<img src="https://github.com/helgesander02/linebot_flask/blob/main/img/setting.png" with="300" heigh="150"></img>
<p>要記得到管理平台把Webhook打開</p>

<h1>參考連結</h1>
<p>https://ithelp.ithome.com.tw/articles/10283836</p>
<p>https://lawrencechuang760223.medium.com/line-bot-%E8%81%8A%E5%A4%A9%E6%A9%9F%E5%99%A8%E4%BA%BA-ch3-%E4%BD%BF%E7%94%A8-python-%E6%89%93%E9%80%A0%E7%AC%AC%E4%B8%80%E5%80%8B-line-%E8%81%8A%E5%A4%A9%E6%A9%9F%E5%99%A8%E4%BA%BA-f8c9f250e578</p>

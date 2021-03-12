import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Your Channel Access Token')

# Channel Secret
handler = WebhookHandler('Your Channel Secret')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Content = event.message.text #輸入內容

    if Content == '股票':
        line_bot_api.reply_message(
            event.reply_token, TemplateSendMessage(
            alt_text = 'Buttons template',
            template = ButtonsTemplate(
                title = '常用股票',
                text = '請選擇股票代號',
                actions = [
                    MessageTemplateAction(
                         label = '0050',
                         text = '0050'
                    ),
                    MessageTemplateAction(
                         label = '0056',
                         text = '0056'
                    ),
                    MessageTemplateAction(
                         label = '2330',
                         text = '2330'
                    )
                ]
            )
        ) 
    )
    else:
        try:
            url = 'https://goodInfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID={}'.format(event.message.text) #Stock網址
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
            re = requests.post(url, headers = headers)
            soup = BeautifulSoup(re.content, "html.parser")  
            data = soup.find_all("table", class_="solid_1_padding_3_1_tbl")

            for i in data:
                Info = list(i.stripped_strings) #去除多餘空白
               
            if Info[5] == '成交價':
                Stock_Name = str(Info[0]) #名稱
                Stock_Date = str(Info[4]) #日期
                Stock_Open = str(Info[13:][5]) #開盤
                Stock_Close = str(Info[13:][0]) #收盤
                Stock_High = str(Info[13:][6]) #最高
                Stock_Low = str(Info[13:][7]) #最低
                Stock_Quote_Change = str(Info[13:][3]) #漲跌幅
                
            elif Info[4] == '成交價':
                Stock_Name = str(Info[0]) #名稱
                Stock_Date = str(Info[3]) #日期
                Stock_Open = str(Info[12:][5]) #開盤
                Stock_Close = str(Info[12:][0]) #收盤
                Stock_High = str(Info[12:][6]) #最高
                Stock_Low = str(Info[12:][7]) #最低
                Stock_Quote_Change = str(Info[12:][3]) #漲跌幅                
            
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='股票名稱:{}\n{}\n開盤:{}\n收盤:{}\n最高:{}\n最低:{}\n漲跌幅:{}\n'.format(Stock_Name,Stock_Date,Stock_Open,Stock_Close,Stock_High,Stock_Low,Stock_Quote_Change))) #回復訊息
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='股票代號輸入錯誤,請重新輸入!')) #回復訊息
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

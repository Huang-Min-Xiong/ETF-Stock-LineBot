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
    Content=event.message.text #輸入內容
    if Content == '0050':
        url = 'https://goodInfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID=0050' #0050網址
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        re=requests.post(url, headers = headers)
        #soup = BeautifulSoup(re.content, "lxml") 
        soup = BeautifulSoup(re.content, "html.parser")  
        data=soup.find_all("table", class_="solid_1_padding_3_1_tbl")
        for i in data:
            Info=list(i.stripped_strings) #去除多餘空白
            #print(Info) #股票內容
            #print('股票名稱:'+Info[0])
            #print('日期:'+Info[3])
            #print('開盤:'+Info[17]) 
            #print('收盤:'+Info[12]) 
            #print('最高:'+Info[18]) 
            #print('最低:'+Info[19]) 
            #print('漲跌幅:'+Info[15])

        Stock_Name=str(Info[0]) #名稱
        Stock_Date=str(Info[3]) #日期
        Stock_Open=str(Info[17]) #開盤
        Stock_Close=str(Info[12]) #收盤
        Stock_High=str(Info[18]) #最高
        Stock_Low=str(Info[19]) #最低
        Stock_Quote_Change=str(Info[15]) #漲跌幅
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='股票名稱:{}\n{}\n開盤:{}\n收盤:{}\n最高:{}\n最低:{}\n漲跌幅:{}\n'.format(Stock_Name,Stock_Date,Stock_Open,Stock_Close,Stock_High,Stock_Low,Stock_Quote_Change))) #回復訊息

    elif Content == '0056':
        url = 'https://goodInfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID=0056' #0056網址
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        re=requests.post(url, headers = headers)
        #soup = BeautifulSoup(re.content, "lxml") 
        soup = BeautifulSoup(re.content, "html.parser")  
        data=soup.find_all("table", class_="solid_1_padding_3_1_tbl")
        for i in data:
            Info=list(i.stripped_strings) #去除多餘空白

        Stock_Name=str(Info[0]) #名稱
        Stock_Date=str(Info[2]) #日期
        Stock_Open=str(Info[16]) #開盤
        Stock_Close=str(Info[11]) #收盤
        Stock_High=str(Info[17]) #最高
        Stock_Low=str(Info[18]) #最低
        Stock_Quote_Change=str(Info[14]) #漲跌幅
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='股票名稱:{}\n{}\n開盤:{}\n收盤:{}\n最高:{}\n最低:{}\n漲跌幅:{}\n'.format(Stock_Name,Stock_Date,Stock_Open,Stock_Close,Stock_High,Stock_Low,Stock_Quote_Change))) #回復訊息
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

import customtkinter
import tkinter
import random
from authentication import Authentication
from account import Account
from websocket import Websocket
import asyncio
import json
import os,time
from sentiment import Sentiment
from trading import Trade
from GUI import GUI
gui = GUI()
auth = Authentication()
x_token,cst = auth.CST_X()
web = Websocket(cst,x_token)
sent  = Sentiment(cst,x_token)
trade = Trade(cst,x_token)
account = Account(cst,x_token)


gui.main_loop()
# trade = Trade(cst=cst,x_token=x_token,market_id='TSLA',side='buy',quantity=1)
# print(trade.create_position())
# print(trade.get_positions())

# print(web.subscribemarket_sync('TSLA'))
# print(sent.get_client_sentiment(['TSLA','AAPL']))
# account = Account(cst,x_token)
# print(account.Risk())
# for i in range(0,100):
#     print(account.get_a_balance())

# print(balance,available,profitLoss)
# print(account.risk(240))
# stock_price = 235
# print(account.check_tpsl(stock_price))




# it should tell me if i buy with the current quantity and how much loss i will be in by looking at the spread
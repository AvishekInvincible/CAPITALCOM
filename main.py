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
xx = []


auth = Authentication()
x_token,cst = auth.CST_X()
web = Websocket(cst,x_token)
sent  = Sentiment(cst,x_token)
trade = Trade(cst,x_token)
print(trade.create_position(market_id='GOLD',side='buy',quantity=5))

stop_loss_distance = 2
# trade = Trade(cst=cst,x_token=x_token,market_id='TSLA',side='buy',quantity=1)
# print(trade.create_position())
# print(trade.get_positions())
# print(sent.get_client_sentiment(['TSLA','AAPL']))
# account = Account(cst,x_token)
# print(account.Risk())
# balance,available,profitLoss = account.get_a_balance()
# print(balance,available,profitLoss)
# print(account.risk(240))
# stock_price = 235
# print(account.check_tpsl(stock_price))


# asyncio.run(web.unsubscribe_from_all_markets())



# it should tell me if i buy with the current quantity and how much loss i will be in by looking at the spread
import pygame
from authentication import Authentication
from account import Account
from websocket import Websocket
import asyncio
import json
import os,time
from sentiment import Sentiment
from trading import Trade
import threading
import queue
from concurrent.futures import ThreadPoolExecutor 
from queue import Queue
import os
q = Queue()
Buy = None
Sell = None
spread = None


class GUI():
    def __init__(self,Stock,pnl,balance):
        self.stock = Stock
        self.pnl = pnl
        self.balance = balance
        
        auth = Authentication()
        self.x_token,self.cst = auth.CST_X()
        self.sent  = Sentiment(self.cst,self.x_token)
        self.trade = Trade(self.cst,self.x_token)
        self.account = Account(self.cst,self.x_token)
        self.web = Websocket(self.cst,self.x_token)
        self.queue = queue.Queue()

    async def async_task(self,):
      global Buy, Sell, spread
      while True:
        Buy, Sell, spread = await self.web.subscribemarket(self.stock)
        q.put((Buy, Sell, spread))
    # Do something with data  
        await asyncio.sleep(1)
    def init_pygame(self):
        pygame.init()

        screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Fast SOOD")
        font = pygame.font.Font(None, 32)
        
        return screen, font
    def run(self,screen,font,loop):
        global Buy, Sell
        font = pygame.font.Font("Colleged.ttf", 32)
        info_label = font.render("Stock: {}".format(self.stock), True, "white")
        TEXT_COLOR = (100, 100, 100)
        sell_image = pygame.image.load("SELL.png") 
        sell_rect = sell_image.get_rect(center=(1100, 170))
        buy_image = pygame.image.load("Buy.png") 
        buy_rect = buy_image.get_rect(center=(930, 170))
        rect = pygame.Rect(865, 100, 300, 350)
        
        

        
        
        font = pygame.font.Font("KGHAPPY.ttf", 20)  
        run = True
        while run:
          screen.fill((0,0,0))
          if not q.empty():
            Buy, Sell, Spread = q.get()
            print(Buy, Sell, Spread)

          # quantity_ = font.render(f'Quantity :', True, 'white')
          # quantity_rect = quantity_.get_rect(topleft=(50, 50)) 
          font = pygame.font.Font("KGHAPPY.ttf", 15) 
          buy_text = font.render(f'{Buy}', True, 'White')
          sell_text = font.render(f'{Sell}', True, 'White') 
          
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
              shutdown_event = asyncio.Event()

              # Schedule the async task to stop
              if loop.is_running():
                # Schedule the async task to stop
                shutdown_event.set()

              # Wait for the async task to stop
              shutdown_event.wait()
              run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
              if buy_rect.collidepoint(event.pos):
                # quantity_def = self.account.risk(Buy)
                # print(trade.create_position(market_id=self.stock,side='buy',quantity=quantity_))
                print("Buy Clicked") 
              if sell_rect.collidepoint(event.pos):
                # quantity_def = account.risk(Sell)
                # print(trade.create_position(market_id=self.stock,side='sell',quantity=quantity_))
                print("Sell Clicked")  

          # Blit assets 

          screen.blit(info_label, (470, 30))
          screen.blit(buy_image, buy_rect)
          screen.blit(sell_image, sell_rect)
          pygame.draw.rect(screen, (0,0,255), rect, width=3)
          # screen.blit(quantity_, quantity_rect) 
         
          screen.blit(buy_text, (500, 120))
          screen.blit(sell_text, (900, 120))
          



          pygame.display.update()

        pygame.quit()
        shutdown_event.cancel()
    def main_loop(self):
      executor = ThreadPoolExecutor()
      loop = asyncio.get_event_loop()
      loop.set_default_executor(executor)
      # Start asyncio task in thread
      t = threading.Thread(target=lambda: asyncio.run(self.async_task()))
      t.start()

      screen , font = self.init_pygame()
      self.run(screen, font,loop)

      # Wait for background thread to finish
      t.join()

      loop.stop()
      loop.close()
      pygame.quit()
R = GUI("GOLD",+1000,99999)
R.main_loop()






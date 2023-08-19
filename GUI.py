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
Buy = 1
Sell = 1
spread = 1


class GUI():
    def __init__(self,Stock  = 'GOLD'):
        self.stock = Stock
        
        
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
        pygame.display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 1)
        screen = pygame.display.set_mode((1200,800),pygame.DOUBLEBUF)
        pygame.display.set_caption("Fast SOOD")
        font = pygame.font.Font(None, 32)
        
        return screen, font
    def run(self,screen,font,loop):
        global Buy, Sell
        font = pygame.font.Font("Colleged.ttf", 32)
        info_label = font.render("Asset: {}".format(self.stock), True, "white")
        TEXT_COLOR = (100, 100, 100)
        sell_image = pygame.image.load("SELL.png") 
        sell_rect = sell_image.get_rect(center=(1100, 170))
        buy_image = pygame.image.load("Buy.png") 
        buy_rect = buy_image.get_rect(center=(930, 170))
        rect = pygame.Rect(865, 100, 300, 350)
        rect_2 = pygame.Rect(900, 2, 300, 50)
        
        
        hw_accel = pygame.display.gl_get_attribute(pygame.GL_ACCELERATED_VISUAL)

        quantity_def = 0
        input_box = pygame.Rect(500, 500, 140, 50)
        color_inactive = pygame.Color('white')
        color_active = pygame.Color('blue')
        color = color_inactive
        active = False
        text = ''
        run = True
        clock = pygame.time.Clock()

        i=0
        while run:
          screen.fill((0,0,0))
          if not q.empty():
            Buy, Sell, Spread = q.get()
            # print(Buy, Sell, Spread)
          balance,available,profitLoss = self.account.get_a_balance()
          if i %5 ==0:
            quantity_def = self.account.risk(Buy)
          Long, Short = self.sent.get_client_sentiment([self.stock])
          quantity_ = font.render(f'Q: {quantity_def}', True, 'white')
          quantity_rect = quantity_.get_rect(topleft=(980, 250)) 
          font = pygame.font.Font("verdana-bold.ttf", 20) 
          sell_text = font.render(f'{Sell}', True, 'Red')
          buy_text = font.render(f'{Buy}', True, 'Green')
          SHORT_SENT = font.render(f'Short: {Short}%', True, 'Red')
          LONG_SENT = font.render(f'Long: {Long}%', True, 'Green')

          font = pygame.font.Font("arial.ttf", 20) 
          
          stop_loss_percentage = 0.05
          target_profit_percentage = stop_loss_percentage * 2 # Set to 2x stop loss percentage
          buy_stop_loss_price = Buy * (1 - stop_loss_percentage)
          target_price = Buy * (1 + target_profit_percentage) 
          buy_target_profit_price = Buy + (target_price - Buy) / 1
          
          buy_tp_text = font.render(f'TP: {round(buy_target_profit_price,2)}', True, 'Green')
          buy_sl_text = font.render(f'SL: {round(buy_stop_loss_price,2)}', True, 'Red')

          stop_loss_percentage = 0.05 
          target_profit_percentage = stop_loss_percentage * 2 

          sell_stop_loss_price = Sell * (1 + stop_loss_percentage)
          target_price = Sell * (1 - target_profit_percentage) 

          sell_target_profit_price = Sell - (Sell - target_price)


          sell_tp_text = font.render(f'TP: {round(sell_target_profit_price,2)}', True, 'Green')
          sell_sl_text = font.render(f'SL: {round(sell_stop_loss_price,2)}', True, 'Red')
          balance_text = font.render(f'Available: {available}', True, 'White')

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
                if quantity_def ==0:
                  pass
                else:
                  print(self.trade.create_position(market_id=self.stock,side='buy',quantity=quantity_def,stop=buy_stop_loss_price,profit=buy_target_profit_price))
                print("Buy Clicked") 
              if sell_rect.collidepoint(event.pos):
                # quantity_def = account.risk(Sell)
                if quantity_def ==0:
                  pass
                else:
                  print(self.trade.create_position(market_id=self.stock,side='sell',quantity=quantity_def,stop=sell_stop_loss_price,profit=sell_target_profit_price))
                print("Sell Clicked") 
              if input_box.collidepoint(event.pos):
                active = not active
              else:
                  active = False
              color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
      
              if event.key == pygame.K_KP_1:
                print("Buy Clicked")
                print(self.trade.create_position(market_id=self.stock,side='buy',quantity=quantity_def,stop=sell_stop_loss_price,profit=sell_target_profit_price))
              if event.key == pygame.K_KP_0:
                print("Sell Clicked")
                print(self.trade.create_position(market_id=self.stock,side='sell',quantity=quantity_def,stop=sell_stop_loss_price,profit=sell_target_profit_price))
              if event.key == pygame.K_q:
                run = False
              if active:
                if event.key == pygame.K_RETURN:
                    self.stock = text.upper()
                    font = pygame.font.Font("Colleged.ttf", 32)
                    info_label = font.render("Asset: {}".format(self.stock), True, "white")
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
              

          # Blit assets 
          pygame.draw.rect(screen, color, input_box)
          txt_surface = pygame.font.Font(None, 50).render(text, True, 'white')
          width = max(200, txt_surface.get_width()+10)
          input_box.w = width
          screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

          pygame.display.flip()
          screen.blit(info_label, (470, 30))
          screen.blit(buy_image, buy_rect)
          screen.blit(sell_image, sell_rect)
          pygame.draw.rect(screen, (255,255,255), rect, width=3)
          pygame.draw.rect(screen, (255,255,255), rect_2, width=3)
          screen.blit(quantity_, quantity_rect) 

          screen.blit(buy_tp_text, (880, 350))
          screen.blit(buy_sl_text, (880, 390))
          screen.blit(sell_tp_text, (1040, 350))
          screen.blit(sell_sl_text, (1040, 390))
          screen.blit(balance_text, (980, 8))
          screen.blit(sell_text,(1060, 110))
          screen.blit(buy_text,(890, 110))
          screen.blit(SHORT_SENT, (1000, 600))
          screen.blit(LONG_SENT,(800, 600))

          


          pygame.display.update()
          clock.tick(120)
          i+=1

        pygame.quit()
        os._exit(0)

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







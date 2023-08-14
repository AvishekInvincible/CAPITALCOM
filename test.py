# import websocket
# import json
# import requests

# # Set your API key and CST
# api_key = "P7A0abF2IPCe0KEi"

# import asyncio
# import websockets
# url = 'https://api-capital.backend-capital.com'
# key = 'P7A0abF2IPCe0KEi'
# import requests



# # Create the request headers
# payload = json.dumps({
#     'encryptedKey':False,
#   "identifier": "avisheksood01@gmail.com",
#   "password": "Chand@20054"
# })

# headers = {
#   'X-CAP-API-KEY': key,
#   'Content-Type': 'application/json'
# }

# # Make the request
# response = requests.post("{}/api/v1/session".format(url),  payload,headers=headers)
# X_TOKEN,CST= response.headers['X-SECURITY-TOKEN'],response.headers['CST']

# url = 'wss://api-streaming-capital.backend-capital.com/connect'
# async def connect_websocket():
#     # Establish WebSocket connection
#     async with websockets.connect('wss://api-streaming-capital.backend-capital.com/connect') as websocket:
#         # Send authentication and subscription message
#         subscribe_message = {
#             'destination': 'OHLCMarketData.subscribe',
#             'correlationId': '1',
#             'cst': CST,
#             'securityToken':X_TOKEN,
#             'payload': {
#                "epics": [
#             "EURUSD"
#         ],
#         "resolutions": [
#             "MINUTE"
#         ],
#         "type": "classic"
#             }
#         }
#         await websocket.send(json.dumps(subscribe_message))

#         # Listen for incoming messages
#         for i in range(0,2):
#             message = await websocket.recv()
#             # Process the received message as needed
#             message  = json.loads(message)
#             if i >=1:
#                 print(message['payload']['h'])
            
# asyncio.get_event_loop().run_until_complete(connect_websocket())
# import csv
# with open('subscribed.csv', 'r', newline='') as csvfile:
#             reader = csv.reader(csvfile, delimiter=',')
            
#             for row in reader:
#                  print(row)
# import json
# def get_deal_references(filename):
#     with open(filename, "r") as f:
#         data = json.load(f)

#     # Get all the deal references
#     deal_references = []
#     for position in data:
#         deal_references.append(position["deal_id"])

#     return deal_references
# print(get_deal_references('deal_id.json'))
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
auth = Authentication()
x_token,cst = auth.CST_X()
web = Websocket(cst,x_token)
from queue import Queue
import os
q = Queue()
Buy = None
Sell = None
spread = None
async def async_task():
  global Buy, Sell, spread
  while True:
    
    Buy, Sell, spread = await web.subscribemarket('GOLD')
    q.put((Buy, Sell, spread))
    # Do something with data
    await asyncio.sleep(1)

def init_pygame():
  pygame.init()
  screen = pygame.display.set_mode((800, 600))
  
  font = pygame.font.Font(None, 32)
  # Pygame setup
  
  return screen, font

def run_pygame(screen, font):
  global Buy, Sell
  run = True
  while run:

    if not q.empty():
        Buy, Sell, Spread = q.get()
        print(Buy, Sell, Spread)
    buy_text = font.render(f'Buy: {Buy}', True, 'White')
    sell_text = font.render(f'Sell: {Sell}', True, 'White')  
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
        
      # Pygame event handling
    
    # Pygame render loop
    screen.fill((0,0,0))
    screen.blit(buy_text, (10, 10))
    screen.blit(sell_text, (10, 50))  
    
    pygame.display.update()
    
  pygame.quit()
  shutdown_event.cancel()

  
  
if __name__ == "__main__":


  executor = ThreadPoolExecutor()
  loop = asyncio.get_event_loop()
  loop.set_default_executor(executor)
  # Start asyncio task in thread
  t = threading.Thread(target=lambda: asyncio.run(async_task()))
  t.start()

  screen , font = init_pygame()
  run_pygame(screen, font)

  # Wait for background thread to finish
  t.join()

  loop.stop()
  loop.close()
  pygame.quit()


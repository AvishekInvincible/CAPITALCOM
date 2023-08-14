import websockets,json,asyncio
from authentication import Authentication
from extra import CSV
class Websocket():
    def __init__(self,cst,x_token):
        self.url = 'wss://api-streaming-capital.backend-capital.com/connect'
        # self.url  = 'wss://demo-api-capital.backend-capital.com/connect'
        self.cst = cst
        self.x_token = x_token
        
        # csv = CSV()
        # assets = csv.read_csv('subscribed.csv')
        # if self.asset in assets:
        #     pass
        
    
   
    async def subscribeohlc(self,asset):
        # Establish WebSocket connection
        async with websockets.connect(self.url) as websocket:
            # Send authentication and subscription message
            subscribe_message = {
                'destination': 'OHLCMarketData.subscribe',
                'correlationId': '1',
                'cst': self.cst,
                'securityToken':self.x_token,
                'payload': {
                "epics": [
                asset
            ],
            "resolutions": [
                "MINUTE"
            ],
            "type": "classic"
                }
            }
            await websocket.send(json.dumps(subscribe_message))
            i = 0 
            while  True:
                message = await websocket.recv()
                # Process the received message as needed
                message  = json.loads(message)
                if i >=1:
                    if message['payload']['priceType'] == 'bid':
                        buy =  [message['payload']['o'],message['payload']['h'],message['payload']['l'],message['payload']['c']]
                        print('Buy' , 'O', message['payload']['o'],'H' ,  message['payload']['h'],'L' ,  message['payload']['l'],'C' ,  message['payload']['c'])
                    elif message['payload']['priceType'] == 'ask':
                        sell =  [message['payload']['o'],message['payload']['h'],message['payload']['l'],message['payload']['c']]
                        print('Sell' , 'O', message['payload']['o'],'H' ,  message['payload']['h'],'L' ,  message['payload']['l'],'C' ,  message['payload']['c'])
                    return buy, sell
                i+=1
                    
    
    async def subscribemarket(self,asset):
    # Establish WebSocket connection
        async with websockets.connect(self.url) as websocket:
            # Send authentication and subscription message
            subscribe_message = {
                'destination': 'marketData.subscribe',
                'correlationId': '1',
                'cst': self.cst,
                'securityToken': self.x_token,
                "payload": {
                    "epics": [
                        asset
                    ]
                }
            }
            await websocket.send(json.dumps(subscribe_message))
            i = 0 
            while  True:
                
                message = await websocket.recv()
                if i>=1:
                    data = json.loads(message)
                    # print(data)
                    Buy = data['payload']['bid']
                    Sell = data['payload']['ofr']
                    spread = round(abs(Buy - Sell),2)
                    print('Buy: ', Buy, 'Offer: ', Sell , 'Spread: ', spread)
                    return Buy, Sell,spread
                i+=1
                

    async def run(self,asset):
        # self.subscribeohlc(asset), 
        tasks = [self.subscribeohlc(asset),self.subscribemarket(asset)]
        await asyncio.gather(*tasks)
    # def run(self,asset):
    #     # asyncio.run(self.subscribeohlc(asset))
    #     try:
    #         asyncio.run(self.subscribemarket(asset))
    #     except Exception as e:
    #         print(e)
            
    async def unsubscribe_from_all_markets(self,):
    # Establish WebSocket connection
        async with websockets.connect(self.url) as websocket:
            # Send authentication message
            authenticate_message = {
                'destination': 'Authenticate',
                'correlationId': '1',
                'cst': self.cst,
                'securityToken': self.x_token
            }
            await websocket.send(json.dumps(authenticate_message))

            # Send market data request
            market_data_request = {
                'destination': 'MarketData.unsubscribeAll',
                'correlationId': '2',
            }
            await websocket.send(json.dumps(market_data_request))

            # Listen for incoming messages
            while True:
                message = await websocket.recv()
                if 'destination' in message:
                    break




               
        # asyncio.run(connect_websocket()) need to run this

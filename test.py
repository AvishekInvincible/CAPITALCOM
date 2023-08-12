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
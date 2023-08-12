import random
import requests
import websockets 
import json
import asyncio
from key import api_key

class Authentication:
    def __init__(self):
        self.config = {
        "key": api_key,
        "url": "https://api-capital.backend-capital.com"
        # 'url': 'https://demo-api-capital.backend-capital.com'
    }
    def CST_X(self):
        """Generate a CST-X token returns X_TOKEN , CST"""
        payload = json.dumps({
            'encryptedKey':False,
        "identifier": "avisheksood01@gmail.com",
        "password": "Chand@20054"
        })

        headers = {
        'X-CAP-API-KEY': self.config['key'],
        'Content-Type': 'application/json'
        }

        # Make the request
        response = requests.post("{}/api/v1/session".format(self.config['url']),  payload,headers=headers)
        X_TOKEN,CST= response.headers['X-SECURITY-TOKEN'],response.headers['CST']
        return X_TOKEN,CST
    def close_session(self):


        # URL
       

        # Headers
        headers = {
        'X-SECURITY-TOKEN': self.CST_X()[0],
        'CST': self.CST_X()[1]
        }

        # Send DELETE request using requests
        response = requests.delete("{}/api/v1/session".format(self.config['url']),headers=headers)

        # Print the response
        print(response.text)



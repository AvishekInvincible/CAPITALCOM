import requests
import json
import random
import math
from key import api_key
class Trade():
    def __init__(self,cst,x_token,market_id, side, quantity) :
        self.cst = cst
        self.x_token = x_token
        # self.url = 'https://api-capital.backend-capital.com/api/v1/positions'
        self.url = 'https://demo-api-capital.backend-capital.com/api/v1/positions'
        self.market_id = market_id.upper()
        self.side = side.upper()
        self.quantity = quantity
        self.deal_id = None


    def create_position(self):
        """
        Creates a position in the market.

        Returns:
            The response from the API call, either the deal reference if successful or the error message.
        """
        
        payload = {
            "direction": self.side,
            "epic": self.market_id,
            "size": self.quantity,
            
        }
        headers = {
            "X-SECURITY-TOKEN": self.x_token,
            "CST": self.cst,
            "Content-Type": "application/json"
        }

        response = requests.post(self.url, json=payload, headers=headers)

        if response.status_code == 200:
            self.deal_id = response.json()['dealReference']
            xx = open('deal_id.txt','a')
            # xx.write(self.market_id ,self.deal_id)
            return response.json()
        
        else:
            return response.text



    def close_position(self):
        """
        Deletes the position associated with the current instance.

        :return: The JSON response if the deletion was successful, None otherwise.
        """
        url = "https://api-capital.backend-capital.com/api/v1/positions/{}".format(self.deal_id)
        response = requests.delete(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_positions(self):
        """
        Retrieves the positions using the provided API credentials.

        Returns:
            - If the response status code is 200, returns the response JSON.
            - Otherwise, returns None.
        """
        
        headers = {
            "X-SECURITY-TOKEN": api_key,
            "CST": self.cst,
        }

        response = requests.get(self.url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None















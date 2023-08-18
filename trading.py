import requests
import json
import random
import math
from key import api_key
class Trade():
    def __init__(self,cst,x_token) :
        self.cst = cst
        self.x_token = x_token
        self.url = 'https://api-capital.backend-capital.com/api/v1/positions'
        # self.url = 'https://demo-api-capital.backend-capital.com/api/v1/positions'
        
        self.deal_id = None


    def create_position(self,market_id,side,quantity,stop=None,profit=None,):
        self.market_id = market_id.upper()
        self.side = side.upper()
        self.quantity = quantity
        
        """
        Creates a position in the market.

        Returns:
            The response from the API call, either the deal reference if successful or the error message.
        """
        
        payload = {
            "direction": self.side,
            "epic": self.market_id,
            "size": self.quantity,
            "stopLevel": stop,
            "profitLevel": profit
            
        }
        headers = {
            "X-SECURITY-TOKEN": self.x_token,
            "CST": self.cst,
            "Content-Type": "application/json"
        }

        response = requests.post(self.url, json=payload, headers=headers)

        if response.status_code == 200:
            self.deal_id = response.json()['dealReference']
            with open('deal_id.json', "r") as f:
                data = json.load(f)

            # Append the new position to the list
            data.append({
                "quantity": self.quantity,
                "side": self.side,
                "market_id": self.market_id,
                "deal_id": self.deal_id,
            })

            # Write the updated list to the file
            with open('deal_id.json', "w") as f:
                json.dump(data, f)
            return response.json()
        
        else:
            return response.text

    # def get_deal_references(self,filename):
    #         with open(filename, "r") as f:
    #             data = json.load(f)

    #         # Get all the deal references
    #         deal_references = []
    #         for position in data:
    #             deal_references.append(position["deal_id"])

    #         return deal_references
     
    # def close_position(self):
    #     """
    #     Deletes the position associated with the current instance.

    #     :return: The JSON response if the deletion was successful, None otherwise.
    #     """
        
    #     import requests

    #     url = 'https://api-capital.backend-capital.com/api/v1/positions/o_15c1c961-b8c2-435e-a3a8-40ddea567b6d'

    #     headers = {
    #     "X-SECURITY-TOKEN": self.x_token,
    #             "CST": self.cst,
    #     }

    #     response = requests.delete(url, headers=headers)

    #     print(response.text ,response.content)
        # deals = self.get_deal_references('deal_id.json')
        # # print(deals)
        # responses = []
        # for i in range(0,len(deals)):

        #     url = "{}/{}".format(self.url,deals[i])
        #     print(url)
        # # print(deals[i])
        #     headers = {
        #         "X-SECURITY-TOKEN": self.x_token,
        #         "CST": self.cst,
                
        #     }
        #     response = requests.delete(url,headers=headers)

        #     if response.status_code == 200:
        #         responses.append((response.json()))
        #         return response.json()
        #     else:
        #         print(response.content)
        #         return response.content
        # print(responses)
        # return responses















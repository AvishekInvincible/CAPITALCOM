import requests
from authentication import Authentication
from account import Account
import json

class Sentiment():
    def __init__(self, cst, x_token):
        self.CST = cst
        self.X_TOKEN = x_token
    def get_client_sentiment(self,market_ids):
        # url = 'https://api-capital.backend-capital.com/api/v1/clientsentiment'
        url = 'https://demo-api-capital.backend-capital.com/api/v1/clientsentiment'
        headers = {
            'X-SECURITY-TOKEN': self.X_TOKEN,
            'CST': self.CST
        }
        params = {
            'marketIds': market_ids
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            client_sentiments = json.loads(json.dumps(response.json()))["clientSentiments"]

            for i in client_sentiments:
                ID = i["marketId"]
                LONG = i["longPositionPercentage"]
                SHORT = i["shortPositionPercentage"]
                return LONG,SHORT
                # return ID, LONG, SHORT

        else:
            return None




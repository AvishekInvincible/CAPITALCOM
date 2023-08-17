import requests,json
import math
class  Account():
    def __init__(self, cst, x_token):
        self.CST = cst
        self.X_TOKEN = x_token
        # self.url = 'https://api-capital.backend-capital.com/api/v1/accounts'
        self.url = 'https://demo-api-capital.backend-capital.com/api/v1/accounts'
        self.response = self._get_response()

    def _get_response(self):
        headers = {'X-SECURITY-TOKEN':self.X_TOKEN, 'CST':self.CST}
        return requests.get(self.url, headers=headers)
        
    def get_a_balance(self):
        import http.client

        conn = http.client.HTTPSConnection("demo-api-capital.backend-capital.com")
        payload = ''
        headers = {
        'X-SECURITY-TOKEN': self.X_TOKEN,
        'CST': self.CST,}
        conn.request("GET", "/api/v1/accounts", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        data = json.loads(data)
        available = data['accounts'][0]['balance']['available']
        profitLoss = data['accounts'][0]['balance']['profitLoss']
        balance = data['accounts'][0]['balance']['balance']
        
        return balance,available,profitLoss
   
    def check_tpsl(self,current_price, risk_appetite=0.6,target_price=None,stop_price=None):
        """Returns the target profit and stop loss"""
        if target_price and stop_price != None:

            quantity = 1 

            stop_loss_percentage = 0.05
            target_profit_percentage = stop_loss_percentage * 2 # Set to 2x stop loss percentage

            stop_loss_price = current_price * (1 - stop_loss_percentage)
            target_price = current_price * (1 + target_profit_percentage) 
            target_profit_price = current_price + (target_price - current_price) / quantity
        else :
            target_profit_price = target_price
            stop_loss_price = stop_price
        return target_profit_price,stop_loss_price


    def risk(self,price):
        """Returns the max quantity to buy or sell based on the current price"""
        balance = self.get_a_balance()
        max_trade = round(balance[1] * 0.2,2)
        quantity = max_trade / price
        return round(quantity,1) 

        
        

    
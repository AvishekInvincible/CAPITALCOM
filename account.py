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
        data_str = self.response.content.decode("utf-8")
        parsed_data = json.loads(data_str)
        available = parsed_data['accounts'][0]['balance']['available']
        profitLoss = parsed_data['accounts'][0]['balance']['profitLoss']
        balance = parsed_data['accounts'][0]['balance']['balance']
        return balance,available,profitLoss
   
    def check_tpsl(self,current_price, risk_appetite=0.6,target_price=None,stop_price=None):
        """Returns the target profit and stop loss"""
        
        quantity = 1 

        stop_loss_percentage = 0.05
        target_profit_percentage = stop_loss_percentage * 2 # Set to 2x stop loss percentage

        stop_loss_price = current_price * (1 - stop_loss_percentage)
        target_price = current_price * (1 + target_profit_percentage) 
        target_profit_price = current_price + (target_price - current_price) / quantity
        return target_profit_price,stop_loss_price


    def risk(self,price):
        """Returns the max quantity to buy or sell based on the current price"""
        balance = self.get_a_balance()
        print(balance[0])
        max_trade = round(balance[0] * 0.2,2)
        quantity = max_trade / price
        return round(quantity,1) 

        
        

    
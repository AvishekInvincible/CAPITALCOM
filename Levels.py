import datetime
import yfinance as yf
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Levels():
    def __init__(self,Stock) -> None:
        self.stock = Stock.upper()
        self.date = self.get_date()
    def get_levels(self):   
        print('Finding Levels...')
        # Load the data from a CSV file (replace 'data.csv' with your file path)
        data = pd.read_csv(f'data/{self.stock}.csv')


        dates = pd.to_datetime(data['Date'])
        close = data['Close']
        open = data['Open']
        try:

            first_derivative_high = np.gradient(close)


            peak_indices = np.where((first_derivative_high[:-1] > 0) & (first_derivative_high[1:] < 0))[0] + 1
            valley_indices = np.where((first_derivative_high[:-1] < 0) & (first_derivative_high[1:] > 0))[0] + 1

            # Create DataFrames for peaks and valleys
            peaks_data = pd.DataFrame({'Date': dates[peak_indices], 'Type': 'Peak', 'Price': close[peak_indices]})
            valleys_data = pd.DataFrame({'Date': dates[valley_indices], 'Type': 'Valley', 'Price': open[valley_indices]})

            # Combine peaks and valleys data into one DataFrame
            peaks_valleys_data = pd.concat([peaks_data, valleys_data], ignore_index=True)

            # Sort the combined data by date
            peaks_valleys_data = peaks_valleys_data.sort_values(by='Date')

            # Format the dates as DD-MM-YYYY
            peaks_valleys_data['Date'] = peaks_valleys_data['Date'].dt.strftime('%d-%m-%Y')

            # Save peaks and valleys data to a CSV file
            peaks_valleys_data.to_csv(f'derivatives/{self.stock}_peaks_valleys_derivative.csv', index=False)
            return list(peaks_valleys_data['Price'])
        except Exception as e:
            print(e)
    def get_date(self):
        date = str(datetime.datetime.now()).split(' ')[0]
        return date
    def get_data(self):
        print('Downloading data...')
        data = yf.download(self.stock, start="2018-01-01", end=self.date)
        data.to_csv(f'data/{self.stock}.csv')
    def check_data_if_there(self):
        dir = os.listdir('data')
        for i in dir:
            if i == f'{self.stock}.csv':
                return True
            else:
                return False
    def main(self):
        if self.check_data_if_there():
            x = self.get_levels()
            return x
            
        else:
            self.get_data()
            x = self.get_levels()
            return x
            



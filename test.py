# # import pandas as pd 
# # import numpy as np

# # data = pd.read_csv('TSLA.csv')
# # data["Gradient"] = (data["Open"] - data["Close"]) / 2

# # # Find the days where the gradient is zero
# # flat_days = data[data["Gradient"] == 0]

# # # Print the flat days
# # print(flat_days)
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# # # Load the data from a CSV file (replace 'data.csv' with your file path)
# # data = pd.read_csv('TSLA.csv')

# # # Extract relevant columns
# # dates = pd.to_datetime(data['Date'])
# # highs = data['High']
# # lows = data['Low']

# # # Calculate gradients
# # def calculate_gradients(data_series):
# #     return np.gradient(data_series)

# # gradient_highs = calculate_gradients(highs)
# # gradient_lows = calculate_gradients(lows)

# # # Set a threshold for the gradient to identify peaks and valleys
# # gradient_threshold = 0.1  # Adjust this value as needed

# # # Find the indices where gradient is near zero for peaks (positive gradient) and valleys (negative gradient)
# # peak_indices = np.where(np.abs(gradient_highs) < gradient_threshold)[0]
# # valley_indices = np.where(np.abs(gradient_lows) < gradient_threshold)[0]

# # # Create DataFrames for peaks and valleys
# # peak_data = pd.DataFrame({'Date': dates.iloc[peak_indices], 'High_Peak': highs.iloc[peak_indices]})
# # valley_data = pd.DataFrame({'Date': dates.iloc[valley_indices], 'Low_Valley': lows.iloc[valley_indices]})

# # # Merge peak and valley DataFrames on 'Date'
# # peaks_and_valleys = pd.merge(peak_data, valley_data, on='Date', how='outer')

# # # Save the peaks and valleys data to a CSV file
# # peaks_and_valleys.to_csv('peaks_and_valleys.csv', index=False)

# # print("Peaks and valleys data saved to 'peaks_and_valleys.csv'")


# # Load the data from a CSV file
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt


# # Load the data from a CSV file (replace 'data.csv' with your file path)
# data = pd.read_csv('TSLA.csv')


# dates = pd.to_datetime(data['Date'])
# highs = data['High']
# lows = data['Low']

# first_derivative_high = np.gradient(highs)


# peak_indices = np.where((first_derivative_high[:-1] > 0) & (first_derivative_high[1:] < 0))[0] + 1
# valley_indices = np.where((first_derivative_high[:-1] < 0) & (first_derivative_high[1:] > 0))[0] + 1

# # Create DataFrames for peaks and valleys
# peaks_data = pd.DataFrame({'Date': dates[peak_indices], 'Type': 'Peak', 'Price': highs[peak_indices]})
# valleys_data = pd.DataFrame({'Date': dates[valley_indices], 'Type': 'Valley', 'Price': lows[valley_indices]})

# # Combine peaks and valleys data into one DataFrame
# peaks_valleys_data = pd.concat([peaks_data, valleys_data], ignore_index=True)

# # Sort the combined data by date
# peaks_valleys_data = peaks_valleys_data.sort_values(by='Date')

# # Format the dates as DD-MM-YYYY
# peaks_valleys_data['Date'] = peaks_valleys_data['Date'].dt.strftime('%d-%m-%Y')

# # Save peaks and valleys data to a CSV file
# peaks_valleys_data.to_csv('peaks_valleys_derivative.csv', index=False)

# # Plot the data and identified peaks/valleys
# plt.figure(figsize=(10, 6))
# plt.plot(dates, highs, label='Highs', color='blue')
# plt.plot(dates, lows, label='Lows', color='red')
# plt.scatter(dates[peak_indices], highs[peak_indices], color='purple', marker='^', label='Peaks')
# plt.scatter(dates[valley_indices], lows[valley_indices], color='brown', marker='v', label='Valleys')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.title('Derivative Analysis and Peaks/Valleys')
# plt.legend()
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
# import yfinance as yf

# msft = yf.Ticker("MSFT")
# data = yf.download('TSLA', start="2018-01-01", end="2023-08-21")

# from Levels import Levels
# lev = Levels('TSLA')
# price = lev.main()
# print(price)
import cv2
import pytesseract
import numpy as np

def calculate_total(image_path):
  """
  Calculates the total of the expression in the image.

  Args:
    image_path: The path to the image file.

  Returns:
    The total of the expression.
  """

  # Read the image.
  image = cv2.imread(image_path)

  # Preprocess the image.
  image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]
  image = cv2.GaussianBlur(image, (5, 5), 0)

  # Recognize the text.
  text = pytesseract.image_to_string(image)

  # Extract the numbers.
  numbers = re.findall(r"\d+\.\d+", text)

  # Identify the red and blue numbers.
  red_numbers = []
  blue_numbers = []
  for number in numbers:
    if number[0] == "-":
      red_numbers.append(number[1:])
    else:
      blue_numbers.append(number)

  # Perform the calculation.
  total = 0
  for number in blue_numbers:
    total += float(number)
  for number in red_numbers:
    total -= float(number)

  return total


if __name__ == "__main__":
  # Get the image path from the user.
  image_path = 'Screenshot 2023-08-21 184610.png'

  # Calculate the total.
  total = calculate_total(image_path)

  print("The total is:", total)

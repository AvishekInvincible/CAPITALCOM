import requests
import csv

class CapitalAPI():
    API_KEY = "YOUR_API_KEY"

    def __init__(self, epic, from_date, to_date, max=10, resolution="MINUTE"):
        self.epic = epic
        self.from_date = from_date
        self.to_date = to_date
        self.max = max
        self.resolution = resolution

    def get_prices(self):
        url = "https://api-capital.backend-capital.com/api/v1/prices/{{epic}}?resolution={{resolution}}&max={{max}}&from={{from_date}}&to={{to_date}}"

        headers = {
            "X-SECURITY-TOKEN": "ENTER_OBTAINED_SECURITY_TOKEN",
            "CST": "ENTER_OBTAINED_CST_TOKEN",
            "apiKey": self.API_KEY,
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None

    def save_prices_to_csv(self, filename):
        prices = self.get_prices()

        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for price in prices:
                writer.writerow([price["date"], price["open"], price["high"], price["low"], price["close"], price["volume"]])


if __name__ == "__main__":
    epic = "AAPL"
    from_date = "2022-02-24T00:00:00"
    to_date = "2022-02-24T01:00:00"

    capital_api = CapitalAPI(epic, from_date, to_date)

    prices = capital_api.get_prices()

    if prices is not None:
        asset = capital_api.epic
        filename = f"{asset}_prices.csv"
        capital_api.save_prices_to_csv(filename)
        print(f"Prices for {asset} saved to {filename}")
    else:
        print("Error getting prices")

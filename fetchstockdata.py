import yfinance as yf 
import pandas as pd 

class FetchStockData:

	def __init__(self, ticker = "GSPC"):

		self.ticker = yf.Ticker(ticker)

	def fetch_latest_day_data(self):

		#This will return the last or latest trading day data
		#It will be the pandas dataframe
		#Columns: ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']


		return self.ticker.history(period = "1D").reset_index()


fetchstockdata = FetchStockData("AAPL")
print(fetchstockdata.fetch_latest_day_data())
print(fetchstockdata.fetch_latest_day_data().columns)


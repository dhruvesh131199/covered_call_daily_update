import pandas as pd
import yfinance as yf
from position import Position

##Create a that fetches the options
class FetchOptionData:

	def __init__(self, strike_price, expiry, ticker = "AAPL"):
		self.ticker = yf.Ticker(ticker)
		self.strike_price = strike_price
		self.expiry = expiry

	def pick_expiry(self):

		#This function is called on a new day
		#We pick a nearest expiry to trade and create a position
		#Set this expiry to self.expiry for this class and Position class

		expiries = pd.to_datetime(list(self.ticker.options))
		expiries = sorted(expiries)

		#Incase yahoo finance provides the expiry date which are already expired,
		#We handle it below

		if pd.Timestamp.today().strftime("%Y-%m-%d") >= expiries[0].strftime("%Y-%m-%d"):
			self.expiry = expiries[1]
		else:
			self.expiry = expiries[0]

		return self.expiry


	def pick_strike_price(self, current_price, percentage_away = 0.1):

		#This function is called on a new day
		#We select a strike price and set it to self.strike_price both for this class and Position class
		#Find the the percentage_away price from the current price
		#Fetch all the strike prices, find the difference between strikes and derived percentage away price
		#Pick the strike price with the lowest difference

		rough_strike_price = current_price + current_price * percentage_away
		option_chain = self.ticker.option_chain(self.expiry.strftime("%Y-%m-%d"))
		option_chain = option_chain.calls
		option_chain["diff_from_rough_strike_price"] = abs(option_chain["strike"] - rough_strike_price)
		lowest_diff = option_chain["diff_from_rough_strike_price"].min()

		option_chain = option_chain[option_chain["diff_from_rough_strike_price"] == lowest_diff].head(1)

		self.strike_price = option_chain.iloc[0]["strike"]
		return self.strike_price

	def fetch_strike_data(self):

		#This function is called on a new day and days before expiry
		#We already have expiry and strike price from expiry date
		#This will only return the details of the contract we are interested in
		#It will be a dataframe, user can fetch any details such as bid, ask, IV with iloc[0]["column name"]

		#This are the columns in the dataframe
		#['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask',
        #'change', 'percentChange', 'volume', 'openInterest',
        #'impliedVolatility', 'inTheMoney', 'contractSize', 'currency']

		option_chain = self.ticker.option_chain(self.expiry.strftime("%Y-%m-%d"))
		option_chain = option_chain.calls
		option_chain = option_chain[option_chain["strike"] == self.strike_price]

		return option_chain.round(2)

	def fetch_atm_data(self):

		#This function is used to return option chain data of the ATM strike price
		#Can be used to select strike price to trade from implied volatility

		option_chain = self.ticker.option_chain(self.expiry.strftime("%Y-%m-%d"))
		option_chain = option_chain.calls
		option_chain = option_chain[option_chain["inTheMoney"] == False]
		option_chain = option_chain.sort_values(by = "strike")
		option_chain = option_chain.head(1)

		return option_chain.round(2)

#testing
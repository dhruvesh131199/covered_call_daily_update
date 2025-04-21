import yfinance as yf 
import pandas as pd
from fetchoptiondata import FetchOptionData
from fetchstockdata import FetchStockData
from math import sqrt

#This class will be used to manage the position and return an updated position to save on position.csv file

class PositionManager:

	def __init__(self, position):
		self.position = position


	def create_a_new_position(self, fetch_option_data, fetch_stock_data):
		stock_qty = self.position.stk_qty
		stock_data = fetch_stock_data.fetch_latest_day_data()
		stock_open_price = stock_data.iloc[0]["Open"]

		if stock_qty == 0:
			self.position.buy_stocks(stock_open_price)

		#Selecting a strike price
		expiry = fetch_option_data.pick_expiry() #We always need to first pick the expiry

		option_data_atm = fetch_option_data.fetch_atm_data()
		implied_vol = option_data_atm.iloc[0]["impliedVolatility"]

		days_to_next_expiry = (expiry - pd.Timestamp.today()).days
		vol_till_next_expiry = (implied_vol * sqrt(days_to_next_expiry/252) ) + 0.01

		strike_price = fetch_option_data.pick_strike_price(stock_data.loc[0]["Close"], percentage_away = vol_till_next_expiry)
		option_data_strike = fetch_option_data.fetch_strike_data()

		option_bid_price = option_data_strike.iloc[0]["bid"]       #We can sell at bidding price

		#sell the option
		self.position.sell_option(option_bid_price, strike_price, expiry)

		#We only create a new position on a new day, so once the new days is over
		#We set isNewDay as False, next day when we do data calculation, we don't create a new position

		self.position.isNewDay = False

	def close_position(self, fetch_option_data, fetch_stock_data):

		stock_close = fetch_stock_data.fetch_latest_day_data().iloc[0]["Close"]

		opt_realized = self.position.calculate_opt_realised()
		stk_realized = 0

		#if stock price crossed the strike price, then realise the stock profit
		if stock_close > self.position.strike_price:
			stk_realized = self.position.calculate_stk_realised()

		self.position.isNewDay = True
		return (stk_realized, opt_realized)

	def update_unrealized(self, fetch_option_data, fetch_stock_data):
		self.position.calculate_stk_unrealised(fetch_stock_data.fetch_latest_day_data().iloc[0]["Close"])
		self.position.calculate_opt_unrealised(fetch_option_data.fetch_strike_data().iloc[0]["ask"])
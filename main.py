import pandas as pd 
import yfinance as yf 
from fetchoptiondata import FetchOptionData
from position import Position
from fetchstockdata import FetchStockData
from math import sqrt

#On a new day(Day after last expiry) we create a new position
#If we had to sell our equity, we need to buy the equity again at a new price
#To choose a strike price, we will use the IV of ATM option, and find the volatility till next expiry
#Volatility = IV * SQRT(days to next expiry / 252) + 1 (We add 1% just for the safety)
def create_a_new_position(position, fetch_option_data, fetch_stock_data):

	stock_qty = position.stk_qty
	stock_data = fetch_stock_data.fetch_latest_day_data()
	stock_open_price = stock_data.iloc[0]["Open"]

	if stock_qty == 0:
		position.buy_stocks(stock_open_price)

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
	position.sell_option(option_bid_price, strike_price, expiry)

	#print the position detail
	position.print_attributes()

	is_new_day = False



#create the first position and save to csv
#Latest position is fetched from the position csv file
position = Position.fetch_last_position()
for i in range(5):
	position.print_attributes()
	position.balance += 10000
	print("-----------------------------------------")
	position.update_position_file()

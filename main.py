import pandas as pd 
import yfinance as yf 
from fetchoptiondata import FetchOptionData
from position import Position
from fetchstockdata import FetchStockData
from positionmanager import PositionManager
from math import sqrt

def main():
    
    #We create all the class instances
	position = Position.fetch_last_position()
	fetch_option_data = FetchOptionData(position.strike_price, position.opt_expiry, ticker = position.ticker)
	fetch_stock_data = FetchStockData(ticker = position.ticker)
	position_manager = PositionManager(position)

	#Fetch the latest trading data date
	latest_date = pd.Timestamp(fetch_stock_data.fetch_latest_day_data().iloc[0]["Date"]).date()

	#Check if the position is already updated today or not
	if position.date.strftime("%Y-%m-%d") == latest_date.strftime("%Y-%m-%d"):
		print("The position is already updated today/for last trading day")
		print("#############################################")
		return

	position.date = latest_date   #Set the position date to today's date/latest date since we will update the file

	#Create a new position if it is a new day
	if position.isNewDay:
		position_manager.create_a_new_position(fetch_option_data, fetch_stock_data)

	#Close the position if it an expiry day
	stk_realized = 0
	opt_realized = 0
	if position.opt_expiry.strftime("%Y-%m-%d") == pd.Timestamp.today().strftime("%Y-%m-%d"):
		stk_realized, opt_realized = position_manager.close_position(fetch_option_data, fetch_stock_data)

	position_manager.update_unrealized(fetch_option_data, fetch_stock_data)

	position = position_manager.position   #update the position, it is updated in the position_manaeger
	position.update_position_file()

	#Summary sheet creation
	summary_dict = {
	"Date": position.date.strftime("%Y-%m-%d"),
	"Ticker": position.ticker,
	"Stock_qty": position.stk_qty,
	"Stock_buy_price": position.stk_buy_price,
	"Stock_close_price": fetch_stock_data.fetch_latest_day_data().iloc[0]["Close"],
	"Option_strike": position.strike_price,
	"Option_expiry": position.opt_expiry,
	"Option_qty": position.opt_qty,
	"Option_sell_price": position.opt_sell_price,
	"Option_ask_price": fetch_option_data.fetch_strike_data().iloc[0]["ask"],
	"Stock_unrealized": position.stk_unrealised,
	"Option_unrealized": position.opt_unrealised,
	"Total_unrealized": position.stk_unrealised + position.opt_unrealised,
	"Stock_realized": stk_realized,
	"Option_realized": opt_realized,
	"Total_realized": stk_realized + opt_realized
	}

	summary = pd.DataFrame([summary_dict])
	summary = summary.round(2)
	summary.to_csv("summary.csv", mode = "a", header = False, index = False)


if __name__ == "__main__":
	main()
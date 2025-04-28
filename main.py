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
		print("It's new day")
		print("We sell new option contract")
		position_manager.create_a_new_position(fetch_option_data, fetch_stock_data)

	#Close the position if it an expiry day
	stk_realized = 0
	opt_realized = 0

	if position.opt_expiry.strftime("%Y-%m-%d") == pd.Timestamp.today().strftime("%Y-%m-%d"):
		print("It is an expiry day")
		print("We realise the profit and loss")
		stk_realized, opt_realized = position_manager.close_position(fetch_option_data, fetch_stock_data)

	position_manager.update_unrealized(fetch_option_data, fetch_stock_data)

	position = position_manager.position   #update the position, it is updated in the position_manaeger
	position.update_position_file()
	print("Updated the position file")

	#Summary sheet creation
	if position.isNewDay:
		option_ask_price = 0
	else:
		option_ask_price = fetch_option_data.fetch_strike_data().iloc[0]["ask"]

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
	"Option_ask_price": option_ask_price,
	"Stock_unrealized": position.stk_unrealised,
	"Option_unrealized": position.opt_unrealised,
	"Total_unrealized": position.stk_unrealised + position.opt_unrealised,
	"Stock_realized": stk_realized,
	"Option_realized": opt_realized,
	"Total_realized": stk_realized + opt_realized
	}

	summary = pd.DataFrame([summary_dict])
	summary = summary.round(2)
	summary.to_csv("sheets/summary.csv", mode = "a", header = False, index = False)
	print("Updated the summary file")

	#Let's save the ATM implied volatility each day, not on expiry day because it is zero
	if position.isNewDay == False:
		fetch_option_data.pick_expiry()
		option_data_atm = fetch_option_data.fetch_atm_data()
		implied_vol = option_data_atm.iloc[0]["impliedVolatility"]
		days_till_next_expiry = (pd.Timestamp(fetch_option_data.expiry) - pd.Timestamp.today()).days
		volatility_till_expiry = (implied_vol * sqrt(days_till_next_expiry/252))

		volatility_dict = {
		"Date": position.date.strftime("%Y-%m-%d"),
		"Implied_volatility": implied_vol,
		"Days_till_expiry": int(days_till_next_expiry) + 1,
		"volatility_till_expiry": volatility_till_expiry
		}
		volatility = pd.DataFrame([volatility_dict])
		volatility = volatility.round(2)
		volatility.to_csv("sheets/volatility.csv", mode = "a", header = False, index = False)
		print("Updated the volatility file")
	else:
		print("Volatility sheet is not updated on expiry day")


if __name__ == "__main__":
	main()

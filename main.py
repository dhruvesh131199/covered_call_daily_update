import yfinance as yf
import pandas as pd 

##Create a class that tracks the position at any given time
##This will also contain methods to modify positions

class Position:

	def __init__(self, ticker = "GSPC", strike_price = 0.00, balance = 10000, stk_qty = 0, opt_qty = 0, opt_sell_price = 0, stk_buy_price = 0, stk_unrealised = 0, stk_realised = 0, opt_unrealised = 0, opt_realised = 0, lot_size = 0):
		self.ticker = ticker
		self.strike_price = strike_price
		self.balance = balance
		self.stk_qty = stk_qty
		self.opt_qty = opt_qty
		self.opt_sell_price = opt_sell_price
		self.stk_buy_price = stk_buy_price
		self.stk_unrealised = stk_unrealised
		self.opt_unrealised = opt_unrealised
		self.lot_size = lot_size

	def print_attributes(self):
		for key, value in self.__dict__.items():
			print(f"{key} = {value}")

	def buy_stocks(self, buy_price):
		#This method is called whenever we buy stocks
		#calculate the qty, it will be the floor value of balance//buyprice

		self.stk_buy_price = buy_price
		self.stk_qty += self.balance // self.stk_buy_price
		self.balance -= (self.stk_qty*self.stk_buy_price)

	def calculate_stk_unrealised(self, current_price):
		#we only calculate unrealised when stk_qty is greater than 0
		#It is simply qty*(current_price - buy_price)

		if self.stk_qty > 0:
			self.stk_unrealised = self.stk_qty*(current_price - self.stk_buy_price)

	def calculate_stk_realised(self):
		#Whenever a stock is sold, we return the realised gain
		#Since we always close the whole position in this strategy
		#In this strategy, we only close the stock position when price breaches strike price on expiry
		#It would be qty*(sell_price-buy_price)
		#Once it is realised, we update stk_qty, balance and buy_price, stk_unrealised

		realised = self.stk_qty*(self.strike_price - self.stk_buy_price)
		self.balance += self.stk_qty*self.strike_price
		self.stk_qty = 0
		self.stk_buy_price = 0
		self.stk_unrealised = 0

		return realised

	def sell_option(self, sell_price):
		#This method is called to create a short position in option
		#The qty would be the multiple of lot size and <= stk_qty
		#We can only short option if stk_qty>=lot_size

		if self.stk_qty>=self.lot_size:
			sold_lots = self.stk_qty // self.lot_size
			self.opt_qty = -1 * (sold_lots * self.lot_size)
			self.opt_sell_price = sell_price
		else:
			print("You need to buy stocks first to short option")

	def calculate_opt_unrealised(self, current_price):
		#we only calculate unrealised when opt_qty is less than 0
		#It is simply qty*(sell_price - current_price)

		if self.opt_qty < 0:
			self.opt_unrealised = abs(self.opt_qty)*(self.opt_sell_price - current_price)

	def calculate_opt_realised(self):
		#In this strategy, we never excersise the option
		#On each expiry, we collect the whole premium and add it to the realised gain
		#We update opt_qty, balance and opt_price, opt_unrealised, strike_price

		realised = abs(self.opt_qty)*(self.opt_sell_price)
		self.balance += realised
		self.opt_qty = 0
		self.opt_sell_price = 0
		self.opt_unrealised = 0
		self.strike_price = 0

		return realised


#test it
position = Position(ticker = "AAPL", strike_price = 270.00, lot_size = 10)
position.buy_stocks(240.00)
position.sell_option(2.00)
position.calculate_stk_unrealised(200.00)
position.calculate_opt_unrealised(1)
print("-----------------------------------------")
print("-----------------------------------------")
position.print_attributes()
print("-----------------------------------------")

position.calculate_stk_unrealised(245)
position.calculate_opt_unrealised(1.5)
position.print_attributes()
print("-----------------------------------------")

position.calculate_opt_realised()
position.print_attributes()

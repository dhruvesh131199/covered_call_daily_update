import pandas as pd
import matplotlib.pyplot as plt

def plot_investment_vs_strategy_graph():
	position = pd.read_csv("sheets/position.csv")
	summary = pd.read_csv("sheets/summary.csv")

	"""
	To calculate portfolio value if we just had invested money in apple without
	following the covered call strategy
	Portfolio value = (close price * 258.0) + 136.79
	Why 258 and 136.79? (Because we bought 258 shares qty at 193.27, and
	we were left with balance of 136.79 from inital balance of 50000.45)
	"""

	"""
	To calculate portfolio value if we follow the covered call strategy,
	Then, we always have either unrealised or realised profit/loss
	To calculate portfolio value, we use the following formula
	Stock investment value + Option profit/Loss + Balance
	"""

	"""
	We merge the position and summary sheet on the basis of date
	Only keep the required columns
	Create two new columns for the portfolio value(One for simple investment and one with the strategy)
	Plot the graph
	"""

	position = position[['date', 'balance']]
	summary = summary[['Date', 'Stock_close_price', 'Stock_qty', 'Option_unrealized']]

	merged_df = position.merge(summary, left_on = "date", right_on = "Date", how = "inner")
	merged_df["simple_investing_portfolio"] = (merged_df["Stock_close_price"] * 258.0) + 136.79
	merged_df["covered_call_strategy_portfolio"] = (merged_df["Stock_close_price"] * merged_df["Stock_qty"]) + merged_df["Option_unrealized"] + merged_df["balance"]

	last_portfolio_value_investing = merged_df['simple_investing_portfolio'].iloc[-1]
	last_portfolio_value_strategy = merged_df['covered_call_strategy_portfolio'].iloc[-1]

	investment_returns = round(((last_portfolio_value_investing - 50000.45)/50000.45)*100 ,2)
	strategy_returns = round(((last_portfolio_value_strategy - 50000.45)/50000.45)*100, 2)


	# Make sure 'date' is a datetime column
	merged_df['date'] = pd.to_datetime(merged_df['date'])

	# Plot
	plt.figure(figsize=(10, 5))
	plt.plot(merged_df['date'], merged_df['simple_investing_portfolio'], label=f'Simply buying the stock: Returns: {investment_returns}%', marker='o')
	plt.plot(merged_df['date'], merged_df['covered_call_strategy_portfolio'], label=f'Following the covered call strategy: Returns: {strategy_returns}%', marker='x')

	# Styling
	plt.xlabel('Date')
	plt.ylabel('Portfolio value')
	plt.title('Stock Close Price and Option Unrealized Over Time')
	plt.legend(loc='upper left')
	plt.grid(True)
	plt.xticks(rotation=45)

	plt.tight_layout()

	plt.savefig('sheets/Strategy_vs_Investment_Returns.png')
	plt.close()
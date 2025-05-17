# Auto Daily Covered Call Backtester

A project that automatically fetches live market data each day to perform forward-style backtesting of the covered call strategy.
It updates a CSV file and a performance graph (in the sheets/ folder), allowing you to compare the strategy’s results against a simple buy-and-hold investment in the stock.

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Logic flow](#logic-flow)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Features

- Automatically updates the CSV file each day for the position and the summary of the strategy.
- Automatically updates the graph to compare the strategy against the simple investment.
- Tracks stock price, option position, and unrealized and realized P/L.
- Designed specifically for covered call strategies.
- Simple and extendable Python codebase.

## Demo
- Daily jobs on GitHub action workflow to update CSV files and the graph

![screenshots](screenshots/daily1.JPG)
![screenshots](screenshots/dailyjob2.JPG)

- Position file

![screenshots](screenshots/position.JPG)

- Summary file

![screenshots](screenshots/summary.JPG)

- Covered Call vs Investment Graph

![screenshots](sheets/Strategy_vs_Investment_Returns.png)

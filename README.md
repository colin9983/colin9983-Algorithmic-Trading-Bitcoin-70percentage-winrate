# colin9983-Algorithmic-Trading-Bitcoin-70percentage-winrate
This project is an algorithmic trade with high returns and a high win rate. Users need to have an account through the Binance exchange and access to the API

# Backtesting returns
The average win rate in the backtesting is 71% in past six months, meaning that 71 out of 100 trades will result in a positive return. The rate of return for a month is 17%! It also has a much higher Sharpe rate than the S&P500.

# Recommanded
The trading system is strongly recommended for OS on a Linux with 24-hour power enviroment because it is an auto trading :)

# Strategy
This algorithmic trading strategy is based on capturing the five most recent K-lines of BTCUSDT, with the highest and lowest price being the most likely entry and exit points.

Entry point:Buy if the current price is below the last five K-lines, short if the current price is higher than the high of the last five k-lines.
Stop loss:1.5%

# Requirements
Libraries:
numpy
pandas
pandas_datareader
datetime
matplotlib.pyplot
seaborn
ta
time
pytz
datetime
requests
binance_f
json








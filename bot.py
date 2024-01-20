from config import ALPACA_CREDS

from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader 
from datetime import datetime

print(ALPACA_CREDS)
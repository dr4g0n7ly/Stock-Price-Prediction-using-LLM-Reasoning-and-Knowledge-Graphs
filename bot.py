from config import ALPACA_CREDS

from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader 
from datetime import datetime


class MLTrader(Strategy):
    def initialize(self, symbol:str="SPY"):
        self.symbol = symbol
        pass
    def on_trading_iteration(self):
        pass

start_date = datetime(2023, 12, 15)
end_date = datetime(2023, 12, 31)

broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlstrat', broker=broker,  parameters={"symbol":"SPY"})
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={}
)
from datetime import datetime

from lumibot.backtesting import BacktestingBroker, YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.traders import Trader

class TradeStrategy(Strategy):
    def initialize(self, symbol:str="UNH", cash_at_risk:float=.5):
        self.symbol = symbol
        self.cash_at_risk = cash_at_risk
        self.sleeptime = "24H"
        self.last_trade = None

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        
    def on_trading_iteration(self):
        if self.last_trade==None:
            order = self.create_order(
                self.symbol,
                10,
                "buy",
                type="market"
            )
            self.submit_order(order)
            self.last_trade="buy"


# Pick the dates that you want to start and end your backtest
# and the allocated budget
backtesting_start = datetime(2020, 12, 12)
backtesting_end = datetime(2020, 12, 21)

# Run the backtest
trader = Trader(backtest=True)
data_source = YahooDataBacktesting(
    datetime_start=backtesting_start,
    datetime_end=backtesting_end,
)
broker = BacktestingBroker(data_source)
strat = TradeStrategy(
    broker=broker
)
trader.add_strategy(strat)
trader.run_all()
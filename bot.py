from config import API_KEY, API_SECRET, BASE_URL

from lumibot.backtesting import BacktestingBroker, YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.traders import Trader

from alpaca_trade_api import REST

from datetime import datetime
from timedelta import Timedelta

class TradeStrategy(Strategy):
    def initialize(self, symbol:str="SPY", cash_at_risk:float=.5):
        self.symbol = symbol
        self.cash_at_risk = cash_at_risk
        self.sleeptime = "24H"
        self.last_trade = None
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price)
        return cash, last_price, quantity
        
    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')
    
    def get_news(self):
        today, p3_date = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=p3_date, end=today)
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        return news
    
    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        if cash > last_price:
            if self.last_trade==None:
                news = self.get_news()
                print(news)
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price*1.20,
                    stop_loss_price=last_price*.95
                )
                self.submit_order(order)
                self.last_trade="buy"


# Pick the dates that you want to start and end your backtest
# and the allocated budget
backtesting_start = datetime(2020, 12, 21)
backtesting_end = datetime(2020, 12, 31)

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
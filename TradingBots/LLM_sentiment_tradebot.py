from datetime import datetime

from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
import pandas as pd

stock = "TSLA"
# A simple strategy that buys AAPL on the first day and hold it
class MyStrategy(Strategy):

    def initialize(self, symbol:str=stock, cash_at_risk:float=.4): 
        self.symbol = symbol
        self.sleeptime = "24H" 
        self.last_trade = None 
        self.cash_at_risk = cash_at_risk
    
    def position_sizing(self): 
        cash = self.get_cash() 
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity
    
    def get_sentiment(self): 
        today = self.get_datetime().strftime('%Y-%m-%d')
        df = pd.read_csv('modified_tesla_news_with_output.csv')
        print("\n", str(today))
        filtered_row = df[df['date'] == str(today)]
        if not filtered_row.empty:
            confidence = filtered_row['confidence_score'].values[0]
            print(" confidence:", confidence)
            return  confidence
        else:
            print("No data found for the given date.")
            return  5

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing() 
        confidence = self.get_sentiment()

        if cash > last_price: 
            if confidence > 7: 
                if self.last_trade == "sell": 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "buy", 
                    type="bracket", 
                    take_profit_price=last_price*1.20, 
                    stop_loss_price=last_price*.95
                )
                self.submit_order(order) 
                self.last_trade = "buy"
            elif confidence < 5: 
                if self.last_trade == "buy": 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "sell", 
                    type="bracket", 
                    take_profit_price=last_price*.8, 
                    stop_loss_price=last_price*1.05
                )
                self.submit_order(order) 
                self.last_trade = "sell"


# Pick the dates that you want to start and end your backtest
# and the allocated budget
backtesting_start = datetime(2022, 1, 20)
backtesting_end = datetime(2023, 8, 10)

# Run the backtest
MyStrategy.backtest(
    YahooDataBacktesting,
    backtesting_start,
    backtesting_end,
    benchmark_asset=stock
)
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
        df = pd.read_csv('tesla_news_with_sentiment.csv')
        print("\n", str(today))
        filtered_row = df[df['date'] == str(today)]
        if not filtered_row.empty:
            probability = filtered_row['probability'].values[0]
            sentiment = filtered_row['sentiment'].values[0]
            print("Probability:", probability)
            print("Sentiment:", sentiment)
            return  probability, sentiment
        else:
            print("No data found for the given date.")
            return  0, "neutral"

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing() 
        probability, sentiment = self.get_sentiment()

        if cash > last_price: 
            if sentiment == "positive" and probability > .7: 
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
            elif sentiment == "negative" and probability > .7: 
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
backtesting_start = datetime(2022, 1, 1)
backtesting_end = datetime(2023, 8, 20)

# Run the backtest
MyStrategy.backtest(
    YahooDataBacktesting,
    backtesting_start,
    backtesting_end,
    benchmark_asset=stock
)
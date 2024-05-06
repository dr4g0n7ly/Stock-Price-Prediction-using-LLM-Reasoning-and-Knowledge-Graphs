# change only this variable
# change it to the file name of the csv file containing the news
# make sure to NOT ADD .csv
FILENAME = 'tesla_news'
stock = "TSLA"

from datetime import datetime

from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
import pandas as pd


target_file = FILENAME+'_with_sentiment.csv'
df = pd.read_csv(target_file)

# A simple strategy that buys AAPL on the first day and hold it
class SentimentAnalysis(Strategy):

    def initialize(self, symbol:str=stock, cash_at_risk:float=.4): 
        self.symbol = symbol
        self.sleeptime = "24H" 
        self.last_trade = None 
        self.cash_at_risk = cash_at_risk
    
    def position_sizing(self): 
        cash = self.get_cash() 
        last_price = self.get_last_price(self.symbol)
        if cash < 1000:
            self.cash_at_risk=0.9
        else:
            self.cash_at_risk=0.4
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity
    
    def get_sentiment(self): 
        today = self.get_datetime().strftime('%Y-%m-%d')

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
                    take_profit_price=last_price*1.5, 
                    stop_loss_price=last_price*.85
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
                    take_profit_price=last_price*1.5, 
                    stop_loss_price=last_price*.85
                )
                self.submit_order(order) 
                self.last_trade = "sell"

backtesting_start = datetime(2022, 1, 11)
backtesting_end = datetime(2024, 3, 31)

# Run the backtest
SentimentAnalysis.backtest(
    YahooDataBacktesting,
    backtesting_start,
    backtesting_end,
    benchmark_asset=stock
)
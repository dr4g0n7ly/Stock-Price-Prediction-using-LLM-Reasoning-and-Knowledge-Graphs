FILENAME = "tesla_news_2"
stock = "TSLA"

# FILENAME = "nvdia_news"
# stock = "NVDA"

# FILENAME = "apple_news"
# stock = "AAPL"

# FILENAME = "amd_news"
# stock = "AMD"

# FILENAME = "google_news"
# stock = "GOOG"

# FILENAME = "msft_news"
# stock = "MSFT"

from datetime import datetime, timedelta

from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy

import pandas as pd
df = pd.read_csv(FILENAME+'_with_confidence.csv')


# A simple strategy that buys AAPL on the first day and hold it
class LLM_Reasoning(Strategy):

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
        today = self.get_datetime()
        yesterday = today - timedelta(days=1)
        filtered_row = df[df['date'] == str(today.strftime('%Y-%m-%d'))]
        if not filtered_row.empty:
            confidence = filtered_row['confidence'].values[0]
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
                    take_profit_price=last_price*1.5, 
                    stop_loss_price=last_price*.85
                )
                self.submit_order(order) 
                self.last_trade = "buy"
            elif confidence < 3: 
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


# Pick the dates that you want to start and end your backtest
# and the allocated budget
backtesting_start = datetime(2022, 1, 11)
backtesting_end = datetime(2024, 3, 31)

# Run the backtest
LLM_Reasoning.backtest(
    YahooDataBacktesting,
    backtesting_start,
    backtesting_end,
    benchmark_asset=stock
)
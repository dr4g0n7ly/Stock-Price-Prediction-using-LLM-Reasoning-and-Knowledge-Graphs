from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader

ALPACA_CONFIG = {
     # Put your own Alpaca key here:
     "API_KEY": "PKKT9FMTI8QS1DK0QDEX",
     # Put your own Alpaca secret here:
     "API_SECRET": "ihN5QmFZf3HY08BjaI5d38OlUv7VaRY1J1D",
     # If you want to go live, you must change this. It is currently set for paper trading
     "ENDPOINT": "https://paper-api.alpaca.markets"
 }


# A simple strategy that buys AAPL on the first day and hold it
class MyStrategy(Strategy):
   def on_trading_iteration(self):
      if self.first_iteration:
            aapl_price = self.get_last_price("AAPL")
            quantity = self.portfolio_value // aapl_price
            order = self.create_order("AAPL", quantity, "buy")
            self.submit_order(order)


trader = Trader()
broker = Alpaca(ALPACA_CONFIG)
strategy = MyStrategy(broker=broker)

# Run the strategy live
trader.add_strategy(strategy)
trader.run_all()
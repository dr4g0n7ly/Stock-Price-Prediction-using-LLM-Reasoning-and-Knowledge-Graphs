import alpaca_trade_api as tradeapi
from config import BASE_URL, API_KEY, API_SECRET

api = tradeapi.REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)
news = api.get_news(symbol='TSLA', start="2023-06-08",end="2023-06-09", limit=5, min_match_score=7, filter_entities=True)
news = [ev.__dict__["_raw"]["headline"] for ev in news]

print("News for TSLA:")
print(news)


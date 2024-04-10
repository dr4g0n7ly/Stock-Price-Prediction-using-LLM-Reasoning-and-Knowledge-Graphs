import pandas as pd
from marketaux_news import get_news
from datetime import datetime, timedelta 
from config import MARKETAUX_KEY_1, MARKETAUX_KEY_2

api_token = MARKETAUX_KEY_2
symbols = 'NVDA'

start_date = datetime.strptime('2023-03-31', '%Y-%m-%d')
num_days = 95

try:
    df = pd.read_csv('nvdia_news.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=['date', 'news'])
for i in range(0, num_days):
    publish_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
    summary = str(get_news(api_token, symbols, publish_date))
    new_df = pd.DataFrame({"date": [publish_date], "news": [summary]})
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv('nvdia_news.csv', index=False)
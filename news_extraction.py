import pandas as pd
from marketaux_news import get_news
from datetime import datetime, timedelta 
from config import MARKETAUX_KEY

api_token = MARKETAUX_KEY
symbols = 'TSLA'

start_date = datetime.strptime('2023-02-20', '%Y-%m-%d')
num_days = 95


try:
    df = pd.read_csv('tesla_news.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=['date', 'news'])

for i in range(0, num_days):
    publish_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
    summary = get_news(api_token, symbols, publish_date)
    new_df = pd.DataFrame({"date": [publish_date], "news": [summary]})
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv('tesla_news.csv', index=False)



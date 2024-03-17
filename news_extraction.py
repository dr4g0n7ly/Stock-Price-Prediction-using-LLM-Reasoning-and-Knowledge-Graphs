import pandas as pd
from marketaux_news import get_news
from datetime import datetime, timedelta 
from config import MARKETAUX_KEY

api_token = MARKETAUX_KEY
symbols = 'TSLA'
<<<<<<< HEAD
start_date = datetime.strptime('2022-03-22', '%Y-%m-%d')
num_days = 55
=======
start_date = datetime.strptime('2022-01-01', '%Y-%m-%d')
num_days = 80
>>>>>>> a6bce7b990a04915ec38f661b8ce46c7b12b93ba

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



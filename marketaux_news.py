import requests
from timedelta import Timedelta
from finbert_utils import estimate_sentiment 
from config import MARKETAUX_KEY


def get_news(api_token, symbols, publish_date, filter_entities=True, language='en'):
    url = f"https://api.marketaux.com/v1/news/all?symbols={symbols}&filter_entities={filter_entities}&published_on={publish_date}&language={language}&api_token={api_token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

api_token = MARKETAUX_KEY

# Example usage:
symbols = 'TSLA'
news_data = get_news(api_token, symbols, publish_date='2024-01-02')

highlights = []

for item in news_data['data']:
    for entity in item['entities']:
        if entity['symbol'] == 'TSLA':
            for highlight in entity['highlights']:
                highlights.append(highlight['highlight'].replace('<em>', '').replace('</em>', ''))

if news_data:
   print('\n'.join(highlights)) # This will print the retrieved news data

   probability, sentiment = estimate_sentiment(highlights)
   print("SENTIMENT: ",  sentiment, " - ", probability)

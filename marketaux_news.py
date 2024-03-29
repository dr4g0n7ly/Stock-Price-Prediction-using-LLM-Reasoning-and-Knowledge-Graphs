import requests

def get_news(api_token, symbols, publish_date, filter_entities=True, limit=5, language='en'):
    url = f"https://api.marketaux.com/v1/news/all?symbols={symbols}&filter_entities={filter_entities}&published_on={publish_date}&language={language}&limit={limit}&api_token={api_token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        highlights = []
        for item in news_data['data']:
            for entity in item['entities']:
                if entity['symbol'] == 'TSLA':
                    for highlight in entity['highlights']:
                        highlights.append(highlight['highlight'].replace('<em>', '').replace('</em>', ''))

        return highlights
    else:
        print(f"Error: {response.status_code}")
        return None

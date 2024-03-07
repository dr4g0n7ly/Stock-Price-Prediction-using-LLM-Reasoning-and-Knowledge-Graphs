from newspaper import Article

def extract_text_from_url(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

# Replace 'url' with the URL of the article you want to extract text from
url = 'https://www.benzinga.com/markets/options/23/06/32784185/10-consumer-discretionary-stocks-with-whale-alerts-in-todays-session'
article_text = extract_text_from_url(url)
print(article_text)
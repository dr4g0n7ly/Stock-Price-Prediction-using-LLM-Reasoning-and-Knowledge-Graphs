import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('tesla_news_with_sentiment.csv')

# Assuming 'date' column is in yyyy-mm-dd format
desired_date = '2022-01-01'  # Replace this with the date you have

# Filter the DataFrame to get the row with the desired date
filtered_row = df[df['date'] == desired_date]

if not filtered_row.empty:
    # Retrieve the probability and sentiment
    probability = filtered_row['probability'].values[0]
    sentiment = filtered_row['sentiment'].values[0]

    print("Probability:", probability)
    print("Sentiment:", sentiment)
else:
    print("No data found for the given date.")
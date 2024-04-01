from finbert_utils import estimate_sentiment
import os
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('tesla_news.csv')

# Define the batch size (number of rows to process before saving)
batch_size = 10

# Check if there's a checkpoint file to resume from
checkpoint_file = 'sentiment_checkpoint.txt'
start_index = 0
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as f:
        start_index = int(f.read())

# Process the DataFrame in batches and periodically save the CSV file
for i in range(start_index, len(df)):
    news = df.at[i, 'news']
    prob, sentiment = estimate_sentiment(news[1:1000])
    print(news[1:10], prob.item(), sentiment)
    df.at[i, 'probability'] = prob.item()
    df.at[i, 'sentiment'] = sentiment
    
    # Check if it's time to save the CSV file
    if (i + 1) % batch_size == 0:
        # Save the DataFrame to a CSV file with the new column
        df[:i+1].to_csv('tesla_news_with_sentiment.csv', index=False)
        
        # Update the checkpoint file with the index of the last processed row
        with open(checkpoint_file, 'w') as f:
            f.write(str(i + 1))
        
        print(f"Saved {i + 1} rows.")

# Save the remaining rows
df.to_csv('tesla_news_with_sentiment.csv', index=False)
print(f"Total {len(df)} rows processed and saved.")

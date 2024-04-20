# change only this variable
# change it to the file name of the csv file containing the news
# make sure to NOT ADD .csv
FILENAME = 'tesla_news' 

import os
import pandas as pd

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
device = "cuda:0" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["positive", "negative", "neutral"]

def estimate_sentiment(news):
    if news:
        tokens = tokenizer(news, return_tensors="pt", padding=True).to(device)

        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])[
            "logits"
        ]
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        probability = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]
        return probability, sentiment
    else:
        return 0, labels[-1]
    
# Load the CSV file into a pandas DataFrame
df = pd.read_csv(FILENAME+".csv")

# Define the batch size (number of rows to process before saving)
batch_size = 10

# Check if there's a checkpoint file to resume from
checkpoint_file = FILENAME+'checkpoint.txt'
start_index = 0
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as f:
        start_index = int(f.read())

# Process the DataFrame in batches and periodically save the CSV file
for i in range(start_index, len(df)):
    news = df.at[i, 'news']

    if len(news) > 5:
        prob, sentiment = estimate_sentiment(news[1:1000])
        print(news[1:10], prob.item(), sentiment)
        df.at[i, 'probability'] = prob.item()
        df.at[i, 'sentiment'] = sentiment

    else:
        print(news, 0, "neutral")
        df.at[i, 'probability'] = 0
        df.at[i, 'sentiment'] = "neutral"
    
    # Check if it's time to save the CSV file
    if (i + 1) % batch_size == 0:
        # Save the DataFrame to a CSV file with the new column
        df[:i+1].to_csv(FILENAME+'_with_sentiment.csv', index=False)
        
        # Update the checkpoint file with the index of the last processed row
        with open(checkpoint_file, 'w') as f:
            f.write(str(i + 1))
        
        print(f"Saved {i + 1} rows.")

# Save the remaining rows
df.to_csv(FILENAME+'_with_sentiment.csv', index=False)
print(f"Total {len(df)} rows processed and saved.")

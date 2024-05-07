
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


FILE_NAME = 'tesla_news'
df = pd.read_csv(FILE_NAME+'.csv')

batch_size = 10

checkpoint_file = FILE_NAME+'sentiment_checkpoint.txt'
start_index = 0
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as f:
        start_index = int(f.read())

for i in range(start_index, len(df)):
    news = df.at[i, 'news']
    prob, sentiment = estimate_sentiment(news[1:1000])
    print(news[1:10], prob.item(), sentiment)
    df.at[i, 'probability'] = prob.item()
    df.at[i, 'sentiment'] = sentiment

    if (i + 1) % batch_size == 0:
        df[:i+1].to_csv(FILE_NAME+'_with_sentiment.csv', index=False)
        with open(checkpoint_file, 'w') as f:
            f.write(str(i + 1))
        print(f"Saved {i + 1} rows.")

df.to_csv(FILE_NAME+'_with_sentiment.csv', index=False)
print(f"Total {len(df)} rows processed and saved.")

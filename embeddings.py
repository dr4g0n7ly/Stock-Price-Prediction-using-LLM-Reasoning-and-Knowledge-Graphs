from config import GOOGLE_API_KEY
import google.generativeai as genai
import pandas as pd
import os
import numpy as np

# Configure generative AI with API key
genai.configure(api_key=GOOGLE_API_KEY)

# Read the DataFrame from CSV
df = pd.read_csv('CSV/triplets_for_all_dates_updated.csv')

# Define the model
model = 'models/embedding-001'

# Function to generate embeddings
def embed_fn(text):
    return genai.embed_content(model=model,
                               content=text,
                               task_type="retrieval_document")["embedding"]

batch_size = 5

# Check if there's a checkpoint file to resume from
checkpoint_file = 'embed_checkpoint.txt'
start_index = 0
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as f:
        start_index = int(f.read())

checkpoint_file = 'embed_errors.txt'

# Iterate over DataFrame, generate embeddings, and store in a new column

df['embedding'] = np.empty((len(df), 0)).tolist()

for i, row in df.iterrows():
    try:
        if i > 1655: 
            sentence = row['sentence']
            embedding = embed_fn(sentence)
            df.at[i, 'embedding'] = embedding

    except:
        print(f"Row: {i + 2}")

    if (i + 1) % batch_size == 0:
        df[:i+1].to_csv('triplet_embeddings2.csv', index=False)
        with open(checkpoint_file, 'w') as f:
            f.write(str(i + 1))
        print(f"Saved {i + 1} rows.")


df.to_csv('triplet_embeddings2.csv', index=False)
print(f"Total {len(df)} rows processed and saved.")



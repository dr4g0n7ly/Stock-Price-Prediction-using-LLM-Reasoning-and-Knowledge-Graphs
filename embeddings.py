from config import GOOGLE_API_KEY
import google.generativeai as genai
import os
import pandas as pd
import pickle

genai.configure(api_key=GOOGLE_API_KEY)

model = 'models/embedding-001'

def embed_fn(text):
  embedding = genai.embed_content(model=model, content=text, task_type="retrieval_document")["embedding"]
  return embedding

# Read the DataFrame from CSV
df = pd.read_csv('CSV/triplets_for_all_dates_updated.csv')
checkpoint_file = 'embed_checkpoint.txt'

# Iterate over DataFrame, generate embeddings, and store in a new column
df['embeddings'] = [None] * len(df)
for i in range(0, len(df)):
  df.at[i, 'embeddings'] = embed_fn(df.at[i, 'sentence'])
  with open(checkpoint_file, 'w') as f:
    f.write(str(i + 1))
    print(f"Saved {i + 1} rows.")

# Save the DataFrame with pickle
with open('triplet_embed.pkl', 'wb') as f:
  pickle.dump(df, f)

print(f"Total {len(df)} rows processed and saved.")
FILENAME = 'tesla_news'

from config import GOOGLE_API_KEY
import google.generativeai as genai
import pandas as pd
import pickle
genai.configure(api_key=GOOGLE_API_KEY)

model = 'models/embedding-001'

def embed_fn(text):
  embedding = genai.embed_content(model=model, content=text, task_type="retrieval_document")["embedding"]
  return embedding

# Read the DataFrame from CSV
df = pd.read_csv(FILENAME+'_triplets_for_all_dates.csv')

# Iterate over DataFrame, generate embeddings, and store in a new column
err_count = 0

df['embeddings'] = [None] * len(df)
for i in range(0, len(df)):
  try:
    df.at[i, 'embeddings'] = embed_fn(df.at[i, 'sentence'])
    print(f"Embedded {i + 1} rows.")
  except Exception as e:
    print("\nERROR: ", e, "\nROW: ", i+1, "\nDATE: ", df.at[i, 'date'], "\n")
    err_count += 1

# Save the DataFrame with pickle
with open(FILENAME+'_embeddings.pkl', 'wb') as f:
  pickle.dump(df, f)

print(f"Total {len(df)} rows processed and saved.")
print("No. of errors", err_count)
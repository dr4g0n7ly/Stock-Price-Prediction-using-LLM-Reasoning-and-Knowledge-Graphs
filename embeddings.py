from config import GOOGLE_API_KEY
import google.generativeai as genai
import pandas as pd

genai.configure(api_key=GOOGLE_API_KEY)

df = pd.read_csv('triplets_for_all_dates.csv')
model = 'models/embedding-001'

def embed_fn(text):
  return genai.embed_content(model=model,
                             content=text,
                             task_type="retrieval_document",
                             )["embedding"]

df['embeddings'] = df.apply(lambda row: embed_fn(row['triplet']), axis=1)
df.head()

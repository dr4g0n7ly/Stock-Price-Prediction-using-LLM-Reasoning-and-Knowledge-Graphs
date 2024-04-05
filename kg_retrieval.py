import numpy as np
import pickle
import google.generativeai as genai
from config import GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

with open('triplet_embed.pkl', 'rb') as f:
  df = pickle.load(f)
# Print lengths and identify mismatched dimensions

query = "Panasonic has supply problems"
model = 'models/embedding-001'

def find_best_passage(query, dataframe):
  query_embedding = genai.embed_content(model=model,
                                        content=query,
                                        task_type="retrieval_query")
  dot_products = np.dot(np.stack(dataframe['embeddings']), query_embedding["embedding"])
  idx = np.argmax(dot_products)
  return dataframe.iloc[idx]['sentence']


def find_top_k_passages(query, dataframe, k=5):
    query_embedding = genai.embed_content(model=model, content=query, task_type="retrieval_query")
    dot_products = np.dot(np.stack(dataframe['embeddings']), query_embedding["embedding"])

    dataframe_sorted = dataframe.copy()
    dataframe_sorted['score'] = dot_products
    dataframe_sorted = dataframe_sorted.sort_values(by='score', ascending=False)

    top_k_passages = list(dataframe_sorted['sentence'].head(k))
    top_k_scores = list(dataframe_sorted['score'].head(k))

    return top_k_passages, top_k_scores


passage = find_top_k_passages(query, df, 5)
print(passage)

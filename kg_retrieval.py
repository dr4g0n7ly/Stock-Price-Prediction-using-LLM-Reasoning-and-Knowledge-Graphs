import numpy as np
import pandas as pd
import pickle
from datetime import datetime, timedelta
import google.generativeai as genai
from config import GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

with open('triplet_embed.pkl', 'rb') as f:
  df = pickle.load(f)


query = "Panasonic has supply problems"
model = 'models/embedding-001'

def find_top_k_passages_by_week(date, query, dataframe, k=5):
    query_date = datetime.strptime(date, '%Y-%m-%d')
    start_date = query_date - timedelta(days=7)
    end_date = query_date - timedelta(days=1)

    dataframe['date'] = pd.to_datetime(dataframe['date'], format='%d-%m-%Y')
    dataframe_filtered = dataframe[(dataframe['date'] > start_date) & (dataframe['date'] < end_date)]
    query_embedding = genai.embed_content(model=model, content=query, task_type="retrieval_query")
    dot_products = np.dot(np.stack(dataframe_filtered['embeddings']), query_embedding["embedding"])

    dataframe_filtered['score'] = dot_products
    dataframe_sorted = dataframe_filtered.sort_values(by='score', ascending=False)
    dataframe_sorted = dataframe_sorted.head(k)
    dataframe_sorted = dataframe_sorted.sort_values(by='date', ascending=True)

    output_strings = []
    for idx, row in dataframe_sorted.iterrows():
        output_strings.append(f"{row['date'].strftime('%Y-%m-%d')} {row['sentence']}")

    return '\n'.join(output_strings)


def find_top_k_passages(date, query, dataframe, k=5):
    query_date = datetime.strptime(date, '%Y-%m-%d')


    dataframe['date'] = pd.to_datetime(dataframe['date'], format='%d-%m-%Y')
    query_embedding = genai.embed_content(model=model, content=query, task_type="retrieval_query")
    dot_products = np.dot(np.stack(dataframe['embeddings']), query_embedding["embedding"])

    dataframe['score'] = dot_products
    dataframe_sorted = dataframe.sort_values(by='score', ascending=False)
    dataframe_sorted = dataframe_sorted.head(k)
    dataframe_sorted = dataframe_sorted.sort_values(by='date', ascending=True)

    output_strings = []
    for idx, row in dataframe_sorted.iterrows():
        output_strings.append(f"{row['date'].strftime('%Y-%m-%d')} {row['sentence']}")

    return '\n'.join(output_strings)


passages = find_top_k_passages('2022-10-10', query, df, 10)
print(passages)


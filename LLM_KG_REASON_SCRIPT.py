# CHANGE STOCK NAME IN SYSTEM PROMPT 3 TIMES

FILENAME = 'tesla_news'

import os
import numpy as np
import pandas as pd
import pickle
from datetime import datetime, timedelta

import google.generativeai as genai
from config import GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

def find_top_k_passages_by_week(date, query, dataframe, k=5):

    model = 'models/embedding-001'

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



def find_top_k_passages(query, dataframe, k=5):

    model = 'models/embedding-001'

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


def remove_quotes(s):
    return s.replace("'", "").replace('"', '')

def LLM_Response(news, week_context, general_context):

    model = genai.GenerativeModel('gemini-pro')

    try:
        system_prompt = """ You are an expert stock news analyser. With respect to the context news and current news provided respond with a reasons for whether you should buy or sell Tesla stock and give a confidence ranging from 0 (sell) to 9 (buy). You must ensure the following rules are followed when giving your analysis:
        RULES:
        1. Please respond in json format: { reason: string, confidence: integer }, where reason contains the reasons for buying or selling Tesla stock, and confidence is a integer ranging from 0 (sell) to 9 (buy)
        2. Please ensure that the NEWS is critically analysed before writing the reasons for the prediction of the stock price
        3. The LAST WEEK CONTEXT NEWS is relevant news titles from the past week along with dates. Ensure that this LAST WEEK CONTEXT NEWS is also critically analysed before writing the reasons for the prediction of the stock
        4. The GENERAL CONTEXT is relevant news titles or information in general that is relevant to the provided news along with the dates. Ensure that this GENERAL CONTEXT NEWS is also critically analysed before writing the reasons for the prediction of the stock
        5. Try to find meaningful information that may be most detrimental to Tesla Stock price movement. This is very important!
        """

        ARTICLE = news

        response = model.generate_content(
            f'''
            SYSTEM PROMPT: {system_prompt}

            GENERAL CONTEXT NEWS: {general_context}

            LAST WEEK CONTEXT NEWS: {week_context}

            NEWS: {remove_quotes(ARTICLE)}''', 
            stream=True,
        )

        output = ''
        for chunk in response:
            output += chunk.text

        return output
    except Exception as e:
        print(f"An error occurred: {e}\nfor news: {news}")
        return '{""reason"": ""error"", ""confidence"": 1}' # Return ONLY_HIGH if an error occurs
    

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(FILENAME+'.csv')

with open('triplet_embed.pkl', 'rb') as f:
  triplet_df = pickle.load(f)

# Define the batch size (number of rows to process before saving)
batch_size = 5

# Check if there's a checkpoint file to resume from
checkpoint_file = FILENAME+'_LLM_KG_checkpoint.txt'
start_index = 0
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as f:
        start_index = int(f.read())

# Process the DataFrame in batches and periodically save the CSV file
for i in range(start_index, len(df)):
  if i < 5:
      continue
  try:
    general_context = find_top_k_passages(df.at[i, 'news'], triplet_df, 10)
  except:
    general_context = "No context"

  try:
    week_context = find_top_k_passages_by_week(df.at[i, 'date'], df.at[i, 'news'], triplet_df, 10)
  except:
    week_context = "No context"

  df.at[i, 'LLM_output'] = LLM_Response(df.at[i, 'news'], week_context, general_context)

  print("DATE: ", df.at[i, 'date'])
  print(df.at[i, 'LLM_output'], "\n\n")

  # Drop the 'news' column before saving
  df_to_save = df.drop('news', axis=1)  # axis=1 specifies dropping a column

  # Check if it's time to save the CSV file
  if (i + 1) % batch_size == 0:
    # Save the DataFrame to a CSV file without the 'news' column
    df_to_save.to_csv(FILENAME+'_with_LLM_KG.csv', index=False)

    # Update the checkpoint file with the index of the last processed row
    with open(checkpoint_file, 'w') as f:
      f.write(str(i + 1))

    print(f"Saved {i + 1} rows.")

# Save the remaining rows (without 'news' column)
df.drop('news', axis=1, inplace=True)  # Drop directly modifies the DataFrame
df.to_csv(FILENAME+'_with_LLM_KG.csv', index=False)
print(f"Total {len(df)} rows processed and saved.")
with open(checkpoint_file, 'w') as f:
      f.write('0')
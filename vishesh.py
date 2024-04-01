import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

import os
import pandas as pd

def remove_quotes(s):
    return s.replace("'", "").replace('"', '')

def LLM_Triplet(news):
    try:
        system_prompt = 'With respect to the entire news provided below, please generate 2 knowledge graph triplets containing {head, relation, tail} that contain the most relevant information that will cause Tesla stock price movement. Please be specific to the news provided. Please respond in json format: { triplets[{head, relation, tail}, {head, relation, tail}]} and nothing else as it needs to be used directly as json.'

        response = model.generate_content(
        f'''
        SYSTEM PROMPT: {system_prompt}
        NEWS: {remove_quotes(news)}''', 
        stream=True)

        output = ''
        for chunk in response:
            output += chunk.text

        return output
    except Exception as e:
        print(f"An error occurred: {e}\nfor news: {news}")
        return '{error: news blocked}'

df = pd.read_csv('tesla_news.csv')
batch_size = 5

checkpoint_file = 'checkpoint.txt'
start_index = 0
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as f:
        start_index = int(f.read())

for i in range(start_index, len(df)):
    df.at[i, 'LLM_Triplet'] = LLM_Triplet(df.at[i, 'news'])
    
    if (i + 1) % batch_size == 0:
        df[:i+1].to_csv('tesla_news_with_triplets.csv', index=False)

        with open(checkpoint_file, 'w') as f:
            f.write(str(i + 1))
        
        print(f"Saved {i + 1} rows.")


df.to_csv('tesla_news_with_triplets.csv', index=False)
print(f"Total {len(df)} rows processed and saved.")

with open(checkpoint_file, 'w') as f:
    f.write(str(i + 1))
        
print(f"Saved {i + 1} rows.")
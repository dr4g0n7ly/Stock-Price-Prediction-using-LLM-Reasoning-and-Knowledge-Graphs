# Read the CSV file
df = pd.read_csv('your_file.csv')

import pandas as pd
import json

FILENAME = ""

df = pd.read_csv('modified_tesla_news_with_triplets.csv')

df['LLM_Triplet'] = df['LLM_Triplet'].str.replace("```", '')
df.to_csv('modified_tesla_news_with_triplets.csv', index=False)

def check_json_format(df):
    for index, row in df.iterrows():
        try:
            triplet_json = json.loads(row['LLM_Triplet'])
            if 'triplets' not in triplet_json and 'error' not in triplet_json:
                print(f"Row {index + 1}: LLM_Triplet doesn't contain 'triplets' or 'error'.")
        except json.JSONDecodeError:
            print(f"Date - {row['date']}: LLM_Triplet is not in valid JSON format.")

# Call the function to check JSON format
check_json_format(df)
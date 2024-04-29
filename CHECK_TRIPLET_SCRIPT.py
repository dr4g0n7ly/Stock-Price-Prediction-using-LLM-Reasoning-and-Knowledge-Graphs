# CHANGE FILENAME TO LLM REASON OUTPUT FILE
FILENAME = 'tesla_news'

import pandas as pd
import json

def check_json_format(df):
    for index, row in df.iterrows():
        try:
            output = json.loads(row['LLM_Triplet'])
            if 'triplets' not in output and 'error' not in output:
                print(f"Row {index + 1} Date - {row['date']}: LLM_Triplet doesn't contain 'confidence' or 'error'.")
        except json.JSONDecodeError:
            print(f"Date - {row['date']}: LLM_Triplet is not in valid JSON format.")


# Call the function to check JSON format
df = pd.read_csv(FILENAME+'_with_triplets.csv')

df['LLM_Triplet'] = df['LLM_Triplet'].str.replace("```", '')
df['LLM_Triplet'] = df['LLM_Triplet'].str.replace("json", '')
df['LLM_Triplet'] = df['LLM_Triplet'].str.replace("JSON", '')
df['LLM_Triplet'] = df['LLM_Triplet'].str.replace("/", "'")
df['LLM_Triplet'] = df['LLM_Triplet'].str.replace("_", ' ')
df['LLM_Triplet'] = df['LLM_Triplet'].str.replace("error: news blocked", '"error": "news blocked"')

# df.drop(columns=['news'], inplace=True)

# df.to_csv(FILENAME+'_with_triplets.csv', index=False)


check_json_format(df)
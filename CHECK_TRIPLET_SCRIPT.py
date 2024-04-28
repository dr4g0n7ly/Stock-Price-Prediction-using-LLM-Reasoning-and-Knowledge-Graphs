# Read the CSV file


import pandas as pd
import json

FILENAME = "tesla_news"

df = pd.read_csv(FILENAME+'_with_triplets.csv')

# df['LLM_Triplet'] = df['LLM_Triplet'].str.replace("```", '')
# df.to_csv('modified_tesla_news_with_triplets.csv', index=False)
import json

def check_json_format(df):
    for index, row in df.iterrows():
        try:
            triplet_json = json.loads(row['LLM_Triplet'])
            # if 'triplets' not in triplet_json and 'error' not in triplet_json:
            #     print(f"Row {index + 1}: LLM_Triplet doesn't contain 'triplets' or 'error'.")
            # elif 'triplets' in triplet_json:
            #     triplets = triplet_json['triplets']
            #     for triplet in triplets:
            #         if 'head' not in triplet or 'relation' not in triplet or 'tail' not in triplet:
            #             print(f"Row {index + 1}: One or more elements in 'triplets' are missing required keys.")
        except json.JSONDecodeError:
            print(f"Date - {row['date']}: LLM_Triplet is not in valid JSON format.")

# Example usage:
# check_json_format(your_dataframe)

# Call the function to check JSON format
check_json_format(df)
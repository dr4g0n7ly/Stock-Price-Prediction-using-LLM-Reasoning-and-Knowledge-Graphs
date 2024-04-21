# CHANGE FILENAME TO LLM REASON OUTPUT FILE
FILENAME = 'tesla_news'

import pandas as pd
import json

def check_json_format(df):
    for index, row in df.iterrows():
        try:
            output = json.loads(row['LLM_output'])
            if 'confidence' in output:
                df.at[index, 'confidence'] = output['confidence']
            else:
                print(f"Row {index + 1}: LLM_output doesn't contain 'confidence'.")
            if 'reason' not in output and 'error' not in output:
                print(f"Row {index + 1}: LLM_output doesn't contain 'reason' or 'error'.")
        except json.JSONDecodeError:
            print(f"Date - {row['date']}: LLM_output is not in valid JSON format.")

    df.to_csv(FILENAME + '_with_confidence.csv', index=False)



# Call the function to check JSON format
df = pd.read_csv(FILENAME+'_with_LLM_Reason.csv')

df['LLM_output'] = df['LLM_output'].str.replace("```", '')
df['LLM_output'] = df['LLM_output'].str.replace("json", '')
df['LLM_output'] = df['LLM_output'].str.replace("JSON", '')
df['LLM_output'] = df['LLM_output'].str.replace("reason: error, confidence: 2", '""reason"": ""error"", ""confidence"": 2')


check_json_format(df)

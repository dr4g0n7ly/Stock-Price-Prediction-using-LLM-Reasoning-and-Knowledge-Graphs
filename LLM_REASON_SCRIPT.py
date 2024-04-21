# CHANGE STOCK NAME IN SYSTEM PROMPT 3 TIMES

FILENAME = 'nvdia_news'

import os
import pandas as pd

import google.generativeai as genai
from config import GOOGLE_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def remove_quotes(s):
    return s.replace("'", "").replace('"', '')

def LLM_Response(news):
    try:
        system_prompt = """ You are an expert stock news analyser. With respect to the news provided respond with a reasons for whether you should buy or sell Nvidia stock and give a confidence ranging from 0 (sell) to 9 (buy). You must ensure the following rules are followed when giving your analysis:
        RULES:
        1. Please respond in json format: { reason: string, confidence: integer }, where reason contains the reasons for buying or selling Nvidia stock, and confidence is a integer ranging from 0 (sell) to 9 (buy)
        2. Please ensure that the news is critically analysed before writing the reasons for the prediction of the stock price
        3. Try to find meaningful information that may be most detrimental to Nvidia Stock price movement. This is very important!
        """

        ARTICLE = news

        from google.generativeai.types import HarmCategory, HarmBlockThreshold

        response = model.generate_content(
            f'''
            SYSTEM PROMPT: {system_prompt}
            NEWS: {remove_quotes(ARTICLE)}''', 
            stream=True,
        )

        output = ''
        for chunk in response:
            output += chunk.text

        return output
    except Exception as e:
        print(f"An error occurred: {e}\nfor news: {news}")
        return '{""reason"": ""error"", ""confidence"": 2}' # Return ONLY_HIGH if an error occurs
    

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(FILENAME+'.csv')

# Define the batch size (number of rows to process before saving)
batch_size = 5

# Check if there's a checkpoint file to resume from
checkpoint_file = FILENAME+'_LLM_Reason_checkpoint.txt'
start_index = 0
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as f:
        start_index = int(f.read())

# Process the DataFrame in batches and periodically save the CSV file
for i in range(start_index, len(df)):
  # Apply LLM_response function to the 'news' column
  df.at[i, 'LLM_output'] = LLM_Response(df.at[i, 'news'])

  # Drop the 'news' column before saving
  df_to_save = df.drop('news', axis=1)  # axis=1 specifies dropping a column

  # Check if it's time to save the CSV file
  if (i + 1) % batch_size == 0:
    # Save the DataFrame to a CSV file without the 'news' column
    df_to_save.to_csv(FILENAME+'_with_LLM_Reason.csv', index=False)

    # Update the checkpoint file with the index of the last processed row
    with open(checkpoint_file, 'w') as f:
      f.write(str(i + 1))

    print(f"Saved {i + 1} rows.")

# Save the remaining rows (without 'news' column)
df.drop('news', axis=1, inplace=True)  # Drop directly modifies the DataFrame
df.to_csv(FILENAME+'_with_LLM_Reason.csv', index=False)
print(f"Total {len(df)} rows processed and saved.")
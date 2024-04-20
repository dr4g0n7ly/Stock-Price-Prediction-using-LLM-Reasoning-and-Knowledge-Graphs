# CHANGE FILENAME TO LLM REASON OUTPUT FILE
df = pd.read_csv('your_file.csv')

import pandas as pd
import json

def check_json_format(df):
    for index, row in df.iterrows():
        try:
            reason_json = json.loads(row['LLM_output'])
            if 'reason' not in reason_json and 'error' not in reason_json:
                print(f"Row {index + 1}: LLM_output doesn't contain 'reason' or 'error'.")
        except json.JSONDecodeError:
            print(f"Date - {row['date']}: LLM_output is not in valid JSON format.")

# Call the function to check JSON format
check_json_format(df)

# # Function to extract confidence score
# def extract_confidence(row):
#     try:
#         # Try loading as JSON
#         output_dict = json.loads(row)
#         return output_dict['confidence']
#     except (json.JSONDecodeError, KeyError):
#         try:
#             # If JSON loading fails, try extracting with regex
#             match = re.search(r'confidence:\s*(\d+)', row)
#             if match:
#                 return int(match.group(1))
#             else:
#                 return None
#         except Exception as e:
#             print(f"Error: {e}")
#             return None
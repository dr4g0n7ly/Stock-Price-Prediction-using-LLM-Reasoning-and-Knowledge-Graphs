# ==================================================
# READ CSV FILE AND EXTRACT CONFIDENCE

# import pandas as pd
# import json
# import re

# # Read the CSV file
# file_path = 'tesla_news_with_triplets.csv'  # Update with your file path
# df = pd.read_csv(file_path)

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

# # Replace NaN values with empty string
# df['LLM_output'].fillna('', inplace=True)

# # Add a new column for confidence scores
# df['confidence_score'] = df['LLM_output'].apply(extract_confidence)

# # Update with your desired output file path
# df.to_csv(file_path, index=False)

# print("Modified CSV file with confidence scores saved successfully.")

# Print the number of rows where confidence_score is None
# Count the number of rows with confidence_score as None
# none_count = df['confidence_score'].isnull().sum()

# # Total number of rows
# total_rows = len(df)

# print(f"Number of rows with confidence_score as None: {none_count}")
# print(f"Total number of rows: {total_rows}")


# ==================================================
# CHECK JSON FORMAT OF TRIPLETS IN CSV FILE

import pandas as pd
import json

def check_json_format(df):
    count = 0
    for index, row in df.iterrows():
        try:
            triplet_json = json.loads(row['triplet'])
            if 'head' not in triplet_json or 'tail' not in triplet_json or 'relation' not in triplet_json:
                print(f"Row {index + 1}: triplet doesn't contain head relation tail.")
                if 'error' not in triplet_json:
                    print("We have a problem: error is also not there")
        except json.JSONDecodeError:
            print(f"Row {index + 2}: Date - {row['date']}: LLM_Triplet is not in valid JSON format.")
            count += 1
    print("COUNT: ", count)

# Read the CSV file
df = pd.read_csv('triplets_for_all_dates.csv')

def remove_last_character(s):
    if s:
        return s[:-1]
    return s

def process_triplet(triplet):
    # Remove double quotes from the outside
    triplet = triplet.strip('"')

    # Replace single quotes with double quotes
    triplet = triplet.replace("'", '"')

    return triplet

# Apply the function to the 'triplets' column
# df['triplet'] = df['triplet'].apply(process_triplet)
# Call the function to check JSON format
check_json_format(df)

df.to_csv('triplets_for_all_dates.csv', index=False)

# ==================================================
# PRINT TRIPLETS FOR SPECIFIC DATE

# import pandas as pd
# import json

# # Read the CSV file into a pandas DataFrame
# df = pd.read_csv('modified_tesla_news_with_triplets.csv')

# # Iterate over each row in the DataFrame
# for index, row in df.iterrows():
#     # Check if the date matches the specified date
    
#     if row['date'] == '30-01-2022':
#         # Parse the JSON data from the 'LLM_triplets' column
#         triplets = json.loads(row['LLM_Triplet'])
        
#         # Print the triplets
#         print("Triplets for the date 01-30-2022:")
#         for triplet in triplets['triplets']:
#             print(f"Head: {triplet['head']}")
#             print(f"Relation: {triplet['relation']}")
#             print(f"Tail: {triplet['tail']}")
#             print()  # Add a newline for better readability


# ==================================================
# EXTRACT ALL TRIPLETS TO A NEW CSV FILE

# import pandas as pd
# import json

# # Read the CSV file into a pandas DataFrame
# df = pd.read_csv('modified_tesla_news_with_triplets.csv')

# # Initialize an empty list to store rows
# new_rows = []

# # Iterate over each row in the DataFrame
# for index, row in df.iterrows():
#     # Parse the JSON data from the 'LLM_triplets' column
#     triplets = json.loads(row['LLM_Triplet'])
    
#     # Check if 'triplets' key is present
#     if 'triplets' in triplets:
#         # Iterate over each triplet
#         for triplet in triplets['triplets']:
#             # Append a new row to the list
#             new_rows.append({'date': row['date'], 'triplet': triplet})
#     else:
#         # Handle the case when 'triplets' key is not present
#         print(f"Warning: 'triplets' key not found for DATE {row['date']}")
#         print(f"{row['LLM_Triplet']}")
#         print("\n")

# # Create a new DataFrame from the list of rows
# new_df = pd.DataFrame(new_rows)

# # Write the new DataFrame to a CSV file
# new_df.to_csv('triplets_for_all_dates.csv', index=False)



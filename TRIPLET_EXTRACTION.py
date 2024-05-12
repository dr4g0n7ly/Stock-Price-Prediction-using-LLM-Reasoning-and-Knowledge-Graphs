FILENAME = 'tesla_news'

import pandas as pd
import json

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(FILENAME+'_with_triplets.csv')

# Initialize an empty list to store rows
new_rows = []

warning_flag = False

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    
    try:
        output = json.loads(row['LLM_Triplet'])
        if 'triplets' not in output and 'error' not in output:
            print(f"Row {index + 1} Date - {row['date']}: LLM_Triplet doesn't contain 'triplets' or 'error'.")
            warning_flag = True
    except json.JSONDecodeError:
        print(f"Date - {row['date']}: LLM_Triplet is not in valid JSON format.")
        warning_flag = True

    # Parse the JSON data from the 'LLM_triplets' column
    triplets = json.loads(row['LLM_Triplet'])
    
    # Check if 'triplets' key is present
    if 'triplets' in triplets:
        # Iterate over each triplet
        for triplet in triplets['triplets']:
            # Append a new row to the list
            if not triplet['head']:
                print(f"Warning: 'head' not found for DATE {row['date']}")
                warning_flag = True
            if not triplet['tail']:
                print(f"Warning: 'tail' not found for DATE {row['date']}")
                warning_flag = True
            if not triplet['relation']:
                print(f"Warning: 'relation' not found for DATE {row['date']}")
                warning_flag = True
    else:
        if 'error' not in triplets:
            # Handle the case when 'triplets' key is not present
            print(f"Warning: 'triplets' key not found for DATE {row['date']}")
            print(f"{row['date']}: {row['LLM_Triplet']}")
            print("\n")
            warning_flag = True

if warning_flag == False:
    for index, row in df.iterrows():
        triplets = json.loads(row['LLM_Triplet'])

        if index != 57:
            continue
        
        # Check if 'triplets' key is present
        if 'triplets' in triplets:
            # Iterate over each triplet
            for triplet in triplets['triplets']:
                head = str(triplet['head'])
                relation = str(triplet['relation'])
                tail = str(triplet['tail'])
                sentence = head + " " + relation + " " + tail
                print("\n")
                print({'date': row['date'], '\ntriplet': triplet, '\nhead':head, '\nrelation':relation, '\ntail':tail, '\nsentence':sentence})
        else:
            if 'error' in triplets:
                new_rows.append({'date': row['date'], 'triplet': 'error: news blocked', 'head': '-', 'relation': '-', 'tail': '-'})

    # # Create a new DataFrame from the list of rows
    # new_df = pd.DataFrame(new_rows)

    # # Write the new DataFrame to a CSV file
    # new_df.to_csv(FILENAME+'_triplets_for_all_dates.csv', index=False)
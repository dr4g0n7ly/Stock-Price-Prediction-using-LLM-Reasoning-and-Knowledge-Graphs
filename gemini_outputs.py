from gemini import LLM_Response
import os
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('tesla_news.csv')

# Define the batch size (number of rows to process before saving)
batch_size = 5

# Check if there's a checkpoint file to resume from
checkpoint_file = 'Checkpoint.txt'
start_index = 0
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as f:
        start_index = int(f.read())

# Process the DataFrame in batches and periodically save the CSV file
for i in range(start_index, len(df)):
    # Apply LLM_response function to the 'news' column
    df.at[i, 'LLM_output'] = LLM_Response(df.at[i, 'news'])
    
    # Check if it's time to save the CSV file
    if (i + 1) % batch_size == 0:
        # Save the DataFrame to a CSV file with the new column
        df[:i+1].to_csv('tesla_news_with_output.csv', index=False)
        
        # Update the checkpoint file with the index of the last processed row
        with open(checkpoint_file, 'w') as f:
            f.write(str(i + 1))
        
        print(f"Saved {i + 1} rows.")

# Save the remaining rows
df.to_csv('tesla_news_with_output.csv', index=False)
print(f"Total {len(df)} rows processed and saved.")

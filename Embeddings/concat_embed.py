import pandas as pd
import pickle

# Function to read and concatenate pickle files
def concat_pkls_and_check_length(pkl_files):
    dfs = []
    total_length = 0

    # Read each pickle file, print its length, and add it to the list of DataFrames
    for pkl_file in pkl_files:
        with open(pkl_file, 'rb') as f:
            df = pickle.load(f)
            dfs.append(df)
            length = len(df)
            print(f"Length of {pkl_file}: {length}")
            total_length += length

    # Concatenate all DataFrames
    concatenated_df = pd.concat(dfs, ignore_index=True)

    # Check if the length of the concatenated DataFrame matches the sum of lengths of individual DataFrames
    if len(concatenated_df) == total_length:
        print(len(concatenated_df), total_length)
        print("Lengths match!")
    else:
        print("Lengths don't match!")
        print(len(concatenated_df), total_length)

    # Save the concatenated DataFrame to a new pickle file
    output_file = "EMBEDDINGS.pkl"
    with open(output_file, 'wb') as f:
        pickle.dump(concatenated_df, f)
        print(f"Concatenated data saved to {output_file}")

# List of pkl files
pkl_files = ['Amazon_news_embeddings.pkl', 'amd_news_embeddings.pkl', 'apple_news_embeddings.pkl', 'google_news_embeddings.pkl', 'JP_news_embeddings.pkl', 'msft_news_embeddings.pkl', 'nvdia_news_embeddings.pkl', 'tesla_news_embeddings.pkl']  # Replace with your list of pkl files

# Call the function
concat_pkls_and_check_length(pkl_files)

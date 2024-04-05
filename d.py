import pandas as pd

# Read the original CSV file
df = pd.read_csv('dataset.csv')

# Duplicate each row three times
duplicated_df = df.loc[df.index.repeat(3)]

# Save the duplicated rows to a new CSV file
duplicated_df.to_csv('dataset.csv', index=False)

import csv
from datetime import datetime

def convert_date_format(date_string):
    try:
        date_obj = datetime.strptime(date_string, '%m-%d-%Y')
    except ValueError:
        try:
            date_obj = datetime.strptime(date_string, '%m/%d/%Y')
        except ValueError:
            return None
    return date_obj.strftime('%d-%m-%Y')

def process_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:  # Specify encoding explicitly
        reader = csv.reader(f)
        header = next(reader)  # Read the header
        
        # Find the index of the date column
        date_column_index = None
        for i, col in enumerate(header):
            if 'date' in col.lower():
                date_column_index = i
                break
        
        if date_column_index is None:
            print("Date column not found in the CSV.")
            return
        
        rows = []
        for row in reader:
            if len(row) > date_column_index:
                # Apply conversion function to date column
                row[date_column_index] = convert_date_format(row[date_column_index])
            rows.append(row)

    # Write the updated rows to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:  # Specify encoding explicitly
        writer = csv.writer(f)
        writer.writerow(header)  # Write the header
        writer.writerows(rows)
# Example usage:
input_file = 'modified_tesla_news_with_triplets.csv'   # Replace 'input.csv' with your input CSV file
output_file = 'modified_tesla_news_with_triplets_date.csv' # Output file where the processed CSV will be saved
process_csv(input_file, output_file)

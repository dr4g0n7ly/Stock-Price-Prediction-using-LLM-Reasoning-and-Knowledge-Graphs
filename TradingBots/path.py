from pathlib import Path

# Get the current working directory as a Path object
current_directory = Path.cwd()

# Navigate to the CSV folder (assuming it's at the same level as the current directory)
csv_folder = current_directory.parent / 'CSV'

# Check if the CSV folder exists
if csv_folder.exists():
    # List all files and directories in the CSV folder
    files_and_directories = csv_folder.iterdir()

    # Print the list of files and directories
    print("Files and directories in the CSV folder:")
    for item in files_and_directories:
        print(item)

    # Check if the file exists in the CSV folder
    target_file = csv_folder / 'tesla_news_with_sentiment.csv'
    if target_file.exists():
        print(f"The file {target_file.name} exists in the CSV folder.")
    else:
        print(f"The file {target_file.name} does not exist in the CSV folder.")
else:
    print("The CSV folder does not exist.")

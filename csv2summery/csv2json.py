import csv
import json
import pandas as pd


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csv_file_path, json_file_path):
    # Read the CSV file
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Convert the DataFrame to JSON
        data = df.to_json(orient='records', lines=False, indent=4)
        
        # Write JSON to file
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json_file.write(data)
            
        # print(f"CSV data successfully converted to JSON and saved to {json_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
		

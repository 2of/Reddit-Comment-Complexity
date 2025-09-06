import json
import os

def merge_json_files(input_folder, output_file):
    all_data = []
    num_files = 0

    # Loop through each file in the folder
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        
        # Only process JSON files
        if filename.endswith(".json"):
            num_files += 1
            with open(file_path, "r") as file:
                data = json.load(file)
                # Append the contents of the current file into all_data list
                if isinstance(data, list):
                    all_data.extend(data)  # If the file contains a list, merge its elements
                else:
                    all_data.append(data)  # If the file contains a dictionary, append it as is

    # Write the merged data to the output file
    with open(output_file, "w") as output:
        json.dump(all_data, output, indent=4)

    # Print the number of files and the number of entries in the merged data
    print(f"Processed {num_files} JSON files.")
    print(f"Merged JSON data has been saved to {output_file}")
    print(f"Number of entries in the merged JSON: {len(all_data)}")

# Specify the folder containing the JSON files and the output file path
input_folder = "./data/NZ"
output_file = "merged_output_NZ.json"

merge_json_files(input_folder, output_file)

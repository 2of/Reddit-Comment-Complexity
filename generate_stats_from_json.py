import json
from analysis import SentimentAnalyzer



def load_json(file_path):
    """
    Load JSON data from a file.
    """
    with open(file_path, "r") as file:
        return json.load(file)

def save_json(data, file_path):
    """
    Save JSON data to a file.
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def process_comments(analyzer, comments):
    """
    Process a list of comments using the SentimentAnalyzer.
    """
    return analyzer(comments)

def update_json_with_statistics(json_data, analyzer):
    """
    Update each object in the JSON with sentiment, emotion, and writing level statistics.
    """
    for i,item in enumerate(json_data):
        print(i)
        comments = item.get("COMMENTS", [])
        if comments:
            # Process the comments
            results = process_comments(analyzer, comments)

            # Add the overall statistics to the JSON object
            item["statistics"] = results["overall_statistics"]

    return json_data

def main():
    # Path to the input JSON file
    input_file = "data/NZ/merged_output_NZ.json"
    # Path to the output JSON file
    output_file = "NZ_with_stats.json"

    # Load the JSON data
    json_data = load_json(input_file)

    # Initialize the SentimentAnalyzer
    analyzer = SentimentAnalyzer()

    # Update the JSON data with statistics
    updated_json_data = update_json_with_statistics(json_data, analyzer)

    # Save the updated JSON data
    save_json(updated_json_data, output_file)

    print(f"Processed JSON saved to {output_file}")

if __name__ == "__main__":
    main()
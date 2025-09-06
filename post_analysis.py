import json
from collections import defaultdict
import numpy as np

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_statistics(data):
    """Calculate statistics for the given JSON data and track best/worst posts."""
    stats_summary = defaultdict(lambda: defaultdict(list))
    best_worst_posts = defaultdict(lambda: defaultdict(dict))

    # Aggregate all statistics and track URLs
    for entry in data:
        url = entry['URL']
        for stat_category, values in entry['statistics'].items():
            for stat_name, stat_value in values.items():
                stats_summary[stat_category][stat_name].append(stat_value)
                # Track URLs for min and max values
                if stat_name not in best_worst_posts[stat_category]:
                    best_worst_posts[stat_category][stat_name] = {
                        'min': {'value': stat_value, 'url': url},
                        'max': {'value': stat_value, 'url': url}
                    }
                else:
                    if stat_value < best_worst_posts[stat_category][stat_name]['min']['value']:
                        best_worst_posts[stat_category][stat_name]['min'] = {'value': stat_value, 'url': url}
                    if stat_value > best_worst_posts[stat_category][stat_name]['max']['value']:
                        best_worst_posts[stat_category][stat_name]['max'] = {'value': stat_value, 'url': url}

    # Calculate averages, min, max, std, and median for each statistic
    results = {}
    for stat_category, stats in stats_summary.items():
        results[stat_category] = {}
        for stat_name, values in stats.items():
            results[stat_category][stat_name] = {
                'average': np.mean(values),
                'min': np.min(values),
                'max': np.max(values),
                'std': np.std(values),
                'median': np.median(values),
                'best_post': best_worst_posts[stat_category][stat_name]['max'],
                'worst_post': best_worst_posts[stat_category][stat_name]['min']
            }

    return results

def print_statistics(results):
    """Print statistics to the console in a readable format."""
    for stat_category, stats in results.items():
        print(f"=== {stat_category.upper()} ===")
        for stat_name, values in stats.items():
            print(f"{stat_name}:")
            print(f"  Average: {values['average']:.4f}")
            print(f"  Min: {values['min']:.4f}")
            print(f"  Max: {values['max']:.4f}")
            print(f"  Std: {values['std']:.4f}")
            print(f"  Median: {values['median']:.4f}")
            print(f"  Best Post (Max): {values['best_post']['url']} (Value: {values['best_post']['value']:.4f})")
            print(f"  Worst Post (Min): {values['worst_post']['url']} (Value: {values['worst_post']['value']:.4f})")
        print()  # Add a blank line between categories

def save_results(results, output_file):
    """Save the results to a JSON file."""
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)

def main(input_file, output_file):
    """Main function to process the JSON file and save results."""
    data = load_json(input_file)
    results = calculate_statistics(data)
    
    # Print statistics to console
    print_statistics(results)
    
    # Save statistics to file
    save_results(results, output_file)
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    input_file = 'data/NZ/NZ_with_stats.json'  # Replace with your input JSON file path
    output_file = 'statistics_summary.json'  # Replace with your desired output file path
    main(input_file, output_file)
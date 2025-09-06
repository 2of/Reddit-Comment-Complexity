import json
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
from scipy.stats import pearsonr
from collections import *

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_averages(data):
    """Calculate averages for each statistic across all posts."""
    stats_summary = defaultdict(lambda: defaultdict(list))

    # Aggregate all statistics
    for entry in data:
        for stat_category, values in entry['statistics'].items():
            for stat_name, stat_value in values.items():
                stats_summary[stat_category][stat_name].append(stat_value)

    # Calculate averages for each statistic
    averages = {}
    for stat_category, stats in stats_summary.items():
        averages[stat_category] = {}
        for stat_name, values in stats.items():
            averages[stat_category][stat_name] = {
                'average': np.mean(values),
                'median': np.median(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values)
            }

    return averages

def compare_statistics(file1, file2):
    """Compare statistics between two JSON files."""
    data1 = load_json(file1)
    data2 = load_json(file2)

    # Calculate averages for each file
    averages1 = calculate_averages(data1)
    averages2 = calculate_averages(data2)

    # Ensure both files have the same structure
    if averages1.keys() != averages2.keys():
        raise ValueError("The two JSON files have different structures.")

    comparison_results = {}
    for stat_category in averages1:
        comparison_results[stat_category] = {}
        for stat_name in averages1[stat_category]:
            comparison_results[stat_category][stat_name] = {
                'file1': averages1[stat_category][stat_name],
                'file2': averages2[stat_category][stat_name]
            }

    return comparison_results

def get_statistic_description(stat_name):
    """Return a description for the given statistic."""
    descriptions = {
        "mean": "Mean value of the statistic.",
        "median": "Median value of the statistic.",
        "std": "Standard deviation of the statistic.",
        "min": "Minimum value of the statistic.",
        "max": "Maximum value of the statistic.",
        "flesch_reading_ease": "Flesch Reading Ease score (higher = easier to read).",
        "flesch_kincaid_grade": "Flesch-Kincaid Grade Level (higher = harder to read).",
        "gunning_fog": "Gunning Fog Index (higher = harder to read).",
        "smog_index": "SMOG Index (higher = harder to read).",
        "lexical_diversity": "Lexical Diversity (higher = more diverse vocabulary)."
    }
    return descriptions.get(stat_name, "No description available.")

def add_reading_level_scale(ax, stat_name):
    """Add a scale for reading and writing level statistics."""
    if stat_name == "flesch_reading_ease":
        # Flesch Reading Ease scale
        levels = [
            (90, "Very Easy (5th grade)"),
            (80, "Easy (6th grade)"),
            (70, "Fairly Easy (7th grade)"),
            (60, "Standard (8th-9th grade)"),
            (50, "Fairly Difficult (10th-12th grade)"),
            (30, "Difficult (College)"),
            (0, "Very Difficult (Post-college)")
        ]
        for score, label in levels:
            ax.axhline(score, color='gray', linestyle='--', alpha=0.3)
            ax.text(1.02, score, label, va='center', ha='left', fontsize=9, color='gray', transform=ax.get_yaxis_transform())
    elif stat_name == "flesch_kincaid_grade":
        # Flesch-Kincaid Grade Level scale
        levels = [
            (1, "Year 1"),
            (2, "Year 2"),
            (3, "Year 3"),
            (4, "Year 4"),
            (5, "Year 5"),
            (6, "Year 6"),
            (7, "Year 7"),
            (8, "Year 8"),
            (9, "Year 9"),
            (10, "Year 10"),
            (11, "Year 11"),
            (12, "Year 12"),
            (13, "College"),
            (14, "Post-college")
        ]
        for score, label in levels:
            ax.axhline(score, color='gray', linestyle='--', alpha=0.3)
            ax.text(1.02, score, label, va='center', ha='left', fontsize=9, color='gray', transform=ax.get_yaxis_transform())
    elif stat_name == "gunning_fog":
        # Gunning Fog Index scale
        levels = [
            (6, "6 (Year 6)"),
            (7, "7 (Year 7)"),
            (8, "8 (Year 8)"),
            (9, "9 (Year 9)"),
            (10, "10 (Year 10)"),
            (11, "11 (Year 11)"),
            (12, "12 (Year 12)"),
            (13, "13 (College)"),
            (14, "14 (Post-college)")
        ]
        for score, label in levels:
            ax.axhline(score, color='gray', linestyle='--', alpha=0.3)
            ax.text(1.02, score, label, va='center', ha='left', fontsize=9, color='gray', transform=ax.get_yaxis_transform())
    elif stat_name == "smog_index":
        # SMOG Index scale
        levels = [
            (1, "1 (Year 1)"),
            (2, "2 (Year 2)"),
            (3, "3 (Year 3)"),
            (4, "4 (Year 4)"),
            (5, "5 (Year 5)"),
            (6, "6 (Year 6)"),
            (7, "7 (Year 7)"),
            (8, "8 (Year 8)"),
            (9, "9 (Year 9)"),
            (10, "10 (Year 10)"),
            (11, "11 (Year 11)"),
            (12, "12 (Year 12)"),
            (13, "13 (College)"),
            (14, "14 (Post-college)")
        ]
        for score, label in levels:
            ax.axhline(score, color='gray', linestyle='--', alpha=0.3)
            ax.text(1.02, score, label, va='center', ha='left', fontsize=9, color='gray', transform=ax.get_yaxis_transform())
        ax.set_ylim(0, 15)  # Explicitly set y-axis range for SMOG Index

def plot_grouped_bar(comparison_results, dataset1_label, dataset2_label, output_dir):
    """Generate grouped bar charts for averages and medians."""
    for stat_category, stats in comparison_results.items():
        for stat_name, values in stats.items():
            file1_values = values['file1']
            file2_values = values['file2']

            # Extract median and average values
            file1_avg = file1_values['average']
            file1_median = file1_values['median']
            file2_avg = file2_values['average']
            file2_median = file2_values['median']

            # Create a grouped bar chart for comparison
            labels = ['Average', 'Median']
            file1_data = [file1_avg, file1_median]
            file2_data = [file2_avg, file2_median]

            x = np.arange(len(labels))  # the label locations
            width = 0.35  # the width of the bars

            fig, ax = plt.subplots(figsize=(10, 6))
            rects1 = ax.bar(x - width/2, file1_data, width, label=dataset1_label, color='skyblue')
            rects2 = ax.bar(x + width/2, file2_data, width, label=dataset2_label, color='lightcoral')

            # Add descriptions and labels
            ax.set_xlabel('Metric')
            ax.set_ylabel('Value')
            ax.set_title(f'Comparison of {stat_category} - {stat_name}\n{get_statistic_description(stat_name)}')
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)

            # Add value labels on top of the bars
            for rects, data in zip([rects1, rects2], [file1_data, file2_data]):
                for rect, value in zip(rects, data):
                    height = rect.get_height()
                    ax.annotate(f'{value:.2f}',
                               xy=(rect.get_x() + rect.get_width() / 2, height),
                               xytext=(0, 3),  # 3 points vertical offset
                               textcoords="offset points",
                               ha='center', va='bottom')

            # Add reading level scale if applicable
            if stat_name in ["flesch_reading_ease", "flesch_kincaid_grade", "gunning_fog", "smog_index"]:
                add_reading_level_scale(ax, stat_name)

            # Save the plot
            plot_filename = f"{output_dir}/grouped_bar_{stat_category}_{stat_name}_{dataset1_label}_vs_{dataset2_label}.png"
            plt.savefig(plot_filename, bbox_inches='tight')
            plt.close()

            print(f"Saved plot: {plot_filename}")

def plot_boxplot(comparison_results, dataset1_label, dataset2_label, output_dir):
    """Generate box plots for distribution of values."""
    for stat_category, stats in comparison_results.items():
        for stat_name, values in stats.items():
            file1_values = values['file1']
            file2_values = values['file2']

            # Extract all values for the statistic
            file1_data = [file1_values['average'], file1_values['min'], file1_values['max'], file1_values['median']]
            file2_data = [file2_values['average'], file2_values['min'], file2_values['max'], file2_values['median']]

            # Create a box plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.boxplot([file1_data, file2_data], labels=[dataset1_label, dataset2_label], patch_artist=True,
                       boxprops=dict(facecolor='skyblue', color='black'),
                       whiskerprops=dict(color='black'),
                       capprops=dict(color='black'),
                       medianprops=dict(color='red'))

            # Add descriptions and labels
            ax.set_xlabel('Dataset')
            ax.set_ylabel('Value')
            ax.set_title(f'Distribution of {stat_category} - {stat_name}\n{get_statistic_description(stat_name)}')
            ax.grid(True, linestyle='--', alpha=0.6)

            # Save the plot
            plot_filename = f"{output_dir}/boxplot_{stat_category}_{stat_name}_{dataset1_label}_vs_{dataset2_label}.png"
            plt.savefig(plot_filename, bbox_inches='tight')
            plt.close()

            print(f"Saved plot: {plot_filename}")

def plot_scatter(comparison_results, dataset1_label, dataset2_label, output_dir):
    """Generate scatter plots for comparing two statistics."""
    stat_categories = list(comparison_results.keys())
    for i in range(len(stat_categories)):
        for j in range(i + 1, len(stat_categories)):
            stat1 = stat_categories[i]
            stat2 = stat_categories[j]

            # Extract data for the two statistics
            stat1_values = [comparison_results[stat1]['mean']['file1']['average'], comparison_results[stat1]['mean']['file2']['average']]
            stat2_values = [comparison_results[stat2]['mean']['file1']['average'], comparison_results[stat2]['mean']['file2']['average']]

            # Create a scatter plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(stat1_values[0], stat2_values[0], label=dataset1_label, color='skyblue', s=100)
            ax.scatter(stat1_values[1], stat2_values[1], label=dataset2_label, color='lightcoral', s=100)

            # Add descriptions and labels
            ax.set_xlabel(stat1)
            ax.set_ylabel(stat2)
            ax.set_title(f'Scatter Plot: {stat1} vs. {stat2}')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)

            # Save the plot
            plot_filename = f"{output_dir}/scatter_{stat1}_vs_{stat2}_{dataset1_label}_vs_{dataset2_label}.png"
            plt.savefig(plot_filename, bbox_inches='tight')
            plt.close()

            print(f"Saved plot: {plot_filename}")

def plot_heatmap(comparison_results, dataset1_label, dataset2_label, output_dir):
    """Generate heatmaps for correlations between statistics."""
    stat_categories = list(comparison_results.keys())
    num_stats = len(stat_categories)
    correlation_matrix = np.zeros((num_stats, num_stats))

    # Calculate correlation matrix
    for i in range(num_stats):
        for j in range(num_stats):
            stat1 = stat_categories[i]
            stat2 = stat_categories[j]
            stat1_values = [comparison_results[stat1]['mean']['file1']['average'], comparison_results[stat1]['mean']['file2']['average']]
            stat2_values = [comparison_results[stat2]['mean']['file1']['average'], comparison_results[stat2]['mean']['file2']['average']]
            correlation_matrix[i, j], _ = pearsonr(stat1_values, stat2_values)

    # Create a heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, xticklabels=stat_categories, yticklabels=stat_categories, cmap='coolwarm', ax=ax)
    ax.set_title(f'Correlation Heatmap: {dataset1_label} vs. {dataset2_label}')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)

    # Save the plot
    plot_filename = f"{output_dir}/heatmap_correlation_{dataset1_label}_vs_{dataset2_label}.png"
    plt.savefig(plot_filename, bbox_inches='tight')
    plt.close()

    print(f"Saved plot: {plot_filename}")

def plot_histogram(comparison_results, dataset1_label, dataset2_label, output_dir):
    """Generate histograms for frequency distribution of values."""
    for stat_category, stats in comparison_results.items():
        for stat_name, values in stats.items():
            file1_values = values['file1']
            file2_values = values['file2']

            # Extract all values for the statistic
            file1_data = [file1_values['average'], file1_values['min'], file1_values['max'], file1_values['median']]
            file2_data = [file2_values['average'], file2_values['min'], file2_values['max'], file2_values['median']]

            # Create a histogram
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist([file1_data, file2_data], bins=10, label=[dataset1_label, dataset2_label], color=['skyblue', 'lightcoral'], alpha=0.7)

            # Add descriptions and labels
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            ax.set_title(f'Histogram of {stat_category} - {stat_name}\n{get_statistic_description(stat_name)}')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)

            # Save the plot
            plot_filename = f"{output_dir}/histogram_{stat_category}_{stat_name}_{dataset1_label}_vs_{dataset2_label}.png"
            plt.savefig(plot_filename, bbox_inches='tight')
            plt.close()

            print(f"Saved plot: {plot_filename}")

def main(file1, file2, dataset1_label, dataset2_label, output_dir="comparison_plots"):
    """Main function to compare two JSON files and generate plots."""
    comparison_results = compare_statistics(file1, file2)

    # Generate all types of plots
    plot_grouped_bar(comparison_results, dataset1_label, dataset2_label, output_dir)
    plot_boxplot(comparison_results, dataset1_label, dataset2_label, output_dir)
    plot_scatter(comparison_results, dataset1_label, dataset2_label, output_dir)
    plot_heatmap(comparison_results, dataset1_label, dataset2_label, output_dir)
    plot_histogram(comparison_results, dataset1_label, dataset2_label, output_dir)

    print(f"All comparison plots saved to '{output_dir}'.")

if __name__ == "__main__":
    file1 = 'data/CK/CK_Stats.json'  # Replace with your first JSON file path
    file2 = 'data/NZ/NZ_with_stats.json'  # Replace with your second JSON file path
    dataset1_label = "CK"  # Custom label for the first dataset
    dataset2_label = "NZ"  # Custom label for the second dataset
    output_dir = "comparison_plots"  # Directory to save comparison plots
    main(file1, file2, dataset1_label, dataset2_label, output_dir)
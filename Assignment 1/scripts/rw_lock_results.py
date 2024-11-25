#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def plot_results(csv_file):
    """
    Reads the CSV file and creates a combined plot with different line styles.
    """
    # Check if the CSV file exists
    if not os.path.isfile(csv_file):
        print(f"Error: The file '{csv_file}' was not found.")
        sys.exit(1)
    
    # Read the CSV into a DataFrame
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error: Could not read the CSV file. {e}")
        sys.exit(1)
    
    # Set the style of the plots
    plt.style.use('ggplot')
    
    # List of unique priority_modes and member_percents
    priority_modes_unique = df['priority_mode'].unique()
    member_percents_unique = sorted(df['member_percent'].unique(), reverse=True)
    thread_counts_unique = sorted(df['num_threads'].unique())
    
    # Create a combined plot
    plt.figure(figsize=(12, 8))
    
    line_styles = {
        priority_modes_unique[0]: '-',
        priority_modes_unique[1]: '--'
    }
    
    for priority in priority_modes_unique:
        subset = df[df['priority_mode'] == priority]
        
        for member_percent in member_percents_unique:
            data = subset[subset['member_percent'] == member_percent]
            plt.plot(
                data['num_threads'],
                data['average_elapsed_time'],
                marker='o',
                linestyle=line_styles[priority],
                label=f'{priority.capitalize()} - Member: {member_percent*100:.1f}%'
            )
    
    # Add title and labels
    plt.title('Average Elapsed Time vs Number of Threads for All Priorities')
    plt.xlabel('Number of Threads')
    plt.ylabel('Average Elapsed Time (seconds)')
    plt.xticks(thread_counts_unique)
    plt.legend(title='Priority and Operation Percentages')
    plt.grid(True)
    plt.tight_layout()
    
    # Save the plot as an image
    plot_filename = 'combined_plot.png'
    plt.savefig(plot_filename)
    print(f"Combined plot saved as '{plot_filename}'.")
    plt.show()

def main():
    # Specify the CSV file
    csv_file = "rw_lock_results.csv"
    
    # Call the plotting function
    plot_results(csv_file)

if __name__ == "__main__":
    main()

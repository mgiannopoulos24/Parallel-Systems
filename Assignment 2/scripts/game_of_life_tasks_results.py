#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

def plot_results(csv_file):
    """
    Reads the CSV file and creates a combined plot with lines and dots for serial and parallel tasks.
    Filters rows containing 'Average' in the 'Run' column.
    """
    # Check if the CSV file exists
    if not os.path.isfile(csv_file):
        print(f"Error: The file '{csv_file}' was not found.")
        sys.exit(1)
    
    # Read the CSV into a DataFrame
    try:
        df = pd.read_csv(
            csv_file,
            names=['Grid Size', 'Threads', 'Mode', 'Run', 'Execution Time (s)'],
            header=None
        )
    except Exception as e:
        print(f"Error: Could not read the CSV file. {e}")
        sys.exit(1)
    
    # Filter rows containing the word "Average" in the 'Run' column
    df = df[df['Run'].str.contains('Average', na=False)]
    
    # Convert numeric columns
    df['Threads'] = pd.to_numeric(df['Threads'], errors='coerce')
    df['Execution Time (s)'] = pd.to_numeric(df['Execution Time (s)'], errors='coerce')

    # Set Seaborn style for better aesthetics
    sns.set(style="whitegrid")
    
    # List of unique grid sizes and thread counts
    grid_sizes_unique = sorted(df['Grid Size'].unique())
    thread_counts_unique = sorted(df['Threads'].dropna().unique())
    
    # Create a plot
    plt.figure(figsize=(14, 10))
    
    for grid_size in grid_sizes_unique:
        grid_data = df[df['Grid Size'] == grid_size]
        
        for mode in grid_data['Mode'].unique():
            mode_data = grid_data[grid_data['Mode'] == mode]
            
            label = f"Grid {grid_size}, Mode {mode}"
            
            # Plot the data with lines and dots
            plt.plot(
                mode_data['Threads'],
                mode_data['Execution Time (s)'],
                marker='o',  # Dots at each data point
                linestyle='-',  # Solid line connecting the points
                linewidth=2,  # Thicker lines for better visibility
                markersize=6,  # Moderate-sized markers
                label=label
            )
    
    # Add title and labels
    plt.title('Execution Time vs Number of Threads for Game of Life (Average Runs)', fontsize=18)
    plt.xlabel('Number of Threads', fontsize=14)
    plt.ylabel('Execution Time (seconds)', fontsize=14)
    plt.xticks(thread_counts_unique)
    plt.legend(title='Grid Sizes and Modes', loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=12)
    plt.grid(True, linestyle=':', color='gray')
    plt.tight_layout()
    
    # Save the plot as an image
    plot_filename = 'game_of_life_tasks_results.png'
    plt.savefig(plot_filename, dpi=300)
    print(f"Plot saved as '{plot_filename}'.")
    plt.show()

def main():
    # Specify the CSV file with results
    csv_file = "game_of_life_tasks_results.csv"
    
    # Call the plotting function
    plot_results(csv_file)

if __name__ == "__main__":
    main()

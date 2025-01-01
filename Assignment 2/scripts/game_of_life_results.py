#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import seaborn as sns

def plot_results(csv_file):
    """
    Reads the CSV file, filters lines containing 'Average', and creates a line plot with connected lines and markers.
    """
    # Check if the CSV file exists
    if not os.path.isfile(csv_file):
        print(f"Error: The file '{csv_file}' was not found.")
        sys.exit(1)
    
    # Read the CSV into a DataFrame
    try:
        df = pd.read_csv(csv_file, header=None, names=['Grid Size', 'Threads', 'Metric', 'Empty', 'Execution Time', 'Mode'])
    except Exception as e:
        print(f"Error: Could not read the CSV file. {e}")
        sys.exit(1)
    
    # Filter only rows with 'Average'
    df = df[df['Metric'].str.contains('Average', na=False)]
    
    # Handle missing thread counts (replace empty threads with 1 for serial mode)
    df['Threads'] = pd.to_numeric(df['Threads'], errors='coerce').fillna(1).astype(int)
    
    # Convert grid size to integers for sorting and plotting
    df['Grid Size'] = df['Grid Size'].str.extract(r'(\d+)x\d+').astype(int)
    
    # Convert Execution Time to numeric and handle non-numeric values
    df['Execution Time'] = pd.to_numeric(df['Execution Time'], errors='coerce')
    df = df.dropna(subset=['Execution Time'])  # Drop rows with invalid Execution Time values
    
    # Drop unused column
    df.drop(columns=['Metric', 'Empty'], inplace=True)
    
    # Set plot style
    sns.set(style="whitegrid")
    
    # Unique grid sizes
    grid_sizes_unique = sorted(df['Grid Size'].unique())
    
    # Create a combined plot
    plt.figure(figsize=(14, 10))
    palette = sns.color_palette("Set2", len(grid_sizes_unique))
    line_styles = ['-', '--', '-.', ':']  # Line styles for variety
    
    for i, grid_size in enumerate(grid_sizes_unique):
        grid_data = df[df['Grid Size'] == grid_size]
        
        # Sort by threads for correct line connections
        grid_data = grid_data.sort_values('Threads')
        
        # Plot line and marker for each grid size
        plt.plot(
            grid_data['Threads'],
            grid_data['Execution Time'],
            color=palette[i],
            marker='o',
            linestyle=line_styles[i % len(line_styles)],
            linewidth=2,
            markersize=8,
            label=f"Grid {grid_size}"
        )
    
    # Determine the range for the y-axis
    max_time = df['Execution Time'].max()
    
    # Set the y-axis range and ticks
    plt.ylim(0, max_time + 10)  # Add a buffer above the maximum value
    plt.yticks(range(0, int(max_time) + 20, 20))  # Create ticks at intervals of 20

    # Add title and labels
    plt.title('Execution Time vs Number of Threads for Game of Life', fontsize=18)
    plt.xlabel('Number of Threads', fontsize=14)
    plt.ylabel('Execution Time (seconds)', fontsize=14)
    plt.xticks(sorted(df['Threads'].unique()))
    plt.legend(title='Grid Sizes', loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=12)
    plt.grid(True, linestyle=':', color='gray')
    plt.tight_layout()
    
    # Save the plot as an image
    plot_filename = 'game_of_life_results.png'
    plt.savefig(plot_filename, dpi=300)
    print(f"Plot saved as '{plot_filename}'.")
    plt.show()

def main():
    # Specify the CSV file with results
    csv_file = "game_of_life_results.csv"
    
    # Call the plotting function
    plot_results(csv_file)

if __name__ == "__main__":
    main()

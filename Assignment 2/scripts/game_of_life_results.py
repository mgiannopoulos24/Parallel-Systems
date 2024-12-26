#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import seaborn as sns

def plot_results(csv_file):
    """
    Reads the CSV file and creates a combined scatter plot with different styles for better visibility.
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
    
    # Set a more distinct style for better visibility
    sns.set(style="whitegrid")  # Use seaborn's whitegrid style for better readability
    
    # List of unique grid sizes and thread counts
    grid_sizes_unique = sorted(df['Grid Size'].unique())
    thread_counts_unique = sorted(df['Threads'].unique())
    
    # Create a combined plot
    plt.figure(figsize=(14, 10))
    
    # Use a color palette for different grid sizes
    palette = sns.color_palette("Set2", len(grid_sizes_unique))  # Color palette for grid sizes
    
    for i, grid_size in enumerate(grid_sizes_unique):
        grid_data = df[df['Grid Size'] == grid_size]
        
        # Scatter plot for execution times with different markers for each thread count
        for j, thread_count in enumerate(thread_counts_unique):
            data = grid_data[grid_data['Threads'] == thread_count]
            
            # Select a marker for each thread count
            markers = ['o', 's', '^', 'D', 'p', 'H']
            marker = markers[j % len(markers)]
            
            # Plot with transparency for better visibility in case of overlapping points
            plt.scatter(
                data['Threads'],
                data['Execution Time (s)'],
                color=palette[i],  # Use a distinct color for each grid size
                marker=marker,
                s=100,  # Size of the marker
                alpha=0.7,  # Transparency for better clarity
                label=f"Grid {grid_size}, {thread_count} threads"
            )
    
    # Add title and labels
    plt.title('Execution Time vs Number of Threads for Game of Life', fontsize=18)
    plt.xlabel('Number of Threads', fontsize=14)
    plt.ylabel('Execution Time (seconds)', fontsize=14)
    plt.xticks(thread_counts_unique)
    plt.legend(title='Grid Sizes and Thread Counts', loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=12)
    plt.grid(True, linestyle=':', color='gray')  # Lighter grid for better clarity
    plt.tight_layout()
    
    # Save the plot as an image
    plot_filename = 'game_of_life_results.png'
    plt.savefig(plot_filename, dpi=300)  # High resolution for better clarity
    print(f"Plot saved as '{plot_filename}'.")
    plt.show()

def main():
    # Specify the CSV file with results
    csv_file = "game_of_life_results.csv"
    
    # Call the plotting function
    plot_results(csv_file)

if __name__ == "__main__":
    main()

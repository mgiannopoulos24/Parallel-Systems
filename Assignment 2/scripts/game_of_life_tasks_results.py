#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def plot_results(csv_file):
    """
    Reads the CSV file and creates a combined plot with different line styles and markers for serial and parallel tasks.
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
    plt.style.use('ggplot')  # Use built-in 'ggplot' style
    
    # List of unique grid sizes and thread counts
    grid_sizes_unique = sorted(df['Grid Size'].unique())
    thread_counts_unique = sorted(df['Threads'].unique())
    
    # Create a combined plot
    plt.figure(figsize=(14, 10))
    
    # Define line styles and markers for better visibility
    line_styles = {
        1: '-',  # Serial case (solid line)
        2: '--', # Parallel cases (dashed line)
        3: ':',  # Mode 2 parallel (dotted line)
    }
    
    markers = ['o', 's', '^', 'D', 'p', 'H']  # Different markers for better distinction
    
    for grid_size in grid_sizes_unique:
        grid_data = df[df['Grid Size'] == grid_size]
        
        # Plot execution times for serial and parallel threads (including mode 2)
        for i, thread_count in enumerate(thread_counts_unique):
            data = grid_data[grid_data['Threads'] == thread_count]
            mode = grid_data['Mode'].iloc[0]  # Assuming mode is the same for all rows in a given grid size
            
            if mode == 1:  # Serial case
                line_style = line_styles[1]  # Solid line for serial
                label = f"Serial ({grid_size})"
                marker = markers[0]  # First marker for serial
            elif mode == 2:  # Parallel task (mode 2)
                line_style = line_styles[3]  # Dotted line for parallel task
                label = f"Parallel Task (Mode 2, {grid_size})"
                marker = markers[i % len(markers)]  # Cycle through different markers for parallel task
            else:  # Parallel threads (mode 2 can be separate from the general parallel)
                line_style = line_styles[2]  # Dashed line for general parallel
                label = f"Parallel ({grid_size}, {thread_count} threads)"
                marker = markers[i % len(markers)]  # Cycle through different markers for parallel
            
            # Plot the data with corresponding line style, marker, and increased line width
            plt.plot(
                data['Threads'],
                data['Execution Time (s)'],
                marker=marker,
                linestyle=line_style,
                linewidth=2,  # Increased line width for clarity
                markersize=8,  # Larger markers for better visibility
                label=label
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
    plot_filename = 'game_of_life_results_plot_mode2.png'
    plt.savefig(plot_filename, dpi=300)  # High resolution for better clarity
    print(f"Plot saved as '{plot_filename}'.")
    plt.show()

def main():
    # Specify the CSV file with results
    csv_file = "game_of_life_tasks_results.csv"
    
    # Call the plotting function
    plot_results(csv_file)

if __name__ == "__main__":
    main()

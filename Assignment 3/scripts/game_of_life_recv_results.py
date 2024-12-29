#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import seaborn as sns

def plot_results(csv_file):
    """
    Reads the CSV file and creates a combined scatter plot with grid sizes and process counts.
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
    
    # Convert process counts to string for better labeling
    df['Processes'] = df['Processes'].astype(str)
    
    # Create a combined plot
    plt.figure(figsize=(16, 12))
    
    # Use a color palette for grid sizes
    palette = sns.color_palette("Set2", len(df['Grid Size'].unique()))
    
    # Scatter plot with different markers for process counts
    sns.scatterplot(
        data=df,
        x='Generations',
        y='Execution Time (s)',
        hue='Grid Size',  # Color by grid size
        style='Processes',  # Marker style by process count
        palette=palette,
        s=100,  # Marker size
        alpha=0.7  # Transparency for better clarity
    )
    
    # Add title and labels
    plt.title('Execution Time vs Generations for Game of Life', fontsize=18)
    plt.xlabel('Generations', fontsize=14)
    plt.ylabel('Execution Time (seconds)', fontsize=14)
    
    # Configure legend
    plt.legend(
        title='Grid Sizes / Processes',
        loc='upper left',
        bbox_to_anchor=(1.05, 1),
        fontsize=12
    )
    plt.grid(True, linestyle=':', color='gray')  # Lighter grid for better clarity
    plt.tight_layout()
    
    # Save the plot as an image
    plot_filename = 'game_of_life_results_with_processes.png'
    plt.savefig(plot_filename, dpi=300)  # High resolution for better clarity
    print(f"Plot saved as '{plot_filename}'.")
    plt.show()

def main():
    # Specify the CSV file with results
    csv_file = "game_of_life_recv_results.csv"
    
    # Call the plotting function
    plot_results(csv_file)

if __name__ == "__main__":
    main()

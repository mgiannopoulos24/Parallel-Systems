#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import seaborn as sns

def plot_results(csv_file):
    """
    Reads the CSV file and creates a line plot with processes on the x-axis and time on the y-axis.
    Only includes rows where the 'Run' column contains the word 'Average'.
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
    
    # Filter the DataFrame to include only rows where 'Run' contains 'Average'
    df = df[df['Run'].str.contains('Average', na=False)]
    
    # Set a more distinct style for better visibility
    sns.set(style="whitegrid")
    
    # Convert processes to string for labeling
    df['Processes'] = df['Processes'].astype(str)
    
    # Create a figure
    plt.figure(figsize=(16, 10))
    
    # Use a color palette for generations
    palette = sns.color_palette("tab10", len(df['Grid Size'].unique()))
    
    # Plot the data grouped by grid size
    sns.lineplot(
        data=df,
        x='Processes',
        y='Average Time (s)',
        hue='Grid Size',
        style='Grid Size',  # Style lines by grid size
        markers=True,  # Add markers to the lines
        dashes=False,  # Use solid lines
        palette=palette
    )
    
    # Add title and labels
    plt.title('Average Execution Time vs Processes for Game of Life', fontsize=18)
    plt.xlabel('Processes', fontsize=14)
    plt.ylabel('Average Execution Time (seconds)', fontsize=14)
    
    # Configure legend
    plt.legend(
        title='Grid Sizes',
        loc='upper left',
        bbox_to_anchor=(1.05, 1),
        fontsize=12
    )
    
    plt.grid(True, linestyle=':', color='gray')  # Lighter grid for better clarity
    plt.tight_layout()
    
    # Save the plot as an image
    plot_filename = 'game_of_life_mpi_results.png'
    plt.savefig(plot_filename, dpi=300)  # High resolution for better clarity
    print(f"Plot saved as '{plot_filename}'.")
    plt.show()

def main():
    # Specify the CSV file with results
    csv_file = "game_of_life_mpi_results.csv"
    
    # Call the plotting function
    plot_results(csv_file)

if __name__ == "__main__":
    main()
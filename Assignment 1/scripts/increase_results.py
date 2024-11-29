import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV data
csv_file = "increase_results.csv"
data = pd.read_csv(csv_file)

# Filter only the rows for "Average" times
average_data = data[data['Run'] == "Average"]

# Prepare the plot
plt.figure(figsize=(12, 8))

# Create a bar plot for average execution times for each implementation and thread count
unique_threads = sorted(average_data['Threads'].unique())
bar_width = 0.35  # Width of the bars
x_positions = np.arange(len(unique_threads))  # Positions for thread counts on the x-axis

# Loop through each implementation to create grouped bars
implementations = average_data['Implementation'].unique()
for idx, implementation in enumerate(implementations):
    subset = average_data[average_data['Implementation'] == implementation]
    avg_times = [
        subset[subset['Threads'] == thread]['Average Time (s)'].values[0] 
        if thread in subset['Threads'].values 
        else 0 
        for thread in unique_threads
    ]
    plt.bar(x_positions + idx * bar_width, avg_times, bar_width, label=implementation)

# Update x-axis labels and positions
plt.xticks(x_positions + (bar_width * (len(implementations) - 1) / 2), [str(thread) for thread in unique_threads], rotation=45)
plt.xlabel('Threads', fontsize=14)
plt.ylabel('Average Execution Time (s)', fontsize=14)
plt.title('Average Execution Time Comparison: increase vs increase_atomic', fontsize=16)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save and show the plot
plt.savefig("increase_results.png")
plt.show()
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_file = "increase_results.csv"
data = pd.read_csv(csv_file)

# Filter only the rows for "Average" times
average_data = data[data['Run'] == "Average"]

# Prepare the plot
plt.figure(figsize=(12, 8))

# Plot average execution times for each implementation and thread count
for implementation in average_data['Implementation'].unique():
    subset = average_data[average_data['Implementation'] == implementation]
    threads = subset['Threads']  # Use only threads corresponding to the implementation
    avg_times = subset['Average Time (s)']
    plt.plot(threads, avg_times, label=f"{implementation}", marker='o')

# Use a log scale for thread count (optional)
plt.xscale('log', base=2)

# Add labels, legend, and title
plt.xlabel('Threads (log scale)', fontsize=14)
plt.ylabel('Average Execution Time (s)', fontsize=14)
plt.title('Average Execution Time Comparison: increase vs increase_atomic', fontsize=16)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save and show the plot
plt.savefig("increase_results_plot.png")
plt.show()
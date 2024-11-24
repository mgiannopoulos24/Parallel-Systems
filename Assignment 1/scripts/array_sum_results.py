import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_file = "array_sum_results.csv"
data = pd.read_csv(csv_file)

# Get the unique thread counts
threads = sorted(data['Threads'].unique())

# Calculate the mean execution time for each thread count
means = []
for thread_count in threads:
    subset = data[data['Threads'] == thread_count]
    mean_time = subset['Execution Time (s)'].mean()  # Calculate the mean execution time
    means.append(mean_time)

# Prepare the plot
plt.figure(figsize=(12, 8))

# Plot the mean execution times
plt.plot(threads, means, label="array_sum", marker='o')

# Log scale for thread count if needed (optional)
plt.xscale('log', base=2)

# Add labels, legend, and title
plt.xlabel('Threads (log scale)', fontsize=14)
plt.ylabel('Execution Time (s)', fontsize=14)
plt.title('Execution Time for array_sum', fontsize=16)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save and show the plot
plt.savefig("array_sum_results_plot.png")
plt.show()

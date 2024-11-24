import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_file = "increase_results.csv"
data = pd.read_csv(csv_file)

# Group data by implementation and threads
implementations = data['Implementation'].unique()
threads = sorted(data['Threads'].unique())

# Prepare the plot
plt.figure(figsize=(12, 8))

# Plot execution times for each implementation and thread count
for implementation in implementations:
    means = []
    for thread_count in threads:
        subset = data[(data['Implementation'] == implementation) & (data['Threads'] == thread_count)]
        mean_time = subset['Execution Time (s)'].mean()  # Calculate the mean execution time
        means.append(mean_time)

    # Plot the mean execution times
    plt.plot(threads, means, label=f"{implementation}", marker='o')

# Log scale for thread count if needed (optional)
plt.xscale('log', base=2)

# Add labels, legend, and title
plt.xlabel('Threads (log scale)', fontsize=14)
plt.ylabel('Execution Time (s)', fontsize=14)
plt.title('Execution Time Comparison: increase vs increase_atomic', fontsize=16)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save and show the plot
plt.savefig("increase_results_plot.png")
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_file = "gauss_elimination_results.csv"
data = pd.read_csv(csv_file)

# Get the unique thread counts
threads = sorted(data['Threads'].unique())

# Get the unique sizes
sizes = sorted(data['Size'].unique())

# Prepare a plot for each size
plt.figure(figsize=(12, 8))

# Iterate over each size to plot the results
for size in sizes:
    # Subset the data for the current size
    subset = data[data['Size'] == size]
    
    # Calculate the mean execution time for each thread count
    means = []
    for thread_count in threads:
        thread_subset = subset[subset['Threads'] == thread_count]
        mean_time = thread_subset['Time (s)'].mean()  # Calculate the mean execution time
        means.append(mean_time)
    
    # Plot the mean execution times
    plt.plot(threads, means, label=f"Size {size}", marker='o')

# Log scale for thread count (optional)
plt.xscale('log', base=2)

# Add labels, legend, and title
plt.xlabel('Threads (log scale)', fontsize=14)
plt.ylabel('Execution Time (s)', fontsize=14)
plt.title('Execution Time for Gauss Elimination', fontsize=16)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save and show the plot
plt.savefig("gauss_elimination_results_plot.png")
plt.show()

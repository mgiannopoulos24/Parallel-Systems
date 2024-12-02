import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_file = "monte_carlo_results.csv"
data = pd.read_csv(csv_file)

# Calculate speedup
data['Speedup'] = data['Sequential Time (s)'] / data['Parallel Time (s)']

# Group data by threads
threads = data['Threads'].unique()

# Plot speedup for each thread count
plt.figure(figsize=(12, 8))

for thread_count in threads:
    subset = data[data['Threads'] == thread_count]
    plt.plot(subset['Throws'], subset['Speedup'], label=f"Speedup (Threads={thread_count})", marker='o')

# Add labels, legend, and title
plt.xscale('log')  # Use logarithmic scale for the x-axis
plt.xlabel('Throws (log scale)', fontsize=14)
plt.ylabel('Speedup', fontsize=14)
plt.title('Monte Carlo Simulation: Speedup vs Throws', fontsize=16)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save and show the plot
plt.savefig("monte_carlo_speedup.png")
plt.show()

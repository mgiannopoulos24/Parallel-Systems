import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_file = "monte_carlo_results.csv"
data = pd.read_csv(csv_file)

# Group data by threads
threads = data['Threads'].unique()

# Plot sequential and parallel times for each thread count
plt.figure(figsize=(12, 8))

for thread_count in threads:
    subset = data[data['Threads'] == thread_count]
    # plt.plot(subset['Throws'], subset['Sequential Time (s)'], label=f"Seq Time (Threads={thread_count})", linestyle="--") # Uncomment to plot sequential times
    plt.plot(subset['Throws'], subset['Parallel Time (s)'], label=f"Par Time (Threads={thread_count})", marker='o')

# Add labels, legend, and title
plt.xlabel('Throws (log scale)', fontsize=14)
plt.ylabel('Time (s)', fontsize=14)
plt.title('Monte Carlo Simulation: Parallel Times', fontsize=16)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save and show the plot
plt.savefig("monte_carlo_plot.png")
plt.show()

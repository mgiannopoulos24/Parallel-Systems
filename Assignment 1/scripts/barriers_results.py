import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_file = "barrier_results.csv"
data = pd.read_csv(csv_file)

# Filter out average rows and calculate the mean execution time for each executable and thread count
filtered_data = data[data['Run'] != "Average"]
data['Execution Time (s)'] = pd.to_numeric(data['Execution Time (s)'], errors='coerce')

average_times = (
    filtered_data.groupby(['Executable', 'Threads'])['Execution Time (s)']
    .mean()
    .reset_index()
)

# Plot average execution time for each executable
plt.figure(figsize=(12, 8))

executables = average_times['Executable'].unique()
for exe in executables:
    subset = average_times[average_times['Executable'] == exe]
    plt.plot(
        subset['Threads'],
        subset['Execution Time (s)'],
        label=f"{exe}",
        marker='o'
    )

# Add labels, legend, and title
plt.xlabel('Threads (log scale)', fontsize=14)
plt.ylabel('Average Execution Time (s)', fontsize=14)
plt.title('Barrier Implementations: Execution Time vs Threads', fontsize=16)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save and show the plot
plt.savefig("barrier_execution_times.png")
plt.show()

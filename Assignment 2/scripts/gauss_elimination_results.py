import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_file = "gauss_elimination_results.csv"
data = pd.read_csv(
    csv_file,
    names=['Grid Size', 'Threads', 'Mode', 'Schedule', 'Run', 'Execution Time (s)'],
    header=None
)

# Filter rows containing the word "Average" in the "Run" column
data = data[data['Run'].str.contains('Average', na=False)]

# Ensure required columns exist
required_columns = ['Grid Size', 'Threads', 'Mode', 'Schedule', 'Execution Time (s)']
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"Missing required column: {col}")

# Convert Threads to numeric and handle non-numeric values
data['Threads'] = pd.to_numeric(data['Threads'], errors='coerce')
data['Execution Time (s)'] = pd.to_numeric(data['Execution Time (s)'], errors='coerce')

# Get the unique thread counts and grid sizes
threads = sorted(data['Threads'].dropna().unique())
grid_sizes = sorted(data['Grid Size'].unique())

# Plot Execution Time
plt.figure(figsize=(14, 10))

# Iterate over each grid size, mode, and schedule to plot the results
for grid_size in grid_sizes:
    for mode in data['Mode'].unique():
        for schedule in data['Schedule'].unique():
            # Subset the data for the current combination of grid size, mode, and schedule
            subset = data[(data['Grid Size'] == grid_size) &
                          (data['Mode'] == mode) &
                          (data['Schedule'] == schedule)]
            
            # Calculate the mean execution time for each thread count
            means = []
            for thread_count in threads:
                thread_subset = subset[subset['Threads'] == thread_count]
                mean_time = thread_subset['Execution Time (s)'].mean()
                means.append(mean_time)
            
            # Plot the mean execution times
            label = f"Size {grid_size}, Mode {mode}, Schedule {schedule}"
            plt.plot(threads, means, label=label, marker='o')

# Plotting Execution Time
plt.xlabel('Threads', fontsize=14)
plt.ylabel('Execution Time (s)', fontsize=14)
plt.title('Execution Time for Grid Size, Mode, and Schedule', fontsize=16)
plt.xticks(threads)
plt.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

# Save the plot for Execution Time
plt.tight_layout()
plt.savefig("gauss_elimination_results.png", bbox_inches='tight')
plt.close()

# Plot Speedup
plt.figure(figsize=(14, 10))

# Iterate over each grid size, mode, and schedule to plot the results
for grid_size in grid_sizes:
    for mode in data['Mode'].unique():
        for schedule in data['Schedule'].unique():
            # Subset the data for the current combination of grid size, mode, and schedule
            subset = data[(data['Grid Size'] == grid_size) &
                          (data['Mode'] == mode) &
                          (data['Schedule'] == schedule)]
            
            # Calculate the mean execution time for each thread count
            means = []
            for thread_count in threads:
                thread_subset = subset[subset['Threads'] == thread_count]
                mean_time = thread_subset['Execution Time (s)'].mean()
                means.append(mean_time)
            
            # Calculate and plot speedup
            if means[0] > 0:  # Avoid division by zero
                serial_time = means[0]  # Serial time (minimum threads)
                speedup = [serial_time / time if time > 0 else 0 for time in means]
                label = f"Size {grid_size}, Mode {mode}, Schedule {schedule}"
                plt.plot(threads, speedup, label=label, marker='o')

# Plotting Speedup
plt.xlabel('Threads', fontsize=14)
plt.ylabel('Speedup', fontsize=14)
plt.title('Gauss Elimination Speedup (Average)', fontsize=16)
plt.xticks(threads)
plt.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

# Save the plot for Speedup
plt.tight_layout()
plt.savefig("gauss_elimination_speedup.png", bbox_inches='tight')
plt.close()

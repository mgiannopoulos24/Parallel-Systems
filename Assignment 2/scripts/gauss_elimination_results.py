import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_file = "gauss_elimination_results.csv"
data = pd.read_csv(csv_file)

# Ensure required columns exist
required_columns = ['Grid Size', 'Threads', 'Mode', 'Schedule', 'Run', 'Execution Time (s)']
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"Missing required column: {col}")

# Get the unique thread counts and grid sizes
threads = sorted(data['Threads'].unique())
grid_sizes = sorted(data['Grid Size'].unique())

# Plot Execution Time
plt.figure(figsize=(14, 10))  # Increase the figure size

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
                mean_time = thread_subset['Execution Time (s)'].mean()  # Calculate the mean execution time
                means.append(mean_time)
            
            # Plot the mean execution times
            label = f"Size {grid_size}, Mode {mode}, Schedule {schedule}"
            plt.plot(threads, means, label=label, marker='o')

# Plotting Execution Time
plt.xlabel('Threads', fontsize=14)
plt.ylabel('Execution Time (s)', fontsize=14)
plt.title('Execution time for Grid Size, Mode and Schedule', fontsize=16)

plt.xticks(threads)  # Set x-ticks to thread counts
plt.grid(True)

# Adjust legend position and size
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)  # Move legend further to the right

# Save the plot for Execution Time
plt.tight_layout()
plt.savefig("gauss_elimination_results.png", bbox_inches='tight')  # Ensure legend is fully visible
plt.close()

# Plot Speedup
plt.figure(figsize=(14, 10))  # Increase the figure size

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
                mean_time = thread_subset['Execution Time (s)'].mean()  # Calculate the mean execution time
                means.append(mean_time)
            
            # Calculate and plot speedup
            if means[0] != 0:  # Avoid division by zero
                serial_time = means[0]  # Serial time (thread count == minimum threads)
                speedup = [serial_time / time if time > 0 else 0 for time in means]
                label = f"Size {grid_size}, Mode {mode}, Schedule {schedule}"
                plt.plot(threads, speedup, label=label, marker='o')

# Plotting Speedup
plt.xlabel('Threads', fontsize=14)
plt.ylabel('Speedup', fontsize=14)
plt.title('Gauss Elimination Speedup', fontsize=16)

# Use custom x-ticks
plt.xticks(threads)  # Set x-ticks to thread counts

plt.grid(True)

# Adjust legend position and size
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)  # Move legend further to the right

# Save the plot for Speedup
plt.tight_layout()
plt.savefig("gauss_elimination_speedup.png", bbox_inches='tight')  # Ensure legend is fully visible
plt.close()

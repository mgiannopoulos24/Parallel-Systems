import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_file = "matrix_vector_mpi_results.csv"  # Update CSV file name
data = pd.read_csv(csv_file)

# Convert the 'Run' column to numeric, forcing errors to NaN (if any invalid values exist)
data['Run'] = pd.to_numeric(data['Run'], errors='coerce')

# Ensure required columns exist
required_columns = ['Grid Size', 'Run', 'Execution Time (s)']
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"Missing required column: {col}")

# Get the unique grid sizes
grid_sizes = sorted(data['Grid Size'].unique())

# Plot Execution Time
plt.figure(figsize=(14, 10))  # Increase the figure size

# Iterate over each grid size to plot the results
for grid_size in grid_sizes:
    # Subset the data for the current grid size
    subset = data[data['Grid Size'] == grid_size]
    
    # Calculate the mean execution time for each run
    means = []
    for run in range(1, int(subset['Run'].max()) + 1):
        run_subset = subset[subset['Run'] == run]
        mean_time = run_subset['Execution Time (s)'].mean()  # Calculate the mean execution time
        means.append(mean_time)
    
    # Plot the mean execution times
    label = f"Size {grid_size}"
    plt.plot(range(1, len(means) + 1), means, label=label, marker='o')

# Plotting Execution Time
plt.xlabel('Run', fontsize=14)
plt.ylabel('Execution Time (s)', fontsize=14)
plt.title('Execution Time for Different Grid Sizes', fontsize=16)

plt.xticks(range(1, len(means) + 1))  # Set x-ticks to run numbers
plt.grid(True)

# Adjust legend position and size
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)  # Move legend further to the right

# Save the plot for Execution Time
plt.tight_layout()
plt.savefig("matrix_vector_mpi_results.png", bbox_inches='tight')  # Ensure legend is fully visible
plt.close()

# Plot Speedup (assuming comparison with serial execution)
plt.figure(figsize=(14, 10))  # Increase the figure size

# Iterate over each grid size to plot the results
for grid_size in grid_sizes:
    # Subset the data for the current grid size
    subset = data[data['Grid Size'] == grid_size]
    
    # Calculate the mean execution time for each run
    means = []
    for run in range(1, int(subset['Run'].max()) + 1):
        run_subset = subset[subset['Run'] == run]
        mean_time = run_subset['Execution Time (s)'].mean()  # Calculate the mean execution time
        means.append(mean_time)
    
    # Calculate and plot speedup
    if means[0] != 0:  # Avoid division by zero
        serial_time = means[0]  # Serial time (run == 1)
        speedup = [serial_time / time if time > 0 else 0 for time in means]
        label = f"Size {grid_size}"
        plt.plot(range(1, len(speedup) + 1), speedup, label=label, marker='o')

# Plotting Speedup
plt.xlabel('Run', fontsize=14)
plt.ylabel('Speedup', fontsize=14)
plt.title('Speedup for Matrix-Vector Multiplication', fontsize=16)

plt.xticks(range(1, len(speedup) + 1))  # Set x-ticks to run numbers

plt.grid(True)

# Adjust legend position and size
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)  # Move legend further to the right

# Save the plot for Speedup
plt.tight_layout()
plt.savefig("matrix_vector_multiplication_speedup.png", bbox_inches='tight')  # Ensure legend is fully visible
plt.close()

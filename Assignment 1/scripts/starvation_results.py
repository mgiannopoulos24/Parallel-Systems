import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
csv_file = "starvation_results.csv"
data = pd.read_csv(csv_file)

# Plot average reader and writer times by test case
plt.figure(figsize=(14, 8))

# Plot reader and writer times
plt.plot(
    data["Test Case"], 
    data["Total Reader Time"], 
    label="Total Reader Time", 
    marker='o', 
    linestyle='-', 
    color='blue'
)
plt.plot(
    data["Test Case"], 
    data["Total Writer Time"], 
    label="Total Writer Time", 
    marker='s', 
    linestyle='--', 
    color='orange'
)

# Add labels, legend, and title
plt.xlabel('Test Case', fontsize=14)
plt.ylabel('Total Time (s)', fontsize=14)
plt.title('Total Reader and Writer Times by Test Case', fontsize=16)
plt.xticks(data["Test Case"], rotation=45)  # Rotate x-axis labels for readability
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# Save and show the plot
plt.savefig("test_case_times_plot.png")
plt.show()

#!/usr/bin/env python3

import subprocess
import csv
import math
import sys
from pathlib import Path

# Configuration
EXECUTABLE = Path("../build/monte_carlo")
OUTPUT_CSV = "monte_carlo_results.csv"
POINT_COUNTS = [10**i for i in range(0, 10)]  # 10^0 to 10^9 (10^0=1 may be too small)
THREAD_COUNTS = [4, 8, 16, 32]
RUNS_PER_TEST = 5

def run_executable(threads, points):
    """
    Runs the Monte Carlo executable with the specified number of threads and points.
    Returns a dictionary with 'sequential_time', 'parallel_time', and 'pi'.
    """
    try:
        # Execute the command and capture the output
        result = subprocess.run(
            [str(EXECUTABLE), str(threads), str(points)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error executing {EXECUTABLE} with threads={threads}, points={points}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)

    # Initialize variables
    seq_time = None
    par_time = None
    pi_estimate = None
    seq_pi_estimate = None  # To capture Sequential π estimate if needed

    # Parse the output
    for line in result.stdout.splitlines():
        if "Sequential time" in line:
            try:
                # Split by ':' and then take the first part before 'seconds'
                seq_time_str = line.split(':')[1].strip().split()[0]
                seq_time = float(seq_time_str)
            except (IndexError, ValueError):
                print(f"Failed to parse sequential time from line: {line}")
                sys.exit(1)
        elif "Parallel time" in line:
            try:
                par_time_str = line.split(':')[1].strip().split()[0]
                par_time = float(par_time_str)
            except (IndexError, ValueError):
                print(f"Failed to parse parallel time from line: {line}")
                sys.exit(1)
        elif "Parallel π estimate" in line:
            try:
                pi_estimate = float(line.split()[-1])
            except ValueError:
                print(f"Failed to parse π estimate from line: {line}")
                sys.exit(1)
        elif "Sequential π estimate" in line:
            try:
                seq_pi_estimate = float(line.split()[-1])
            except ValueError:
                print(f"Failed to parse sequential π estimate from line: {line}")
                sys.exit(1)

    if seq_time is None or par_time is None or pi_estimate is None:
        print(f"Incomplete output from executable for threads={threads}, points={points}")
        print("Output was:")
        print(result.stdout)
        sys.exit(1)

    return {
        "sequential_time": seq_time,
        "parallel_time": par_time,
        "pi": pi_estimate,
        "sequential_pi": seq_pi_estimate  # Optional: include if you want to track it
    }

def main():
    # Check if the executable exists and is executable
    if not EXECUTABLE.is_file():
        print(f"Executable not found at {EXECUTABLE}")
        sys.exit(1)
    if not os.access(EXECUTABLE, os.X_OK):
        print(f"Executable at {EXECUTABLE} is not executable.")
        sys.exit(1)

    # Open the CSV file for writing
    with open(OUTPUT_CSV, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header
        csv_writer.writerow(["Threads", "Throws", "Sequential Time (s)", "Parallel Time (s)", "Pi"])

        # Iterate over each thread count
        for threads in THREAD_COUNTS:
            print(f"Testing with {threads} threads")
            print(f"{'Throws':<15} {'Sequential Time (s)':<25} {'Parallel Time (s)':<25} {'π':<15}")
            print(f"{'-'*15} {'-'*25} {'-'*25} {'-'*15}")

            for points in POINT_COUNTS:
                seq_total_time = 0.0
                par_total_time = 0.0
                pi_value = 0.0

                for run in range(RUNS_PER_TEST):
                    results = run_executable(threads, points)
                    seq_total_time += results["sequential_time"]
                    par_total_time += results["parallel_time"]
                    pi_value = results["pi"]  # Assuming π estimate is consistent across runs

                # Calculate averages
                avg_seq_time = seq_total_time / RUNS_PER_TEST
                avg_par_time = par_total_time / RUNS_PER_TEST

                # Format π to 6 decimal places
                pi_formatted = f"{pi_value:.6f}"

                # Print the results
                print(f"{points:<15} {avg_seq_time:<25.6f} {avg_par_time:<25.6f} {pi_formatted:<15}")

                # Write to CSV
                csv_writer.writerow([threads, points, f"{avg_seq_time:.6f}", f"{avg_par_time:.6f}", pi_formatted])

            print()  # Blank line for readability

    print(f"Tests completed. Results saved to {OUTPUT_CSV}.")

if __name__ == "__main__":
        import os  # Moved import inside to avoid NameError for os.access
        main()

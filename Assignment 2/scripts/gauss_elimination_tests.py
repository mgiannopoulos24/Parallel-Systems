#!/usr/bin/env python3

import subprocess
import csv
import sys
import os
import time
from pathlib import Path

# Configuration
EXECUTABLE = Path("../build/gauss_elimination")
OUTPUT_CSV = "gauss_elimination_results.csv"
SIZE_LIST = [100, 1000, 5000, 10000]  # Test sizes: n = 100, 1000, 5000, 10000
THREAD_COUNTS = [2, 4, 8, 16]  # Thread counts to test
RUNS_PER_TEST = 5  # Number of runs per test for averaging

def run_executable(threads, size, algo_type, exec_type):
    """
    Runs the Gauss Elimination executable with the specified parameters:
    - threads: number of threads
    - size: size of the matrix (n)
    - algo_type: 'row' or 'column' (row-wise or column-wise algorithm)
    - exec_type: 'serial' or 'parallel'
    Returns a dictionary with 'time' and 'error'.
    """
    start_time = time.time()  # Start time to measure the execution time

    try:
        # Run the executable
        result = subprocess.run(
            [str(EXECUTABLE), str(size), exec_type, algo_type, str(threads)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error executing {EXECUTABLE} with threads={threads}, size={size}, algo={algo_type}, exec={exec_type}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time

    # The error is not provided by the executable, so we'll just return None for now.
    # You can add error calculation logic here if needed.
    error = None

    return {
        "time": elapsed_time,
        "error": error
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
        csv_writer.writerow(["Threads", "Size", "Algorithm", "Execution Type", "Time (s)", "Error"])

        # Iterate over each thread count and matrix size
        for threads in THREAD_COUNTS:
            print(f"Testing with {threads} threads")
            print(f"{'Size':<15} {'Algorithm':<12} {'Execution Type':<15} {'Time (s)':<25} {'Error':<15}")
            print(f"{'-'*15} {'-'*12} {'-'*15} {'-'*25} {'-'*15}")

            for size in SIZE_LIST:
                for algo in ['row', 'column']:  # Loop over row-wise and column-wise algorithms
                    for exec_type in ['serial', 'parallel']:  # Loop over serial and parallel execution
                        total_time = 0.0
                        total_error = 0.0

                        for run in range(RUNS_PER_TEST):
                            results = run_executable(threads, size, algo, exec_type)
                            total_time += results["time"]
                            if results["error"] is not None:
                                total_error += results["error"]

                        # Calculate averages
                        avg_time = total_time / RUNS_PER_TEST
                        avg_error = total_error / RUNS_PER_TEST if RUNS_PER_TEST > 0 else 0.0

                        # Print the results
                        print(f"{size:<15} {algo:<12} {exec_type:<15} {avg_time:<25.6f} {avg_error:<15.6f}")

                        # Write to CSV
                        csv_writer.writerow([threads, size, algo, exec_type, f"{avg_time:.6f}", f"{avg_error:.6f}"])

            print()  # Blank line for readability

    print(f"Tests completed. Results saved to {OUTPUT_CSV}.")

if __name__ == "__main__":
    main()

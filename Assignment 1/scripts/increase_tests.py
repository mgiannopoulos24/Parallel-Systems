#!/usr/bin/env python3

import subprocess
import csv
import time
import sys
import os
from pathlib import Path

# Configuration
IMPLEMENTATIONS = {
    "increase": "../build/increase",
    "increase_atomic": "../build/increase_atomic"
}
OUTPUT_CSV = "increase_results.csv"
THREAD_COUNTS = [1, 2, 4, 8, 16, 32]
ITERATIONS_VALUES = [1234567, 9876543, 456789012, 1234567890, 34100654080]
RUNS_PER_TEST = 5

def run_test(exec_path: Path, implementation_name: str, iterations: int, csv_writer: csv.writer):
    """
    Runs the specified implementation executable with different thread counts
    and iterations, measures execution times, and records the results to the CSV file.

    Args:
        exec_path (Path): Path to the implementation executable.
        implementation_name (str): Name of the implementation (for display and CSV).
        iterations (int): Number of iterations to test.
        csv_writer (csv.writer): CSV writer object to record the results.
    """
    for threads in THREAD_COUNTS:
        print(f"\nTesting {implementation_name} with {threads} threads and {iterations} iterations")
        # Print table header for formatted display
        print(f"{'Implementation':<20} {'Threads':<10} {'Iterations':<15} {'Run':<10} {'Execution Time (s)':<20}")
        print(f"{'-'*20} {'-'*10} {'-'*15} {'-'*10} {'-'*20}")

        total_time = 0.0

        for run in range(1, RUNS_PER_TEST + 1):
            # Measure execution time
            start_time = time.time()
            try:
                # Run the executable with the specified number of threads and iterations
                subprocess.run(
                    [str(exec_path), str(threads), str(iterations)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print(f"Error: Execution failed for {implementation_name} with {threads} threads and {iterations} iterations on run {run}")
                print(f"Command: {' '.join(e.cmd)}")
                print(f"Return Code: {e.returncode}")
                sys.exit(1)
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Accumulate total execution time
            total_time += elapsed_time

            # Print formatted row to the console
            print(f"{implementation_name:<20} {threads:<10} {iterations:<15} {run:<10} {elapsed_time:<20.5f}")

            # Save the result to the CSV (Average Time column left empty for individual runs)
            csv_writer.writerow([implementation_name, threads, iterations, run, f"{elapsed_time:.5f}", ""])

        # Calculate and print the average execution time
        avg_time = total_time / RUNS_PER_TEST
        print(f"Average time for {implementation_name} with {threads} threads and {iterations} iterations: {avg_time:.5f} seconds")

        # Append average time to the CSV
        csv_writer.writerow([implementation_name, threads, iterations, "Average", "", f"{avg_time:.5f}"])

def main():
    # Verify that all implementation executables exist and are executable
    valid_implementations = {}
    for name, path_str in IMPLEMENTATIONS.items():
        exec_path = Path(path_str)
        if exec_path.is_file() and os.access(exec_path, os.X_OK):
            valid_implementations[name] = exec_path
        else:
            print(f"Warning: Executable '{exec_path}' not found or not executable. Skipping '{name}'.")

    if not valid_implementations:
        print("Error: No valid implementation executables found. Exiting.")
        sys.exit(1)

    # Open the CSV file for writing
    try:
        with open(OUTPUT_CSV, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write the header
            csv_writer.writerow(["Implementation", "Threads", "Iterations", "Run", "Execution Time (s)", "Average Time (s)"])

            # Iterate over each valid implementation
            for implementation_name, exec_path in valid_implementations.items():
                for iterations in ITERATIONS_VALUES:
                    run_test(exec_path, implementation_name, iterations, csv_writer)

        # Notify completion
        print(f"\nAll tests completed. Results saved to {OUTPUT_CSV}.")

    except IOError as e:
        print(f"IOError while handling the CSV file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
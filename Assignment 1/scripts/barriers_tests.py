#!/usr/bin/env python3

import subprocess
import csv
import time
import sys
import os
from pathlib import Path

# Configuration
BARRIERS = ["barrier_mutex_cond", "barrier_pthread", "barrier_sense_reversal"]
BUILD_DIR = Path("../build")
OUTPUT_CSV = "barrier_results.csv"
THREAD_COUNTS = [2, 4, 8, 16, 32]
RUNS_PER_TEST = 5

def run_test(barrier_exec: Path, barrier_name: str, csv_writer: csv.writer):
    """
    Runs the barrier executable with different thread counts, measures execution times,
    and records the results to the CSV file.

    Args:
        barrier_exec (Path): Path to the barrier executable.
        barrier_name (str): Name of the barrier (for display and CSV).
        csv_writer (csv.writer): CSV writer object to record the results.
    """
    for threads in THREAD_COUNTS:
        print(f"\nTesting {barrier_name} with {threads} threads")
        # Print table header for formatted display
        print(f"{'Barrier':<25} {'Threads':<10} {'Run':<10} {'Execution Time (s)':<20}")
        print(f"{'-'*25} {'-'*10} {'-'*10} {'-'*20}")

        total_time = 0.0

        for run in range(1, RUNS_PER_TEST + 1):
            # Measure execution time
            start_time = time.time()
            try:
                # Run the executable with the specified number of threads
                subprocess.run(
                    [str(barrier_exec), str(threads)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print(f"Error: Execution failed for {barrier_name} with {threads} threads on run {run}")
                print(f"Command: {' '.join(e.cmd)}")
                print(f"Return Code: {e.returncode}")
                sys.exit(1)
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Accumulate total execution time
            total_time += elapsed_time

            # Print formatted row to the console
            print(f"{barrier_name:<25} {threads:<10} {run:<10} {elapsed_time:<20.5f}")

            # Save the result to the CSV (Average Time column left empty for individual runs)
            csv_writer.writerow([barrier_name, threads, run, f"{elapsed_time:.5f}", ""])

        # Calculate and print the average execution time
        avg_time = total_time / RUNS_PER_TEST
        print(f"Average time for {barrier_name} with {threads} threads: {avg_time:.5f} seconds")

        # Append average time to the CSV
        csv_writer.writerow([barrier_name, threads, "Average", "", f"{avg_time:.5f}"])

def main():
    # Check if all barrier executables exist and are executable
    barrier_executables = {}
    for barrier in BARRIERS:
        exec_path = BUILD_DIR / barrier
        if exec_path.is_file() and os.access(exec_path, os.X_OK):
            barrier_executables[barrier] = exec_path
        else:
            print(f"Warning: Executable {exec_path} not found or not executable. Skipping this barrier.")
    
    if not barrier_executables:
        print("Error: No valid barrier executables found. Exiting.")
        sys.exit(1)

    # Open the CSV file for writing
    try:
        with open(OUTPUT_CSV, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write the header
            csv_writer.writerow(["Barrier", "Threads", "Run", "Execution Time (s)", "Average Execution Time (s)"])

            # Iterate over each barrier executable
            for barrier_name, barrier_exec in barrier_executables.items():
                run_test(barrier_exec, barrier_name, csv_writer)

        # Notify completion
        print(f"\nAll tests completed. Results saved to {OUTPUT_CSV}.")

    except IOError as e:
        print(f"IOError while handling the CSV file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

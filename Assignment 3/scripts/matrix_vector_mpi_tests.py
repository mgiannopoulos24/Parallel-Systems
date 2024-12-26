#!/usr/bin/env python3

import subprocess
import csv
import sys
import os
import time
from pathlib import Path

# Configuration
EXECUTABLE = Path("../build/matrix_vector_mpi")  
OUTPUT_CSV = "matrix_vector_mpi_results.csv"
SIZE_LIST = [100, 1000, 5000, 10000]  # Grid sizes to test
RUNS_PER_TEST = 5

def run_executable(size):
    start_time = time.time()
    try:
        command = [str(EXECUTABLE), str(size)] 
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error executing {EXECUTABLE} with size={size}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)

    elapsed_time = time.time() - start_time
    return elapsed_time

def main():
    if not EXECUTABLE.is_file():
        print(f"Executable not found at {EXECUTABLE}")
        sys.exit(1)
    if not os.access(EXECUTABLE, os.X_OK):
        print(f"Executable at {EXECUTABLE} is not executable.")
        sys.exit(1)

    with open(OUTPUT_CSV, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Grid Size", "Run", "Execution Time (s)"])

        for size in SIZE_LIST:
            print(f"Testing with grid size {size}")
            total_time = 0.0
            for run in range(1, RUNS_PER_TEST + 1):
                exec_time = run_executable(size)
                total_time += exec_time
                print(f"{size:<10} {run:<10} {exec_time:<20.6f}")
                csv_writer.writerow([f"{size}x{size}", run, f"{exec_time:.6f}"])

            avg_time = total_time / RUNS_PER_TEST
            print(f"\nAverage time for grid size {size}: {avg_time:.6f} seconds.\n")
            csv_writer.writerow([f"{size}x{size}", "Average", f"{avg_time:.6f}"])

if __name__ == "__main__":
    main()

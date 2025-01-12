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
MACHINES_FILE = Path("../machines")  # Path to the machines file
PROCESSES = [2, 4, 8]  # Number of processes to test
SIZE_LIST = [100, 1000, 5000, 10000]  # Grid sizes to test
RUNS_PER_TEST = 5

def run_executable(proc, size):
    start_time = time.time()
    try:
        command = ["mpiexec", "-f", str(MACHINES_FILE), "-n", str(proc), str(EXECUTABLE), str(size)]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error executing {EXECUTABLE} with size={size} and processes={proc}")
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
        csv_writer.writerow(["Processes", "Grid Size", "Run", "Execution Time (s)"])

        for proc in PROCESSES:
            for size in SIZE_LIST:
                print(f"Testing with {proc} processes and grid size {size}")
                print(f"{'Processes':<12} {'Grid':<10} {'Execution Time (s)':<20}")
                print(f"{'-'*12} {'-'*10} {'-'*20}")
                
                total_time = 0.0
                for run in range(1, RUNS_PER_TEST + 1):
                    exec_time = run_executable(proc, size)
                    total_time += exec_time
                    print(f"{proc:<10} {size:<10} {run:<10} {exec_time:<20.6f}")
                    csv_writer.writerow([proc, f"{size}x{size}", run, f"{exec_time:.6f}"])

                avg_time = total_time / RUNS_PER_TEST
                print(f"\nAverage time for {proc} processes and grid size {size}: {avg_time:.6f} seconds.\n")
                csv_writer.writerow([proc, f"{size}x{size}", "Average", f"{avg_time:.6f}"])

if __name__ == "__main__":
    main()

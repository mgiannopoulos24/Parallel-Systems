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
SIZE_LIST = [100, 1000, 5000, 10000]
THREAD_COUNTS = [2, 4, 8, 16]
SCHEDULE_MODES = ["static", "dynamic", "guided", "runtime"]
RUNS_PER_TEST = 5

def run_executable(threads, size, algo_type, exec_type, schedule_mode):
    start_time = time.time()
    try:
        command = [str(EXECUTABLE), str(size), exec_type, algo_type, str(threads), schedule_mode]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error executing {EXECUTABLE} with threads={threads}, size={size}, algo={algo_type}, exec={exec_type}, schedule={schedule_mode}")
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
        csv_writer.writerow(["Grid Size", "Threads", "Mode", "Schedule", "Run", "Execution Time (s)"])

        for threads in THREAD_COUNTS:
            print(f"Testing with {threads} threads")
            for size in SIZE_LIST:
                for algo in ['row', 'column']:
                    for exec_type in ['serial', 'parallel']:
                        for schedule_mode in SCHEDULE_MODES:
                            print(f"\nGrid Size            Threads    Mode       Schedule   Run        Execution Time (s)")
                            print(f"{'-'*20} {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*20}")

                            total_time = 0.0
                            for run in range(1, RUNS_PER_TEST + 1):
                                exec_time = run_executable(threads, size, algo, exec_type, schedule_mode)
                                total_time += exec_time
                                print(f"{size:<20} {threads:<10} {algo:<10} {exec_type:<10} {schedule_mode:<10} {run:<10} {exec_time:<20.6f}")
                                csv_writer.writerow([f"{size}x{size}", threads, algo, schedule_mode, run, f"{exec_time:.6f}"])

                            avg_time = total_time / RUNS_PER_TEST
                            print(f"\nAverage time for mode {exec_type} with {size} size and {threads} threads and schedule {schedule_mode}: {avg_time:.6f} seconds.\n")
                            csv_writer.writerow([f"{size}x{size}", threads, algo, schedule_mode, "Average", f"{avg_time:.6f}"])

if __name__ == "__main__":
    main()

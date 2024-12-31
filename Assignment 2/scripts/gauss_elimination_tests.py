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

def run_executable(size, exec_type, algo_type, schedule_mode, threads):
    start_time = time.time()
    try:
        command = [str(EXECUTABLE), str(size), exec_type, algo_type, schedule_mode, str(threads)]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # print(command) # Debug print
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

        for size in SIZE_LIST:
            for algo in ['row', 'column']:
                # Header for Serial Execution
                print(f"\nGrid Size            Threads    Mode       Schedule   Run        Execution Time (s)")
                print(f"{'-'*20} {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*20}")

                total_time = 0.0
                for run in range(1, RUNS_PER_TEST + 1):
                    exec_time = run_executable(size, "serial", algo, "none", 1)
                    total_time += exec_time
                    print(f"{size:<20} {1:<10} {algo:<10} {'none':<10} {run:<10} {exec_time:<20.6f}")
                    csv_writer.writerow([f"{size}x{size}", 1, algo, "none", run, f"{exec_time:.6f}"])

                avg_time = total_time / RUNS_PER_TEST
                print(f"\nAverage time for serial execution with grid size {size}: {avg_time:.6f} seconds.\n")
                csv_writer.writerow([f"{size}x{size}", 1, algo, "none", "Average", f"{avg_time:.6f}"])

        # Parallel Execution
        for threads in THREAD_COUNTS:
            print(f"Testing with {threads} threads")
            for size in SIZE_LIST:
                for algo in ['row', 'column']:
                    for schedule_mode in SCHEDULE_MODES:
                        print(f"\nGrid Size            Threads    Mode       Schedule   Run        Execution Time (s)")
                        print(f"{'-'*20} {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*20}")

                        total_time = 0.0
                        for run in range(1, RUNS_PER_TEST + 1):
                            exec_time = run_executable(size, "parallel", algo, schedule_mode, threads)
                            total_time += exec_time
                            print(f"{size:<20} {threads:<10} {algo:<10} {'parallel':<10} {schedule_mode:<10} {run:<10} {exec_time:<20.6f}")
                            csv_writer.writerow([f"{size}x{size}", threads, algo, schedule_mode, run, f"{exec_time:.6f}"])

                        avg_time = total_time / RUNS_PER_TEST
                        print(f"\nAverage time for parallel execution with grid size {size}, {threads} threads, schedule {schedule_mode}: {avg_time:.6f} seconds.\n")
                        csv_writer.writerow([f"{size}x{size}", threads, algo, schedule_mode, "Average", f"{avg_time:.6f}"])

        # Notify completion
        print(f"\nTests completed. Results saved to {OUTPUT_CSV}.")
    
    except IOError as e:
        print(f"IOError while handling the CSV file: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()

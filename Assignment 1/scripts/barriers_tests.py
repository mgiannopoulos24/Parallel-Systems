#!/usr/bin/env python3

import subprocess
import csv
import time
import sys
from pathlib import Path

# Configuration
EXECUTABLES = [
    Path("../build/barrier_mutex_cond"),
    Path("../build/barrier_pthread"),
    Path("../build/barrier_sense_reversal")
]
OUTPUT_CSV = "barrier_results.csv"
THREAD_COUNTS = [2, 4, 8, 16]
RUNS_PER_TEST = 5

def run_test():
    """
    Runs each executable with different thread counts and records execution times.
    Results are printed to the console and saved to a CSV file.
    """
    for exe in EXECUTABLES:
        if not exe.is_file():
            print(f"Error: The executable '{exe}' does not exist.")
            sys.exit(1)

    try:
        with open(OUTPUT_CSV, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write the header
            csv_writer.writerow(["Executable", "Threads", "Run", "Execution Time (s)", "Average Time (s)"])
            
            for exe in EXECUTABLES:
                print(f"\nTesting executable: {exe}")
                
                for threads in THREAD_COUNTS:
                    print(f"\nTesting with {threads} threads for {exe.name}")
                    # Print table header for formatted display
                    print(f"{'Executable':<25} {'Threads':<10} {'Run':<10} {'Execution Time (s)':<20}")
                    print(f"{'-'*25} {'-'*10} {'-'*10} {'-'*20}")
                    
                    total_time = 0.0
                    for run in range(1, RUNS_PER_TEST + 1):
                        # Measure execution time
                        start_time = time.time()
                        try:
                            # Run the executable with the specified number of threads
                            subprocess.run(
                                [str(exe), str(threads)],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                check=True
                            )
                        except subprocess.CalledProcessError as e:
                            print(f"Error: Execution failed for {exe.name} with threads={threads}, run={run}")
                            print(f"Command: {' '.join(e.cmd)}")
                            print(f"Return Code: {e.returncode}")
                            sys.exit(1)
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        # Accumulate total execution time
                        total_time += elapsed_time
                        # Print formatted row to the console
                        print(f"{exe.name:<25} {threads:<10} {run:<10} {elapsed_time:<20.5f}")
                        # Save the result to the CSV
                        csv_writer.writerow([exe.name, threads, run, f"{elapsed_time:.5f}", ""])
                    
                    # Calculate and print the average execution time
                    avg_time = total_time / RUNS_PER_TEST
                    print(f"Average time for {exe.name} with {threads} threads: {avg_time:.5f} seconds")
                    # Append the average time to the CSV
                    csv_writer.writerow([exe.name, threads, "Average", "", f"{avg_time:.5f}"])
        
        # Notify completion
        print(f"\nTests completed. Results saved to {OUTPUT_CSV}.")
    
    except IOError as e:
        print(f"IOError while handling the CSV file: {e}")
        sys.exit(1)

def main():
    run_test()

if __name__ == "__main__":
    main()

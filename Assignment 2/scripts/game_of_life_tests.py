#!/usr/bin/env python3

import subprocess
import csv
import time
import sys
from pathlib import Path

# Configuration
GAME_OF_LIFE_EXEC = Path("../build/game_of_life")
OUTPUT_CSV = "game_of_life_results.csv"
GRIDS = [(64, 64), (1024, 1024), (4096, 4096)]  # Grid sizes
THREAD_COUNTS = [2, 4, 8, 16]  # Thread counts
RUNS_PER_TEST = 5
GENERATIONS = 1000

def run_test():
    """
    Runs the game_of_life executable with different grid sizes, thread counts, and serial/parallel modes.
    Records execution times and saves them to a CSV file.
    """
    # Check if the executable exists and is executable
    if not GAME_OF_LIFE_EXEC.is_file():
        print(f"Error: The executable '{GAME_OF_LIFE_EXEC}' does not exist.")
        sys.exit(1)

    try:
        with open(OUTPUT_CSV, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write the header
            csv_writer.writerow(["Grid Size", "Threads", "Run", "Execution Time (s)", "Average Time (s)", "Mode"])

            # Iterate over each grid size
            for grid in GRIDS:
                rows, cols = grid
                print(f"\nTesting with grid size {rows}x{cols}")
                # Print table header for formatted display
                print(f"{'Grid Size':<20} {'Threads':<10} {'Run':<10} {'Execution Time (s)':<20} {'Mode':<10}")
                print(f"{'-'*20} {'-'*10} {'-'*10} {'-'*20} {'-'*10}")

                # Run serial test
                total_time_serial = 0.0
                for run in range(1, RUNS_PER_TEST + 1):
                    start_time = time.time()
                    try:
                        # Run the executable with serial mode (pass 1 thread)
                        command = [str(GAME_OF_LIFE_EXEC), str(GENERATIONS), str(rows), str(0), str(1)]
                        subprocess.run(
                            command,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            check=True
                        )
                        print(command) # Debug print
                    except subprocess.CalledProcessError as e:
                        print(f"Error: Execution failed for grid={grid}, serial, run={run}")
                        print(f"Command: {' '.join(e.cmd)}")
                        print(f"Return Code: {e.returncode}")
                        sys.exit(1)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    total_time_serial += elapsed_time
                    # Print formatted row to the console
                    print(f"{rows}x{cols:<20} {'1':<10} {run:<10} {elapsed_time:<20.5f} {'Serial':<10}")
                    # Save the result to the CSV
                    csv_writer.writerow([f"{rows}x{cols}", run, f"{elapsed_time:.5f}", "", "Serial"])

                avg_time_serial = total_time_serial / RUNS_PER_TEST
                print(f"Average time for serial with {rows}x{cols} grid: {avg_time_serial:.5f} seconds")
                csv_writer.writerow([f"{rows}x{cols}", "Average", "", f"{avg_time_serial:.5f}", "Serial"])

                # Run parallel tests for each thread count
                for threads in THREAD_COUNTS:
                    total_time_parallel = 0.0
                    for run in range(1, RUNS_PER_TEST + 1):
                        start_time = time.time()
                        try:
                            command = [str(GAME_OF_LIFE_EXEC), str(GENERATIONS), str(rows), str(1), str(threads)]
                            # Run the executable with the specified number of threads
                            subprocess.run(
                                command,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                check=True
                            )
                            print(command)
                        except subprocess.CalledProcessError as e:
                            print(f"Error: Execution failed for grid={grid}, threads={threads}, run={run}")
                            print(f"Command: {' '.join(e.cmd)}")
                            print(f"Return Code: {e.returncode}")
                            sys.exit(1)
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        total_time_parallel += elapsed_time
                        # Print formatted row to the console
                        print(f"{rows}x{cols:<10} {threads:<10} {run:<10} {elapsed_time:<20.5f} {'Parallel':<10}")
                        # Save the result to the CSV
                        csv_writer.writerow([f"{rows}x{cols}", threads, run, f"{elapsed_time:.5f}", "", "Parallel"])

                    avg_time_parallel = total_time_parallel / RUNS_PER_TEST
                    print(f"Average time for {threads} threads with {rows}x{cols} grid: {avg_time_parallel:.5f} seconds")
                    csv_writer.writerow([f"{rows}x{cols}", threads, "Average", "", f"{avg_time_parallel:.5f}", "Parallel"])

        # Notify completion
        print(f"\nTests completed. Results saved to {OUTPUT_CSV}.")
    
    except IOError as e:
        print(f"IOError while handling the CSV file: {e}")
        sys.exit(1)

def main():
    run_test()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import subprocess
import csv
import time
import sys
from pathlib import Path

# Configuration
GAME_OF_LIFE_EXEC = Path("../build/game_of_life_tasks")
OUTPUT_CSV = "game_of_life_tasks_results.csv"
GRIDS = [(64, 64), (1024, 1024), (4096, 4096)]  # Grid sizes
THREAD_COUNTS = [2, 4, 8, 16]  # Thread counts
RUNS_PER_TEST = 5
GENERATIONS = 1000
MODES = [0, 1, 2]  # Modes: 0 = Serial, 1 = Parallel-For, 2 = Parallel-Task

def run_test():
    """
    Runs the game_of_life_tasks executable with different grid sizes, thread counts, 
    serial/parallel modes and records execution times to a CSV file.
    """
    # Check if the executable exists and is executable
    if not GAME_OF_LIFE_EXEC.is_file():
        print(f"Error: The executable '{GAME_OF_LIFE_EXEC}' does not exist.")
        sys.exit(1)

    try:
        with open(OUTPUT_CSV, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write the header
            csv_writer.writerow(["Grid Size", "Threads", "Mode", "Run", "Execution Time (s)"])

            # Iterate over each grid size
            for grid in GRIDS:
                rows, cols = grid
                print(f"\nTesting with grid size {rows}x{cols}")
                print(f"{'Grid Size':<20} {'Threads':<10} {'Mode':<10} {'Run':<10} {'Execution Time (s)':<20}")
                print(f"{'-'*20} {'-'*10} {'-'*10} {'-'*10} {'-'*20}")

                # Run tests for each mode
                for mode in MODES:
                    # Run tests for each thread count
                    for threads in THREAD_COUNTS:
                        # For serial mode (mode 0), force thread count to 1
                        if mode == 0:
                            threads = 1

                        total_time_mode = 0.0
                        for run in range(1, RUNS_PER_TEST + 1):
                            start_time = time.time()
                            try:
                                # Run the executable with the specified mode and thread count
                                command = [str(GAME_OF_LIFE_EXEC), str(GENERATIONS), str(rows), str(mode), str(threads)]
                                subprocess.run(
                                    command,
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL,
                                    check=True
                                )
                                print(command)
                            except subprocess.CalledProcessError as e:
                                print(f"Error: Execution failed for grid={grid}, mode={mode}, threads={threads}, run={run}")
                                print(f"Command: {' '.join(e.cmd)}")
                                print(f"Return Code: {e.returncode}")
                                sys.exit(1)
                            end_time = time.time()
                            elapsed_time = end_time - start_time
                            total_time_mode += elapsed_time
                            # Print formatted row to the console
                            print(f"{rows}x{cols:<20} {threads:<10} {mode:<10} {run:<10} {elapsed_time:<20.5f}")
                            # Save the result to the CSV
                            csv_writer.writerow([f"{rows}x{cols}", threads, mode, run, f"{elapsed_time:.5f}", ""])

                        avg_time_mode = total_time_mode / RUNS_PER_TEST
                        print(f"Average time for mode {mode} with {rows}x{cols} grid and {threads} threads: {avg_time_mode:.5f} seconds")
                        csv_writer.writerow([f"{rows}x{cols}", threads, mode, "Average", "", f"{avg_time_mode:.5f}"])

        # Notify completion
        print(f"\nTests completed. Results saved to {OUTPUT_CSV}.")
    
    except IOError as e:
        print(f"IOError while handling the CSV file: {e}")
        sys.exit(1)

def main():
    run_test()

if __name__ == "__main__":
    main()

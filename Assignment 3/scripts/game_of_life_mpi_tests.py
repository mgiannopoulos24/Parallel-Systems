#!/usr/bin/env python3

import subprocess
import csv
import time
import sys
from pathlib import Path

# Configuration
GAME_OF_LIFE_EXEC = Path("../build/game_of_life_mpi")
OUTPUT_CSV = "game_of_life_mpi_results.csv"
GRIDS = [(64, 64), (1024, 1024), (4096, 4096)]  # Grid sizes
GENERATIONS = 1000
RUNS_PER_TEST = 5

def run_test():
    """
    Runs the game_of_life executable with different grid sizes and generations.
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
            csv_writer.writerow(["Grid Size", "Generations", "Run", "Execution Time (s)", "Average Time (s)"])

            # Iterate over each grid size
            for grid in GRIDS:
                rows, cols = grid
                print(f"\nTesting with grid size {rows}x{cols}")
                # Print table header for formatted display
                print(f"{'Grid Size':<20} {'Run':<10} {'Execution Time (s)':<20}")
                print(f"{'-'*20} {'-'*10} {'-'*20}")

                total_time = 0.0
                for run in range(1, RUNS_PER_TEST + 1):
                    start_time = time.time()
                    try:
                        # Run the executable with the specified grid size and generations
                        subprocess.run(
                            [str(GAME_OF_LIFE_EXEC), str(rows), str(cols), str(GENERATIONS)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            check=True
                        )
                    except subprocess.CalledProcessError as e:
                        print(f"Error: Execution failed for grid={grid}, run={run}")
                        print(f"Command: {' '.join(e.cmd)}")
                        print(f"Return Code: {e.returncode}")
                        sys.exit(1)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    total_time += elapsed_time
                    # Print formatted row to the console
                    print(f"{rows}x{cols:<10} {run:<10} {elapsed_time:<20.5f}")
                    # Save the result to the CSV
                    csv_writer.writerow([f"{rows}x{cols}", GENERATIONS, run, f"{elapsed_time:.5f}", ""])

                avg_time = total_time / RUNS_PER_TEST
                print(f"Average time for {rows}x{cols} grid: {avg_time:.5f} seconds")
                csv_writer.writerow([f"{rows}x{cols}", GENERATIONS, "Average", "", f"{avg_time:.5f}"])

        # Notify completion
        print(f"\nTests completed. Results saved to {OUTPUT_CSV}.")
    
    except IOError as e:
        print(f"IOError while handling the CSV file: {e}")
        sys.exit(1)

def main():
    run_test()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import subprocess
import csv
import time
import sys
from pathlib import Path

# Configuration
GAME_OF_LIFE_EXEC = Path("../build/game_of_life_hybrid")
MACHINES_FILE = Path("../machines")  # Path to the machines file
OUTPUT_CSV = "game_of_life_hybrid_results.csv"
GRIDS = [(64, 64), (1024, 1024), (4096, 4096)]  # Grid sizes
GENERATIONS = 1000
RUNS_PER_TEST = 5
PROCESSES = [2, 4, 8, 16]  # Number of processes to test

def run_test():
    """
    Runs the game_of_life executable with different grid sizes, generations, and process counts.
    Records execution times and saves them to a CSV file.
    """
    if not GAME_OF_LIFE_EXEC.is_file():
        print(f"Error: The executable '{GAME_OF_LIFE_EXEC}' does not exist.")
        sys.exit(1)

    if not MACHINES_FILE.is_file():
        print(f"Error: The machines file '{MACHINES_FILE}' does not exist.")
        sys.exit(1)

    try:
        with open(OUTPUT_CSV, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Grid Size", "Processes", "Generations", "Run", "Execution Time (s)", "Average Time (s)"])

            for grid in GRIDS:
                rows, cols = grid
                for proc in PROCESSES:
                    print(f"\nTesting {proc} processes with grid size {rows}x{cols}")
                    print(f"{'Processes':<12} {'Run':<10} {'Execution Time (s)':<20}")
                    print(f"{'-'*12} {'-'*10} {'-'*20}")

                    total_time = 0.0
                    for run in range(1, RUNS_PER_TEST + 1):
                        start_time = time.time()
                        try:
                            command = ["mpiexec", "-f", str(MACHINES_FILE), "-n", str(proc), str(GAME_OF_LIFE_EXEC), str(GENERATIONS), str(rows)]
                            subprocess.run(
                                command,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                check=True
                            )
                            print(f"Command: {' '.join(command)}") # Debugging
                        except subprocess.CalledProcessError as e:
                            print(f"Error: Execution failed for grid={grid}, processes={proc}, run={run}")
                            print(f"Command: {' '.join(e.cmd)}")
                            print(f"Return Code: {e.returncode}")
                            sys.exit(1)

                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        total_time += elapsed_time
                        print(f"{proc:<12} {run:<10} {elapsed_time:<20.5f}")
                        csv_writer.writerow([f"{rows}x{cols}", proc, GENERATIONS, run, f"{elapsed_time:.5f}", ""])

                    avg_time = total_time / RUNS_PER_TEST
                    print(f"Average time for {rows}x{cols} grid with {proc} processes: {avg_time:.5f} seconds")
                    csv_writer.writerow([f"{rows}x{cols}", proc, GENERATIONS, "Average", "", f"{avg_time:.5f}"])

        print(f"\nTests completed. Results saved to {OUTPUT_CSV}.")
    
    except IOError as e:
        print(f"IOError while handling the CSV file: {e}")
        sys.exit(1)

def main():
    run_test()

if __name__ == "__main__":
    main()
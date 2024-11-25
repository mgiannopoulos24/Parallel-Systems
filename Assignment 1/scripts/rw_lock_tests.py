#!/usr/bin/env python3

import subprocess
import csv
import sys
import os
from statistics import mean

def run_rw_lock(num_threads, priority_mode, member_percent, insert_percent):
    """
    Executes the rw_lock program with the given parameters and returns the execution time.
    """
    # Path to the rw_lock program
    rw_lock_path = "../build/rw_lock"
    
    # Check if the program exists and is executable
    if not os.path.isfile(rw_lock_path):
        print(f"Error: The program '{rw_lock_path}' was not found.")
        sys.exit(1)
    if not os.access(rw_lock_path, os.X_OK):
        print(f"Error: The program '{rw_lock_path}' is not executable.")
        sys.exit(1)
    
    # Create the input list
    inputs = f"1000\n500000\n{member_percent}\n{insert_percent}\n"
    
    try:
        # Execute the program with subprocess
        result = subprocess.run(
            [rw_lock_path, str(num_threads), priority_mode],
            input=inputs,
            text=True,
            capture_output=True,
            timeout=300  # Timeout 5 minutes per run
        )
        
        # Check if there were errors during execution
        if result.returncode != 0:
            print(f"Warning: The program returned an error for num_threads={num_threads}, priority_mode={priority_mode}, member_percent={member_percent}, insert_percent={insert_percent}")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")
            return None
        
        # Search for the line with the execution time
        for line in result.stdout.splitlines():
            if "Elapsed time =" in line:
                # Example line: "Elapsed time = 1.234567e+00 seconds"
                parts = line.strip().split()
                try:
                    elapsed_time = float(parts[3])
                    return elapsed_time
                except (IndexError, ValueError):
                    print(f"Warning: Could not parse the time from the line: '{line}'")
                    return None
        
        # If the line with the execution time is not found
        print(f"Warning: The 'Elapsed time' line was not found in the output for num_threads={num_threads}, priority_mode={priority_mode}, member_percent={member_percent}, insert_percent={insert_percent}")
        return None
    
    except subprocess.TimeoutExpired:
        print(f"Warning: The program timed out after 5 minutes for num_threads={num_threads}, priority_mode={priority_mode}, member_percent={member_percent}, insert_percent={insert_percent}")
        return None

def main():
    # Define the CSV file for saving the results
    output_file = "rw_lock_results.csv"
    
    # Define the test parameters
    priority_modes = ["read", "write"]
    thread_counts = [2, 4, 8, 16]
    member_percents = [0.999, 0.95, 0.90]
    num_runs = 5  # Number of repetitions per test
    
    # Create and write the header in the CSV file
    with open(output_file, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["priority_mode", "num_threads", "member_percent", "average_elapsed_time"])
        
        # Loop for each priority mode
        for priority_mode in priority_modes:
            print(f"Running tests with priority_mode: {priority_mode}")
            
            # Loop for each thread count
            for num_threads in thread_counts:
                print(f"  Number of threads: {num_threads}")
                
                # Loop for each Member() percentage
                for member_percent in member_percents:
                    insert_percent = 1.0 - member_percent
                    print(f"    Member percent: {member_percent} (Insert percent: {insert_percent})")
                    
                    elapsed_times = []
                    
                    # Execute the tests
                    for run in range(1, num_runs + 1):
                        print(f"      Run {run}...")
                        elapsed = run_rw_lock(num_threads, priority_mode, member_percent, insert_percent)
                        if elapsed is not None:
                            elapsed_times.append(elapsed)
                            print(f"        Elapsed time: {elapsed} seconds")
                        else:
                            print(f"        Elapsed time: N/A")
                    
                    # Calculate the average
                    if elapsed_times:
                        average_elapsed = mean(elapsed_times)
                        average_str = f"{average_elapsed:.6f}"
                    else:
                        average_str = "N/A"
                    
                    # Write the results to the CSV
                    csv_writer.writerow([priority_mode, num_threads, member_percent, average_str])
                    
                    print(f"      Average elapsed time: {average_str} seconds\n")
    
    print(f"All tests completed. Results saved in '{output_file}'.")

if __name__ == "__main__":
    main()

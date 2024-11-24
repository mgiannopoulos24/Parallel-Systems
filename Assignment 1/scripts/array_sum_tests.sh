#!/bin/bash

# Path to the executable
ARRAY_SUM_EXEC="../build/array_sum"
OUTPUT_CSV="array_sum_results.csv"

# Thread counts to test
THREAD_COUNTS=(1 2 4 8 16 32)

# Write headers to the CSV file
echo "Threads,Run,Execution Time (s)" > $OUTPUT_CSV

# Function to run tests and collect data
run_test() {
    for threads in "${THREAD_COUNTS[@]}"; do
        echo -e "\nTesting with $threads threads"
        # Print table header for formatted display
        printf "\n%-10s %-10s %-20s\n" "Threads" "Run" "Execution Time (s)"
        printf "%-10s %-10s %-20s\n" "-------" "-----" "-----------------"
        for run in {1..5}; do
            # Measure execution time
            start_time=$(date +%s.%N)
            $ARRAY_SUM_EXEC $threads >/dev/null 2>&1
            end_time=$(date +%s.%N)
            elapsed_time=$(echo "$end_time - $start_time" | bc)

            # Print formatted row to the console
            printf "%-10d %-10d %-20.5f\n" "$threads" "$run" "$elapsed_time"

            # Save the result to the CSV
            echo "$threads,$run,$elapsed_time" >> $OUTPUT_CSV
        done
    done
}

# Run tests for array_sum implementation
run_test

# Notify completion
echo -e "\nTests completed. Results saved to $OUTPUT_CSV."

#!/bin/bash

# Path to the executables
BARRIERS=("barrier_mutex_cond" "barrier_pthread" "barrier_sense_reversal")
BUILD_DIR="../build"
OUTPUT_CSV="barrier_results.csv"

# Thread counts to test
THREAD_COUNTS=(2 4 8 16 32)

# Write headers to the CSV file
echo "Barrier,Threads,Run,Execution Time (s)" > $OUTPUT_CSV

# Function to run tests and collect data for a given barrier
run_test() {
    local barrier_exec=$1
    local barrier_name=$2

    for threads in "${THREAD_COUNTS[@]}"; do
        echo -e "\nTesting $barrier_name with $threads threads"
        # Print table header for formatted display
        printf "\n%-15s %-10s %-10s %-20s\n" "Barrier" "Threads" "Run" "Execution Time (s)"
        printf "%-15s %-10s %-10s %-20s\n" "-------" "-------" "-----" "-----------------"
        for run in {1..5}; do
            # Measure execution time
            start_time=$(date +%s.%N)
            $barrier_exec $threads >/dev/null 2>&1
            end_time=$(date +%s.%N)
            elapsed_time=$(echo "$end_time - $start_time" | bc)

            # Print formatted row to the console
            printf "%-15s %-10d %-10d %-20.5f\n" "$barrier_name" "$threads" "$run" "$elapsed_time"

            # Save the result to the CSV
            echo "$barrier_name,$threads,$run,$elapsed_time" >> $OUTPUT_CSV
        done
    done
}

# Run tests for all barriers
for barrier in "${BARRIERS[@]}"; do
    barrier_exec="$BUILD_DIR/$barrier"
    if [[ -x "$barrier_exec" ]]; then
        run_test "$barrier_exec" "$barrier"
    else
        echo "Executable $barrier_exec not found or not executable!"
    fi
done

# Notify completion
echo -e "\nAll tests completed. Results saved to $OUTPUT_CSV."
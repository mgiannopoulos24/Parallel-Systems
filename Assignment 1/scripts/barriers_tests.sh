#!/bin/bash

# Path to the executables
BARRIERS=("barrier_mutex_cond" "barrier_pthread" "barrier_sense_reversal")
BUILD_DIR="../build"
OUTPUT_CSV="barrier_results.csv"

# Thread counts to test
THREAD_COUNTS=(2 4 8 16 32)

# Write headers to the CSV file
echo "Barrier,Threads,Run,Execution Time (s),Average Execution Time (s)" > $OUTPUT_CSV

# Function to run tests and collect data for a given barrier
run_test() {
    local barrier_exec=$1
    local barrier_name=$2

    for threads in "${THREAD_COUNTS[@]}"; do
        echo -e "\nTesting $barrier_name with $threads threads"
        # Print table header for formatted display
        printf "\n%-25s %-10s %-10s %-20s\n" "Barrier" "Threads" "Run" "Execution Time (s)"
        printf "%-25s %-10s %-10s %-20s\n" "-------------------------" "-------" "-----" "-----------------"

        total_time=0

        for run in {1..5}; do
            # Measure execution time
            start_time=$(date +%s.%N)
            $barrier_exec $threads >/dev/null 2>&1
            end_time=$(date +%s.%N)
            elapsed_time=$(echo "$end_time - $start_time" | bc)

            # Accumulate the total execution time
            total_time=$(echo "$total_time + $elapsed_time" | bc)

            # Print formatted row to the console
            printf "%-25s %-10d %-10d %-20.5f\n" "$barrier_name" "$threads" "$run" "$elapsed_time"

            # Save the result to the CSV
            echo "$barrier_name,$threads,$run,$elapsed_time," >> $OUTPUT_CSV
        done

        # Calculate and print the average execution time
        avg_time=$(echo "scale=5; $total_time / 5" | bc)
        echo -e "Average time for $barrier_name with $threads threads: $avg_time seconds"
        
        # Append average time to the CSV
        echo "$barrier_name,$threads,Average,$avg_time,$avg_time" >> $OUTPUT_CSV
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
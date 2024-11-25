#!/bin/bash

# Paths to the executables
INCREASE_EXEC="../build/increase"
INCREASE_ATOMIC_EXEC="../build/increase_atomic"
OUTPUT_CSV="increase_results.csv"

# Thread counts to test
THREAD_COUNTS=(1 2 4 8 16 32)

# Write headers to the CSV file
echo "Implementation,Threads,Run,Execution Time (s),Average Time (s)" > $OUTPUT_CSV

# Function to run tests and collect data
run_test() {
    local exec=$1
    local implementation_name=$2

    for threads in "${THREAD_COUNTS[@]}"; do
        echo -e "\nTesting $implementation_name with $threads threads"
        # Print table header for formatted display
        printf "\n%-20s %-10s %-10s %-20s\n" "Implementation" "Threads" "Run" "Execution Time (s)"
        printf "%-20s %-10s %-10s %-20s\n" "--------------" "-------" "-----" "-----------------"

        total_time=0

        for run in {1..5}; do
            # Measure execution time
            start_time=$(date +%s.%N)
            $exec $threads >/dev/null 2>&1
            end_time=$(date +%s.%N)
            elapsed_time=$(echo "$end_time - $start_time" | bc)

            # Accumulate the total execution time
            total_time=$(echo "$total_time + $elapsed_time" | bc)

            # Print formatted row to the console
            printf "%-20s %-10d %-10d %-20.5f\n" "$implementation_name" "$threads" "$run" "$elapsed_time"

            # Save the result to the CSV
            echo "$implementation_name,$threads,$run,$elapsed_time," >> $OUTPUT_CSV
        done

        # Calculate and print the average execution time
        avg_time=$(echo "scale=5; $total_time / 5" | bc)
        echo -e "Average time for $implementation_name with $threads threads: $avg_time seconds"
        
        # Append average time to the CSV
        echo "$implementation_name,$threads,Average,$avg_time,$avg_time" >> $OUTPUT_CSV
    done
}

# Run tests for both implementations
run_test $INCREASE_EXEC "increase"
run_test $INCREASE_ATOMIC_EXEC "increase_atomic"

# Notify completion
echo -e "\nTests completed. Results saved to $OUTPUT_CSV."
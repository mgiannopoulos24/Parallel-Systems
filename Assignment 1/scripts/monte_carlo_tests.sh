#!/bin/bash

# Path to the executable
EXECUTABLE="../build/monte_carlo"
OUTPUT_CSV="monte_carlo_results.csv"

# Generate point counts dynamically from 10^0 to 10^9
POINT_COUNTS=( $(for i in {0..9}; do echo $((10**i)); done) )
THREAD_COUNTS=(4 8 16 32)

# Write headers to the CSV file
echo "Threads,Throws,Sequential Time (s),Parallel Time (s),Pi" > $OUTPUT_CSV

# Run tests and calculate average times
for threads in "${THREAD_COUNTS[@]}"; do
    echo "Testing with $threads threads"
    printf "%-15s %-25s %-25s %-15s\n" "Throws" "Sequential Time (s)" "Parallel Time (s)" "π"
    for points in "${POINT_COUNTS[@]}"; do
        seq_total_time=0
        par_total_time=0
        pi_value=0
        for i in {1..5}; do
            # Run the executable and extract relevant information
            output=$( $EXECUTABLE $threads $points )
            seq_time=$(echo "$output" | grep "Sequential time" | awk '{print $3}')
            par_time=$(echo "$output" | grep "Parallel time" | awk '{print $3}')
            pi=$(echo "$output" | grep "Parallel π estimate" | awk '{print $4}')
            seq_total_time=$(echo "$seq_total_time + $seq_time" | bc)
            par_total_time=$(echo "$par_total_time + $par_time" | bc)
            pi_value=$pi
        done
        # Calculate the average times and format results
        avg_seq_time=$(printf "%.5f" "$(echo "scale=5; $seq_total_time / 5" | bc)")
        avg_par_time=$(printf "%.5f" "$(echo "scale=5; $par_total_time / 5" | bc)")
        pi_value=$(printf "%.6f" "$pi_value")

        # Print the formatted output
        printf "%-15s %-25s %-25s %-15s\n" "$points" "$avg_seq_time" "$avg_par_time" "$pi_value"

        # Save the data to the CSV
        echo "$threads,$points,$avg_seq_time,$avg_par_time,$pi_value" >> $OUTPUT_CSV
    done
    echo
done

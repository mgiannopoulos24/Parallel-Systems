#!/bin/bash

# Define the program and output CSV file
PROGRAM="../build/rw_lock"
OUTPUT_FILE="starvation_results.csv"

# Header for the CSV file and terminal display
echo "Test Case,Readers,Writers,Priority Mode,Total Reader Time,Reader Time %,Total Writer Time,Writer Time %" > $OUTPUT_FILE
printf "%-10s %-8s %-8s %-15s %-18s %-15s %-18s %-15s\n" "Test Case" "Readers" "Writers" "Priority Mode" "Total Reader Time" "Reader Time %" "Total Writer Time" "Writer Time %"
printf "%-10s %-8s %-8s %-15s %-18s %-15s %-18s %-15s\n" "---------" "-------" "-------" "-------------" "-----------------" "--------------" "-----------------" "--------------"

# Test cases
declare -a TEST_CASES=(
    # Format: "readers,writers,priority"
    "5,1,1"    # Test Case 1: Detect Writer Starvation (Reader-Priority)
    "1,5,0"    # Test Case 2: Detect Reader Starvation (Writer-Priority)
    "10,2,1"   # Test Case 3: Continuous Readers with Intermittent Writers
    "2,10,0"   # Test Case 4: Continuous Writers with Intermittent Readers
    "5,5,1"    # Test Case 5a: Balanced Readers and Writers (Reader-Priority)
    "5,5,0"    # Test Case 5b: Balanced Readers and Writers (Writer-Priority)
    "20,1,1"   # Test Case 6: Heavy Readers, Single Writer
    "1,20,0"   # Test Case 7: Single Reader, Heavy Writers
    "10,10,1"  # Test Case 8: Equal Readers and Writers, Reader-Priority
    "10,10,0"  # Test Case 9: Equal Readers and Writers, Writer-Priority
    "50,5,1"   # Test Case 10: Large Number of Readers, Few Writers
    "5,50,0"   # Test Case 11: Few Readers, Large Number of Writers
    "0,5,1"    # Test Case 12: No Readers, Only Writers (Reader-Priority)
    "5,0,0"    # Test Case 13: Only Readers, No Writers (Writer-Priority)
    "20,20,1"  # Test Case 14: Heavy Workload, Reader-Priority
    "20,20,0"  # Test Case 15: Heavy Workload, Writer-Priority
)

# Run each test case
for i in "${!TEST_CASES[@]}"; do
    TEST_CONFIG=(${TEST_CASES[$i]//,/ })  # Split readers, writers, and priority
    READERS=${TEST_CONFIG[0]}
    WRITERS=${TEST_CONFIG[1]}
    PRIORITY=${TEST_CONFIG[2]}

    # Run the program and capture output
    OUTPUT=$($PROGRAM $READERS $WRITERS $PRIORITY 2>/dev/null)

    # Parse statistics from the output
    READER_TIME=$(echo "$OUTPUT" | grep "Total reader time" | awk '{print $4}')
    READER_PERCENT=$(echo "$OUTPUT" | grep "Total reader time" | awk '{print $6}' | tr -d '()%')
    WRITER_TIME=$(echo "$OUTPUT" | grep "Total writer time" | awk '{print $4}')
    WRITER_PERCENT=$(echo "$OUTPUT" | grep "Total writer time" | awk '{print $6}' | tr -d '()%')

    # Append results to the CSV file
    echo "$((i+1)),$READERS,$WRITERS,$PRIORITY,$READER_TIME,$READER_PERCENT,$WRITER_TIME,$WRITER_PERCENT" >> $OUTPUT_FILE

    # Print results to the terminal in a formatted way
    printf "%-10s %-8s %-8s %-15s %-18s %-15s %-18s %-15s\n" \
    "$((i+1))" "$READERS" "$WRITERS" "$PRIORITY" "$READER_TIME" "$READER_PERCENT" "$WRITER_TIME" "$WRITER_PERCENT"
done

# Notify the user
echo "Test cases completed. Results are saved in $OUTPUT_FILE."

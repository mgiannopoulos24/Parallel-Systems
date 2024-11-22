#!/bin/bash

TIMEFORMAT=%R  # Set time format to output real time in seconds

# Ensure there are an even number of arguments (program and argument pairs)
if (( $# % 2 != 0 )); then
    echo "Error: Each program must have a corresponding argument."
    exit 1
fi

# Process each program and its argument
for (( i=1; i<=$#; i+=2 ))
do
    exec_prog=${!i}         # Get the program name
    k=$((i+1))
    eval arg_prog=\$$k    

    avg_time=0

    for (( j=1; j<=2; j++ ))
    do
        time_prog=$( { time ./$exec_prog $arg_prog > /dev/null; } 2>&1 )
        avg_time=$(echo "$avg_time + $time_prog" | bc)
    done

    avg_time=$(echo "$avg_time / 2" | bc -l)
    avg_time=$(printf "%.4f" "$avg_time")

    echo "The average time for $exec_prog with argument '$arg_prog' is: $avg_time seconds"
done

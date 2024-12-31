# Project: Synchronization and Barriers with Pthreads

## Overview

This project contains multiple implementations of synchronization mechanisms and barrier techniques using the Pthreads library in C. Each implementation demonstrates different approaches to handle concurrent threads efficiently, ensuring proper synchronization and barrier operations.

## Implementations

### 1. Monte Carlo Pi Estimation (`monte_carlo_pi.c`)
This program uses the Monte Carlo method to estimate the value of $\pi$. It supports both serial and parallel execution using threads, providing insights into the performance differences between the two approaches.
### 2. Shared Variable Update (`increase.c` and `increase_atomic.c`)
This program demonstrates a shared variable update using Pthreads. Each thread increases a shared variable using two approaches:
- Mutex-based synchronization.
- Atomic operations.
### 3. Shared Array Update (`array_sum.c`)
This program demonstrates parallel computation using threads to distribute a large number of iterations among them. Each thread updates its own portion of a global array, and the results are summed to verify the computation.
### 4. Reader-Writer Locks (`rw_lock.c`)
This program implements two approaches for reader-writer synchronization:
- Reader Priority: Prioritizes readers over writers.
- Writer Priority: Prioritizes writers over readers.
### 5. Barrier Implementations
#### 5.1. Barrier using pthread_barrier_t (`barrier_pthread.c`)
This program uses the native Pthreads `pthread_barrier_t` to synchronize threads at a barrier point.
#### 5.2. Barrier using Mutex and Condition Variables (`barrier_mutex_cond.c`)
This program manually implements a barrier using mutexes and condition variables, offering flexibility for environments without native barrier support.
#### 5.3. Sense-Reversal Barrier (`barrier_sense_reversal.c`)
This program implements a centralized barrier mechanism using the sense-reversal technique, which is highly efficient for synchronization.

## How to Build and Run
1. Compile the programs using the provided Makefile.
```bash
make monte_carlo          # Builds the Monte Carlo program
make shared_variable      # Builds the shared variable program
make shared_array         # Builds the shared array program
make rw_lock              # Builds the reader-writer lock program
make barrier_pthread      # Builds the pthread barrier program
make barrier_mutex_cond   # Builds the mutex/condition variable barrier program
make barrier_sense_reversal # Builds the sense-reversal barrier program
```
2. Run the desired program:
```bash
./build/<program_name>
```
Replace `<program_name>` with the appropriate executable (e.g., `monte_carlo`, `rw_lock`).
## Authors

- [Dimitris Skondras Mexis](https://github.com/dimskomex)
- [Marios Giannopoulos](https://github.com/mgiannopoulos24)

## Acknowledgments

References include "Parallel Computer Architecture: A Hardware/Software Approach" by D. Culler and "Introduction to Parallel Programming" by P. Pacheco.

The Pthreads library and related resources were instrumental in implementing these programs.
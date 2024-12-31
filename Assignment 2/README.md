# Project: with OpenMP

## Overview
This project contains multiple implementations of parallelization techniques using OpenMP in C. Each implementation demonstrates different approaches to optimize performance for simulations and numerical computations, including Conway's Game of Life and Gauss elimination, with options for both serial and parallel execution modes.

## Implementations

### 1. Game of Life with OpenMP(`game_of_life.c`)
This program simulates Conway's Game of Life, a cellular automaton, for a specified number of generations. It supports both serial and parallel execution modes using OpenMP, allowing comparison of performance across different thread counts.
### 2. Gauss Elimination (`gauss_elimination.c`)
This program implements back substitution for solving upper triangular systems of linear equations. It supports both serial and parallel execution modes using OpenMP, with row-based and column-based approaches. Parallel execution includes various scheduling strategies: static, dynamic, guided, and runtime, enabling performance comparisons.
### 3. Game of Life with OpenMP Tasks (`game_of_life_tasks.c`)
This program efficiently simulates Conway's Game of Life with various parallelization strategies to improve performance, especially for large grids. The user has control over the number of threads used and can choose between serial or parallel execution modes to suit different hardware capabilities.

## How to Build and Run
1. Compile the programs using the provided Makefile.
```bash
make game_of_life       # Builds the game of life program
make gauss_elimination  # Builds the gauss elimination program
make game_of_life_tasks # Builds the game of life tasks program
```
2. Run the desired program:
```bash
./build/<program_name>
```
Replace `<program_name>` with the appropriate executable (e.g., `game_of_life`) and the arguments it needs.
## Authors

- [Marios Giannopoulos](https://github.com/mgiannopoulos24)


## Acknowledgments

References include "Parallel Computer Architecture: A Hardware/Software Approach" by D. Culler and "Introduction to Parallel Programming" by P. Pacheco.

The OpenMP API and related resources were instrumental in implementing these programs.
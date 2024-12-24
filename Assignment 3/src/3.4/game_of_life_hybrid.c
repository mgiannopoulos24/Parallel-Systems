#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>
#include <omp.h>

// Function to initialize the grid with random values
void initialize_grid(int **grid, int size) {
    #pragma omp parallel for
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            grid[i][j] = rand() % 2;
        }
    }
}

// Function to count alive neighbors for a given cell
int count_alive_neighbors(int **grid, int size, int x, int y) {
    int count = 0;
    for (int i = -1; i <= 1; i++) {
        for (int j = -1; j <= 1; j++) {
            if (i == 0 && j == 0) continue; // Skip the cell itself
            int nx = x + i;
            int ny = y + j;
            if (nx >= 0 && ny >= 0 && nx < size && ny < size) {
                count += grid[nx][ny];
            }
        }
    }
    return count;
}

// Function to compute the next generation of the grid
void next_generation(int **current, int **next, int size) {
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            int alive_neighbors = count_alive_neighbors(current, size, i, j);
            if (current[i][j] == 1) {
                // Alive cell rules
                if (alive_neighbors < 2 || alive_neighbors > 3) {
                    next[i][j] = 0; // Dies
                } else {
                    next[i][j] = 1; // Survives
                }
            } else {
                // Dead cell rules
                if (alive_neighbors == 3) {
                    next[i][j] = 1; // Becomes alive
                } else {
                    next[i][j] = 0; // Stays dead
                }
            }
        }
    }
}

// Function to print the grid (optional for debugging)
void print_grid(int **grid, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            printf("%c ", grid[i][j] ? 'O' : '.');
        }
        printf("\n");
    }
    printf("\n");
}

// Main function
int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <num_generations> <grid_size>\n", argv[0]);
        return EXIT_FAILURE;
    }

    int num_generations = atoi(argv[1]);
    int grid_size = atoi(argv[2]);

    // Initialize MPI
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Allocate memory for the grids
    int **current_grid = (int **)malloc(grid_size * sizeof(int *));
    int **next_grid = (int **)malloc(grid_size * sizeof(int *));
    for (int i = 0; i < grid_size; i++) {
        current_grid[i] = (int *)malloc(grid_size * sizeof(int));
        next_grid[i] = (int *)malloc(grid_size * sizeof(int));
    }

    // Process 0 initializes the grid
    if (rank == 0) {
        srand(time(NULL));
        initialize_grid(current_grid, grid_size);
    }

    // Broadcast the grid to all processes
    MPI_Bcast(current_grid[0], grid_size * grid_size, MPI_INT, 0, MPI_COMM_WORLD);

    // Calculate the rows each process will handle
    int rows_per_process = grid_size / size;
    int start_row = rank * rows_per_process;
    int end_row = (rank == size - 1) ? grid_size : start_row + rows_per_process;

    // Measure execution time
    double start_time = MPI_Wtime();

    for (int gen = 0; gen < num_generations; gen++) {
        next_generation(current_grid, next_grid, grid_size);

        // Swap grids
        int **temp = current_grid;
        current_grid = next_grid;
        next_grid = temp;

        // Create a temporary buffer to store the gathered data
        int *temp_buffer = (int *)malloc(rows_per_process * grid_size * sizeof(int));

        // Gather the grids back to process 0
        MPI_Gather(current_grid[start_row], rows_per_process * grid_size, MPI_INT, 
                   temp_buffer, rows_per_process * grid_size, MPI_INT, 
                   0, MPI_COMM_WORLD);

        // Copy the gathered data back to the main grid on process 0
        if (rank == 0) {
            for (int i = 0; i < size; i++) {
                for (int j = 0; j < grid_size; j++) {
                    current_grid[i][j] = temp_buffer[i * grid_size + j];
                }
            }
        }

        // Free the temporary buffer
        free(temp_buffer);

        if (rank == 0 && grid_size <= 64) {
            printf("Generation %d:\n", gen + 1);
            print_grid(current_grid, grid_size);
        }
    }

    double end_time = MPI_Wtime();
    if (rank == 0) {
        printf("Execution Time: %f seconds\n", end_time - start_time);
    }

    // Free allocated memory
    for (int i = 0; i < grid_size; i++) {
        free(current_grid[i]);
        free(next_grid[i]);
    }
    free(current_grid);
    free(next_grid);

    // Finalize MPI
    MPI_Finalize();

    return EXIT_SUCCESS;
}

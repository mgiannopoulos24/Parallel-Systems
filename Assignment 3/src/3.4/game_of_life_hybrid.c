#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

// Function to initialize the grid with random values
void initialize_grid(int *grid, int size) {
    for (int i = 0; i < size * size; i++) {
        grid[i] = rand() % 2;
    }
}

// Function to count alive neighbors for a given cell
int count_alive_neighbors(int *grid, int size, int x, int y) {
    int count = 0;
    for (int i = -1; i <= 1; i++) {
        for (int j = -1; j <= 1; j++) {
            if (i == 0 && j == 0) continue; // Skip the cell itself
            int nx = x + i;
            int ny = y + j;
            if (nx >= 0 && ny >= 0 && nx < size && ny < size) {
                count += grid[nx * size + ny];
            }
        }
    }
    return count;
}

// Function to compute the next generation of the grid
void next_generation(int *current, int *next, int size, int start_row, int end_row, int *top_row, int *bottom_row) {
    #pragma omp parallel for
    for (int i = start_row; i < end_row; i++) {
        for (int j = 0; j < size; j++) {
            int alive_neighbors = 0;

            // Count neighbors using top row if necessary
            if (i == start_row && top_row) {
                for (int dj = -1; dj <= 1; dj++) {
                    if (j + dj >= 0 && j + dj < size) {
                        alive_neighbors += top_row[j + dj];
                    }
                }
            }

            // Count neighbors from bottom row if necessary
            if (i == end_row - 1 && bottom_row) {
                for (int dj = -1; dj <= 1; dj++) {
                    if (j + dj >= 0 && j + dj < size) {
                        alive_neighbors += bottom_row[j + dj];
                    }
                }
            }

            // Count neighbors within the current grid
            alive_neighbors += count_alive_neighbors(current, size, i, j);

            // Apply Game of Life rules
            if (current[i * size + j] == 1) {
                next[i * size + j] = (alive_neighbors == 2 || alive_neighbors == 3) ? 1 : 0;
            } else {
                next[i * size + j] = (alive_neighbors == 3) ? 1 : 0;
            }
        }
    }
}

void print_grid(int *grid, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            printf("%c ", grid[i * size + j] ? 'O' : '.');
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

    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (grid_size % size != 0) {
        if (rank == 0) {
            fprintf(stderr, "Grid size must be divisible by the number of processes.\n");
        }
        MPI_Finalize();
        return EXIT_FAILURE;
    }

    int rows_per_process = grid_size / size;
    int *current_grid = NULL;
    int *next_grid = NULL;

    if (rank == 0) {
        current_grid = malloc(grid_size * grid_size * sizeof(int));
        next_grid = malloc(grid_size * grid_size * sizeof(int));
        srand(time(NULL));
        initialize_grid(current_grid, grid_size);
    }

    int *local_current = malloc(rows_per_process * grid_size * sizeof(int));
    int *local_next = malloc(rows_per_process * grid_size * sizeof(int));
    int *top_row = malloc(grid_size * sizeof(int));
    int *bottom_row = malloc(grid_size * sizeof(int));

    MPI_Scatter(current_grid, rows_per_process * grid_size, MPI_INT, local_current,
                rows_per_process * grid_size, MPI_INT, 0, MPI_COMM_WORLD);

    double start_time = MPI_Wtime();

    for (int gen = 0; gen < num_generations; gen++) {
        // Exchange borders using MPI_Isend and MPI_Irecv for non-blocking communication
        MPI_Request request_send_top, request_recv_bottom, request_send_bottom, request_recv_top;
        
        if (rank > 0) {
            MPI_Isend(local_current, grid_size, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, &request_send_top);
            MPI_Irecv(top_row, grid_size, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, &request_recv_top);
        }
        if (rank < size - 1) {
            MPI_Isend(&local_current[(rows_per_process - 1) * grid_size], grid_size, MPI_INT, rank + 1, 0, MPI_COMM_WORLD, &request_send_bottom);
            MPI_Irecv(bottom_row, grid_size, MPI_INT, rank + 1, 0, MPI_COMM_WORLD, &request_recv_bottom);
        }

        // Compute next generation
        next_generation(local_current, local_next, grid_size, 0, rows_per_process,
                        rank > 0 ? top_row : NULL, rank < size - 1 ? bottom_row : NULL);

        // Wait for the communication to finish
        if (rank > 0) {
            MPI_Wait(&request_send_top, MPI_STATUS_IGNORE);
            MPI_Wait(&request_recv_top, MPI_STATUS_IGNORE);
        }
        if (rank < size - 1) {
            MPI_Wait(&request_send_bottom, MPI_STATUS_IGNORE);
            MPI_Wait(&request_recv_bottom, MPI_STATUS_IGNORE);
        }

        // Swap grids
        int *temp = local_current;
        local_current = local_next;
        local_next = temp;

        // Gather updated grid to process 0
        MPI_Gather(local_current, rows_per_process * grid_size, MPI_INT, current_grid,
                   rows_per_process * grid_size, MPI_INT, 0, MPI_COMM_WORLD);

        if (rank == 0 && grid_size <= 64) {
            printf("Generation %d:\n", gen + 1);
            print_grid(current_grid, grid_size);
        }
    }

    double end_time = MPI_Wtime();
    if (rank == 0) {
        printf("Execution Time: %f seconds\n", end_time - start_time);
    }

    free(local_current);
    free(local_next);
    free(top_row);
    free(bottom_row);
    if (rank == 0) {
        free(current_grid);
        free(next_grid);
    }

    MPI_Finalize();
    return EXIT_SUCCESS;
}

#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Function to initialize the grid with random values
void initialize_grid(int *grid, int size) {
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      grid[i * size + j] = rand() % 2;
    }
  }
}

// Function to count alive neighbors for a given cell
int count_alive_neighbors(int *grid, int size, int x, int y) {
  int count = 0;
  for (int i = -1; i <= 1; i++) {
    for (int j = -1; j <= 1; j++) {
      if (i == 0 && j == 0)
        continue; // Skip the cell itself
      int nx = x + i;
      int ny = y + j;
      if (nx >= 0 && ny >= 0 && nx < size && ny < size) {
        count += grid[nx * size + ny];
      }
    }
  }
  return count;
}

// Function to compute the next generation
void next_generation(int *current, int *next, int size, int start_row, int end_row) {
  for (int i = start_row; i < end_row; i++) {
    for (int j = 0; j < size; j++) {
      int alive_neighbors = count_alive_neighbors(current, size, i, j);
      if (current[i * size + j] == 1) {
        next[i * size + j] = (alive_neighbors < 2 || alive_neighbors > 3) ? 0 : 1;
      } else {
        next[i * size + j] = (alive_neighbors == 3) ? 1 : 0;
      }
    }
  }
}

// Function to print the grid
void print_grid(int *grid, int size) {
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      printf("%c ", grid[i * size + j] ? 'O' : '.');
    }
    printf("\n");
  }
  printf("\n");
}

int main(int argc, char *argv[]) {
  MPI_Init(&argc, &argv);

  int rank, size;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  if (argc < 3) {
    if (rank == 0) {
      fprintf(stderr, "Usage: %s <num_generations> <grid_size>\n", argv[0]);
    }
    MPI_Finalize();
    return EXIT_FAILURE;
  }

  int num_generations = atoi(argv[1]);
  int grid_size = atoi(argv[2]);

  int *global_grid = NULL;
  int *local_grid = NULL;
  int *local_next = NULL;

  int rows_per_process = grid_size / size;
  int extra_rows = grid_size % size;

  int start_row = rank * rows_per_process + (rank < extra_rows ? rank : extra_rows);
  int end_row = start_row + rows_per_process + (rank < extra_rows ? 1 : 0);

  int local_rows = end_row - start_row;

  if (rank == 0) {
    global_grid = (int *)malloc(grid_size * grid_size * sizeof(int));
    srand(time(NULL));
    initialize_grid(global_grid, grid_size);

    if (grid_size <= 64) {
      printf("Initial Grid:\n");
      print_grid(global_grid, grid_size);
    }
  }

  local_grid = (int *)malloc((local_rows + 2) * grid_size * sizeof(int)); // +2 for ghost rows
  local_next = (int *)malloc((local_rows + 2) * grid_size * sizeof(int));

  MPI_Scatter(global_grid, local_rows * grid_size, MPI_INT, local_grid + grid_size, local_rows * grid_size, MPI_INT, 0, MPI_COMM_WORLD);

  double start_time = MPI_Wtime();

  MPI_Request send_request[2], recv_request[2];
  MPI_Status send_status[2], recv_status[2];

  for (int gen = 0; gen < num_generations; gen++) {
    // Exchange boundary rows with neighboring processes
    if (rank > 0) {
      MPI_Isend(local_grid + grid_size, grid_size, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, &send_request[0]);
      MPI_Irecv(local_grid, grid_size, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, &recv_request[0]);
    }
    if (rank < size - 1) {
      MPI_Isend(local_grid + local_rows * grid_size, grid_size, MPI_INT, rank + 1, 0, MPI_COMM_WORLD, &send_request[1]);
      MPI_Irecv(local_grid + (local_rows + 1) * grid_size, grid_size, MPI_INT, rank + 1, 0, MPI_COMM_WORLD, &recv_request[1]);
    }

    // Compute the next generation for the inner rows (non-boundary)
    next_generation(local_grid, local_next, grid_size, 1, local_rows + 1);

    // Wait for the communication to complete
    if (rank > 0) {
      MPI_Wait(&recv_request[0], &recv_status[0]);
      MPI_Wait(&send_request[0], &send_status[0]);
    }
    if (rank < size - 1) {
      MPI_Wait(&recv_request[1], &recv_status[1]);
      MPI_Wait(&send_request[1], &send_status[1]);
    }

    // Compute the next generation for the boundary rows
    if (rank > 0) {
      next_generation(local_grid, local_next, grid_size, 0, 1);
    }
    if (rank < size - 1) {
      next_generation(local_grid, local_next, grid_size, local_rows + 1, local_rows + 2);
    }

    // Swap grids
    int *temp = local_grid;
    local_grid = local_next;
    local_next = temp;
  }

  double end_time = MPI_Wtime();

  MPI_Gather(local_grid + grid_size, local_rows * grid_size, MPI_INT, global_grid, local_rows * grid_size, MPI_INT, 0, MPI_COMM_WORLD);

  if (rank == 0) {
    if (grid_size <= 64) {
      printf("Final Grid:\n");
      print_grid(global_grid, grid_size);
    }
    printf("Execution Time: %f seconds\n", end_time - start_time);
    free(global_grid);
  }

  free(local_grid);
  free(local_next);

  MPI_Finalize();
  return EXIT_SUCCESS;
}
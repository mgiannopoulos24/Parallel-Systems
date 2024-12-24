#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Function to initialize the grid with random values
void initialize_grid(int **grid, int size) {
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
      if (i == 0 && j == 0) continue;  // Skip the cell itself
      int nx = x + i;
      int ny = y + j;
      if (nx >= 0 && ny >= 0 && nx < size && ny < size) {
        count += grid[nx][ny];
      }
    }
  }
  return count;
}

// Function to compute the next generation using parallel tasks
void next_generation_task(int **current, int **next, int size,
                          int num_threads) {
#pragma omp parallel num_threads(num_threads)
  {
#pragma omp single
    {
      for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
#pragma omp task firstprivate(i, j)
          {
            int alive_neighbors = count_alive_neighbors(current, size, i, j);
            if (current[i][j] == 1) {
              // Alive cell rules
              if (alive_neighbors < 2 || alive_neighbors > 3) {
                next[i][j] = 0;  // Dies
              } else {
                next[i][j] = 1;  // Survives
              }
            } else {
              // Dead cell rules
              if (alive_neighbors == 3) {
                next[i][j] = 1;  // Becomes alive
              } else {
                next[i][j] = 0;  // Stays dead
              }
            }
          }
        }
      }
    }
  }
}

// Function to compute the next generation using parallel for
void next_generation_for(int **current, int **next, int size, int num_threads) {
#pragma omp parallel for num_threads(num_threads) collapse(2)
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      int alive_neighbors = count_alive_neighbors(current, size, i, j);
      if (current[i][j] == 1) {
        if (alive_neighbors < 2 || alive_neighbors > 3) {
          next[i][j] = 0;
        } else {
          next[i][j] = 1;
        }
      } else {
        if (alive_neighbors == 3) {
          next[i][j] = 1;
        } else {
          next[i][j] = 0;
        }
      }
    }
  }
}

// Function to compute the next generation in serial
void next_generation_serial(int **current, int **next, int size) {
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      int alive_neighbors = count_alive_neighbors(current, size, i, j);
      if (current[i][j] == 1) {
        if (alive_neighbors < 2 || alive_neighbors > 3) {
          next[i][j] = 0;
        } else {
          next[i][j] = 1;
        }
      } else {
        if (alive_neighbors == 3) {
          next[i][j] = 1;
        } else {
          next[i][j] = 0;
        }
      }
    }
  }
}

void print_grid(int **grid, int size) {
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      printf("%c ", grid[i][j] ? 'O' : '.');
    }
    printf("\n");
  }
  printf("\n");
}

int main(int argc, char *argv[]) {
  if (argc < 5) {
    fprintf(stderr,
            "Usage: %s <num_generations> <grid_size> <mode: 0=serial, "
            "1=parallel-for, 2=parallel-task> <num_threads>\n",
            argv[0]);
    return EXIT_FAILURE;
  }

  int num_generations = atoi(argv[1]);
  int grid_size = atoi(argv[2]);
  int parallel_mode = atoi(argv[3]);
  int num_threads = atoi(argv[4]);

  int **current_grid = (int **)malloc(grid_size * sizeof(int *));
  int **next_grid = (int **)malloc(grid_size * sizeof(int *));
  for (int i = 0; i < grid_size; i++) {
    current_grid[i] = (int *)malloc(grid_size * sizeof(int));
    next_grid[i] = (int *)malloc(grid_size * sizeof(int));
  }

  srand(time(NULL));
  initialize_grid(current_grid, grid_size);

  if (grid_size <= 64) {
    printf("Initial Grid:\n");
    print_grid(current_grid, grid_size);
  }

  double start_time = omp_get_wtime();

  for (int gen = 0; gen < num_generations; gen++) {
    if (parallel_mode == 1) {
      next_generation_for(current_grid, next_grid, grid_size, num_threads);
    } else if (parallel_mode == 2) {
      next_generation_task(current_grid, next_grid, grid_size, num_threads);
    } else {
      next_generation_serial(current_grid, next_grid, grid_size);
    }

    // Swap grids
    int **temp = current_grid;
    current_grid = next_grid;
    next_grid = temp;

    if (grid_size <= 64) {
      printf("Generation %d:\n", gen + 1);
      print_grid(current_grid, grid_size);
    }
  }

  double end_time = omp_get_wtime();
  printf("Execution Time: %f seconds\n", end_time - start_time);

  for (int i = 0; i < grid_size; i++) {
    free(current_grid[i]);
    free(next_grid[i]);
  }
  free(current_grid);
  free(next_grid);

  return EXIT_SUCCESS;
}

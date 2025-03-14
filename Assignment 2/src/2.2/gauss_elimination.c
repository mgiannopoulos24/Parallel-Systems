#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to perform back substitution (Row-based approach)
void back_substitution_row_based(double** A, double* b, double* x, int n) {
  for (int row = n - 1; row >= 0; row--) {
    x[row] = b[row];
    for (int col = row + 1; col < n; col++) {
      x[row] -= A[row][col] * x[col];
    }
    x[row] /= A[row][row];
  }
}

// Function to perform back substitution (Column-based approach)
void back_substitution_column_based(double** A, double* b, double* x, int n) {
  for (int row = 0; row < n; row++) {
    x[row] = b[row];
  }
  for (int col = n - 1; col >= 0; col--) {
    x[col] /= A[col][col];
    for (int row = 0; row < col; row++) {
      x[row] -= A[row][col] * x[col];
    }
  }
}

// Function to initialize the system of equations (upper-triangular form)
void initialize_system(double** A, double* b, int n) {
  for (int i = 0; i < n; i++) {
    for (int j = i; j < n; j++) {
      A[i][j] = rand() % 10 + 1;  // Random values
    }
    b[i] = rand() % 10 + 1;  // Random right-hand side values
  }
}

int main(int argc, char* argv[]) {
  if (argc != 6) {
    printf("Usage: %s <size> <serial/parallel> <row/column> [<schedule_mode>] <num_threads>\n",
           argv[0]);
    return 1;
  }

  int n = atoi(argv[1]);
  char* execution_mode = argv[2];
  char* algorithm_mode = argv[3];
  char* schedule_mode = argv[4];
  int num_threads = atoi(argv[5]);

  double** A = (double**)malloc(n * sizeof(double*));
  for (int i = 0; i < n; i++) {
    A[i] = (double*)malloc(n * sizeof(double));
  }
  double* b = (double*)malloc(n * sizeof(double));
  double* x = (double*)malloc(n * sizeof(double));

  initialize_system(A, b, n);

  omp_set_num_threads(num_threads);

  // Choose between serial or parallel execution
  if (strcmp(execution_mode, "serial") == 0) {
    omp_set_num_threads(1); 
    if (strcmp(algorithm_mode, "row") == 0) {
        // Serial execution (Row-based back substitution)
        for (int row = n - 1; row >= 0; row--) {
            x[row] = b[row];
            for (int col = row + 1; col < n; col++) {
                x[row] -= A[row][col] * x[col];
            }
            x[row] /= A[row][row];
        }
    } else if (strcmp(algorithm_mode, "column") == 0) {
        // Serial execution (Column-based back substitution)
        for (int row = 0; row < n; row++) {
            x[row] = b[row];
        }
        for (int col = n - 1; col >= 0; col--) {
            x[col] /= A[col][col];
            for (int row = 0; row < col; row++) {
                x[row] -= A[row][col] * x[col];
            }
        }
    }
  } else if (strcmp(execution_mode, "parallel") == 0) {
    if (strcmp(algorithm_mode, "row") == 0) {
      // Parallel execution of back substitution (Row-based)
      if (strcmp(schedule_mode, "static") == 0) {
        #pragma omp parallel for schedule(static)
        for (int row = n - 1; row >= 0; row--) {
          x[row] = b[row];
          for (int col = row + 1; col < n; col++) {
            x[row] -= A[row][col] * x[col];
          }
          x[row] /= A[row][row];
        }
      } else if (strcmp(schedule_mode, "dynamic") == 0) {
        #pragma omp parallel for schedule(dynamic)
        for (int row = n - 1; row >= 0; row--) {
          x[row] = b[row];
          for (int col = row + 1; col < n; col++) {
            x[row] -= A[row][col] * x[col];
          }
          x[row] /= A[row][row];
        }
      } else if (strcmp(schedule_mode, "guided") == 0) {
        #pragma omp parallel for schedule(guided)
        for (int row = n - 1; row >= 0; row--) {
          x[row] = b[row];
          for (int col = row + 1; col < n; col++) {
            x[row] -= A[row][col] * x[col];
          }
          x[row] /= A[row][row];
        }
      } else if (strcmp(schedule_mode, "runtime") == 0) {
        #pragma omp parallel for schedule(runtime)
        for (int row = n - 1; row >= 0; row--) {
          x[row] = b[row];
          for (int col = row + 1; col < n; col++) {
            x[row] -= A[row][col] * x[col];
          }
          x[row] /= A[row][row];
        }
      }
    } else if (strcmp(algorithm_mode, "column") == 0) {
      // Parallel execution of back substitution (Column-based)
      if (strcmp(schedule_mode, "static") == 0) {
        #pragma omp parallel for schedule(static)
        for (int row = 0; row < n; row++) {
          x[row] = b[row];
        }
        #pragma omp parallel for schedule(static)
        for (int col = n - 1; col >= 0; col--) {
          x[col] /= A[col][col];
          for (int row = 0; row < col; row++) {
            x[row] -= A[row][col] * x[col];
          }
        }
      } else if (strcmp(schedule_mode, "dynamic") == 0) {
        #pragma omp parallel for schedule(dynamic)
        for (int row = 0; row < n; row++) {
          x[row] = b[row];
        }
        #pragma omp parallel for schedule(dynamic)
        for (int col = n - 1; col >= 0; col--) {
          x[col] /= A[col][col];
          for (int row = 0; row < col; row++) {
            x[row] -= A[row][col] * x[col];
          }
        }
      } else if (strcmp(schedule_mode, "guided") == 0) {
        #pragma omp parallel for schedule(guided)
        for (int row = 0; row < n; row++) {
          x[row] = b[row];
        }
        #pragma omp parallel for schedule(guided)
        for (int col = n - 1; col >= 0; col--) {
          x[col] /= A[col][col];
          for (int row = 0; row < col; row++) {
            x[row] -= A[row][col] * x[col];
          }
        }
      } else if (strcmp(schedule_mode, "runtime") == 0) {
        #pragma omp parallel for schedule(runtime)
        for (int row = 0; row < n; row++) {
          x[row] = b[row];
        }
        #pragma omp parallel for schedule(runtime)
        for (int col = n - 1; col >= 0; col--) {
          x[col] /= A[col][col];
          for (int row = 0; row < col; row++) {
            x[row] -= A[row][col] * x[col];
          }
        }
      }
    }
  } else {
    printf("Invalid execution mode. Use 'serial' or 'parallel'.\n");
    return 1;
  }

  printf("Solution:\n");
  for (int i = 0; i < n; i++) {
    printf("x[%d] = %f\n", i, x[i]);
  }

  for (int i = 0; i < n; i++) {
    free(A[i]);
  }
  free(A);
  free(b);
  free(x);

  return 0;
}

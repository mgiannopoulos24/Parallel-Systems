#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Function to initialize the matrix and vector
void initialize_matrix_and_vector(double *matrix, double *vector, int n) {
  srand(time(NULL));
  for (int i = 0; i < n * n; i++) {
    matrix[i] = (double)(rand() % 10);
  }
  for (int i = 0; i < n; i++) {
    vector[i] = (double)(rand() % 10);
  }
}

// Function to print the matrix or vector
void print_matrix_or_vector(double *data, int rows, int cols) {
  for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
      printf("%.2f ", data[i * cols + j]);
    }
    printf("\n");
  }
}

// Serial matrix-vector multiplication
void serial_matrix_vector_mult(double *matrix, double *vector, double *result, int n) {
  for (int i = 0; i < n; i++) {
    result[i] = 0.0;
    for (int j = 0; j < n; j++) {
      result[i] += matrix[i * n + j] * vector[j];
    }
  }
}

int main(int argc, char *argv[]) {
  if (argc < 2) {
    fprintf(stderr, "Usage: %s <matrix_size>\n", argv[0]);
    return EXIT_FAILURE;
  }

  int n = atoi(argv[1]);

  MPI_Init(&argc, &argv);
  int rank, size;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  if (n % size != 0) {
    if (rank == 0) {
      fprintf(stderr,
              "Matrix size must be divisible by the number of processes.\n");
    }
    MPI_Finalize();
    return EXIT_FAILURE;
  }

  int block_size = n / size;
  double *matrix = NULL;
  double *vector = NULL;
  double *local_matrix = (double *)malloc(n * block_size * sizeof(double));
  double *local_result = (double *)malloc(n * sizeof(double));

  if (rank == 0) {
    matrix = (double *)malloc(n * n * sizeof(double));
    vector = (double *)malloc(n * sizeof(double));
    initialize_matrix_and_vector(matrix, vector, n);

    printf("Matrix:\n");
    print_matrix_or_vector(matrix, n, n);

    printf("Vector:\n");
    print_matrix_or_vector(vector, n, 1);
  }

  // Scatter the matrix by columns
  MPI_Scatter(matrix, n * block_size, MPI_DOUBLE, local_matrix, n * block_size,
              MPI_DOUBLE, 0, MPI_COMM_WORLD);

  // Broadcast the vector to all processes
  MPI_Bcast(vector, n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

  // Start timing
  double start_time = MPI_Wtime();

  // Perform local computation
  for (int i = 0; i < n; i++) {
    local_result[i] = 0.0;
    for (int j = 0; j < block_size; j++) {
      local_result[i] += local_matrix[i * block_size + j] * vector[rank * block_size + j];
    }
  }

  // Reduce the results to process 0
  double *result = NULL;
  if (rank == 0) {
    result = (double *)malloc(n * sizeof(double));
  }

  MPI_Reduce(local_result, result, n, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

  // Stop timing
  double end_time = MPI_Wtime();

  // Print the result on process 0
  if (rank == 0) {
    printf("Result:\n");
    print_matrix_or_vector(result, n, 1);

    // Serial computation for comparison
    double *serial_result = (double *)malloc(n * sizeof(double));
    double serial_start_time = MPI_Wtime();
    serial_matrix_vector_mult(matrix, vector, serial_result, n);
    double serial_end_time = MPI_Wtime();

    printf("Serial Result:\n");
    print_matrix_or_vector(serial_result, n, 1);

    // Print timing results
    printf("Parallel Time: %.6f seconds\n", end_time - start_time);
    printf("Serial Time: %.6f seconds\n", serial_end_time - serial_start_time);

    free(matrix);
    free(vector);
    free(result);
    free(serial_result);
  }

  free(local_matrix);
  free(local_result);

  MPI_Finalize();
  return EXIT_SUCCESS;
}
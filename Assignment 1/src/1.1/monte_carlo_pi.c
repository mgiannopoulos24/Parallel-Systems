#include <bits/time.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

long long total_points;          // Total number of points to be thrown
long long points_in_circle = 0;  // Total points inside the circle
int thread_count;                // Number of threads
pthread_mutex_t mutex;           // Mutex for synchronization

void* MonteCarloPiParallel(void* rank);
double MonteCarloPiSequential(long long total_points);
double GetTime();

int main(int argc, char* argv[]) {
  if (argc != 3) {
    fprintf(stderr, "Usage: %s <number of threads> <number of points>\n",
            argv[0]);
    exit(1);
  }

  thread_count =
      strtol(argv[1], NULL, 10);  // Number of threads from command line
  total_points = strtoll(argv[2], NULL, 10);  // Total points from command line

  if (thread_count <= 0 || total_points <= 0) {
    fprintf(stderr,
            "Error: Number of threads and points must be positive integers.\n");
    exit(1);
  }

  // Sequential Monte Carlo Simulation
  double start = GetTime();
  double pi_sequential = MonteCarloPiSequential(total_points);
  double finish = GetTime();
  printf("Sequential π estimate: %f\n", pi_sequential);
  printf("Sequential time: %f seconds\n", finish - start);

  // Parallel Monte Carlo Simulation
  pthread_t* thread_handles = malloc(thread_count * sizeof(pthread_t));
  pthread_mutex_init(&mutex, NULL);

  start = GetTime();
  for (long thread = 0; thread < thread_count; thread++) {
    pthread_create(&thread_handles[thread], NULL, MonteCarloPiParallel,
                   (void*)thread);
  }

  for (long thread = 0; thread < thread_count; thread++) {
    pthread_join(thread_handles[thread], NULL);
  }
  finish = GetTime();

  double pi_parallel = 4 * ((double)points_in_circle / (double)total_points);
  printf("Parallel π estimate: %f\n", pi_parallel);
  printf("Parallel time: %f seconds\n", finish - start);

  pthread_mutex_destroy(&mutex);
  free(thread_handles);

  return 0;
}

void* MonteCarloPiParallel(void* rank) {
  unsigned seed =
      (unsigned)time(NULL) + (unsigned)(size_t)rank;  // Seed for random numbers
  long long points_per_thread = total_points / thread_count;
  long long remainder = total_points % thread_count;

  if ((long)rank < remainder) {
    points_per_thread++;
  }

  long long local_points_in_circle = 0;

  for (long long i = 0; i < points_per_thread; i++) {
    double x = (double)rand_r(&seed) / RAND_MAX * 2.0 - 1.0;
    double y = (double)rand_r(&seed) / RAND_MAX * 2.0 - 1.0;
    if ((x * x + y * y) <= 1.0) {
      local_points_in_circle++;
    }
  }

  pthread_mutex_lock(&mutex);
  points_in_circle += local_points_in_circle;
  pthread_mutex_unlock(&mutex);

  return NULL;
}

double MonteCarloPiSequential(long long total_points) {
  long long points_in_circle = 0;
  for (long long i = 0; i < total_points; i++) {
    double x = (double)rand() / RAND_MAX * 2.0 - 1.0;
    double y = (double)rand() / RAND_MAX * 2.0 - 1.0;
    if ((x * x + y * y) <= 1.0) {
      points_in_circle++;
    }
  }
  return 4 * ((double)points_in_circle / total_points);
}

double GetTime() {
  struct timespec time;
  clock_gettime(CLOCK_MONOTONIC, &time);
  return time.tv_sec + time.tv_nsec * 1e-9;
}

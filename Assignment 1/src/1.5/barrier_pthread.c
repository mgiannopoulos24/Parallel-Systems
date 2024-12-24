#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define N 10    // Default number of threads
#define REPS 5  // Default number of iterations

pthread_mutex_t mutex;
pthread_cond_t cond;
int count = 0;        // Counter for threads reaching the barrier
int num_threads = 0;  // Number of threads

void Usage(char* prog_name) {
  fprintf(stderr, "Usage: %s [num_threads]\n", prog_name);
  exit(0);
}

// Custom barrier implementation
void Barrier() {
  pthread_mutex_lock(&mutex);
  count++;
  if (count == num_threads) {
    count = 0;                      // Reset for the next iteration
    pthread_cond_broadcast(&cond);  // Wake up all threads
  } else {
    while (pthread_cond_wait(&cond, &mutex) != 0);  // Wait for signal
  }
  pthread_mutex_unlock(&mutex);
}

void* ThreadWork(void* rank) {
  long my_rank = (long)rank;

  for (int i = 0; i < REPS; i++) {
    printf("Thread %ld is working on iteration %d\n", my_rank, i);
    usleep(20000);  // Simulate work

    Barrier();  // Custom barrier
    printf("Thread %ld passed the barrier on iteration %d\n", my_rank, i);
  }

  return NULL;
}

int main(int argc, char* argv[]) {
  if (argc != 2) Usage(argv[0]);

  num_threads = strtol(argv[1], NULL, 10);
  if (num_threads <= 0) Usage(argv[0]);

  pthread_t threads[num_threads];

  pthread_mutex_init(&mutex, NULL);
  pthread_cond_init(&cond, NULL);

  for (long thread = 0; thread < num_threads; thread++) {
    pthread_create(&threads[thread], NULL, ThreadWork, (void*)thread);
  }

  for (long thread = 0; thread < num_threads; thread++) {
    pthread_join(threads[thread], NULL);
  }

  pthread_mutex_destroy(&mutex);
  pthread_cond_destroy(&cond);
  return 0;
}
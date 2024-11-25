#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define N 10 // Default number of threads
#define REPS 5 // Default number of iterations

pthread_barrier_t barrier;

void Usage(char* prog_name) {
    fprintf(stderr, "Usage: %s [num_threads]\n", prog_name);
    exit(0);
}

void* ThreadWork(void* rank) {
    long my_rank = (long)rank;

    for (int i = 0; i < REPS; i++) {
        printf("Thread %ld is working on iteration %d\n", my_rank, i);
        usleep(20000); // Simulate work

        pthread_barrier_wait(&barrier);
        printf("Thread %ld passed the barrier on iteration %d\n", my_rank, i);
    }

    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 2) Usage(argv[0]);

    int num_threads = strtol(argv[1], NULL, 10);
    if (num_threads <= 0) Usage(argv[0]);

    pthread_t threads[num_threads];
    pthread_barrier_init(&barrier, NULL, num_threads);

    for (long thread = 0; thread < num_threads; thread++) {
        pthread_create(&threads[thread], NULL, ThreadWork, (void*)thread);
    }

    for (long thread = 0; thread < num_threads; thread++) {
        pthread_join(threads[thread], NULL);
    }

    pthread_barrier_destroy(&barrier);
    return 0;
}

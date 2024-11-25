#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define REPS 5 // Default number of iterations

int count = 0;
int sense = 0;
int num_threads = 0; // Global variable for the number of threads
pthread_mutex_t mutex;

void Usage(char* prog_name) {
    fprintf(stderr, "Usage: %s [num_threads]\n", prog_name);
    exit(0);
}

void Barrier(int* local_sense) {
    pthread_mutex_lock(&mutex);
    count++;
    if (count == num_threads) { // Use global num_threads instead of N
        count = 0;
        sense = *local_sense;
        pthread_mutex_unlock(&mutex);
    } else {
        pthread_mutex_unlock(&mutex);
        while (sense != *local_sense); // Busy wait
    }
}

void* ThreadWork(void* rank) {
    long my_rank = (long)rank;
    int local_sense = 1;

    for (int i = 0; i < REPS; i++) {
        printf("Thread %ld is working on iteration %d\n", my_rank, i);
        usleep(20000); // Simulate work

        Barrier(&local_sense);
        printf("Thread %ld passed the barrier on iteration %d\n", my_rank, i);

        local_sense = 1 - local_sense; // Toggle local sense
    }

    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 2) Usage(argv[0]);

    num_threads = strtol(argv[1], NULL, 10); // Assign to global num_threads
    if (num_threads <= 0) Usage(argv[0]);

    pthread_t threads[num_threads];
    pthread_mutex_init(&mutex, NULL);

    for (long thread = 0; thread < num_threads; thread++) {
        pthread_create(&threads[thread], NULL, ThreadWork, (void*)thread);
    }

    for (long thread = 0; thread < num_threads; thread++) {
        pthread_join(threads[thread], NULL);
    }

    pthread_mutex_destroy(&mutex);
    return 0;
}

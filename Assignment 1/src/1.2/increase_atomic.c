#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdatomic.h>

// Global variables
int threads_count;
_Atomic unsigned long long value = 0; 
const unsigned long long ITERATIONS = 34100654080;

void* increase_value(void* rank) {
    long my_rank = *(long*)rank;
    long my_n = ITERATIONS / threads_count;
    long my_first_i = my_n * my_rank;
    long my_last_i = (my_rank == threads_count - 1) ? ITERATIONS : my_first_i + my_n;
    unsigned long long my_value = 0;

    for (long i = my_first_i; i < my_last_i; i++) {
        my_value++; // Increment the thread-local counter
    }

    // Atomically update the shared counter
    atomic_fetch_add(&value, my_value);

    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number_of_threads>\n", argv[0]);
        return EXIT_FAILURE;
    }

    threads_count = strtol(argv[1], NULL, 10);
    if (threads_count <= 0 || threads_count > ITERATIONS) {
        fprintf(stderr, "Error: Number of threads must be between 1 and %llu.\n", ITERATIONS);
        return EXIT_FAILURE;
    }

    pthread_t* threads = malloc(threads_count * sizeof(pthread_t));
    long* thread_indices = malloc(threads_count * sizeof(long));

    for (int i = 0; i < threads_count; i++) {
        thread_indices[i] = i;
        pthread_create(&threads[i], NULL, increase_value, &thread_indices[i]);
    }

    for (int i = 0; i < threads_count; i++) {
        pthread_join(threads[i], NULL);
    }

    free(threads);
    free(thread_indices);

    printf("The value is %llu\n", value);
    return 0;
}
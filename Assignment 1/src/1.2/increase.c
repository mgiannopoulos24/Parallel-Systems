#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// Global variables
int threads_count;
pthread_mutex_t mutex;
unsigned long long value = 0;
const unsigned long long ITERATIONS = 34100654080;

// Function executed by each thread
void* increase_value(void* rank) {
    long my_rank = *(long*)rank;
    unsigned long long my_n = ITERATIONS / threads_count;
    unsigned long long my_first_i = my_n * my_rank;
    unsigned long long my_last_i = (my_rank == threads_count - 1) ? ITERATIONS : my_first_i + my_n;
    unsigned long long my_value = 0; // Local counter for this thread

    for (unsigned long long i = my_first_i; i < my_last_i; i++) {
        my_value++;
    }

    // Update the shared counter safely using a mutex
    pthread_mutex_lock(&mutex);
    value += my_value;
    pthread_mutex_unlock(&mutex);

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

    // Allocate resources for threads and thread indices
    pthread_t* threads = malloc(threads_count * sizeof(pthread_t));
    long* thread_indices = malloc(threads_count * sizeof(long)); 
    pthread_mutex_init(&mutex, NULL);

    // Create threads
    for (long i = 0; i < threads_count; i++) {
        thread_indices[i] = i;
        pthread_create(&threads[i], NULL, increase_value, &thread_indices[i]);
    }

    // Wait for all threads to complete
    for (long i = 0; i < threads_count; i++) {
        pthread_join(threads[i], NULL);
    }

    // Clean up resources
    pthread_mutex_destroy(&mutex);
    free(threads);
    free(thread_indices);

    printf("The value is %lld\n", value);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

// Global variables
int threads_count;
unsigned long long *array;
const unsigned long long ITERATIONS = 24100654080;

// Function executed by each thread
void* increase_array_item(void* index) {
    long my_index = *(long*)index; 
    long my_n = ITERATIONS / threads_count;
    long my_first_i = my_n * my_index;
    long my_last_i = (my_index == threads_count - 1) ? ITERATIONS : my_first_i + my_n;

    for (unsigned long long i = my_first_i; i < my_last_i; i++) {
        array[my_index]++; 
    }

    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number_of_threads>\n", argv[0]);
        return EXIT_FAILURE;
    }

    threads_count = strtol(argv[1], NULL, 10);

    // Validate the number of threads
    if (threads_count <= 0 || threads_count > ITERATIONS) {
        fprintf(stderr, "Error: Number of threads must be between 1 and %llu.\n", ITERATIONS);
        return EXIT_FAILURE;
    }

    // Allocate memory for threads, indices, and the array
    pthread_t* threads = malloc(threads_count * sizeof(pthread_t));
    long* thread_indices = malloc(threads_count * sizeof(long)); 
    array = malloc(threads_count * sizeof(unsigned long long));
    memset(array, 0, threads_count * sizeof(unsigned long long)); 

    // Create threads
    for (long i = 0; i < threads_count; i++) {
        thread_indices[i] = i; 
        pthread_create(&threads[i], NULL, increase_array_item, &thread_indices[i]);
    }

    // Wait for all threads to complete
    for (long i = 0; i < threads_count; i++) {
        pthread_join(threads[i], NULL);
    }

    // Calculate the sum of all elements in the array
    unsigned long long sum = 0;
    for (int i = 0; i < threads_count; i++) {
        sum += array[i];
    }

    printf("The sum is: %llu\n", sum);

    // Free allocated memory
    free(threads);
    free(thread_indices); 
    free(array);

    return 0;
}
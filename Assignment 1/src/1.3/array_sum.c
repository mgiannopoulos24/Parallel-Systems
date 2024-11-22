#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

int threads_count;
int *array;
const unsigned long long ITERATIONS = 24100654080;

void* increase_array_item(void* index) {
    long my_index = *(long*)index; 
    long my_n = ITERATIONS / threads_count;
    long my_first_i = my_n * my_index;
    long my_last_i = (my_index == threads_count - 1) ? ITERATIONS : my_first_i + my_n;

    long i;
    for (i = my_first_i; i < my_last_i; i++) {
        array[my_index]++;
    }

    return NULL;
}

int main(int argc, char* argv[]) {
    threads_count = strtol(argv[1], NULL, 10);
    if (threads_count > ITERATIONS)
        threads_count = ITERATIONS;

    pthread_t* threads = malloc(threads_count * sizeof(pthread_t));
    long* thread_indices = malloc(threads_count * sizeof(long)); 
    array = malloc(threads_count * sizeof(int));
    memset(array, 0, threads_count * sizeof(int));

    int i;
    for (i = 0; i < threads_count; i++) {
        thread_indices[i] = i; 
        pthread_create(&threads[i], NULL, increase_array_item, &thread_indices[i]);
    }

    for (i = 0; i < threads_count; i++) {
        pthread_join(threads[i], NULL);
    }

    long sum = 0;
    for (i = 0; i < threads_count; i++) {
        sum += array[i];
    }

    printf("The sum is: %d\n", sum);

    free(threads);
    free(thread_indices); 
    free(array);

    return 0;
}
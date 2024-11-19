#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

#define ITERATIONS 10000

int threads_count;
int *array;

void* increase_array_item(void *index) {
    long my_index = (long)index;

    int i;
    for (i = 0; i < ITERATIONS; i++) {
        array[my_index]++;
    }

    return NULL;
}

int main(int argc, char* argv[]) {
    threads_count = strtol(argv[1], NULL, 10);
    if (threads_count > ITERATIONS)
        threads_count = ITERATIONS;

    pthread_t* threads = malloc(threads_count * sizeof(pthread_t));
    array = malloc(threads_count * sizeof(int));
    memset(array, 0, threads_count * sizeof(int));

    int i;
    for (i = 0; i < threads_count; i++) {
        pthread_create(&threads[i], NULL, increase_array_item, (void*)i);
    }

    for (i = 0; i < threads_count; i++) {
        pthread_join(threads[i], NULL);
    }

    for (i = 0; i < threads_count; i++) {
        printf("%d%s", array[i], i % 4 == 3 ? "\n" : "\t");
    }

    free(threads);
    free(array);

    return 0;
}
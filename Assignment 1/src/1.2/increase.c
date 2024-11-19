#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define ITERATIONS 1000000000

int threads_count;
pthread_mutex_t mutex;
long value = 0;

void* increase_value(void* rank) {
    long my_rank = (long)rank;
    long my_n = ITERATIONS / threads_count;
    long my_first_i = my_n * my_rank;
    long my_last_i = my_first_i + my_n;
    int my_value = 0;

    long i;
    for (i = my_first_i; i < my_last_i; i++) {
        my_value++;
    }

    pthread_mutex_lock(&mutex);
    value += my_value;
    pthread_mutex_unlock(&mutex);

    return NULL;
}

int main(int arcg, char* argv[]) {
    threads_count = strtol(argv[1], NULL, 10);
    if (threads_count > ITERATIONS)
        threads_count = ITERATIONS;

    pthread_t* threads = malloc(threads_count * sizeof(pthread_t));

    pthread_mutex_init(&mutex, NULL);

    long i;
    for (i = 0; i < threads_count; i++) {
        pthread_create(&threads[i], NULL, increase_value, (void*)i);
    }

    for (i = 0; i < threads_count; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&mutex);
    free(threads);

    printf("The value is %d\n", value);
    return 0;
}
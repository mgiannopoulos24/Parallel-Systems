#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdatomic.h>

#define ITERATIONS 1000

int threads_count;
atomic_int value = ATOMIC_VAR_INIT(0);

void* increase_value(void* rank) {
    long my_rank = (long)rank;
    long my_n = ITERATIONS / threads_count;
    long my_first_i = my_n * my_rank;
    long my_last_i = my_first_i + my_n;
    int my_value = 0;

    int i;
    for (i = my_first_i; i < my_last_i; i++) {
        my_value++;
    }

    atomic_fetch_add(&value, my_value);

    return NULL;
}

int main(int arcg, char* argv[]) {
    threads_count = strtol(argv[1], NULL, 10);
    if (threads_count > ITERATIONS)
        threads_count = ITERATIONS;

    pthread_t* threads = malloc(threads_count * sizeof(pthread_t));

    int i;
    for (i = 0; i < threads_count; i++) {
        pthread_create(&threads[i], NULL, increase_value, (void*)i);
    }

    for (i = 0; i < threads_count; i++) {
        pthread_join(threads[i], NULL);
    }

    free(threads);

    printf("The value is %d\n", value);
    return 0;
}
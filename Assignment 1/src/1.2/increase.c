#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int threads_count;
pthread_mutex_t mutex;
unsigned long long value = 0;
const unsigned long long ITERATIONS = 34100654080;

void* increase_value(void* rank) {
    long my_rank = *(long*)rank;
    unsigned long long my_n = ITERATIONS / threads_count;
    unsigned long long my_first_i = my_n * my_rank;
    unsigned long long my_last_i = (my_rank == threads_count - 1) ? ITERATIONS : my_first_i + my_n;
    unsigned long long my_value = 0;

    unsigned long long i;
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
    long* thread_indices = malloc(threads_count * sizeof(long)); 
    pthread_mutex_init(&mutex, NULL);

    long i;
    for (i = 0; i < threads_count; i++) {
        thread_indices[i] = i; 
        pthread_create(&threads[i], NULL, increase_value, &thread_indices[i]);
    }

    for (i = 0; i < threads_count; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&mutex);

    free(threads);
    free(thread_indices);

    printf("The value is %lld\n", value);
    return 0;
}
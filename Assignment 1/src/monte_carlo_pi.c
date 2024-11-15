#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "my_rand.h"
#include "timer.h"

long long total_points;
long long points_in_circle = 0;
int thread_count;
pthread_mutex_t mutex;

void* MonteCarloPi(void* rank);

int main(int argc, char* argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <number of threads> <number of points>\n", argv[0]);
        exit(1);
    }

    thread_count = strtol(argv[1], NULL, 10);
    total_points = strtoll(argv[2], NULL, 10);

    pthread_t* thread_handles = malloc(thread_count * sizeof(pthread_t));
    pthread_mutex_init(&mutex, NULL);

    double start, finish;
    GET_TIME(start);

    for (long thread = 0; thread < thread_count; thread++) {
        pthread_create(&thread_handles[thread], NULL, MonteCarloPi, (void*)thread);
    }

    for (long thread = 0; thread < thread_count; thread++) {
        pthread_join(thread_handles[thread], NULL);
    }

    GET_TIME(finish);

    double pi_estimate = 4 * ((double)points_in_circle / (double)total_points);
    printf("Estimated value of \u03c0: %f\n", pi_estimate);
    printf("Elapsed time: %e seconds\n", finish - start);

    pthread_mutex_destroy(&mutex);
    free(thread_handles);
    return 0;
}

void* MonteCarloPi(void* rank) {
    unsigned seed = (unsigned)time(NULL) + (unsigned)(size_t)rank;
    long long points_per_thread = total_points / thread_count;
    long long local_points_in_circle = 0;

    for (long long i = 0; i < points_per_thread; i++) {
        double x = my_drand(&seed) * 2.0 - 1.0;
        double y = my_drand(&seed) * 2.0 - 1.0;
        if ((x * x + y * y) <= 1.0) {
            local_points_in_circle++;
        }
    }

    pthread_mutex_lock(&mutex);
    points_in_circle += local_points_in_circle;
    pthread_mutex_unlock(&mutex);

    return NULL;
}

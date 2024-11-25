#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

// Shared variables
int data = 0;
int active_readers = 0, waiting_readers = 0;
int active_writers = 0, waiting_writers = 0;
double total_reader_time = 0, total_writer_time = 0;
double total_reader_wait_time = 0, total_writer_wait_time = 0;

// Synchronization primitives
pthread_mutex_t mutex;
pthread_cond_t readers_cond, writers_cond;

// Control flags
int reader_priority = 1;
const int max_iterations = 5; // Number of operations per thread

double get_time_diff(struct timespec start, struct timespec end) {
    return (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
}

// Reader function
void* Reader(void* rank) {
    long my_rank = (long)rank;
    struct timespec start, end, wait_start, wait_end;

    for (int i = 0; i < max_iterations; i++) {
        clock_gettime(CLOCK_MONOTONIC, &wait_start);

        pthread_mutex_lock(&mutex);
        waiting_readers++;
        while (active_writers > 0 || (waiting_writers > 0 && !reader_priority)) {
            pthread_cond_wait(&readers_cond, &mutex);
        }
        waiting_readers--;
        active_readers++;
        pthread_mutex_unlock(&mutex);

        clock_gettime(CLOCK_MONOTONIC, &wait_end);
        total_reader_wait_time += get_time_diff(wait_start, wait_end);

        clock_gettime(CLOCK_MONOTONIC, &start);

        // Reading data
        printf("Reader %ld: read data = %d\n", my_rank, data);
        usleep(10000); // Simulate work (10ms)

        clock_gettime(CLOCK_MONOTONIC, &end);
        total_reader_time += get_time_diff(start, end);

        pthread_mutex_lock(&mutex);
        active_readers--;
        if (active_readers == 0 && waiting_writers > 0) {
            pthread_cond_signal(&writers_cond);
        }
        pthread_mutex_unlock(&mutex);

        usleep(10000); // Simulate delay before next operation
    }

    return NULL;
}

// Writer function
void* Writer(void* rank) {
    long my_rank = (long)rank;
    struct timespec start, end, wait_start, wait_end;

    for (int i = 0; i < max_iterations; i++) {
        clock_gettime(CLOCK_MONOTONIC, &wait_start);

        pthread_mutex_lock(&mutex);
        waiting_writers++;
        while (active_readers > 0 || active_writers > 0) {
            pthread_cond_wait(&writers_cond, &mutex);
        }
        waiting_writers--;
        active_writers++;
        pthread_mutex_unlock(&mutex);

        clock_gettime(CLOCK_MONOTONIC, &wait_end);
        total_writer_wait_time += get_time_diff(wait_start, wait_end);

        clock_gettime(CLOCK_MONOTONIC, &start);

        // Writing data
        data += 1;
        printf("Writer %ld: updated data to %d\n", my_rank, data);
        usleep(15000); // Simulate work (15ms)

        clock_gettime(CLOCK_MONOTONIC, &end);
        total_writer_time += get_time_diff(start, end);

        pthread_mutex_lock(&mutex);
        active_writers--;
        if (waiting_writers > 0) {
            pthread_cond_signal(&writers_cond);
        } else if (waiting_readers > 0) {
            pthread_cond_broadcast(&readers_cond);
        }
        pthread_mutex_unlock(&mutex);

        usleep(15000); // Simulate delay before next operation
    }

    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <number of readers> <number of writers> <priority: 1=readers, 0=writers>\n", argv[0]);
        exit(1);
    }

    int reader_count = strtol(argv[1], NULL, 10);
    int writer_count = strtol(argv[2], NULL, 10);
    reader_priority = strtol(argv[3], NULL, 10);

    pthread_t* reader_threads = malloc(reader_count * sizeof(pthread_t));
    pthread_t* writer_threads = malloc(writer_count * sizeof(pthread_t));

    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&readers_cond, NULL);
    pthread_cond_init(&writers_cond, NULL);

    for (long i = 0; i < reader_count; i++) {
        pthread_create(&reader_threads[i], NULL, Reader, (void*)(i + 1));
    }

    for (long i = 0; i < writer_count; i++) {
        pthread_create(&writer_threads[i], NULL, Writer, (void*)(i + 1));
    }

    for (int i = 0; i < reader_count; i++) {
        pthread_join(reader_threads[i], NULL);
    }

    for (int i = 0; i < writer_count; i++) {
        pthread_join(writer_threads[i], NULL);
    }

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&readers_cond);
    pthread_cond_destroy(&writers_cond);
    free(reader_threads);
    free(writer_threads);

    double total_time = total_reader_time + total_writer_time;
    printf("\nStatistics:\n");
    printf("Total reader time: %.2f seconds (%.2f%%)\n", total_reader_time, (total_reader_time / total_time) * 100);
    printf("Total writer time: %.2f seconds (%.2f%%)\n", total_writer_time, (total_writer_time / total_time) * 100);
    printf("Average reader wait time: %.5f seconds\n", total_reader_wait_time / (reader_count * max_iterations));
    printf("Average writer wait time: %.5f seconds\n", total_writer_wait_time / (writer_count * max_iterations));

    return 0;
}
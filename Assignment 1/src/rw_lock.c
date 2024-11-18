#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

// Shared variables
int data = 0; // Data to be read or written
int read_count = 0; // Number of active readers
int write_count = 0; // Number of active writers
int waiting_writers = 0; // Writers waiting to acquire the lock

// Synchronization primitives
pthread_mutex_t mutex;
pthread_cond_t readers_ok;
pthread_cond_t writers_ok;

// Function prototypes
void* ReaderPriorityReader(void* rank);
void* ReaderPriorityWriter(void* rank);
void* WriterPriorityReader(void* rank);
void* WriterPriorityWriter(void* rank);

// Control flags for approaches
int reader_priority = 1; // Set to 1 for reader priority, 0 for writer priority

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
    pthread_cond_init(&readers_ok, NULL);
    pthread_cond_init(&writers_ok, NULL);

    for (long i = 0; i < reader_count; i++) {
        if (reader_priority) {
            pthread_create(&reader_threads[i], NULL, ReaderPriorityReader, (void*)(i + 1));
        } else {
            pthread_create(&reader_threads[i], NULL, WriterPriorityReader, (void*)(i + 1));
        }
    }

    for (long i = 0; i < writer_count; i++) {
        if (reader_priority) {
            pthread_create(&writer_threads[i], NULL, ReaderPriorityWriter, (void*)(i + 1));
        } else {
            pthread_create(&writer_threads[i], NULL, WriterPriorityWriter, (void*)(i + 1));
        }
    }

    for (int i = 0; i < reader_count; i++) {
        pthread_join(reader_threads[i], NULL);
    }

    for (int i = 0; i < writer_count; i++) {
        pthread_join(writer_threads[i], NULL);
    }

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&readers_ok);
    pthread_cond_destroy(&writers_ok);
    free(reader_threads);
    free(writer_threads);

    return 0;
}

// Reader function for reader-priority approach
void* ReaderPriorityReader(void* rank) {
    long my_rank = (long)rank;

    for (int i = 0; i < 5; i++) {
        pthread_mutex_lock(&mutex);
        while (write_count > 0) {
            pthread_cond_wait(&readers_ok, &mutex);
        }
        read_count++;
        pthread_mutex_unlock(&mutex);

        // Reading data
        printf("Reader %ld (Reader Priority): read data = %d\n", my_rank, data);
        usleep(100000);

        pthread_mutex_lock(&mutex);
        read_count--;
        if (read_count == 0) {
            pthread_cond_signal(&writers_ok);
        }
        pthread_mutex_unlock(&mutex);

        usleep(100000);
    }

    return NULL;
}

// Writer function for reader-priority approach
void* ReaderPriorityWriter(void* rank) {
    long my_rank = (long)rank;

    for (int i = 0; i < 5; i++) {
        pthread_mutex_lock(&mutex);
        while (read_count > 0 || write_count > 0) {
            pthread_cond_wait(&writers_ok, &mutex);
        }
        write_count++;
        pthread_mutex_unlock(&mutex);

        // Writing data
        data += 1;
        printf("Writer %ld (Reader Priority): updated data to %d\n", my_rank, data);
        usleep(150000);

        pthread_mutex_lock(&mutex);
        write_count--;
        if (waiting_writers > 0) {
            pthread_cond_signal(&writers_ok);
        } else {
            pthread_cond_broadcast(&readers_ok);
        }
        pthread_mutex_unlock(&mutex);

        usleep(150000);
    }

    return NULL;
}

// Reader function for writer-priority approach
void* WriterPriorityReader(void* rank) {
    long my_rank = (long)rank;

    for (int i = 0; i < 5; i++) {
        pthread_mutex_lock(&mutex);
        while (write_count > 0 || waiting_writers > 0) {
            pthread_cond_wait(&readers_ok, &mutex);
        }
        read_count++;
        pthread_mutex_unlock(&mutex);

        // Reading data
        printf("Reader %ld (Writer Priority): read data = %d\n", my_rank, data);
        usleep(100000);

        pthread_mutex_lock(&mutex);
        read_count--;
        if (read_count == 0) {
            pthread_cond_signal(&writers_ok);
        }
        pthread_mutex_unlock(&mutex);

        usleep(100000);
    }

    return NULL;
}


// Writer function for writer-priority approach
void* WriterPriorityWriter(void* rank) {
    long my_rank = (long)rank;

    for (int i = 0; i < 5; i++) {
        pthread_mutex_lock(&mutex);
        waiting_writers++;
        while (read_count > 0 || write_count > 0) {
            pthread_cond_wait(&writers_ok, &mutex);
        }
        waiting_writers--;
        write_count++;
        pthread_mutex_unlock(&mutex);

        // Writing data
        data += 1;
        printf("Writer %ld (Writer Priority): updated data to %d\n", my_rank, data);
        usleep(150000);

        pthread_mutex_lock(&mutex);
        write_count--;
        if (waiting_writers > 0) {
            pthread_cond_signal(&writers_ok);
        } else {
            pthread_cond_broadcast(&readers_ok);
        }
        pthread_mutex_unlock(&mutex);

        usleep(150000);
    }

    return NULL;
}

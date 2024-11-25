#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "my_rand.h"
#include "timer.h"

/* Constants */
const int MAX_KEY = 100000000;

/* Lock preference type */
typedef enum { READER_PREF, WRITER_PREF } lock_type;

/* Custom RWLock structure */
typedef struct {
    pthread_mutex_t mutex;
    pthread_cond_t readers_ok;
    pthread_cond_t writers_ok;
    int readers_active;
    int readers_waiting;
    int writer_active;
    int writers_waiting;
    lock_type preference;
} rwlock_t;

/* List node structure */
struct list_node_s {
    int data;
    struct list_node_s* next;
};

/* Shared variables */
struct list_node_s* head = NULL;
int thread_count, total_ops;
double insert_percent, search_percent, delete_percent;
rwlock_t rwlock;
pthread_mutex_t count_mutex;
int member_count = 0, insert_count = 0, delete_count = 0;

/* Function prototypes */
void Usage(char* prog_name);
void Get_input(int* inserts_in_main_p, lock_type *preference);
void* Thread_work(void* rank);
int Insert(int value);
int Member(int value);
int Delete(int value);
void Free_list(void);
int Is_empty(void);
void rwlock_init(rwlock_t *lock, lock_type preference);
void rwlock_destroy(rwlock_t *lock);
void rwlock_rdlock(rwlock_t *lock);
void rwlock_wrlock(rwlock_t *lock);
void rwlock_unlock(rwlock_t *lock);

/* Main function */
int main(int argc, char* argv[]) {
    long i;
    int key, success, attempts, inserts_in_main;
    pthread_t* thread_handles;
    unsigned seed = 1;
    double start, finish;
    lock_type preference;

    if (argc != 2) Usage(argv[0]);
    thread_count = strtol(argv[1], NULL, 10);

    Get_input(&inserts_in_main, &preference);
    rwlock_init(&rwlock, preference);

    /* Insert initial keys into the list */
    i = attempts = 0;
    while (i < inserts_in_main && attempts < 2 * inserts_in_main) {
        key = my_rand(&seed) % MAX_KEY;
        success = Insert(key);
        attempts++;
        if (success) i++;
    }
    printf("Inserted %ld keys in empty list\n", i);

    thread_handles = malloc(thread_count * sizeof(pthread_t));
    pthread_mutex_init(&count_mutex, NULL);

    GET_TIME(start);
    for (i = 0; i < thread_count; i++)
        pthread_create(&thread_handles[i], NULL, Thread_work, (void*) i);

    for (i = 0; i < thread_count; i++)
        pthread_join(thread_handles[i], NULL);
    GET_TIME(finish);

    printf("Elapsed time = %e seconds\n", finish - start);
    printf("Total ops = %d\n", total_ops);
    printf("Member ops = %d\n", member_count);
    printf("Insert ops = %d\n", insert_count);
    printf("Delete ops = %d\n", delete_count);

    Free_list();
    rwlock_destroy(&rwlock);
    pthread_mutex_destroy(&count_mutex);
    free(thread_handles);

    return 0;
}

/* Function definitions */
void Usage(char* prog_name) {
    fprintf(stderr, "usage: %s <thread_count>\n", prog_name);
    exit(0);
}

void Get_input(int* inserts_in_main_p, lock_type *preference) {
    char pref;
    printf("How many keys should be inserted in the main thread?\n");
    scanf("%d", inserts_in_main_p);
    printf("How many ops total should be executed?\n");
    scanf("%d", &total_ops);
    printf("Percent of ops that should be searches? (between 0 and 1)\n");
    scanf("%lf", &search_percent);
    printf("Percent of ops that should be inserts? (between 0 and 1)\n");
    scanf("%lf", &insert_percent);
    delete_percent = 1.0 - (search_percent + insert_percent);
    printf("Lock preference? (r for reader-preferential, w for writer-preferential):\n");
    scanf(" %c", &pref);
    *preference = (pref == 'r') ? READER_PREF : WRITER_PREF;
}

/* Insert a value into the list */
int Insert(int value) {
    struct list_node_s* curr = head;
    struct list_node_s* pred = NULL;
    struct list_node_s* temp;
    int rv = 1;

    while (curr != NULL && curr->data < value) {
        pred = curr;
        curr = curr->next;
    }

    if (curr == NULL || curr->data > value) {
        temp = malloc(sizeof(struct list_node_s));
        temp->data = value;
        temp->next = curr;
        if (pred == NULL)
            head = temp;
        else
            pred->next = temp;
    } else {
        rv = 0;
    }

    return rv;
}

/* Check membership */
int Member(int value) {
    struct list_node_s* temp = head;

    while (temp != NULL && temp->data < value)
        temp = temp->next;

    return (temp != NULL && temp->data == value);
}

/* Delete a value from the list */
int Delete(int value) {
    struct list_node_s* curr = head;
    struct list_node_s* pred = NULL;
    int rv = 1;

    while (curr != NULL && curr->data < value) {
        pred = curr;
        curr = curr->next;
    }

    if (curr != NULL && curr->data == value) {
        if (pred == NULL)
            head = curr->next;
        else
            pred->next = curr->next;
        free(curr);
    } else {
        rv = 0;
    }

    return rv;
}

/* Free the entire list */
void Free_list(void) {
    struct list_node_s* current = head;
    struct list_node_s* following;

    while (current != NULL) {
        following = current->next;
        free(current);
        current = following;
    }
}

/* Initialize the custom RWLock */
void rwlock_init(rwlock_t *lock, lock_type preference) {
    pthread_mutex_init(&lock->mutex, NULL);
    pthread_cond_init(&lock->readers_ok, NULL);
    pthread_cond_init(&lock->writers_ok, NULL);
    lock->readers_active = 0;
    lock->readers_waiting = 0;
    lock->writer_active = 0;
    lock->writers_waiting = 0;
    lock->preference = preference;
}

/* Destroy the custom RWLock */
void rwlock_destroy(rwlock_t *lock) {
    pthread_mutex_destroy(&lock->mutex);
    pthread_cond_destroy(&lock->readers_ok);
    pthread_cond_destroy(&lock->writers_ok);
}

/* Acquire reader lock */
void rwlock_rdlock(rwlock_t *lock) {
    pthread_mutex_lock(&lock->mutex);
    while (lock->writer_active || (lock->preference == WRITER_PREF && lock->writers_waiting > 0)) {
        lock->readers_waiting++;
        pthread_cond_wait(&lock->readers_ok, &lock->mutex);
        lock->readers_waiting--;
    }
    lock->readers_active++;
    pthread_mutex_unlock(&lock->mutex);
}

/* Acquire writer lock */
void rwlock_wrlock(rwlock_t *lock) {
    pthread_mutex_lock(&lock->mutex);
    while (lock->writer_active || lock->readers_active > 0) {
        lock->writers_waiting++;
        pthread_cond_wait(&lock->writers_ok, &lock->mutex);
        lock->writers_waiting--;
    }
    lock->writer_active = 1;
    pthread_mutex_unlock(&lock->mutex);
}

/* Release the lock */
void rwlock_unlock(rwlock_t *lock) {
    pthread_mutex_lock(&lock->mutex);
    if (lock->writer_active) {
        lock->writer_active = 0;
        if (lock->preference == READER_PREF && lock->readers_waiting > 0)
            pthread_cond_broadcast(&lock->readers_ok);
        else
            pthread_cond_signal(&lock->writers_ok);
    } else {
        lock->readers_active--;
        if (lock->readers_active == 0 && lock->writers_waiting > 0)
            pthread_cond_signal(&lock->writers_ok);
    }
    pthread_mutex_unlock(&lock->mutex);
}

/* Worker thread function */
void* Thread_work(void* rank) {
    long my_rank = (long) rank;
    unsigned seed = my_rank + 1;
    int ops_per_thread = total_ops / thread_count;
    int i, val;
    double which_op;

    for (i = 0; i < ops_per_thread; i++) {
        which_op = my_drand(&seed);
        val = my_rand(&seed) % MAX_KEY;

        if (which_op < search_percent) {
            rwlock_rdlock(&rwlock);
            Member(val);
            rwlock_unlock(&rwlock);
        } else if (which_op < search_percent + insert_percent) {
            rwlock_wrlock(&rwlock);
            Insert(val);
            rwlock_unlock(&rwlock);
        } else {
            rwlock_wrlock(&rwlock);
            Delete(val);
            rwlock_unlock(&rwlock);
        }
    }

    return NULL;
}
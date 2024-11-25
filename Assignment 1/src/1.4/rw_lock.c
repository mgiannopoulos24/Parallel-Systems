#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include "my_rand.h"
#include "timer.h"

/* Constants for priority modes */
#define READ_PRIORITY 0
#define WRITE_PRIORITY 1

/* Random ints are less than MAX_KEY */
const int MAX_KEY = 100000000;

/* Struct for list nodes */
struct list_node_s {
   int    data;
   struct list_node_s* next;
};

/* Custom Read-Write Lock Structure */
typedef struct {
    pthread_mutex_t mutex;          /* Mutex to protect the structure */
    pthread_cond_t readers_cond;    /* Condition variable for readers */
    pthread_cond_t writers_cond;    /* Condition variable for writers */
    int active_readers;             /* Number of active readers */
    int waiting_readers;            /* Number of readers waiting */
    int active_writers;             /* Number of active writers (0 or 1) */
    int waiting_writers;            /* Number of writers waiting */
    int priority;                   /* 0 for read-priority, 1 for write-priority */
} my_rwlock_t;

/* Shared variables */
struct list_node_s* head = NULL;  
int thread_count;
int total_ops;
double insert_percent;
double search_percent;
double delete_percent;
my_rwlock_t rwlock;               /* Custom read-write lock */
pthread_mutex_t count_mutex;
int member_count = 0, insert_count = 0, delete_count = 0;

/* Function declarations */
void Usage(char* prog_name);
void Get_input(int* inserts_in_main_p);
void* Thread_work(void* rank);
int Insert(int value);
void Print(void);
int Member(int value);
int Delete(int value);
void Free_list(void);
int Is_empty(void);

/* Custom Read-Write Lock Functions */

/* Initialize the custom read-write lock */
void my_rwlock_init(my_rwlock_t* lock, int priority_mode) {
    pthread_mutex_init(&lock->mutex, NULL);
    pthread_cond_init(&lock->readers_cond, NULL);
    pthread_cond_init(&lock->writers_cond, NULL);
    lock->active_readers = 0;
    lock->waiting_readers = 0;
    lock->active_writers = 0;
    lock->waiting_writers = 0;
    lock->priority = priority_mode;
}

/* Acquire the lock for reading */
void my_rwlock_rdlock(my_rwlock_t* lock) {
    pthread_mutex_lock(&lock->mutex);
    if (lock->priority == READ_PRIORITY) {
        /* Read-priority: Readers proceed if no active writers */
        while (lock->active_writers > 0) {
            lock->waiting_readers++;
            pthread_cond_wait(&lock->readers_cond, &lock->mutex);
            lock->waiting_readers--;
        }
    } else {
        /* Write-priority: Readers wait if there are active or waiting writers */
        while (lock->active_writers > 0 || lock->waiting_writers > 0) {
            lock->waiting_readers++;
            pthread_cond_wait(&lock->readers_cond, &lock->mutex);
            lock->waiting_readers--;
        }
    }
    lock->active_readers++;
    pthread_mutex_unlock(&lock->mutex);
}

/* Acquire the lock for writing */
void my_rwlock_wrlock(my_rwlock_t* lock) {
    pthread_mutex_lock(&lock->mutex);
    lock->waiting_writers++;
    while (lock->active_writers > 0 || lock->active_readers > 0) {
        pthread_cond_wait(&lock->writers_cond, &lock->mutex);
    }
    lock->waiting_writers--;
    lock->active_writers++;
    pthread_mutex_unlock(&lock->mutex);
}

/* Release the lock */
void my_rwlock_unlock(my_rwlock_t* lock) {
    pthread_mutex_lock(&lock->mutex);
    if (lock->active_writers > 0) {
        /* Unlocking a writer */
        lock->active_writers--;
    } else {
        /* Unlocking a reader */
        lock->active_readers--;
    }

    if (lock->active_writers == 0) {
        if (lock->priority == WRITE_PRIORITY && lock->waiting_writers > 0) {
            /* Give priority to writers */
            pthread_cond_signal(&lock->writers_cond);
        } else if (lock->waiting_readers > 0) {
            /* Wake up all waiting readers */
            pthread_cond_broadcast(&lock->readers_cond);
        } else if (lock->waiting_writers > 0) {
            /* Wake up one waiting writer */
            pthread_cond_signal(&lock->writers_cond);
        }
    }
    pthread_mutex_unlock(&lock->mutex);
}

/*-----------------------------------------------------------------*/
int main(int argc, char* argv[]) {
   long i; 
   int key, success, attempts;
   pthread_t* thread_handles;
   int inserts_in_main;
   unsigned seed = 1;
   double start, finish;
   int priority_mode;

   if (argc != 3) Usage(argv[0]);
   thread_count = strtol(argv[1], NULL, 10);
   
   /* Parse priority mode */
   if (strcmp(argv[2], "read") == 0) {
       priority_mode = READ_PRIORITY;
   } else if (strcmp(argv[2], "write") == 0) {
       priority_mode = WRITE_PRIORITY;
   } else {
       fprintf(stderr, "Invalid priority_mode. Use 'read' or 'write'.\n");
       Usage(argv[0]);
   }

   Get_input(&inserts_in_main);

   /* Try to insert inserts_in_main keys, but give up after */
   /* 2*inserts_in_main attempts.                           */
   i = attempts = 0;
   while (i < inserts_in_main && attempts < 2*inserts_in_main) {
      key = my_rand(&seed) % MAX_KEY;
      success = Insert(key);
      attempts++;
      if (success) i++;
   }
   printf("Inserted %ld keys in empty list\n", i);

#ifdef OUTPUT
   printf("Before starting threads, list = \n");
   Print();
   printf("\n");
#endif

   thread_handles = malloc(thread_count * sizeof(pthread_t));
   pthread_mutex_init(&count_mutex, NULL);
   
   /* Initialize custom read-write lock */
   my_rwlock_init(&rwlock, priority_mode);

   GET_TIME(start);
   for (i = 0; i < thread_count; i++)
      pthread_create(&thread_handles[i], NULL, Thread_work, (void*) i);

   for (i = 0; i < thread_count; i++)
      pthread_join(thread_handles[i], NULL);
   GET_TIME(finish);
   printf("Elapsed time = %e seconds\n", finish - start);
   printf("Total ops = %d\n", total_ops);
   printf("member ops = %d\n", member_count);
   printf("insert ops = %d\n", insert_count);
   printf("delete ops = %d\n", delete_count);

#ifdef OUTPUT
   printf("After threads terminate, list = \n");
   Print();
   printf("\n");
#endif

   Free_list();
   
   /* Destroy custom read-write lock */
   pthread_mutex_destroy(&rwlock.mutex);
   pthread_cond_destroy(&rwlock.readers_cond);
   pthread_cond_destroy(&rwlock.writers_cond);
   
   pthread_mutex_destroy(&count_mutex);
   free(thread_handles);

   return 0;
}  /* main */


/*-----------------------------------------------------------------*/
void Usage(char* prog_name) {
   fprintf(stderr, "usage: %s <thread_count> <priority_mode>\n", prog_name);
   fprintf(stderr, "priority_mode: 'read' for read-priority, 'write' for write-priority\n");
   exit(0);
}  /* Usage */


/*-----------------------------------------------------------------*/
void Get_input(int* inserts_in_main_p) {

   printf("How many keys should be inserted in the main thread?\n");
   scanf("%d", inserts_in_main_p);
   printf("How many ops total should be executed?\n");
   scanf("%d", &total_ops);
   printf("Percent of ops that should be searches? (between 0 and 1)\n");
   scanf("%lf", &search_percent);
   printf("Percent of ops that should be inserts? (between 0 and 1)\n");
   scanf("%lf", &insert_percent);
   delete_percent = 1.0 - (search_percent + insert_percent);
}  /* Get_input */


/*-----------------------------------------------------------------*/
/* Insert value in correct numerical location into list */
/* If value is not in list, return 1, else return 0 */
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
   } else { /* value in list */
      rv = 0;
   }

   return rv;
}  /* Insert */


/*-----------------------------------------------------------------*/
void Print(void) {
   struct list_node_s* temp;

   printf("list = ");

   temp = head;
   while (temp != (struct list_node_s*) NULL) {
      printf("%d ", temp->data);
      temp = temp->next;
   }
   printf("\n");
}  /* Print */


/*-----------------------------------------------------------------*/
int  Member(int value) {
   struct list_node_s* temp;

   temp = head;
   while (temp != NULL && temp->data < value)
      temp = temp->next;

   if (temp == NULL || temp->data > value) {
#ifdef DEBUG
      printf("%d is not in the list\n", value);
#endif
      return 0;
   } else {
#ifdef DEBUG
      printf("%d is in the list\n", value);
#endif
      return 1;
   }
}  /* Member */


/*-----------------------------------------------------------------*/
/* Deletes value from list */
/* If value is in list, return 1, else return 0 */
int Delete(int value) {
   struct list_node_s* curr = head;
   struct list_node_s* pred = NULL;
   int rv = 1;

   /* Find value */
   while (curr != NULL && curr->data < value) {
      pred = curr;
      curr = curr->next;
   }
   
   if (curr != NULL && curr->data == value) {
      if (pred == NULL) { /* first element in list */
         head = curr->next;
#ifdef DEBUG
         printf("Freeing %d\n", value);
#endif
         free(curr);
      } else { 
         pred->next = curr->next;
#ifdef DEBUG
         printf("Freeing %d\n", value);
#endif
         free(curr);
      }
   } else { /* Not in list */
      rv = 0;
   }

   return rv;
}  /* Delete */


/*-----------------------------------------------------------------*/
void Free_list(void) {
   struct list_node_s* current;
   struct list_node_s* following;

   if (Is_empty()) return;
   current = head; 
   following = current->next;
   while (following != NULL) {
#ifdef DEBUG
      printf("Freeing %d\n", current->data);
#endif
      free(current);
      current = following;
      following = current->next;
   }
#ifdef DEBUG
   printf("Freeing %d\n", current->data);
#endif
   free(current);
}  /* Free_list */


/*-----------------------------------------------------------------*/
int  Is_empty(void) {
   if (head == NULL)
      return 1;
   else
      return 0;
}  /* Is_empty */


/*-----------------------------------------------------------------*/
void* Thread_work(void* rank) {
   long my_rank = (long) rank;
   int i, val;
   double which_op;
   unsigned seed = my_rank + 1;
   int my_member_count = 0, my_insert_count=0, my_delete_count=0;
   int ops_per_thread = total_ops / thread_count;

   for (i = 0; i < ops_per_thread; i++) {
      which_op = my_drand(&seed);
      val = my_rand(&seed) % MAX_KEY;
      if (which_op < search_percent) {
         my_rwlock_rdlock(&rwlock);
         Member(val);
         my_rwlock_unlock(&rwlock);
         my_member_count++;
      } else if (which_op < search_percent + insert_percent) {
         my_rwlock_wrlock(&rwlock);
         Insert(val);
         my_rwlock_unlock(&rwlock);
         my_insert_count++;
      } else { /* delete */
         my_rwlock_wrlock(&rwlock);
         Delete(val);
         my_rwlock_unlock(&rwlock);
         my_delete_count++;
      }
   }  /* for */

   pthread_mutex_lock(&count_mutex);
   member_count += my_member_count;
   insert_count += my_insert_count;
   delete_count += my_delete_count;
   pthread_mutex_unlock(&count_mutex);

   return NULL;
}  /* Thread_work */
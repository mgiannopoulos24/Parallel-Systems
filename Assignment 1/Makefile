CC = gcc
CFLAGS = -Wall -g -pthread

# Directories
SRC_DIR = src
OBJ_DIR = obj
BUILD_DIR = build
INCLUDE_DIR = include

# Targets
MONTE_CARLO_TARGET = $(BUILD_DIR)/monte_carlo
SHARED_VAR_TARGET = $(BUILD_DIR)/shared_variable
SHARED_ARRAY_TARGET = $(BUILD_DIR)/shared_array
RW_LOCK_TARGET = $(BUILD_DIR)/rw_lock
BARRIER_PTHREAD_TARGET = $(BUILD_DIR)/barrier_pthread
BARRIER_MUTEX_COND_TARGET = $(BUILD_DIR)/barrier_mutex_cond
BARRIER_SENSE_REVERSAL_TARGET = $(BUILD_DIR)/barrier_sense_reversal


# Source and object files
MONTE_CARLO_SRCS = $(SRC_DIR)/monte_carlo_pi.c $(SRC_DIR)/my_rand.c
MONTE_CARLO_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(MONTE_CARLO_SRCS:.c=.o)))

SHARED_VAR_SRCS = $(SRC_DIR)/shared_variable.c $(SRC_DIR)/my_rand.c
SHARED_VAR_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(SHARED_VAR_SRCS:.c=.o)))

SHARED_ARRAY_SRCS = $(SRC_DIR)/shared_array.c $(SRC_DIR)/my_rand.c
SHARED_ARRAY_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(SHARED_ARRAY_SRCS:.c=.o)))

RW_LOCK_SRCS = $(SRC_DIR)/rw_lock.c $(SRC_DIR)/my_rand.c
RW_LOCK_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(RW_LOCK_SRCS:.c=.o)))

BARRIER_PTHREAD_SRCS = $(SRC_DIR)/barrier_pthread.c
BARRIER_PTHREAD_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(BARRIER_PTHREAD_SRCS:.c=.o)))

BARRIER_MUTEX_COND_SRCS = $(SRC_DIR)/barrier_mutex_cond.c
BARRIER_MUTEX_COND_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(BARRIER_MUTEX_COND_SRCS:.c=.o)))

BARRIER_SENSE_REVERSAL_SRCS = $(SRC_DIR)/barrier_sense_reversal.c
BARRIER_SENSE_REVERSAL_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(BARRIER_SENSE_REVERSAL_SRCS:.c=.o)))

# Include directories
INCLUDES = -I$(INCLUDE_DIR)

# Default rule
all: monte_carlo shared_variable shared_array rw_lock

# Rule to build only monte_carlo
monte_carlo: $(MONTE_CARLO_TARGET)

# Rule to build only shared_variable
shared_variable: $(SHARED_VAR_TARGET)

# Rule to build only shared_array
shared_array: $(SHARED_ARRAY_TARGET)

# Rule to build only rw_lock
rw_lock: $(RW_LOCK_TARGET)

# Rule to build only barrier_pthread
barrier_pthread: $(BARRIER_PTHREAD_TARGET)

# Rule to build only barrier_mutex_cond
barrier_mutex_cond: $(BARRIER_MUTEX_COND_TARGET)

# Rule to build only barrier_sense_reversal
barrier_sense_reversal: $(BARRIER_SENSE_REVERSAL_TARGET)

# Rule to build the monte_carlo executable
$(MONTE_CARLO_TARGET): $(MONTE_CARLO_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to build the shared_variable executable
$(SHARED_VAR_TARGET): $(SHARED_VAR_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to build the shared_array executable
$(SHARED_ARRAY_TARGET): $(SHARED_ARRAY_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to build the rw_lock executable
$(RW_LOCK_TARGET): $(RW_LOCK_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to build the barrier_pthread executable
$(BARRIER_PTHREAD_TARGET): $(BARRIER_PTHREAD_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to build the barrier_mutex_cond executable
$(BARRIER_MUTEX_COND_TARGET): $(BARRIER_MUTEX_COND_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to build the barrier_sense_reversal executable
$(BARRIER_SENSE_REVERSAL_TARGET): $(BARRIER_SENSE_REVERSAL_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to compile .c files into .o files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# Ensure obj directory exists before compiling
$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

# Clean up build files
clean:
	rm -f $(OBJ_DIR)/*.o $(BUILD_DIR)/*

.PHONY: all clean monte_carlo shared_variable shared_array rw_lock barrier_pthread barrier_mutex_cond barrier_sense_reversal

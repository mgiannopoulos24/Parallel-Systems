CC = gcc
CFLAGS = -Wall -g -pthread

# Directories
SRC_DIR = src
OBJ_DIR = obj
BUILD_DIR = build
INCLUDE_DIR = include

# Subdirectories
SUBDIR_1_1 = $(SRC_DIR)/1.1
SUBDIR_1_2 = $(SRC_DIR)/1.2
SUBDIR_1_3 = $(SRC_DIR)/1.3
SUBDIR_1_4 = $(SRC_DIR)/1.4
SUBDIR_1_5 = $(SRC_DIR)/1.5
USEFUL_CODE_DIR = $(SRC_DIR)/useful_code

# Targets
MONTE_CARLO_TARGET = $(BUILD_DIR)/monte_carlo
INCREASE_ATOMIC_TARGET = $(BUILD_DIR)/increase_atomic
INCREASE_TARGET = $(BUILD_DIR)/increase
ARRAY_SUM_TARGET = $(BUILD_DIR)/array_sum
RW_LOCK_TARGET = $(BUILD_DIR)/rw_lock
BARRIER_MUTEX_COND_TARGET = $(BUILD_DIR)/barrier_mutex_cond
BARRIER_PTHREAD_TARGET = $(BUILD_DIR)/barrier_pthread
BARRIER_SENSE_REVERSAL_TARGET = $(BUILD_DIR)/barrier_sense_reversal
PTH_COND_BAR_TARGET = $(BUILD_DIR)/pth_cond_bar

# Source and object files
MONTE_CARLO_SRCS = $(SUBDIR_1_1)/monte_carlo_pi.c $(USEFUL_CODE_DIR)/my_rand.c
MONTE_CARLO_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(MONTE_CARLO_SRCS:.c=.o)))

INCREASE_ATOMIC_SRCS = $(SUBDIR_1_2)/increase_atomic.c
INCREASE_ATOMIC_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(INCREASE_ATOMIC_SRCS:.c=.o)))

INCREASE_SRCS = $(SUBDIR_1_2)/increase.c
INCREASE_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(INCREASE_SRCS:.c=.o)))

ARRAY_SUM_SRCS = $(SUBDIR_1_3)/array_sum.c
ARRAY_SUM_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(ARRAY_SUM_SRCS:.c=.o)))

RW_LOCK_SRCS = $(SUBDIR_1_4)/rw_lock.c $(USEFUL_CODE_DIR)/my_rand.c
RW_LOCK_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(RW_LOCK_SRCS:.c=.o)))

BARRIER_MUTEX_COND_SRCS = $(SUBDIR_1_5)/barrier_mutex_cond.c
BARRIER_MUTEX_COND_OBJS = $(OBJ_DIR)/barrier_mutex_cond.o

BARRIER_PTHREAD_SRCS = $(SUBDIR_1_5)/barrier_pthread.c
BARRIER_PTHREAD_OBJS = $(OBJ_DIR)/barrier_pthread.o

BARRIER_SENSE_REVERSAL_SRCS = $(SUBDIR_1_5)/barrier_sense_reversal.c
BARRIER_SENSE_REVERSAL_OBJS = $(OBJ_DIR)/barrier_sense_reversal.o

# Include directories
INCLUDES = -I$(INCLUDE_DIR)

# Default rule
all: monte_carlo increase_atomic increase array_sum rw_lock barriers

# Rule to build only monte_carlo
monte_carlo: $(MONTE_CARLO_TARGET)

# Rule to build only increase_atomic
increase_atomic: $(INCREASE_ATOMIC_TARGET)

# Rule to build only increase
increase: $(INCREASE_TARGET)

# Rule to build only array_sum
array_sum: $(ARRAY_SUM_TARGET)

# Rule to build only rw_lock
rw_lock: $(RW_LOCK_TARGET)

# Rule to build barrier executables
barriers: $(BARRIER_MUTEX_COND_TARGET) $(BARRIER_PTHREAD_TARGET) $(BARRIER_SENSE_REVERSAL_TARGET)

# Rules for barrier executables
$(BARRIER_MUTEX_COND_TARGET): $(BARRIER_MUTEX_COND_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

$(BARRIER_PTHREAD_TARGET): $(BARRIER_PTHREAD_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

$(BARRIER_SENSE_REVERSAL_TARGET): $(BARRIER_SENSE_REVERSAL_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

$(PTH_COND_BAR_TARGET): $(PTH_COND_BAR_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to build the monte_carlo executable
$(MONTE_CARLO_TARGET): $(MONTE_CARLO_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to build the increase_atomic executable
$(INCREASE_ATOMIC_TARGET): $(INCREASE_ATOMIC_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to build the increase executable
$(INCREASE_TARGET): $(INCREASE_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to build the array_sum executable
$(ARRAY_SUM_TARGET): $(ARRAY_SUM_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to build the rw_lock executable
$(RW_LOCK_TARGET): $(RW_LOCK_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^

# Rule to compile .c files into .o files
$(OBJ_DIR)/%.o: $(SRC_DIR)/*/%.c
	mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# Ensure obj directory exists before compiling
$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

# Clean up build files
clean:
	rm -f $(OBJ_DIR)/*.o $(BUILD_DIR)/*

.PHONY: all clean monte_carlo increase_atomic increase array_sum rw_lock barriers

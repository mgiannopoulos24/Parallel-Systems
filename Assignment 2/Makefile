CC = gcc
CFLAGS = -Wall -g -fopenmp 

# Directories
SRC_DIR = src
OBJ_DIR = obj
BUILD_DIR = build

# Subdirectories
SUBDIR_2_1 = $(SRC_DIR)/2.1
SUBDIR_2_2 = $(SRC_DIR)/2.2
SUBDIR_2_3 = $(SRC_DIR)/2.3

# Targets
GAME_OF_LIFE_TARGET = $(BUILD_DIR)/game_of_life
GAUSS_ELIMINATION_TARGET = $(BUILD_DIR)/gauss_elimination
GAME_OF_LIFE_TASKS_TARGET = $(BUILD_DIR)/game_of_life_tasks

# Source and object files
GAME_OF_LIFE_SRCS = $(SUBDIR_2_1)/game_of_life.c
GAME_OF_LIFE_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(GAME_OF_LIFE_SRCS:.c=.o)))

GAUSS_ELIMINATION_SRCS = $(SUBDIR_2_2)/gauss_elimination.c
GAUSS_ELIMINATION_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(GAUSS_ELIMINATION_SRCS:.c=.o)))

GAME_OF_LIFE_TASKS_SRCS = $(SUBDIR_2_3)/game_of_life_tasks.c
GAME_OF_LIFE_TASKS_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(GAME_OF_LIFE_TASKS_SRCS:.c=.o)))

# Include directories
INCLUDES = -I$(INCLUDE_DIR)

# Default rule
all: game_of_life gauss_elimination game_of_life_tasks

# Rule to build only game_of_life
game_of_life: $(GAME_OF_LIFE_TARGET)

# Rule to build only gauss_elimination
gauss_elimination: $(GAUSS_ELIMINATION_TARGET)

# Rule to build only game_of_life_tasks
game_of_life_tasks: $(GAME_OF_LIFE_TASKS_TARGET)

# Rule to build game_of_life
$(GAME_OF_LIFE_TARGET): $(GAME_OF_LIFE_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $@ $^

# Rule to build gauss_elimination
$(GAUSS_ELIMINATION_TARGET): $(GAUSS_ELIMINATION_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $@ $^

# Rule to build game_of_life_tasks
$(GAME_OF_LIFE_TASKS_TARGET): $(GAME_OF_LIFE_TASKS_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $@ $^

# Rule to compile .c files into .o files
$(OBJ_DIR)/%.o: $(SRC_DIR)/*/%.c
	mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) -c -o $@ $<

# Ensure obj directory exists before compiling
$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

# Clean up build files
clean:
	rm -f $(OBJ_DIR)/*.o $(BUILD_DIR)/*

.PHONY: all clean game_of_life gauss_elimination game_of_life_tasks
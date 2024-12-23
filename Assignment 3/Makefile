CC = mpicc
CFLAGS = -O2

# Directories
SRC_DIR = src
OBJ_DIR = obj
BUILD_DIR = build
INCLUDE_DIR = include

# Subdirectories
SUBDIR_3_1 = $(SRC_DIR)/3.1
SUBDIR_3_2 = $(SRC_DIR)/3.2
SUBDIR_3_3 = $(SRC_DIR)/3.3
SUBDIR_3_4 = $(SRC_DIR)/3.4

# Targets
GAME_OF_LIFE_MPI_TARGET = $(BUILD_DIR)/game_of_life_mpi

# Source and object files
GAME_OF_LIFE_MPI_SRCS = $(SUBDIR_3_1)/game_of_life_mpi.c
GAME_OF_LIFE_MPI_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(GAME_OF_LIFE_MPI_SRCS:.c=.o)))

# Include directories
INCLUDES = -I$(INCLUDE_DIR)

# Default rule
all: $(GAME_OF_LIFE_MPI_TARGET)

# Rule to build the final executable
$(GAME_OF_LIFE_MPI_TARGET): $(GAME_OF_LIFE_MPI_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(GAME_OF_LIFE_MPI_OBJS) -o $@

# Rule to compile .c files into .o files
$(OBJ_DIR)/%.o: $(SRC_DIR)/*/%.c
	mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -c -o $@ $<

# Ensure obj directory exists before compiling
$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

clean:
	rm -f $(OBJ_DIR)/*.o $(BUILD_DIR)/*

.PHONY: all clean

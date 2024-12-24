CC = mpicc
CFLAGS = -O2 -fopenmp 

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
MATRIX_VECTOR_MPI_TARGET = $(BUILD_DIR)/matrix_vector_mpi
GAME_OF_LIFE_RECV_TARGET = $(BUILD_DIR)/game_of_life_recv
GAME_OF_LIFE_HYBRID_TARGET = $(BUILD_DIR)/game_of_life_hybrid

# Source and object files
GAME_OF_LIFE_MPI_SRCS = $(SUBDIR_3_1)/game_of_life_mpi.c
GAME_OF_LIFE_MPI_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(GAME_OF_LIFE_MPI_SRCS:.c=.o)))

MATRIX_VECTOR_MPI_SRCS = $(SUBDIR_3_2)/matrix_vector_mpi.c
MATRIX_VECTOR_MPI_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(MATRIX_VECTOR_MPI_SRCS:.c=.o)))

GAME_OF_LIFE_RECV_SRCS = $(SUBDIR_3_3)/game_of_life_recv.c
GAME_OF_LIFE_RECV_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(GAME_OF_LIFE_RECV_SRCS:.c=.o)))

GAME_OF_LIFE_HYBRID_SRCS = $(SUBDIR_3_4)/game_of_life_hybrid.c 
GAME_OF_LIFE_HYBRID_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(GAME_OF_LIFE_HYBRID_SRCS:.c=.o)))

# Include directories
INCLUDES = -I$(INCLUDE_DIR)

# Default rule
all: $(GAME_OF_LIFE_MPI_TARGET) $(MATRIX_VECTOR_MPI_TARGET) $(GAME_OF_LIFE_HYBRID_TARGET)

# Rule to build only game_of_life_mpi
game_of_life_mpi: $(GAME_OF_LIFE_MPI_TARGET)

# Rule to build only matrix_vector_mpi
matrix_vector_mpi: $(MATRIX_VECTOR_MPI_TARGET)

# Rule to build only game_of_life_recv
game_of_life_recv: $(GAME_OF_LIFE_RECV_TARGET)

# Rule to build only game_of_life_hybrid (MPI + OpenMP)
game_of_life_hybrid: $(GAME_OF_LIFE_HYBRID_TARGET)

# Rule to build the game_of_life_mpi
$(GAME_OF_LIFE_MPI_TARGET): $(GAME_OF_LIFE_MPI_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(GAME_OF_LIFE_MPI_OBJS) -o $@

# Rule to build the matrix_vector_mpi
$(MATRIX_VECTOR_MPI_TARGET): $(MATRIX_VECTOR_MPI_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(MATRIX_VECTOR_MPI_OBJS) -o $@

# Rule to build the game_of_life_recv
$(GAME_OF_LIFE_RECV_TARGET): $(GAME_OF_LIFE_RECV_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(GAME_OF_LIFE_RECV_OBJS) -o $@

# Rule to build the game_of_life_hybrid (MPI + OpenMP)
$(GAME_OF_LIFE_HYBRID_TARGET): $(GAME_OF_LIFE_HYBRID_OBJS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(GAME_OF_LIFE_HYBRID_OBJS) -o $@

# Rule to compile .c files into .o files
$(OBJ_DIR)/%.o: $(SRC_DIR)/*/%.c
	mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -c -o $@ $<

# Ensure obj directory exists before compiling
$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

clean:
	rm -f $(OBJ_DIR)/*.o $(BUILD_DIR)/*

.PHONY: all clean game_of_life_mpi matrix_vector_mpi game_of_life_recv game_of_life_hybrid
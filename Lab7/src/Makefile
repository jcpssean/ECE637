# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: weightedMeanFilter


OBJ = tiff.o allocate.o randlib.o qGGMRF.o solve.o

weightedMeanFilter: weightedMeanFilter.o $(OBJ) 
	$(CC) $(CFLAGS) -o weightedMeanFilter weightedMeanFilter.o $(OBJ) -lm
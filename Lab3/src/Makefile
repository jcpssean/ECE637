# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: seg

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o randlib.o qGGMRF.o solve.o connectedNeighbors.o

seg: seg.o $(OBJ) 
	$(CC) $(CFLAGS) -o seg seg.o $(OBJ) -lm
	mv seg $(BIN)
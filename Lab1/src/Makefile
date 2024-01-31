# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: ImageReadWriteExample SurrogateFunctionExample SolveExample LowPassFilter SharpeningFilter IIRFilter

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o randlib.o qGGMRF.o solve.o

ImageReadWriteExample: ImageReadWriteExample.o $(OBJ) 
	$(CC) $(CFLAGS) -o ImageReadWriteExample ImageReadWriteExample.o $(OBJ) -lm
	mv ImageReadWriteExample $(BIN)

SurrogateFunctionExample: SurrogateFunctionExample.o $(OBJ) 
	$(CC) $(CFLAGS) -o SurrogateFunctionExample SurrogateFunctionExample.o $(OBJ) -lm
	mv SurrogateFunctionExample $(BIN)

SolveExample: SolveExample.o $(OBJ) 
	$(CC) $(CFLAGS) -o SolveExample SolveExample.o $(OBJ) -lm
	mv SolveExample $(BIN)

LowPassFilter: LowPassFilter.o $(OBJ) 
	$(CC) $(CFLAGS) -o LowPassFilter LowPassFilter.o $(OBJ) -lm
	mv LowPassFilter $(BIN)

SharpeningFilter: SharpeningFilter.o $(OBJ) 
	$(CC) $(CFLAGS) -o SharpeningFilter SharpeningFilter.o $(OBJ) -lm
	mv SharpeningFilter $(BIN)	

IIRFilter: IIRFilter.o $(OBJ) 
	$(CC) $(CFLAGS) -o IIRFilter IIRFilter.o $(OBJ) -lm
	mv IIRFilter $(BIN)	
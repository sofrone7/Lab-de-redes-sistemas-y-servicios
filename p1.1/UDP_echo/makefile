all: echo_noc

echo_noc: echo_noc.o DieWithError.o
	gcc echo_noc.o DieWithError.o -o echo_noc

echo_noc.o: echo_noc.c
	gcc -c echo_noc.c

DieWithError.o: DieWithError.c
	gcc -c DieWithError.c

clean:
	rm echo_noc echo_noc.o DieWithError.o

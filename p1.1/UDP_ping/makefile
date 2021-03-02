all: ping_noc ping_noc_serv

ping_noc: ping_noc.c DieWithError.c desvEstandar.c ResolveName.c
	gcc -g -Wall ping_noc.c DieWithError.c ResolveName.c desvEstandar.c -lm -o ping_noc 

ping_noc_serv: ping_noc_serv.c DieWithError.c
	gcc -g -Wall ping_noc_serv.c DieWithError.c -o ping_noc_serv

clean: ping_noc ping_noc_serv

all: ping_oc ping_oc_serv

ping_oc: ping_oc.c
	gcc -g -Wall ping_oc.c -o ping_oc -lm

ping_oc_serv: ping_oc_serv.c
	gcc -g -Wall ping_oc_serv.c -o ping_oc_serv

clean:
	rm ping_oc
	rm ping_oc_serv

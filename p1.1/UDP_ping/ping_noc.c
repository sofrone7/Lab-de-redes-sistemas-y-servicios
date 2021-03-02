#include <stdio.h> /* for printf() and fprintf() */
#include <sys/socket.h> /* for socket(), connect(), sendto(), and recvfrom() */
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <time.h>
#include <math.h>
#include <netdb.h> /* gethostbyname() */

#define ECHOMAX 255
volatile sig_atomic_t stop;

void CtrlCHand(int signum)
{
  stop = 1;
}

void DieWithError(char *errorMessage);
long double desvEstandar(long double datos[], long double media, int cantidad);
unsigned long ResolveName(char name[]);

int main(int argc, char *argv[])
{
  int sock; /* Socket descriptor */
  struct sockaddr_in pingServAddr; /* Echo server address */
  struct sockaddr_in fromAddr; /* Source address of echo*/
  unsigned short echoServPort;
  unsigned int fromSize;
  char *servIP;
  char *pingString;
  char echoBuffer[ECHOMAX+1];
  int pingStringLen;
  int respStringLen;
  int ttl = 64, Recv = 0;
  long double time = 0, time_total = 0, time_min = 0, avg = 0, time_max = 0, mdev = 0;
  long double array[] = { 0 };
  struct timespec time_send, time_recv;

  if ((argc < 2) || (argc > 3)) /* Test for correct number of arguments */
  {
    fprintf(stderr,"Usage: %s <Server IP> [<Echo Port>]\n", argv[0]);
    exit(1);
  }
  
  servIP = argv[1] ;
  pingString = "s" ;
  
  if ((pingStringLen = strlen(pingString)) > ECHOMAX) /* Check input length */
    DieWithError("Echo word too long");
    
  if (argc == 3)
    echoServPort = atoi(argv[2]) ; /* Use given port, if any */
  else
    echoServPort = 7; /* 7 is the well-known port for the echo service */ 
    
  /* Create a datagram/UDP socket */
  if ((sock = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0)
    DieWithError( "socket () failed") ;
    
  /* set TTL unicast packet */
  if (setsockopt(sock, IPPROTO_IP, IP_TTL, &ttl, sizeof(ttl)) < 0)
    DieWithError("setsockopt() failed");
    
  /* Construct the server address structure */
  memset(&pingServAddr, 0, sizeof(pingServAddr)); /* Zero out structure */
  pingServAddr.sin_family = AF_INET; /* Internet addr family */
  pingServAddr.sin_addr.s_addr = ResolveName(servIP); /* Server IP address */
  pingServAddr.sin_port = htons(echoServPort); /* Server port */
  
  printf("PING %s \n", servIP);
  signal(SIGINT, CtrlCHand);
  int i = 0;
  
  while(!stop)
  {
    i ++;
    clock_gettime(CLOCK_REALTIME, &time_send);
    /* Send the string to the server */
    if (sendto(sock, pingString, pingStringLen, 0, (struct sockaddr *) &pingServAddr,                  sizeof(pingServAddr)) != pingStringLen)
      DieWithError("sendto() sent a different number of bytes than expected");
  
    /* Recv a response */
    fromSize = sizeof(fromAddr) ;
    if ((respStringLen = recvfrom(sock, echoBuffer, ECHOMAX, 0, (struct sockaddr *) &fromAddr, &fromSize)) != pingStringLen)
      DieWithError("recvfrom() failed") ;
    if (pingServAddr.sin_addr.s_addr != fromAddr.sin_addr.s_addr)
    {
      fprintf(stderr,"Error: received a packet from unknown source.\n");
      exit(1);
    }
    clock_gettime(CLOCK_REALTIME, &time_recv);
    double timeTranSeg = ((double)(time_recv.tv_nsec - time_send.tv_nsec))/1000000.0;
    time = (time_recv.tv_sec - time_send.tv_sec) + timeTranSeg;
    time *= 1000;
    time += timeTranSeg;
    time_total += time;
    array[i-1] = time;
    //echoBuffer[respStringLen] = '\0' ;
    //printf("Received: %s\n", echoBuffer); /* Print the echoed arg */
    printf("%d bytes from %s: icmp_seq=%d ttl=%d time=%.0Lf ms \n", pingStringLen, servIP, i, ttl, time);
    
    /* Stats */
    if (time_min == 0 || time < time_min)
        time_min = time;
      
      if (time_max == 0 || time > time_max)
        time_max = time;
      
      avg = time_total/i;
    sleep(1);
  }
  mdev = desvEstandar(array, avg, i);
  
  printf("\n");
	printf("--- %s ping statistics ---\n", servIP);
  printf("%d packets transmitted, %d received, %.2f%% packet loss, time %.0Lf ms \n", i, Recv, ((i - Recv)/i) * 100.0, time_total);
  printf("rtt min/avg/max/mdev = %.3Lf/%.3Lf/%.3Lf/%.3Lf ms \n", time_min, avg, time_max, mdev);
  
  close(sock);
  exit(0);
}
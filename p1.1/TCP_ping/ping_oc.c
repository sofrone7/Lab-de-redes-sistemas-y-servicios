#include <stdio.h> /* for printf() and fprintf() */
#include <sys/socket.h> /* for socket(), connect(), send(), and recv() */
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <signal.h>
#include <math.h>
#include <netdb.h> /* gethostbyname() */

#define RCVBUFSIZE 32
volatile sig_atomic_t stop;

void CtrlCHand(int signum)
{
  stop = 1;
}

void DieWithError(char *errorMessage)
{
	perror(errorMessage);
	exit(1);
}

long double desvEstandar(long double datos[], long double media, int cantidad)
{
  long double resultado = 0, var = 0;
  for(int y = 0; y < cantidad; y++)
    var += pow((datos[y] - media) ,2);
  var = var/cantidad;
  resultado = sqrt(var);
  return resultado;
}

unsigned long ResolveName(char name[])
{
  struct hostent *host; /* Structure containing host information */
  if ((host = gethostbyname(name)) == NULL)
  {
    fprintf(stderr, "gethostbyname() failed");
    exit(1);
  }
  
  /* return the binary, network-byte-ordered address */
  return *((unsigned long *) host->h_addr_list[0]);
}

int main(int argc, char *argv[])
{
	int sock;
	struct sockaddr_in pingServAddr;
	unsigned short pingServPort;
	char *servIP;
	char *pingString;
	char echoBuffer[RCVBUFSIZE];
	unsigned int pingStringLen;
	int bytesRcvd, totalBytesRcvd, ttl = 64, Recv = 0;
  long double time = 0, time_total = 0, time_min = 0, avg = 0, time_max = 0, mdev = 0;
  long double array[] = { 0 };
  struct timespec time_send, time_recv;

	if ((argc < 2) || (argc > 3))
	{
		 fprintf(stderr, "Usage: %s <Server IP> [<PING Port>]\n", argv[0]);
		exit(1);
	}

	servIP = argv[1];
  pingString = "s";
	//pingString = argv[2];

	if (argc == 3)
		pingServPort = atoi(argv[2]);
	else
		pingServPort = 7; //puerto para echo service
   
  //Crear socket
	if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
		DieWithError("socket() failed");

  /* set TTL unicast packet */
  if (setsockopt(sock, IPPROTO_IP, IP_TTL, &ttl, sizeof(ttl)) < 0)
    DieWithError("setsockopt() failed");
  
	//Construir la estructura de server address
	memset(&pingServAddr, 0, sizeof(pingServAddr));
	pingServAddr.sin_family = AF_INET;
  pingServAddr.sin_addr.s_addr = ResolveName(servIP);
	//pingServAddr.sin_addr.s_addr = inet_addr(servIP); //inet_addr convierte la cadena serverIP, en notación decimal con puntos estándar de IPv4, en un valor entero adecuado para su uso como dir de Internet
	pingServAddr.sin_port = htons(pingServPort); //htons convierte el entero sin signo pingServPort del orden de bytes del host al orden de bytes de la red

	//Establecer conexión al servidor echo
	if (connect(sock, (struct sockaddr *) &pingServAddr, sizeof(pingServAddr)) < 0)
		DieWithError("connect() failed");

	pingStringLen = strlen(pingString);
  //pingStringLen = 1;
  printf("PING %s \n", servIP);
  
  signal(SIGINT, CtrlCHand);
  int i = 0;
  //for( int x = 0; x < 2; x++)
  while(!stop)
  {
    i ++;
    clock_gettime(CLOCK_REALTIME, &time_send); 
    if (send(sock, pingString, pingStringLen, 0) != pingStringLen)
  	//if (sendto(sock, pingString, pingStringLen, 0, (struct sockaddr *) &pingServAddr, sizeof(pingServAddr)) != pingStringLen)
  		DieWithError("send() sent a different number of bytes than expected");
  
  	totalBytesRcvd = 0;
  	while (totalBytesRcvd < pingStringLen)
  	{
  		if ((bytesRcvd = recv(sock, echoBuffer, RCVBUFSIZE - 1, 0)) <= 0)
        break;
  			//DieWithError("recv() failed or connection closed prematurely");
     else
     {
      Recv++;
  		totalBytesRcvd += bytesRcvd;
  		//echoBuffer[bytesRcvd] = '\0';
      clock_gettime(CLOCK_REALTIME, &time_recv);
      double timeTranSeg = ((double)(time_recv.tv_nsec - time_send.tv_nsec))/1000000.0;
      time = (time_recv.tv_sec - time_send.tv_sec) + timeTranSeg;
      time *= 1000;
      time += timeTranSeg;
      time_total += time;
      array[i-1] = time;
      
  		printf("%d bytes from %s: icmp_seq=%d ttl=%d time=%.0Lf ms \n", pingStringLen, servIP, i, ttl, time);
      //printf("time[%d] = %.0Lf \n", i, array[i-1]);
      /* Stats */
      if (time_min == 0 || time < time_min)
        time_min = time;
      
      if (time_max == 0 || time > time_max)
        time_max = time;
      
      avg = time_total/i;
      sleep(1);
      }
  	}
  }
  mdev = desvEstandar(array, avg, i);
  
  printf("\n");
	printf("--- %s ping statistics ---\n", servIP);
  printf("%d packets transmitted, %d received, %.2f%% packet loss, time %.0Lf ms \n", i, Recv, ((i - Recv)/i) * 100.0, time_total);
  printf("rtt min/avg/max/mdev = %.3Lf/%.3Lf/%.3Lf/%.3Lf ms \n", time_min, avg, time_max, mdev);
	close(sock);
	exit(0);
}

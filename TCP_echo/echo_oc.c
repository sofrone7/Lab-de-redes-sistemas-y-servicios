#include <stdio.h> /* for printf() and fprintf() */
#include <sys/socket.h> /* for socket(), connect(), send(), and recv() */
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define RCVBUFSIZE 32

void DieWithError(char *errorMessage)
{
	perror(errorMessage);
	exit(1);
}

int main(int argc, char *argv[])
{
	int sock;
	struct sockaddr_in echoServAddr;
	unsigned short echoServPort;
	char *servIP;
	char *echoString;
	char echoBuffer[RCVBUFSIZE];
	unsigned int echoStringLen;
	int bytesRcvd, totalBytesRcvd;

	if ((argc < 3) || (argc > 4))
	{
		 fprintf(stderr, "Usage: %s <Server IP> <Echo Word> [<Echo Port>]\n", argv[0]);
		exit(1);
	}

	servIP = argv[1];
	echoString = argv[2];

	if (argc == 4)
		echoServPort = atoi(argv[3]);
	else
		echoServPort = 7; //puerto para echo service

	if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
		DieWithError("socket() failed");

	//Construir la estructura de server address
	memset(&echoServAddr, 0, sizeof(echoServAddr));
	echoServAddr.sin_family = AF_INET;
	echoServAddr.sin_addr.s_addr = inet_addr(servIP); //inet_addr convierte la cadena serverIP, en notación decimal con puntos estándar de IPv4, en un valor entero adecuado para su uso como dir de Internet
	echoServAddr.sin_port = htons(echoServPort); //htons convierte el entero sin signo echoServPort del orden de bytes del host al orden de bytes de la red

	//Establecer conexión al servidor echo
	if (connect(sock, (struct sockaddr *) &echoServAddr, sizeof(echoServAddr)) < 0)
		DieWithError("connect() failed");

	echoStringLen = strlen(echoString);

	if (send(sock, echoString, echoStringLen, 0) != echoStringLen)
		DieWithError("send() sent a different number of bytes than expected");

	totalBytesRcvd = 0;
	printf("Received: ");
	while (totalBytesRcvd < echoStringLen)
	{
		if ((bytesRcvd = recv(sock, echoBuffer, RCVBUFSIZE - 1, 0)) <= 0)
			DieWithError("recv() failed or connection closed prematurely");
		totalBytesRcvd += bytesRcvd;
		echoBuffer[bytesRcvd] = '\0';
		printf(echoBuffer);
	}

	printf("\n");
	close(sock);
	exit(0);
}

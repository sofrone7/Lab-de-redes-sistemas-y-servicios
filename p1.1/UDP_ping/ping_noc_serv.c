#include <stdio.h> /* for printf() and fprintf() */
#include <sys/socket.h> /* for socket() and bind() */
#include <arpa/inet.h> /* for sockaddr_in and inet_ntoa() */
#include <stdlib.h> /* for atoi() */
#include <string.h>
#include <unistd.h>

#define ECHOMAX 255

void DieWithError(char *errorMessage);

int main(int argc, char *argv[])
{
  int sock; /* Socket */
  struct sockaddr_in pingServAddr; /* Local address */
  struct sockaddr_in pingClntAddr; /* Client address */
  unsigned int cliAddrLen; /* Length of incoming message */
  char echoBuffer[ECHOMAX]; /* Buffer for echo string */
  unsigned short pingServPort; /* Server port */
  int recvMsgSize; /* Size of received message */
  
  if (argc != 2) /* Test for correct number of parameters */
  {
    fprintf(stderr, "Usage: %s <UDP SERVER PORT>\n", argv[0]) ;
    exit(1);
  }
  
  pingServPort = atoi(argv[1]) ; /* First arg' local port */
  
  /* Create socket for sending/receiving datagrams */
  if ((sock = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0)
    DieWithError("socket() failed");
    
  /* Construct local address structure */
  memset(&pingServAddr, 0, sizeof(pingServAddr)); /* Zero out structure */
  pingServAddr.sin_family = AF_INET; /* Internet address family */
  pingServAddr.sin_addr.s_addr = htons(INADDR_ANY); /* Any incoming interface */
  pingServAddr.sin_port = htons(pingServPort); /* Local port */
  
  /* Bind to the local address */
  if (bind(sock, (struct sockaddr *) &pingServAddr, sizeof(pingServAddr)) < 0)
    DieWithError("bind() failed");
    
  for (;;) /* Run forever */
  {
    /* Set the size of the in-out parameter */
    cliAddrLen = sizeof(pingClntAddr);
    
    /* Block until receive message from a client */
    if ((recvMsgSize = recvfrom(sock, echoBuffer, ECHOMAX, 0, (struct sockaddr *) &pingClntAddr, &cliAddrLen)) < 0)
      DieWithError("recvfrom() failed");
      
    printf("Handling client %s\n", inet_ntoa(pingClntAddr.sin_addr));
    
    /* Send received datagram back to the client */
    if (sendto(sock, echoBuffer, recvMsgSize, 0, (struct sockaddr *) &pingClntAddr, sizeof(pingClntAddr)) != recvMsgSize)    
      DieWithError("sendto() sent a different number of bytes than expected"); }
    /* NOT REACHED */
}
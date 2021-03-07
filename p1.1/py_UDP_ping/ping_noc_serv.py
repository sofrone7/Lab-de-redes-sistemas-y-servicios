#!/usr/bin/env python3

import sys
import socket

if len(sys.argv) != 2:
  print('Usage:', sys.argv[0], '<Server Port>\n')
  
pingServPort = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Unimos (bind) el socket al puerto
sock.bind(('localhost', int(pingServPort)))

while True:
  message, clntPingAddr = sock.recvfrom(16)
  print('Handling client', clntPingAddr)
  sock.sendto(message, clntPingAddr)
  #try:
    #print('conexion con', clntPingAddr)
    
    #while True:
      #bytesRcvd = sock.recvfrom(16)
      #print('received {!r}'.format(bytesRcvd))
      #if bytesRcvd:
        #print('sending data back to the client')
        #sock.sendto(bytesRcvd)
      #else:
        #print('no hay datos recibidos de')
        #break
        
  #finally:
    #print('Finalizado')
    
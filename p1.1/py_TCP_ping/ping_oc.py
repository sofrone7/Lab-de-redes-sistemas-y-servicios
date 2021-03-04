#!/usr/bin/env python3

import sys
import socket
import time

if len(sys.argv) < 2 or len(sys.argv) > 3:
  print('Usage:', sys.argv[0], '<Server IP> [<PING Port>]')

#Definición de variables
servIP = sys.argv[1]
pingServPort = sys.argv[2]

#Crear socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conexión
sock.connect((servIP, int(pingServPort)))

seq = 0

try:
  for i in [0, 1, 2]:
    seq += 1
    pingString = b"mensaje" #convertido a bytes
    #clock
    sock.sendall(pingString);
      
    totalBytesRcvd = 0;
    pingStringLen = len(pingString) # len = 7
    bytesRcvd = 0
      
    if sock.recv(16):
      print('success')
    #while totalBytesRcvd < pingStringLen:
      #print('recibido de vuelta', sock.recv(16), len(sock.recv(16)))
      #bytesRcvd = sock.recv(16)
      #print('bytes recv', bytesRcvd)
      #totalBytesRcvd += len(bytesRcvd)
      #totalBytesRcvd += len(sock.recv(16))
      #print('bytes recibidos', totalBytesRcvd)
    time.sleep(1)
    
finally:
  sock.close()
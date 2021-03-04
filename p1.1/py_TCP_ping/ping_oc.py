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

print('PING',servIP)
seq = 0

try:
  while True:
    seq += 1
    pingString = b"mensaje" #convertido a bytes
    #clock
    sock.send(pingString);
      
    totalBytesRcvd = 0;
    pingStringLen = len(pingString) # len = 7
    bytesRcvd = 0
      
    if sock.recv(16): #comprobamos que sólo si recibimos respuesta de vuelta
      print(pingStringLen, 'bytes from', servIP, 'icmp_seq=', seq, 'ttl= time= ms')
    
    time.sleep(1)
except KeyboardInterrupt:
  print('stop')
finally:
  print('close socket')
  sock.close()
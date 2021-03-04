#!/usr/bin/env python3

import sys
import socket

if len(sys.argv) != 2:
  print('Usage:', sys.argv[0], '<Server Port>\n')
  
pingServPort = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Unimos (bind) el socket al puerto
sock.bind(('localhost', int(pingServPort)))

sock.listen(1)

while True:
  connection, clntPingAddr = sock.accept()
  try:
    print('conexion con', clntPingAddr)
    
    while True:
      bytesRcvd = connection.recv(16)
      print('received {!r}'.format(bytesRcvd))
      if bytesRcvd:
        print('sending data back to the client')
        connection.sendall(bytesRcvd)
      else:
        print('no hay datos recibidos de', clntPingAddr)
        break
        
  finally:
    connection.close()
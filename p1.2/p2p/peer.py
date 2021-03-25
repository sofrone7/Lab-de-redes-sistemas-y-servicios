#!/usr/bin/env python3

import sys
import socket
import pickle

if len(sys.argv) != 3:
	print('Usage: {} <Server IP> [<PING PORT>]', sys.argv[0])

servIP = sys.argv[1]
ServPort = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((servIP, int(ServPort)))

ServSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServSock.setblocking(0)

ServSock.bind(('', 0))
ServSock.listen(10)
print(ServSock.getsockname()[1])
port = ServSock.getsockname()[1]
sock.sendall(bytes(port, 'utf-8'))
#sock.sendall(bytes(mensaje, 'utf-8'))

direcciones = []
try:
  while True:
    datos = sock.recv(1024)
    if datos:
      datos = pickle.loads(datos)
      print(datos)
      for x in datos:
        print(x)
			

except KeyboardInterrupt:
  sock.close()

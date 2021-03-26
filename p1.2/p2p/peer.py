#!/usr/bin/env python3

import sys
import socket
import pickle
import select
import re

if len(sys.argv) != 3:
	print('Usage: {} <Server IP> [<PING PORT>]', sys.argv[0])

servIP = sys.argv[1]
ServPort = sys.argv[2]

ServSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServSock.connect((servIP, int(ServPort)))

#Socket de escucha
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setblocking(0)
sock.bind(('', 0))
sock.listen(10)

print('Puerto de escucha: ', sock.getsockname()[1])
port = sock.getsockname()[1]
ServSock.sendall(pickle.dumps(port))
#sock.sendall(bytes(mensaje, 'utf-8'))

lectura = [sock, sys.stdin]
datos = ServSock.recv(1024)
if datos:
  lista = pickle.loads(datos)
  #print(lista)
  for x in lista:
    print('Conectamos con:', x)
    sockconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockconn.connect(x)
    lectura.append(sockconn)
print('Lista:')
for p in lectura:
  if p != sock and p != sys.stdin:
    print(p)
print()

#direcciones = []

try:
  while lectura:
    read, write, error = select.select(lectura, [], [])
    for s in read:
      if s is sock:
        connection, clntAddr = sock.accept()
        print('Conexión con peer:', clntAddr)
        lectura.append(connection)
        for x in lectura:
          if x != sys.stdin and x != sock:
            print(x)
      if s is sys.stdin:
        mensaje = input('> ')
        if mensaje:
          for peer in lectura:
            if peer != sock and peer != sys.stdin:
              peer.sendall(bytes(mensaje, 'utf-8')) 
              #sockconn.sendall(bytes(mensaje, 'utf-8')) 
      #if s is sock:
      else:
        datos = s.recv(1024)
        if datos:
          print('\n< ',datos.decode("utf-8"))
			

except KeyboardInterrupt:
  sock.close()
  ServSock.close()

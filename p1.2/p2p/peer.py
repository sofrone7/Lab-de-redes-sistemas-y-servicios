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
  if lista: #Si la lista no está vacía
    for x in lista:
      print('Conectamos con:', x)
      #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.connect(x)
        #lectura.append(s)
        #print('Socket de', x, 'es:', s)
        #print()
      soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      soc.connect(x)
      lectura.append(soc)
print('Lista:')
for p in lectura:
  if p != sys.stdin:
    #conn = sock.getpeername()
    #print(conn)
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
          if x != sys.stdin:
            #print(x.getpeername())
            #print(x)
            #conn = sock.getpeername()
            #print(conn)
            print(x)
        print()
      if s is sys.stdin:
        mensaje = input('> ')
        if mensaje:
          for peer in lectura:
            if peer != sock and peer != sys.stdin:
              peer.sendall(bytes(mensaje, 'utf-8')) 
              #sockconn.sendall(bytes(mensaje, 'utf-8')) 
      #if s is sock:
      else:
        if s != sock: #Entiendo que el primero en conectarse no va a pasar por el primer if y sock se comprobará aquí en tal caso
          #print(s)
          datos = s.recv(1024)
          if datos:
            print('\n< ',datos.decode("utf-8"))
			

except KeyboardInterrupt:
  sock.close()
  ServSock.close()

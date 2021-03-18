#!/usr/bin/env python3
# -*- coding: cp1252 -*-

import sys
import socket
import select

if len(sys.argv) != 2:
  print('Usage:', sys.argv[0], '<Server Port>\n')
  
ServPort = sys.argv[1]

# Socket TCP del servidor
ServSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Configurarlo para que no se bloquee
ServSock.setblocking(0) 

# Unimos (bind) socket al puerto
ServSock.bind(('', int(ServPort)))

# Escucha conexiones entrantes
ServSock.listen(10) # Nº de conexiones posibles

# Sockets que van a ready_to_read
entrantes = [ServSock]

# Sockets que van a ready_to_write
salientes = []

while entrantes:
  ready_to_read, ready_to_write, error = select.select(entrantes, salientes, entrantes)
  for s in ready_to_read:
    if s is ServSock:
      connection, clntAddr = ServSock.accept()
      print( 'Conexión con:', clntAddr)
      entrantes.append(connection) # Añadimos a la lista de entrantes el nuevo cliente
      #for x in entrantes:
        #print(x)
    else:
      datos = s.recv(1024) # Cuando se mande un mensaje
      if datos:
        for cliente in entrantes: # Para todos los clientes en la lista de entrantes
          if cliente != ServSock and cliente != s: # Excepto el servidor y el que manda el mensaje
            cliente.sendall(datos) #Se envía en mensaje de s a cada cliente
      else:
        entrantes.remove(s)
        s.close()
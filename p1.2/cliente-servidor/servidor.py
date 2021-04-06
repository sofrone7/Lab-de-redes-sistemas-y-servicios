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

try:
  while entrantes:
    ready_to_read, ready_to_write, error = select.select(entrantes, salientes, entrantes)
    for s in ready_to_read:
      if s is ServSock: #Si s es el socket del servidor aceptamos las conexiones de los clientes que entran al chat
        connection, clntAddr = ServSock.accept()
        print( 'Conexión con:', clntAddr)
        entrantes.append(connection) # Añadimos a la lista de entrantes el nuevo cliente
      else:
        datos = s.recv(1024) # Cuando se reciba un mensaje
        if datos:
          for cliente in entrantes: # Para todos los clientes en la lista de entrantes
            if cliente != ServSock and cliente != s: # Excepto el servidor y el cliente que ha mandado el mensaje
              cliente.sendall(datos) #El servidor reenvía el mensaje de s a cada cliente
        else: 
          print('Ya no hay conexión con:',s.getpeername())
          entrantes.remove(s) #En caso de perderse la conexión con algún cliente se le expulsa de la lista
          s.close() #Y se cierra su socket asociado
except KeyboardInterrupt:
  for s in ready_to_read: #Se cierran todas las conexiones en caso de cerrar el servidor
    if s != ServSock:
      entrantes.remove(s)
      s.close()         
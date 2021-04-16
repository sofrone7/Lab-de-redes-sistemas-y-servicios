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
ServSock.listen(10) # N� de conexiones posibles

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
        print( 'Conexi�n con:', clntAddr)
        entrantes.append(connection) # A�adimos a la lista de entrantes el nuevo cliente
        
        recvdata = connection.recv(5000).decode()
        if recvdata:
          pieces = recvdata.split("\n")
          if ( len(pieces) > 0 ):
            print(pieces[0])
          
          data = "HTTP/1.1 200 OK\r\n"
          data += "Content-Type: text/html; \r\n"
          data += "\r\n"
          data += "<html><body> Hello World </body></html>\r\n\r\n"
          
          connection.sendall(data.encode())
          #connection.shutdown(SHUT_WR)
        else: 
          print('Ya no hay conexi�n con:',s.getpeername())
          entrantes.remove(s) #En caso de perderse la conexi�n con alg�n cliente se le expulsa de la lista
          s.close() #Y se cierra su socket asociado
except KeyboardInterrupt:
  for s in ready_to_read: #Se cierran todas las conexiones en caso de cerrar el servidor
    if s != ServSock:
      entrantes.remove(s)
      s.close()         
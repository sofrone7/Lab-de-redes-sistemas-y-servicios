#!/usr/bin/env python3

import sys
import socket
import select
import pickle

if len(sys.argv) != 2:
	printf('Usage:', sys.argv[0], '<Server Port>\n')

ServPort = sys.argv[1]

ServSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServSock.setblocking(0)

ServSock.bind(('', int(ServPort)))
ServSock.listen(10)

usuarios = [ServSock]
direcciones = []

try:
  while usuarios:
    ready_to_read, ready_to_write, error = select.select(usuarios,[] ,[] )
    for s in ready_to_read:
      if s is ServSock: #Si s es el socket del servidor aceptamos las conexiones entrantes
        connection, clntAddr = ServSock.accept()
        port = connection.recv(1024) #Recibimos el puerto de escucha del nuevo peer
        port = pickle.loads(port) #Deserializamos la información
        #print(port.decode("utf-8"))
        print( 'Nuevo usuario:', clntAddr)
        #print(connection.getpeername())
        usuarios.append(connection) #Añadimos el nuevo peer a la lista usuarios
        connection.sendall(pickle.dumps(direcciones)) #Enviamos al nuevo peer la lista de peers disponibles formada por duplas (Dirección IP, puerto de escucha)
        Dir = (clntAddr[0], port) #Creamos la dupla del nuevo peer con su dirección  IP a partir del primer elemento de clntAddr y su puerto de escucha
        print('Dirrecion de escucha:', Dir)
        direcciones.append(Dir) #Añadimos la nueva dupla a la lista correspondiente
      else:
        try:	
          conn = ServSock.getpeername() #Obtenemos la dirreción de cada conexión
          s.connect(conn) #Y comprobamos si el peer correspondiente a tal conexión sigue conectado
        except: #En caso de que no siga conectado...
          print('Ya no hay conexión con: ', s.getpeername())
          i = usuarios.index(s) - 1 #La posición correspondiente en la lista de direcciones será la de usuarios - 1(ServSock)
          usuarios.remove(s) #Expulsamos el socket correspondiente de la lista usuarios
          s.close() #Cerramos su conexión
          direcciones.pop(i) #Expulsamos su dirección de escucha de la lista direcciones para que los nuevos peers no traten de conectarse a él
    
except KeyboardInterrupt: #En caso de cerrar el servidor se cierran todas las conexiones
  ServSock.close()
  for s in ready_to_read:
    if s != ServSock:
      s.close()
      usuarios.remove(s)



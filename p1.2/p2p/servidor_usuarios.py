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

while usuarios:
  ready_to_read, ready_to_write, error = select.select(usuarios,[] ,[] )
  for s in ready_to_read:
    if s is ServSock:
      connection, clntAddr = ServSock.accept()
      print( 'Nuevo usuario:', clntAddr)
      usuarios.append(connection)
      connection.sendall(pickle.dumps(direcciones))
      direcciones.append(clntAddr[0])
      direcciones.append(clntAddr[1])
      
			#for x in usuarios:
				#if x != ServSock:
					#msg = x.getpeername()
					#print(msg)
					#connection.send(pickle.dumps(msg))
					#msg = pickle.dumps(msg)
					#connection.sendall(bytes(msg, "utf-8"))
			
    else:
      try:	
        conn = ServSock.getpeername()
				#print(conn)
        s.connect(conn)
      except:
        print('Ya no hay conexión con: ', s.getpeername())
        usuarios.remove(s)
        s.close()



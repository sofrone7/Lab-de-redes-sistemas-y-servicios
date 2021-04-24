#!/usr/bin/env python3
# -*- coding: cp1252 -*-

import sys
import socket
import select
import re #expresiones regulares

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
				recvdata = s.recv(5000).decode()
				if recvdata:
					print(recvdata)
					pieces = recvdata.split("\n")
					if ( len(pieces) > 0):
						pieces = pieces[0].split("/")
						#for i in range(len(pieces)):
							#print(pieces[i])
						modo = pieces[2]
						print('modo:', modo)
						pieces = pieces[1].split()
						solicitud = pieces[0]
						if 'text/html' in recvdata:
							solicitud += '.html'
							print('solicitud:', solicitud)
							try: #Por tanto, intentamos abrirlo y enviar su infromación contenida
								f = open(solicitud, 'rb') 
								bytes_f = f.read() #.encode() #Leemos el archivo y codificamos su información para ser enviada

								if re.findall('[.]html$', solicitud): #En caso de que lo solicitado termine ".html", identificamos que se trata de un archivo html
									data = "HTTP/1.1 200 OK\r\n"
									data += "Content-Type: text/html; \r\n"
									#data += bytes_f
									#data += "\r\n"
									s.sendall(data.encode())
									while(bytes_f):
										s.sendall(bytes_f)
										bytes_f = f.read()
							except FileNotFoundError: 
								f = open('error_404.html', 'rb') 
								bytes_f = f.read() 
								data = "HTTP/1.1 200 OK\r\n"
								data += "Content-Type: text/html; \r\n"
								s.sendall(data.encode())
								while(bytes_f):
									s.sendall(bytes_f)
									bytes_f = f.read()

							finally:
								f.close()

							#s.sendall(data.encode())

							#f = open(solicitud, 'rb') 
							#bytes_f = f.read()
							#s.sendall(bytes_f) 
							#f.close()

					#s.sendall(data.encode())
					#connection.shutdown(SHUT_WR)
				else: 
					print('Ya no hay conexión con:',s.getpeername())
					entrantes.remove(s) #En caso de perderse la conexión con algún cliente se le expulsa de la lista
					s.close() #Y se cierra su socket asociado
except KeyboardInterrupt:
	ServSock.close() 
	print('Cerrado')
	for s in ready_to_read: #Se cierran todas las conexiones en caso de cerrar el servidor
		if s != ServSock:
			entrantes.remove(s)
			s.close()         

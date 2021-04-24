#!/usr/bin/env python3
# -*- coding: cp1252 -*-

import sys
import socket
import select
import re #expresiones regulares
import os

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

#try:
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
				pieces = recvdata.split()

				metodo = pieces[0]
				solicitud = pieces[1]

				print()
				print('Solicitud:', solicitud)

				solicitud = solicitud.lstrip('/') #Elimina el / inicial
				if(solicitud == ''):
					solicitud = 'index.html' #archivo index.html como default
				if 'text/html' in recvdata:
					tipo = 'text/html'
					if re.findall('[.]html$', solicitud): 
						print('Solicitud:', solicitud)
					else:
						solicitud += '.html'
						print('Solicitud:', solicitud)

				if '.jpg' in recvdata:
					tipo = 'image/jpg'
					print('Solicitud:', solicitud)
				#elif 'image/webp' in recvdata:
					#tipo = 'image/webp'

				try: #Por tanto, intentamos abrirlo y enviar su infromación contenida
					f = open(solicitud, 'rb') 
					bytes_f = f.read() #.encode() #Leemos el archivo y codificamos su información para ser enviada
					f.close()

					tam = os.stat(solicitud).st_size
					data = 'HTTP/1.1 200 OK\r\n'
					data += 'Content-Type: ' + str(tipo) + '\r\n'
					data += 'Content-Length: ' + str(tam) + '\r\n'
				except FileNotFoundError: 
					f = open('error_404.html', 'rb') 
					bytes_f = f.read() 
					f.close()
					data = 'HTTP/1.1 404 Not Found\r\n'

				print()
				print(data)
				
				final_data = data.encode()
				final_data += bytes_f		
				s.sendall(final_data)
				entrantes.remove(s)
				s.close()

			else: 
				print('Ya no hay conexión con:',s.getpeername())
				entrantes.remove(s) #En caso de perderse la conexión con algún cliente se le expulsa de la lista
				s.close() #Y se cierra su socket asociado
#except KeyboardInterrupt:
	#ServSock.close() 
	#print('Cerrado')
	#for s in ready_to_read: #Se cierran todas las conexiones en caso de cerrar el servidor
		#if s != ServSock:
			#entrantes.remove(s)
			#s.close()         

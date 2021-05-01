#!/usr/bin/env python3
# -*- coding: cp1252 -*-

import sys
import socket
import select
import re #expresiones regulares
import os
import signal
import time

# Manejador de la señal SIGALARM
def timer(signum, stack):
	print('Servidor web inactivo')

if len(sys.argv) != 2:
	print('Usage:', sys.argv[0], '<Modo> <Server Port>\n')

mode = int(sys.argv[1])

if mode == 1:
	print('Modo persistente\n')
elif mode == 0:
	print('Modo no persistente\n')
else:
	print('Valor introducido inválido:\r')
	print('Modo persistente = 1\r')
	print('Modo no persistente = 0\n')
	exit(1)

ServPort = sys.argv[2]

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

# Establecemos un manejador para la señal SIGALRM. La función que maneja la señal es timer
signal.signal(signal.SIGALRM, timer)

# Cuando pasen 10 segundos se solicita que SIGALARM envié una señal a su manejador
signal.alarm(10) # Inicializamos la alarma aquí, ya que el servidor web puede estar corriendo pero no recibir ninguna petición 
#try:
while entrantes:
	ready_to_read, ready_to_write, error = select.select(entrantes, salientes, entrantes)
	#if ready_to_read == []:
		#print('Servidor web inactivo\n')
	for s in ready_to_read:
		if s is ServSock: #Si s es el socket del servidor aceptamos las conexiones de los clientes que entran al chat
			connection, clntAddr = ServSock.accept()
			print( 'Conexión con:', clntAddr)
			print()
			entrantes.append(connection) # Añadimos a la lista de entrantes el nuevo cliente
		else:
			recvdata = s.recv(5000).decode()
			if recvdata:
				signal.alarm(0) #En caso de recibir datos (una petición) entendemos que el servidro ya no va a estar inactivo (tiene trabajo que hacer) -> quitamos la alarma para que no siga corriendo desde donde se ha quedado
				print(recvdata)
				pieces = recvdata.split()

				metodo = pieces[0]
				solicitud = pieces[1]
				version = pieces[2]

				print()
				print('Solicitud de ',s.getpeername())
				#print('Solicitud:', solicitud)

				solicitud = solicitud.lstrip('/') #Elimina el / inicial

				#if 'GET' in recvdata:
				if metodo=='GET':
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
					if 'application/json' in recvdata:
						tipo = 'application/json'

					try: #Por tanto, intentamos abrirlo y enviar su infromación contenida
						f = open(solicitud, 'rb') 
						bytes_f = f.read() #.encode() #Leemos el archivo y codificamos su información para ser enviada
						f.close()

						tam = os.stat(solicitud).st_size
						data =  version + ' 200 OK\r\n'
						data += 'Content-type: ' + str(tipo) + '\r\n'
						data += 'Content-length: ' + str(tam) + '\r\n' #Importante la longitud ya que el navegador debe saber cuando has acabado de mandar información, sino no se podrá implementar el modo persistente	
						data += '\r\n'
				
					except FileNotFoundError: 
						f = open('error_404.html', 'rb') 
						bytes_f = f.read() 
						f.close()

						tam = os.stat('error_404.html').st_size
						data = version + ' 404 Not Found\r\n'
						data += 'Content-type: text/html\r\n'
						data += 'Content-length: ' + str(tam) + '\r\n'
						data += '\r\n'

					print()
					print(data)
				
					final_data = data.encode()
					final_data += bytes_f		
					s.sendall(final_data)
				
				if 'POST' in recvdata:
					if '.php' in recvdata:
						#tipo = 'application/x-www-form-urlencoded'
						tipo = 'text/html'
						if re.findall('[.]php$', solicitud): 
							print('Solicitud:', solicitud)

					try: #Por tanto, intentamos abrirlo y enviar su infromación contenida
						f = open(solicitud, 'rb') 
						bytes_f = f.read() #.encode() #Leemos el archivo y codificamos su información para ser enviada
						f.close()

						tam = os.stat(solicitud).st_size
						data =  version + ' 200 OK\r\n'
						data += 'Content-type: ' + str(tipo) + '; charset=UTF-8\r\n'
						data += 'Content-length: ' + str(tam) + '\r\n' #Importante la longitud ya que el navegador debe saber cuando has acabado de mandar información, sino no se podrá implementar el modo persistente	
						data += '\r\n'
				
					except FileNotFoundError: 
						f = open('error_404.html', 'rb') 
						bytes_f = f.read() 
						f.close()

						tam = os.stat('error_404.html').st_size
						data = version + ' 404 Not Found\r\n'
						data += 'Content-type: text/html\r\n'
						data += 'Content-length: ' + str(tam) + '\r\n'
						data += '\r\n'

					print()
					print(data)
				
					final_data = data.encode()
					final_data += bytes_f		
					s.sendall(final_data)


				if(version == 'HTTP/1.0'): #Cambiar a if TRUE or FALSE
					print('Modo no persistente, cierro conexión\n')
					entrantes.remove(s)
					s.close()
				signal.alarm(10) #Una vez terminao su trabajo volvemos a establecer la alarma a 10 segundos (la reiniciamos ya que antes la pusimos a 0)
			else: 
				if s != ServSock:
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

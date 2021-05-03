#!/usr/bin/env python3
# -*- coding: cp1252 -*-

import sys
import socket
import select
import re #expresiones regulares
import os
import signal
import time
import requests
import pathlib

# Manejador de la señal SIGALARM
def timer(signum, stack):
	print('Servidor web inactivo')

def functipo(recvdata, solicitud):
	if 'text/html' in recvdata:
		tipo = 'text/html'
		if re.findall('[.]html$', solicitud): 
			print('Solicitud:', solicitud)
			return tipo
		if re.findall('[.]txt$', solicitud):
			print('Solicitud', solicitud)
			return tipo
		else:
			solicitud += '.html'
			print('SolicitudB:', solicitud)
			return tipo

#def remove_suffix(input_string, suffix):
	#if suffix and input_string.endswith(

if len(sys.argv) != 3:
	print('Usage:', sys.argv[0], '<Modo> <Server Port>\n')
	exit(1)

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
				#print(pieces[3])
				#print('Solicitud:', solicitud)

				solicitud = solicitud.lstrip('/') #Elimina el / inicial

				#if 'GET' in recvdata:
				if metodo=='GET':
					if(solicitud == ''):
						solicitud = 'index.html' #archivo index.html como default
					#tipo = functipo(recvdata, solicitud)
					
					if re.findall('[.]txt$', solicitud):
						tipo = 'plain/text'
						print('Solicitud', solicitud)
					else:
						tipo = 'text/html'
						if re.findall('[.]html$', solicitud): 
							print('Solicitud:', solicitud)
						else:
							solicitud += '.html'
							print('SolicitudB:', solicitud)
				
					if '.jpg' in recvdata:
						tipo = 'image/jpg'
						print('Solicitud:', solicitud)
					#elif 'image/webp' in recvdata:
						#tipo = 'image/webp'
					if 'application/json' in recvdata:
						tipo = 'application/json'
					
					if '.txt' in recvdata:
						tipo = 'text/plain'
						if re.findall('[.]html$', solicitud):
							#solicitud = pathlib.Path(solicitud).with_suffix('.html')
							print('Solicitud:', solicitud)


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
					if 'application/x-www-form-urlencoded' in recvdata:
						tipo = 'text/html'
						if re.findall('[.]html$', solicitud): 
							print('Solicitud:', solicitud)
						#else:
							#solicitud += '.html'
							#print('Solicitud:', solicitud)

					if '.php' in recvdata:
						#tipo = 'application/x-www-form-urlencoded'
						tipo = 'text/html'
						if re.findall('[.]php$', solicitud): 
							print('Solicitud:', solicitud)

					#if '.txt' in recvdata:
						#tipo = 'text/plain'
						#if re.findall('[.]html$', solicitud):
							#solicitud = solicitud.lstrip('.html')
							#print('Solicitud:', solicitud)

					datapost = 'Datos: '
					for i in range (0, len(pieces)):
						if i == (len(pieces) - 1):
							print('Datos POST:' + str(pieces[i]) + '\n')
							postdata = str(pieces[i])
							postdata = postdata.split('&')
							#print('Separado &:', postdata)
							for i in range (0, len(postdata)):
								datapost += postdata[i] + '\n'

					try:
						f = open('datos.txt', 'w')
						f.write(datapost)
					except IOError:
						print('Fichero no accesible\n')
					finally:
						f.close()

					try: #Por tanto, intentamos abrirlo y enviar su infromación contenida
						f = open(solicitud, 'rb') 
						bytes_f = f.read() #.encode() #Leemos el archivo y codificamos su información para ser enviada
						f.close()
						
						tam = os.stat(solicitud).st_size
						#tam = 5000
						#response = '<html><body><center><h3>Datos del formulario</h3><p> {} </p></center></body></html>'.format(datapost).encode()
						#response = datapost.encode()
						#tam += os.stat(response).st_size
						data =  version + ' 200 OK\r\n'
						#data = version + ' 307 Temporary Redirect\r\n'
						#data += 'Location: welcome.php\r\n'
						#data += 'Content-encodig: gzip\r\n'
						data += 'Content-type: ' + str(tipo) + '; charset=UTF-8\r\n'
						#data += 'Content-type: ' + str(tipo) + '\r\n'

						data += 'Content-length: ' + str(tam) + '\r\n' #Importante la longitud ya que el navegador debe saber cuando has acabado de mandar información, sino no se podrá implementar el modo persistente	
						#data += 'vary: Accept-Encoding\r\n'
						data += '\r\n'
				
					except FileNotFoundError: 
						f = open('error_404.html', 'rb') 
						bytes_f = f.read() 
						f.close()
						
						print('Solicitud:', solicitud)

						tam = os.stat('error_404.html').st_size
						data = version + ' 404 Not Found\r\n'
						data += 'Content-type: text/html\r\n'
						data += 'Content-length: ' + str(tam) + '\r\n'
						data += '\r\n'

					print()
					print(data)

					final_data = data.encode()
					#final_data += '<html><body>Welcome <?php echo $_POST["name"]; ?><br>Your email address is: <?php echo $_POST["email"]; ?></body></html>'.encode()
					#final_data += postdata.encode()
					#final_data += response
					final_data += bytes_f	
					#userdata = {"name":"pepe","email":"oliet"}
					#resp = requests.post('http://localhost/8082/welcome.php', data = userdata)
					#print(resp.text)
					s.sendall(final_data)


				if(mode == 0): #Cambiar a if TRUE or FALSE
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

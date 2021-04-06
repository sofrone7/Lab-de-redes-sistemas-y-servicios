#!/usr/bin/env python3
# -*- coding: cp1252 -*-

import sys
import socket
import select
import re #expresiones regulares

if len(sys.argv) < 2 or len(sys.argv) > 3:
  print('Usage:', sys.argv[0], '<Server IP> [<PING Port>]')

#Definición de variables
servIP = sys.argv[1]
pingServPort = sys.argv[2]

#Crear socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conexión
sock.connect((servIP, int(pingServPort)))

#En el caso de los clientes, la lista estará formada solo por el socket conectado con el servidor (para recibir los mensajes que nos reenvía) y sys.stdin (para leer nuestro teclado)
lectura = [sock, sys.stdin]

try:
  while lectura:
    read, write, error = select.select(lectura, [], [])
    for s in read:
      if s is sock: #Si es el socket conectado al servidor el que está listo
        datos = sock.recv(1024) #Recibimos el mensaje reenviado por el servidor
        if datos:
          print('\n< ',datos.decode("utf-8")) #Decodificamos la información
          try:
            f = open('recv.txt', 'w') 
            f.write(datos.decode("utf-8")) #Almacenamos los mensajes en un archivo de texto
          except IOError:
            print('El fichero no es accesible')
          finally:
            f.close()
        if not datos:
          sock.close() #En caso de que se pierda la conexión con el servidor
          print('Conexión cerrada')
          break
      if s is sys.stdin: #Si s es sys.stdin leemos de teclado
        mensaje = input('> ')
        if re.findall('[.]txt$', mensaje): #Enc aso de que el mensaje escrito termine en ".txt", identificamos que se trata de un archivo de texto
          try: #Por tanto, intentamos abrirlo y enviar su infromación contenida
            f = open(mensaje, 'r') 
            bytes_f = f.read().encode() #Leemos el archivo y codificamos su información para ser enviada
            sock.sendall(bytes_f)
          except IOError:
            print('El fichero no es accesible')
            sock.sendall(bytes(mensaje, 'utf-8')) #En caso de que no se trate de un archivo de texto como tal, enviamos el nombre del archivo que hemos tratado de abrir
          finally:
            f.close()
        else:
          sock.sendall(bytes(mensaje, 'utf-8')) #El mensaje debe ir codificado
except KeyboardInterrupt:
  sock.close()
  
  
  

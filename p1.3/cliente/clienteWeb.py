#!/usr/bin/env python3
# -*- coding: cp1252 -*-

import sys
import socket
import select
import re #expresiones regulares

if len(sys.argv) != 2:
  print('Usage:', sys.argv[0], '<Server IP> ')

#Definición de variables
servIP = sys.argv[1]
ServPort = 5000

#Crear socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conexión
sock.connect((servIP, int(ServPort)))

lectura = [sock, sys.stdin]

try:
  while lectura:
    read, write, error = select.select(lectura, [], [])
    for s in read:
      if s is sock: #Si es el socket conectado al servidor el que está listo
        data = sock.recv(512)
        if data:
          if len(data) < 1:
            break
          print(data.decode(),end='')
        if not data:
          sock.close() #En caso de que se pierda la conexión con el servidor
          print('Conexión cerrada')
          break
      if s is sys.stdin: #Si s es sys.stdin leemos de teclado
        mensaje = input('> ')
        cmd = 'GET http://127.0.0.1/' + mensaje + ' HTPP/1.0\r\n\r\n'
        cmd = cmd.encode()
        #sock.sendall(bytes(mensaje, 'utf-8')) #El mensaje debe ir codificado
        sock.send(cmd)
except KeyboardInterrupt:
  sock.close()

#cmd = 'GET http://127.0.0.1/index.html HTPP/1.0\r\n\r\n'.encode()
#sock.send(cmd)

#while True:
  #data = sock.recv(512)
  #if len(data) < 1:
    #break
  #print(data.decode(),end='')
  
#sock.close()
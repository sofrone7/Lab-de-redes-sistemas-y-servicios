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

lectura = [sock, sys.stdin]

try:
  while lectura:
    read, write, error = select.select(lectura, [], [])
    for s in read:
      if s is sock:
        datos = sock.recv(1024)
        if datos:
          print('\n< ',datos.decode("utf-8"))
        if not datos:
          sock.close()
          print('Conexión cerrada')
      if s is sys.stdin:
        mensaje = input('> ')
        if re.findall('[.]txt$', mensaje):
          print('ok')
          try:
            f = open(mensaje, 'r')
            bytes_f = f.read().encode()
            sock.sendall(bytes_f)
          except IOError:
            print('El fichero no es accesible')
            sock.sendall(bytes(mensaje, 'utf-8'))
          finally:
            f.close()
        else:
          sock.sendall(bytes(mensaje, 'utf-8')) # El mensaje debe ir codificado
except KeyboardInterrupt:
  sock.close()
  
  
  #for s in socks:
    #datos = sock.recv(1024)
    #print(datos.decode("utf-8"))
    #if not datos:
      #sock.close()
  #if datos:
    #print(datos.decode("utf-8"))
  #else:
    #if not datos:
      #mensaje = input('Chat: ')
      #print('Mensaje:', mensaje)
      #sock.sendall(bytes(mensaje, 'utf-8')) # El mensaje debe ir codificado

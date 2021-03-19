#!/usr/bin/env python3
# -*- coding: cp1252 -*-

import sys
import socket
import select

if len(sys.argv) < 2 or len(sys.argv) > 3:
  print('Usage:', sys.argv[0], '<Server IP> [<PING Port>]')

#Definición de variables
servIP = sys.argv[1]
pingServPort = sys.argv[2]

#Crear socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conexión
sock.connect((servIP, int(pingServPort)))

while True:
  try:
    mensaje = input('Chat: ')
    print('Mensaje:', bytes(mensaje, 'utf-8'))
    sock.sendall(bytes(mensaje, 'utf-8')) 
  except sock.recv(1024):
    datos = sock.recv(1024)
    print(datos.decode("utf-8"))
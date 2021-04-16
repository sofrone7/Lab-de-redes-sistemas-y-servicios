#!/usr/bin/env python3
# -*- coding: cp1252 -*-

import sys
import socket
import select
import re #expresiones regulares

if len(sys.argv) != 1:
  print('Usage:', sys.argv[0], '<Server IP> ')

#Definición de variables
servIP = sys.argv[1]
ServPort = 5000

#Crear socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conexión
sock.connect((servIP, int(ServPort)))

cmd = 'GET http://127.0.0.1/index.html HTPP/1.0\r\n\r\n'.encode()
sock.send(cmd)

while True:
  data = sock.recv(512)
  if len(data) < 1:
    break
  print(data.decode(),end='')
  
sock.close()
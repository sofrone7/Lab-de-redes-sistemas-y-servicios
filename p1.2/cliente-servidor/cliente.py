#!/usr/bin/env python3
# -*- coding: cp1252 -*-

import sys
import socket
import select
#import threading
from threading import Thread # Para no tener que poner threading.Thread
#import shlex

def escucha():
  while True:
    datos = sock.recv(1024)
    if datos:
      print('\n< ',datos.decode("utf-8"))
    if not datos:
      sock.close()
      print('Conexión cerrada')
      
#def salida():
  #while True:
    #mensaje = input('> ')
    #mensaje += '\n'
    #print('Mensaje:', mensaje)
    #sock.sendall(bytes(mensaje, 'utf-8')) # El mensaje debe ir codificado

if len(sys.argv) < 2 or len(sys.argv) > 3:
  print('Usage:', sys.argv[0], '<Server IP> [<PING Port>]')

#Definición de variables
servIP = sys.argv[1]
pingServPort = sys.argv[2]

#Crear socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conexión
sock.connect((servIP, int(pingServPort)))

#socks = [sock]

#back = Thread(target=salida)
job = Thread(target=escucha)

job.start()
#back.start()
try:
  while True:
    mensaje = input('> ')
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

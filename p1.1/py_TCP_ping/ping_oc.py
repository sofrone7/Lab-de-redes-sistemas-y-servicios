#!/usr/bin/env python3

import sys
import socket

if len(sys.argv) < 2 or len(sys.argv) > 3:
  print('Usage:', sys.argv[0], '<Server IP> [<PING Port>]')

#Definición de variables
servIP = sys.argv[1]
pingString = "s"
pingServPort = sys.argv[2]

#Crear socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conexión
sock.connect((servIP, int(pingServPort)))

sock.close()
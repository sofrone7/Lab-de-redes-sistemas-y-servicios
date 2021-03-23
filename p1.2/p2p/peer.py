#!/usr/bin/env python3

import sys
import socket
import pickle

if len(sys.argv) != 3:
	print('Usage: {} <Server IP> [<PING PORT>]', sys.argv[0])

servIP = sys.argv[1]
ServPort = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((servIP, int(ServPort)))

while True:
	datos = sock.recv(1024)
	datos = pickle.loads(datos)
	print(datos)

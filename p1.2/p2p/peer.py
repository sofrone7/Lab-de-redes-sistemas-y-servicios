#!/usr/bin/env python3

import sys
import socket
import pickle
import select
import re

if len(sys.argv) != 3:
	print('Usage: {} <Server IP> [<PING PORT>]', sys.argv[0])

servIP = sys.argv[1]
ServPort = sys.argv[2]

ServSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServSock.connect((servIP, int(ServPort))) #Primero nos conectaremos con el servidor, este, constatará que estamos conectados y le pasaremos el puerto de escucha

#Socket de escucha
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setblocking(0) #El socket de escucha se establece en no bloqueo
sock.bind(('', 0)) #Escuchamos en un puerto aleatorio
sock.listen(10)

print('Puerto de escucha: ', sock.getsockname()[1])
port = sock.getsockname()[1]
ServSock.sendall(pickle.dumps(port)) #Mandamos al servidor el puerto de escucha
#sock.sendall(bytes(mensaje, 'utf-8'))

lectura = [sock, sys.stdin] #Lista con el socket de escucha, sys.stdin y posteriormente los peers con los que nos vayamos conectando
datos = ServSock.recv(1024) #Recibimos del servidor una lista de duplas (dirrección IP, puerto) de los peers disponibles
if datos:
  lista = pickle.loads(datos) #Deserializamos el flujo de datos
  #print(lista)
  if lista: #Si la lista no está vacía
    for x in lista: #Nos conectamos con todos los peers disponibles
      print('Conectamos con:', x)
      #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.connect(x)
        #lectura.append(s)
        #print('Socket de', x, 'es:', s)
        #print()
      soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      soc.connect(x)
      lectura.append(soc) #Añadimos la conexión a la lista lectura
print('Lista:')
for p in lectura:
  if p != sys.stdin:
    #conn = sock.getpeername()
    #print(conn)
    print(p)
print()

#direcciones = []

try:
  while lectura:
    read, write, error = select.select(lectura, [], [])
    for s in read:
      if s is sock: #Si s es el socket de escucha aceptamos las nuevas conexiones
        connection, clntAddr = sock.accept()
        print('Conexión con peer:', clntAddr)
        lectura.append(connection) #Añadimos la nueva conexión a la lista lectura
        for x in lectura:
          if x != sys.stdin:
            #print(x.getpeername())
            #print(x)
            #conn = sock.getpeername()
            #print(conn)
            print(x)
        print()
      if s is sys.stdin: #Si s es sys.stdin leemos de teclado
        mensaje = input('> ')
        if mensaje:
          for peer in lectura: #Mandamos el mensaje a todos los usuarios conectados al chat con nosotros
            if peer != sock and peer != sys.stdin:
              peer.sendall(bytes(mensaje, 'utf-8')) 
              #sockconn.sendall(bytes(mensaje, 'utf-8')) 
      #if s is sock:
      if s != sock and s != sys.stdin: #El resto de sockets correspondientes a las conexiones con los demás usuarios reciben los mensajes y los muestran por pantalla. Entiendo que el primero en conectarse no va a pasar por el primer if y sock se comprobará aquí en tal caso
        datos = s.recv(1024)
        if datos:
          print('\n< ',datos.decode("utf-8"))
        if not datos:
          print('Cerrando conexión con:', s)
          lectura.remove(s) #En caso de desconexión se debe expulsar de la lista el socket correspondiente
          s.close() #Cierre del socket
      else:
        if s != sys.stdin and s != sock:
          print(s)
          try:	
            conn = sock.getpeername() #Obtenemos la dirreción de cada conexión
    				#print(conn)
            s.connect(conn) #Comprobamos que siga conectado
          except:
            print('Ya no hay conexión con: ', s.getpeername())
            lectura.remove(s)
            s.close()

except KeyboardInterrupt:
  sock.close()
  ServSock.close()

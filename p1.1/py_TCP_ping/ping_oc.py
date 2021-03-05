#!/usr/bin/env python3

import sys
import socket
import time

clk_id1 = time.CLOCK_REALTIME # System-wide real-time clock

if len(sys.argv) < 2 or len(sys.argv) > 3:
  print('Usage:', sys.argv[0], '<Server IP> [<PING Port>]')

#Definición de variables
servIP = sys.argv[1]
pingServPort = sys.argv[2]

#Crear socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conexión
sock.connect((servIP, int(pingServPort)))

print('PING',servIP)
seq = 0

try:
  while True:
    seq += 1
    pingString = b"mensaje" #convertido a bytes
    #time_send = time.clock_gettime_ns(clk_id1) #tiempo envío ping en ns
    #time_send = float(round(time.time() * 1000.0))
    time_send = time.time() #tiempo envío ping en seg
    sock.send(pingString);
      
    totalBytesRcvd = 0;
    pingStringLen = len(pingString) # len = 7
    bytesRcvd = 0
      
    if sock.recv(16): #comprobamos que sólo si recibimos respuesta de vuelta
      #time_recv = time.clock_gettime_ns(clk_id1)
      #time_recv = float(round(time.time() * 1000.0))
      time_recv = time.time()
      tiempo = (time_recv - time_send) * 1000
      print("{} bytes from {}: icmp_ser={} ttl= time={:.3f} ms".format(pingStringLen, servIP, seq, tiempo))
      #print resultado.format(pingStringLen, servIP, seq, tiempo)
      #print(pingStringLen, 'bytes from', servIP, 'icmp_seq=', seq, 'ttl= ' 'time={:.2f}', tiempo, 'ms')
    
    time.sleep(1)
except KeyboardInterrupt:
  print('stop')
finally:
  print('close socket')
  sock.close()
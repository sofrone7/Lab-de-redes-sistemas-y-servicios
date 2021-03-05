#!/usr/bin/env python3

import sys
import socket
import time
import math

def desvEstandar(array, avg, seq):
  var = 0 
  resultado = 0
  for i in range(len(array)):
    var += pow((array[i] - avg) ,2)
  var = var/seq
  resultado = math.sqrt(var)
  #print('resultado', resultado)
  return resultado

clk_id1 = time.CLOCK_REALTIME # System-wide real-time clock
ttl = 64
recv = 0 #variable que contendrá el nº de pings recibidos
array = []
time_total = 0
time_min = 0
time_max = 0

if len(sys.argv) < 2 or len(sys.argv) > 3:
  print('Usage:', sys.argv[0], '<Server IP> [<PING Port>]')

#Definición de variables
servIP = sys.argv[1]
pingServPort = sys.argv[2]

#Crear socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Set ttl
sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

#Conexión
sock.connect((servIP, int(pingServPort)))

print('PING',servIP)
seq = 0

try:
  while True:
    seq += 1
    pingString = b"mensaje" #convertido a bytes
    time_send = time.time() #tiempo envío ping en seg
    sock.send(pingString);
      
    totalBytesRcvd = 0;
    pingStringLen = len(pingString) # len = 7
    bytesRcvd = 0
      
    if sock.recv(16): #comprobamos sólo si recibimos respuesta de vuelta
      recv += 1
      time_recv = time.time()
      tiempo = (time_recv - time_send) * 1000
      print("{} bytes from {}: icmp_ser={} ttl={} time={:.3f} ms".format(pingStringLen, servIP, seq, ttl, tiempo))
      time_total += tiempo
      array.append(tiempo) #fill array with the time data
      #for i in range(len(array)):
        #print( array[i])
      if time_min == 0 or tiempo < time_min:
        time_min = tiempo
      
      if time_max == 0 or tiempo > time_max:
        time_max = tiempo
        
      avg = time_total/seq
        
    else:
      recv -= 1
    
    time.sleep(1)
except KeyboardInterrupt:
  mdev = desvEstandar(array, avg, seq)
  #print('mdev', mdev)
  print()
  print("--- {} ping statistics ---".format(servIP))
finally:
  print('{} packets transmitted, {} received, {}% packet loss, time {:.3f} ms'.format(seq, recv, ((seq - recv)/seq) * 100.0, time_total))
  print('rtt min/avg/max/mdev = {:.3f}/{:.3f}/{:.3f}/{:.3f} ms'.format(time_min, avg, time_max, mdev))
  sock.close()
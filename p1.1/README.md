# Lab-de-redes-sistemas-y-servicios

Desarrollar diferentes programas que permitan emular el comando ping, empleando tanto el protocolo de transporte TCP como UDP.
Emplear el lenguaje C así como el lenguaje Python3, tanto en modo no orientado a conexión (NOC) como orientado a conexión (OC).
Es decir, el resultado de la práctica será una herramienta ping que funcione en el modo NOC y otra que funcione en el modo OC.

El nombre de los ficheros fuente que debe emplear son los siguientes:
  - Herramienta ping NOC:
    - ping_noc.c y ping_noc.py: para el cliente ping en modo NOC.
    - ping_noc_serv.c y ping_noc_serv.c: para el servidor ping en modo NOC.
  - Herramienta ping OC:
    - ping_oc.c y ping_oc.py: para el cliente ping en modo OC.
    - ping_oc_serv.c y ping_oc_serv.py: para el servidor ping en modo OC.
    
Los parámetros de entrada para la ejecución serán los siguientes:
  - Los clientes ping aceptan como parámetros de entrada (de manera obligatoria) el nombre de host o dirección IP del servidor de ping
    junto con el puerto donde este servidor se encuentra escuchando.
    Ejemplos posibles de dicha invocación serán, por tanto: “ping localhost 10000” o “ping 127.0.0.1 10000”.
  - Los servidores aceptan como parámetro de entrada únicamente el puerto de escucha
  

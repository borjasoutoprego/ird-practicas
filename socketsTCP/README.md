## Sockets TCP en Python

Cuando trabajamos en una red de ordenadores y queremos establecer una
comunicación (enviar o recibir datos) entre dos procesos que se están ejecutando
en máquinas diferentes de dicha red necesitamos hacer uso de los Sockets para
abstraer las conexiones.
Para diferenciar estas conexiones se les asigna un número de 16 bits (entre
0 y 65535) conocido como puerto. Por tanto para dirigir de manera unívoca la
información entre dos procesos en diferentes máquinas hemos de hacer uso de
la dirección IP y el puerto asignado en cada máquina, así como del protocolo
empleado.
Según el papel que cumplan los programas podremos hablar de cliente o
servidor, siendo el primero el que inicia una petición y recibe la respuesta y el
segundo el que se encuentra a la espera de recibir una conexi´on para generar
una respuesta.

- Ejercicio 1: 'Cliente TCP'

- Ejercicio 2: 'Servidor TCP'

- Ejercicio 3: 'Servidor TCP multihilo'

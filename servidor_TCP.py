import sys
import socket


def main():
    socket_servidor = None
    timeout = 300

    if len(sys.argv) != 2:
        print('Formato ServidorUDP <puerto>')
        sys.exit()
    try:
        # Instrucciones sockets
        # Leemos los argumentos necesarios
        puerto = int(sys.argv[1])
        # Creamos el socket orientado a conexion
        socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Asociamos el socket a cualquier direccion local en el puerto indicado
        socket_servidor.bind(('', puerto))
        # Establecemos un timeout de 300 segs
        socket_servidor.settimeout(timeout)

        # Ponemos el servidor en modo escucha mediante el metodo listen()
        socket_servidor.listen()
        print('Servidor en espera de conexiones')

        # Invocamos el metodo accept que queda esperando hasta recibir la peticion de conexion de un cliente

        while True:
            # connection, client_address = sock.accept()
            connection, client_address = socket_servidor.accept()
            print('connection from ', client_address)

            # Recibimos el mensaje
            data = connection.recv(4096)
            # Mostramos el contenido del mensaje
            print("Recibido mensaje: {} de: {}:{}".format(data.decode('UTF-8'),data[0],data[1]))
            # Enviamos el mensaje
            connection.sendto(data, client_address)
            # Cerramos el socket del cliente
            connection.close()

    except socket.timeout:
        # Captura excepcion si el tiempo de espera se agota.
        print("{} segundos sin recibir nada.".format(timeout))

    except Exception:
        # Captura excepcion generica.
        print("Error: {}".format(sys.exc_info()[0]))
        raise

    finally:
        # Cerramos el socket del servidor al final de la ejecucion
        if socket_servidor is not None:
            socket_servidor.close()
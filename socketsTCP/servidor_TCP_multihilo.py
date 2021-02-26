import sys
import socket
import threading

def main():
    # Comprobación argumentos
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

        # Establecemos un timeout de 300 segundos
        socket_servidor.settimeout(timeout)

        # Ponemos el servidor en modo escucha mediante el metodo listen()
        socket_servidor.listen()
        print('Servidor en espera de conexiones.')

        while True:
            try:
                # Invocamos el metodo accept que queda esperando hasta recibir la peticion de conexion de un cliente
                socket_cliente, address_info = socket_servidor.accept()
                threading.Thread(target=reply_client, args=[socket_cliente, address_info]).start()
            except socket.timeout:
                # Captura excepcion si el tiempo de espera se agota
                print(f'Timeout exception, {timeout} went by without receiving connections.')
                break
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if socket_servidor is not None:
            socket_servidor.close()


def reply_client(client, address_info):
    print(f'Conexión establecida con {address_info[0]}:{address_info[1]}')
    # Recibimos el mensaje
    msg = client.recv(4096)
    print(f'Mensaje recibido: {msg}')
    # Devuelve el mensaje al socket
    client.send(msg)
    # Cierra la conexion con el cliente y vuelve, para esperar por otra
    client.close()


if __name__ == '__main__':
    main()

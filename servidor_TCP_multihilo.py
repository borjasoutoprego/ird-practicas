import sys
import socket
import threading

DEFAULT_TIMEOUT = 200


def main():
    # comprobación argumentos
    if len(sys.argv) != 2:
        print('Formato ServidorUDP <puerto>')
        sys.exit()

    # assign port
    puerto = int(sys.argv[1])

    socket_server = None  # None
    try:
        # create socket instance
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # defines listen address
        listen_address = ('', puerto)

        # assigns listen_address to the created socket
        socket_server.bind(listen_address)

        # sets the default timeout for the accept method wait
        socket_server.settimeout(DEFAULT_TIMEOUT)

        # tells the socket to start listening
        socket_server.listen()
        print('Socket esperando conexiones.')
[21:41]
        while True:
            try:
                # accept waits for an incoming connection, and if none came in DEFAULT_TIMEOUT seconds,
                # raise socket.timeout occur
                # if connection established, returns a new socket (tube) and the addres info -> (ip, port)
                socket_cliente, address_info = socket_server.accept()
                threading.Thread(target=reply_client, args=[socket_cliente, address_info]).start()
            except socket.timeout:
                # if timeout occur, this happens
                print(f'Timeout exception, {DEFAULT_TIMEOUT} went by without receiving connections.')
                break
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        if socket_server is not None:
            socket_server.close()


def reply_client(client, address_info):
    print(f'Conexión establecida con {address_info[0]}:{address_info[1]}')
    buffer_size = 4096
    # read buffer_size bytes from the socket
    msg = client.recv(buffer_size)
    print(f'Mensaje recibido: {msg}')
    # send back to the socket the msg
    client.send(msg)
    # close the connection with the client and go up, to wait for another
    client.close()


if __name__ == '__main__':
    main()

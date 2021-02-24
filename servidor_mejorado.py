import sys
import socket

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

        while True:
            try:
                # accept waits for an incoming connection, and if none came in DEFAULT_TIMEOUT seconds,
                # raise socket.timeout occur
                # if connection established, returns a new socket (tube) and the addres info -> (ip, port)
                socket_cliente, address_info = socket_server.accept()
                print(f'Conexión establecida con {address_info[0]}:{address_info[1]}')
                
                buffer_size = 4096
                # read buffer_size bytes from the socket
                msg = socket_cliente.recv(buffer_size) 
                print(f'Mensaje recibido: {msg}') 
                
                # send back to the socket the msg
                socket_cliente.send(msg)
                
                # close the connection with the client and go up, to wait for another
                socket_cliente.close()
            except socket.timeout:
                # if timeout occur, this happens
                print(f'Timeout exception, {DEFAULT_TIMEOUT} went by without receiving connections.')
                break
                
    except Exception:
        print('An unexpected error occurred.')
    finally:
        if socket_server is not None:
            socket_server.close()


if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 12:04:08 2021

@author: Administrador
"""

import sys
import socket
import threading
import datetime
import os

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
                print(f'{timeout} segundos sin recibir nada')
                break
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if socket_servidor is not None:
            socket_servidor.close()


def reply_client(client, address_info):
    print(f'Conexión establecida con {address_info[0]}:{address_info[1]}')
    
    request = recvall(client)
    request = request.split(b'\r\n')
    request = list(map(lambda line: line.decode('UTF-8'), request)) # decodificacion mensaje utf-8
    
    request_line = request[0]
    request_line = request_line.split(' ')
    if len(request_line) != 3:
        send_error(client, 400)
        return 
    
    metodo = request_line[0]   
    if metodo != 'GET' and metodo != 'HEAD':
        send_error(client, 400)
        return 
    
    url = request_line[1]
    protocolo = request_line[2]
    if url.endswith('jpg') or url.endswith('gif'):
        image = open('data' + url, 'rb') 
        image_read = image.read()
        answer = (b'HTTP/1.0 200 OK\r\n' + default_headers() + b'Content-Type: ' + content_type(url) + b'\r\nLast-Modified: ' + last_modified(url)
                  + b'\r\nContent-Length: ' + str(os.path.getsize('data' + url)).encode() + b'\r\n\r\n' + image_read)
        client.send(answer)
    
    else:     
        try:
            if url == '/':
                url = '/index.html'
            f = open('data' + url, "r", encoding = 'utf-8')
            content = f.read()
            f.close()
            answer = (b'HTTP/1.0 200 OK\r\n' + default_headers() + b'Content-Type: ' + content_type(url) + b'\r\nLast-Modified: ' + last_modified(url)
                      + b'\r\nContent-Length: ' + str(os.path.getsize('data' + url)).encode() + b'\r\n\r\n')
            if metodo == 'GET':
                answer += content.encode('UTF-8')
            client.send(answer)
        except IOError:
            send_error(client, 404)
            return
            
    client.close()

def content_type(url):
    if url.endswith('txt'):
        return b'text/plain'
    elif url.endswith('html'):
        return b'text/html'
    elif url.endswith('gif'):
        return b'image/gif'
    elif url.endswith('jpeg'):
        return b'image/jpeg'
    else: 
        return b'application/octet-stream'
     
def default_headers():
    server = b'MyServer/1.0'
    date = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z') # fecha y hora actuales
    date = date.encode()
    return b'Date:' + date + b'\r\nServer: ' + server + b'\r\n'
    
def send_error(client, error):
    if error == 400:
        client.send(b'HTTP/1.0 400 Bad Request\r\n' + default_headers() + b'Content-Type: text/html\r\nContent-Length: 21\r\n\r\nError 400 Bad-Request')
    
    elif error == 404:
        client.send(b'HTTP/1.0 404 Not Found\r\n' + default_headers() + b'Content-Type: text/html\r\nContent-Length: 19\r\n\r\nError 404 Not Found')
        
    client.close()
    
def last_modified(url):
    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime('data' + url)).strftime('%a, %d %b %Y %H:%M:%S %Z') # fecha de ultima modificacion de url
    return last_modified.encode()

def recvall(sock):
    BUFF_SIZE = 4096 
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data

if __name__ == '__main__':
    main()

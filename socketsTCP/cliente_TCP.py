"""

@author: Borja Souto Prego
"""
import sys
import socket

def main():
    if len(sys.argv) != 4:
        print("Formato ClienteUDP <maquina> <puerto> <mensaje>")
        sys.exit()

    try:
        # Instrucciones sockets
        maquina = sys.argv[1]
        puerto = int(sys.argv[2])
        mensaje = sys.argv[3]

        # Creamos el socket orientado a conexion
        socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Establecemos un timeout de 300 segs
        timeout = 300
        socketCliente.settimeout(timeout)
        print("CLIENTE: Enviando {} a {}:{}".format(mensaje, maquina, puerto))
        
        #Conectamos el socket con el servidor mediante la función connect
        socketCliente.connect((maquina, puerto))
        
        # Enviamos el mensaje a la maquina y puerto indicados
        socketCliente.sendto(mensaje.encode('UTF-8'), (maquina, puerto))
        
        # Recibimos el mensaje de respuesta
        mensajeEco, a = socketCliente.recvfrom(len(mensaje))
        
        #Mostramos el mensaje recibido
        print("CLIENTE: Recibido {} de {}:{}".format(mensajeEco.decode('UTF-8'),maquina,puerto))
    
    except socket.timeout:
    # Captura excepcion si el tiempo de espera se agota
        print("{} segundos sin recibir nada.".format(timeout))
    except:
    # Captura excepcion generica
        print("Error: {}".format(sys.exc_info()[0]))
        raise
    finally:
    # En cualquier caso cierra el socket al final de la ejecución
        socketCliente.close()
        
if __name__ == "__main__":
    main()
    
    

import socket
import select
import errno
import deteccionFiguras
import sys

HEADER_LENGTH = 40
IP = "localhost"
PORT = 50000
my_username = "colors"

# Crear un socket 
# socket.AF_INET - familia de direcciones, IPv4, algunos otros posibles son AF_INET6, AF_BLUETOOTH, AF_UNIX 
# socket.SOCK_STREAM - TCP, basado en conexión, socket.SOCK_DGRAM - UDP, sin conexión, datagramas, socket.SOCK_RAW - IP sin procesar paquetes 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conéctese a una determinada ip y puerto
client_socket.connect((IP, PORT))

# Establezca la conexión en un estado sin bloqueo, por lo que la llamada .recv () no se bloqueará, solo devuelva alguna excepción que manejaremos 
client_socket.setblocking(False)

# Prepare el nombre de usuario y el encabezado y envíelos 
# Necesitamos codificar el nombre de usuario en bytes, luego contar el número de bytes y preparar el encabezado de tamaño fijo, que también codificamos en bytes 
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
def start_connection():
    while True:
        try:
            # Ahora queremos recorrer los mensajes recibidos (puede haber más de uno) e imprimirlos mientras True :
            # Reciba nuestro "encabezado" que contiene la longitud del nombre de usuario, su tamaño está definido y es constante 
            username_header = client_socket.recv(HEADER_LENGTH)

            # Si no recibimos datos, el servidor cerró una conexión con gracia, por ejemplo, usando socket.close () o socket.shutdown (socket.SHUT_RDWR) si no len ( username_header ): print ( 'Conexión cerrada por el servidor' )
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convertir encabezado a valor int 
            username_length = int(username_header.decode('utf-8').strip())

            # Recibir y decodificar nombre de 
            username = client_socket.recv(username_length).decode('utf-8')

            # Ahora haga lo mismo para el mensaje (como recibimos el nombre de usuario, recibimos el mensaje completo, no hay necesidad de verificar si tiene alguna longitud) 
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Imprimir mensaje
            deteccionFiguras.start(message)
            
            print(f'{username} > {message}')
            #client_socket.close()


        except IOError as e:
            # Esto es normal en conexiones que no bloquean - cuando no hay error de datos entrantes va a aparecer 
            # Algunos sistemas operativos indicarán que usando AGAIN, y algunos usando el código de error WOULDBLOCK 
            # Vamos a verificar ambos - si uno de ellos, eso es lo esperado, significa que no hay datos entrantes, continúe como siempre 
            # Si obtuvimos un código de error diferente, algo sucedió
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()

        # Simplemente no recibimos nada
        continue


def refresh():
    # Espere a que el usuario ingrese un mensaje 
    message = input(f'{my_username} > ')

    # Si el mensaje no está vacío, envíelo si el mensaje :
    if message:

        # Codifique el mensaje en bytes, prepare el encabezado y convierta a bytes, como el nombre de usuario anterior, luego envíe 
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)


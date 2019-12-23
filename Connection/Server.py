import socket
import select

HEADER_LENGTH = 40

IP = "localhost"
PORT = 50000

# Crear un socket 
# socket.AF_INET - familia de direcciones, IPv4, algunos otros posibles son AF_INET6, AF_BLUETOOTH, AF_UNIX 
# socket.SOCK_STREAM - TCP, basado en conexión, socket.SOCK_DGRAM - UDP, sin conexión, datagramas, socket.SOCK_RAW - IP sin procesar paquetes 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_ - opción de socket 
# SOL_ - nivel de opción de socket 
# Establece REUSEADDR (como una opción de socket) en 1 en el socket 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Vinculación, de modo que el servidor informa al sistema operativo que va a usar una IP y un puerto dados . 
# Para un servidor que usa 0.0.0.0 significa escuchar en todas las interfaces disponibles, útil para conectarse localmente a 127.0.0.1 y remotamente a la interfaz LAN IP 
server_socket.bind((IP, PORT))

# Esto hace que el servidor escuche nuevas conexiones 
server_socket.listen()

# Lista de sockets para select.select () 
sockets_list = [server_socket]

# Lista de clientes conectados: socket como clave, encabezado de usuario y nombre como 
clients = {}

print(f'Listening for connections on {IP}: {PORT}...')

# Manijas de recepción de mensajes
def receive_message(client_socket):

    try:

        # Reciba nuestro "encabezado(header)" que contiene la longitud del mensaje, su tamaño está definido y es constante 
        message_header = client_socket.recv(HEADER_LENGTH)

        # Si no recibimos datos, el cliente cerró una conexión con gracia, por ejemplo, usando socket.close () o socket.shutdown (socket.SHUT_RDWR) si no len ( message_header ): return False
        if not len(message_header):
            return False

        # Convertir encabezado a valor int 
        message_length = int(message_header.decode('utf-8').strip())

        # Devuelve un objeto del encabezado del mensaje y los datos del mensaje
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
         # Si estamos aquí, el cliente cerró la conexión violentamente, por ejemplo presionando ctrl + c en su script 
         # o simplemente perdió su conexión 
         # socket.close () también invoca socket.shutdown (socket.SHUT_RDWR) lo que envía información sobre cómo cerrar el socket (cierre de lectura / escritura) 
         # y eso también es una causa cuando recibimos un mensaje vacío
        return False

while True:
    # Llamadas llamada al sistema select () de Unix o llamada WinSock de Windows select () con tres parámetros: 
    # - rlist - sockets para monitorear los datos entrantes 
    # - wlist - sockets para los datos a enviar (verifica si, por ejemplo, los buffers no están llenos y el zócalo está listo para enviar algunos datos) 
    # - xlist - zócalos a ser monitoreados para excepciones (queremos monitorear todos los zócalos en busca de errores, para que podamos usar rlist) 
    # Devuelve listas: # - lectura - zócalos en los que recibimos algunos datos de esa manera no tenemos que verificar los sockets manualmente) 
    # - escritura - sockets listos para enviar datos a través de ellos 
    # - errores - sockets con algunas excepciones 
    # Esta es una llamada de bloqueo, la ejecución del código "esperará" aquí y "obtendrá "notificado en caso de que se tome alguna medida
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    # Iterar a través de sockets notificados
    for notified_socket in read_sockets:

        # Si toma notificado es un socket de servidor - nueva conexión, aceptarlo
        if notified_socket == server_socket:
            # Aceptar nueva conexión 
            # Eso nos da un nuevo socket - socket de cliente, conectado a este cliente dado, es único para ese cliente 
            # El otro objeto devuelto es ip / port set 
            client_socket, client_address = server_socket.accept()

            ## El cliente debe enviar su nombre de inmediato, recibirlo 
            user = receive_message(client_socket)

            # Si es falso: el cliente se desconectó antes de enviar su nombre
            if user is False:
                continue

            # Agregue el socket aceptado a select.select () list
            sockets_list.append(client_socket)

            # Guarde también el nombre de usuario y el encabezado de nombre de usuario 
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        # El otro socket existente está enviando un mensaje
        else:

            # Recibir mensaje
            message = receive_message(notified_socket)

             # Si es falso, cliente desconectado, limpieza
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Eliminar de la lista para socket.socket ()
                sockets_list.remove(notified_socket)

                # Eliminar de nuestra lista de usuarios
                del clients[notified_socket]

                continue

            # Obtenga el usuario por socket notificado, así sabremos quién envió el mensaje 
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Iterar sobre clientes conectados y transmitir mensajes
            for client_socket in clients:
                # ¡Pero no lo envíe al remitente
                if client_socket != notified_socket:
                    # Enviar usuario y mensaje (ambos con sus encabezados) 
                    # Estamos reutilizando aquí el encabezado del mensaje enviado por el remitente, y el encabezado del nombre de usuario guardado enviado por el usuario cuando conectó 
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # No es realmente necesario tener esto, pero manejará algunas excepciones de socket solo en caso de
    for notified_socket in exception_sockets:
        # Eliminar de la lista para socket.socket ()
        sockets_list.remove(notified_socket)

        # Eliminar de nuestra lista de usuarios
        del clients[notified_socket]



                
            

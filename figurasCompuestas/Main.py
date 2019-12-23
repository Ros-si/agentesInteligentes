import Client
import threading

x = threading.Thread(target=Client.start_connection)
x.start()
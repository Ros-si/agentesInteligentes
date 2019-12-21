import socket, pickle

class ProcessData:
    process_id = 10
    project_id = 20
    task_id = 1030
    start_time = 30
    end_time = 110
    user_id = 120
    weekend_id = 130


HOST = 'localhost'
PORT = 50007
# Create a socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Create an instance of ProcessData() to send to server.
variable = ProcessData()
variable.task_id = 50
# Pickle the object and send it to the server
data_string = pickle.dumps(variable)
s.send(data_string)

s.close()
print ('Data Sent to Server')
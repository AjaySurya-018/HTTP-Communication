import socket
import os

# Define the server address (IP and port)
server_address = ('192.168.157.226', 12345)

# Create a socket and bind it to the server address
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)

# Listen for incoming connections (1 connection at a time)
server_socket.listen(6)
print("Server is listening for incoming connections...")

def handle_get(client_socket, file_name):
    if os.path.isfile(file_name):
        _, file_extension = os.path.splitext(file_name)

        if file_extension != ".txt":
            response = "Incorrect file format"
            client_socket.send(response.encode())
        else:
            response = "File found"
            client_socket.send(response.encode())

            with open(file_name, "rb") as file:
                file_data = file.read()
                client_socket.send(file_data)
            print(f"Sent '{file_name}' to {client_address}")
    else:
        response = "File not found"
        client_socket.send(response.encode())

def handle_post(client_socket, file_name, data):
    if os.path.isfile(file_name) and os.path.splitext(file_name)[1] == ".txt":
        response = "Resource already exists and cannot be overwritten."
    else:
        with open(file_name, "wb") as file:
            file.write(data.encode())
        response = f"Resource '{file_name}' created with updated content."
    client_socket.send(response.encode())

def handle_put(client_socket, file_name, data):
    if os.path.isfile(file_name):
        _, file_extension = os.path.splitext(file_name)

        if file_extension != ".txt":
            response = "Incorrect file format"
            client_socket.send(response.encode())
        else:
            with open(file_name, "wb") as file:
                file.write(data.encode())
            response = f"Resource '{file_name}' updated successfully."
    else:
        with open(file_name, "wb") as file:
            file.write(data.encode())
        response = f"Resource '{file_name}' created with updated content."
    client_socket.send(response.encode())

def handle_delete(client_socket, file_name):
    if os.path.isfile(file_name):
        _, file_extension = os.path.splitext(file_name)
        if file_extension==".txt":
            os.remove(file_name)
            response = f"Resource '{file_name}' deleted successfully."
        else:
            response = "Incorrect file format"
            client_socket.send(response.encode())
    else:
        response = "File not found"
    client_socket.send(response.encode())

while True:
    # Accept incoming connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    
    # Receive the request from the client
    request = client_socket.recv(1024).decode()

    if request.startswith("GET "):
        handle_get(client_socket, request[4:])
    elif request.startswith("POST "):
        data = client_socket.recv(1024).decode()
        handle_post(client_socket, request[5:], data)
    elif request.startswith("PUT "):
        data = client_socket.recv(1024).decode()
        handle_put(client_socket, request[4:], data)
    elif request.startswith("DELETE "):
        handle_delete(client_socket, request[7:])
    else:
        response = "Invalid request"
        client_socket.send(response.encode())

    client_socket.close()

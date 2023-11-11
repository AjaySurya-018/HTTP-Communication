import socket
import os

# Define the server address (IP and port)
server_address = ('server_ip', port_no)

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

def get_file(file_name):
    client_socket.send(f"GET {file_name}".encode())

    response = client_socket.recv(1024).decode()

    if response == "File found":
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(data, end = '')
        print("\nReceived and displayed content from the server.")
        
    elif response == "File not found":
        print(response)
    elif response == "Incorrect file format":
        print(response)
    else:
        print(response)

def post_file(file_name, data):
    _, file_extension = os.path.splitext(file_name)
    if file_extension != ".txt":
        print("Incorrect file format")
        return

    client_socket.send(f"POST {file_name}".encode())
    client_socket.send(data.encode())

    response = client_socket.recv(1024).decode()
    print(response)

def put_file(file_name, data):
    _, file_extension = os.path.splitext(file_name)
    if file_extension != ".txt":
        print("Incorrect file format")
        return

    client_socket.send(f"PUT {file_name}".encode())
    client_socket.send(data.encode())

    response = client_socket.recv(1024).decode()

    if response == "Incorrect file format":
        print(response)
    else:
        print(response)

def delete_file(file_name):
    client_socket.send(f"DELETE {file_name}".encode())

    response = client_socket.recv(1024).decode()

    if response == "File not found":
        print(response)
    else:
        print(response)

while True:
    request = input("Enter the request (e.g., 'GET filename.txt', 'POST newfile.txt', 'PUT existingfile.txt', or 'DELETE fileToDelete.txt'): ")
    request_parts = request.split(' ', 1)
    
    if len(request_parts) > 1:
        file_name = request_parts[1]
    else:
        file_name = ""

    if request_parts[0] == "GET":
        get_file(file_name)
    elif request_parts[0] == "POST":
        data = input("Enter the data for the resource: ")
        post_file(file_name, data)
    elif request_parts[0] == "PUT":
        data = input("Enter the data for the resource: ")
        put_file(file_name, data)
    elif request_parts[0] == "DELETE":
        delete_file(file_name)
    else:
        print("Invalid request. Please use 'GET filename.txt', 'POST newfile.txt', 'PUT existingfile.txt', or 'DELETE fileToDelete.txt' format.")

client_socket.close()

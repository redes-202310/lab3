import socket
import threading
import hashlib
import os
import time

# Create a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
server_ip = "127.0.0.1" # Change this to the IP address of the server
server_port = 8001 # Change this to the port number that the server will listen on
tcp_socket.bind((server_ip, server_port))

# Listen for incoming connections
tcp_socket.listen(5)

# Initialize a list to store the connected clients
clients = []

# Initialize the file paths and sizes
file_paths = {"file_100MB": "data/file-100.txt", "file_250MB": "data/file-250.txt"}
file_sizes = {"file_100MB": os.path.getsize(file_paths["file_100MB"]), "file_250MB": os.path.getsize(file_paths["file_250MB"])}

# Initialize the log file directory
log_dir = "Logs/"

# Function to handle sending files to clients
def send_file(client_socket, file_path):
    # Open the file to be sent
    with open(file_path, "rb") as f:
        file_data = f.read()

    # Calculate the hash value of the file data
    hash_value = hashlib.sha256(file_data).hexdigest()

    # Send the file size and hash value to the client
    client_socket.send(str(len(file_data)).encode())
    client_socket.send(hash_value.encode())

    # Send the file data to the client
    client_socket.sendall(file_data)

    # Wait for the client to confirm that the file was received successfully
    message = client_socket.recv(1024)
    if message.decode() == "received":
        return True
    else:
        return False

# Function to handle a client connection
def handle_client(client_socket, client_address, file_path):
    # Send a message to the client to indicate that it has successfully connected
    client_socket.send(b"You have successfully connected to the server.")

    # Wait for the client to signal that it is ready to receive the file
    message = client_socket.recv(1024)
    if message.decode() == "ready":
        # Send the file to the client
        if send_file(client_socket, file_path):
            # Log the successful file transfer
            log_message = f"File transfer successful to client {client_address}. File name: {os.path.basename(file_path)}, file size: {file_sizes[os.path.basename(file_path)]} bytes."
            print(log_message)
        else:
            # Log the failed file transfer
            log_message = f"File transfer failed to client {client_address}. File name: {os.path.basename(file_path)}, file size: {file_sizes[os.path.basename(file_path)]} bytes."
            print(log_message)

    # Close the client socket
    client_socket.close()

# Wait for clients to connect
while len(clients) < 2:
    # Accept a new client connection
    client_socket, client_address = tcp_socket.accept()
    
    # Add the new client to the list of connected clients
    clients.append(client_socket)

# Get user input for file selection and number of clients
file_name = input("Enter the name of the file to send (file_100MB or file_250MB): ")
num_clients = int(input("Enter the number of clients to send the file to (1 or 2): "))

# Check if the selected file exists
if file_name in file_paths:
    # Check if the requested number of clients is available
    # Check if the requested number of clients is available
    if num_clients <= len(clients):
        # Send a message to all clients indicating the start of the file transfer
        for client_socket in clients:
            client_socket.send(b"start")

        # Open the file to be sent
        with open(file_path, "rb") as f:
            file_data = f.read()

        # Calculate the hash value of the file
        hash_value = hashlib.md5(file_data).hexdigest()

        # Send the file size and hash value to all clients
        for client_socket in clients:
            client_socket.send(str(file_size).encode())
            client_socket.send(hash_value.encode())

        # Split the file data into chunks and send to all clients
        for i in range(0, file_size, CHUNK_SIZE):
            chunk = file_data[i:i+CHUNK_SIZE]
            for client_socket in clients:
                client_socket.send(chunk)

        # Wait for all clients to confirm successful receipt of the file
        confirmations = 0
        while confirmations < num_clients:
            for client_socket in clients:
                message = client_socket.recv(1024)
                if message.decode() == "received":
                    confirmations += 1

        # Log the transfer information
        log_file.write(f"File transfer to {num_clients} clients successful.\n")
        log_file.write(f"File name: {file_name}\n")
        log_file.write(f"File size: {file_size} bytes\n")
        log_file.write(f"Hash value: {hash_value}\n")
        log_file.write("Transfer times:\n")
        for i, client_socket in enumerate(clients):
            transfer_time = transfer_times[i]
            log_file.write(f"Client {i+1}: {transfer_time} seconds\n")

    else:
        print("Requested number of clients not available.")


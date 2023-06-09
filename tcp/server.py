import socket
import threading
import hashlib
import os
import time
import datetime

# Constants
BLOCK_SIZE = 10 * 1024 * 1024

# Create a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
server_ip = "localhost" # Change this to the IP address of the server
server_port = 8002 # Change this to the port number that the server will listen on
tcp_socket.bind((server_ip, server_port))

# Listen for incoming connections
tcp_socket.listen(25)

# Initialize a list to store the connected clients
clients = []

# Initialize the file paths and sizes
file_paths = {"file_100MB": "data/file-100.txt", "file_250MB": "data/file-250.txt", "lorem": "data/lorem.txt"}
file_sizes = {"data/file-100.txt": os.path.getsize(file_paths["file_100MB"]), "data/file-250.txt": os.path.getsize(file_paths["file_250MB"]), "data/lorem.txt": os.path.getsize(file_paths["lorem"])}

# Initialize the log file directory
log_dir = "Logs/"

# Create the log file directory if it does not exist
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Initialize the log file
log_file = open(log_dir + "server.log", "w")

def calculate_hash(file_path):
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BLOCK_SIZE)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()

def send_file_in_chunks(client_socket, file_path):
    BLOCK_SIZE = 10 * 1024 * 1024
    with open(file_path, 'rb') as f:
        while True:
            time.sleep(0.1)
            data = f.read(BLOCK_SIZE)
            # print("Data length: " + str(len(data)) + " bytes")
            if len(data) <= 0:
                client_socket.send(b"<EOF>")
                print("Data sent.")
                break
            client_socket.sendall(data)


# Function to handle sending files to clients
def send_file(client_socket, file_path):
    # Open the file to be sent
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    # Calculate the hash value of the file data
    hash_value = calculate_hash(file_path)

    # Put a sleep here to simulate a slow connection
    time.sleep(0.1)

    # Send the file size and hash value to the client
    file_size = os.path.getsize(file_path)

    client_socket.send(str(file_size).encode())

    time.sleep(0.1)
    
    client_socket.send(hash_value.encode())

    # Put a sleep here to simulate a slow connection
    time.sleep(0.1)

    # Send the file data to the client
    send_file_in_chunks(client_socket, file_path)
    
    time.sleep(0.1)

    # Wait for the client to confirm that the file was received successfully
    
    message = client_socket.recv(1024)
    
    if message.decode() == "received":
        return True
    elif message.decode() == "error":
        return False

# Function to handle a client connection
def handle_client(client_socket, client_address, file_path):
    # Send a message to the client to indicate that it has successfully connected
    # print(f"Handling client {client_socket}")
    client_socket.send(b"You have successfully connected to the server.")

    # Wait for the client to signal that it is ready to receive the file
    message = client_socket.recv(1024)
    
    if message == b"ready to receive":
        # Send the file to the client
        if send_file(client_socket, file_path):
            # Log the successful file transfer
            log_message = f"File transfer successful to client {client_address}. File name: {file_path}, file size: {file_sizes[file_path]} bytes."
            print(log_message)
        else:
            # Log the failed file transfer
            log_message = f"File transfer failed to client {client_address}. File name: {file_path}, file size: {file_sizes[file_path]} bytes."
            print(log_message)

    # Close the client socket
    client_socket.close()

# Get user input for file selection and number of clients
file_name = input("Enter the name of the file to send (lorem, file_100MB or file_250MB): ")
num_clients = int(input("Enter the number of clients to send the file to: "))

# Wait for clients to connect
while len(clients) < num_clients:
    # Accept a new client connection
    client_socket, client_address = tcp_socket.accept()
    
    # Add the new client to the list of connected clients
    clients.append(client_socket)


# Check if the selected file exists
if file_name in file_paths:
    # Check if the requested number of clients is available
    if num_clients <= len(clients):
        # Send the file to all clients
        transfer_times = []
        successes = []
        for i, client_socket in enumerate(clients):
            start_time = time.time()
            handle_client(client_socket, client_address, file_paths.get(file_name))
            end_time = time.time()
            transfer_times.append(end_time - start_time)
            successes.append(True)

        # Log the transfer information
        log_file.write(f"Date and time: {datetime.datetime.now()}\n")
        log_file.write(f"File transfer to {num_clients} clients successful.\n")
        log_file.write(f"File name: {file_name}\n")
        log_file.write(f"File size: {file_sizes[file_paths.get(file_name)]} bytes\n")
        log_file.write("Transfer times:\n")
        for i, time in enumerate(transfer_times):
            log_file.write(f"Client {i+1}: {time} seconds")
            log_file.write(f"\tSuccessful?:{successes[i]}\n")
            

    else:
        print("Requested number of clients not available.")


# Close the log file
log_file.close()

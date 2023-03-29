import socket
import hashlib
import time
import os

# Create a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_ip = "127.0.0.1" # Change this to the IP address of the server
server_port = 8002 # Change this to the port number that the server is listening on
tcp_socket.connect((server_ip, server_port))

# Initialize the log file directory
log_dir = "Logs/"

# Create the log file directory if it does not exist
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Initialize the log file
log_file = open(log_dir + "client.log", "w")

# Receive a message from the server to indicate successful connection
message = tcp_socket.recv(1024)
print(message)

if message == b"You have successfully connected to the server.":
    # Send a message to the server to indicate readiness to receive the file
    tcp_socket.send(b"ready to receive")

    file_size = tcp_socket.recv(1024).decode()
    hash_value = tcp_socket.recv(1024).decode()

    print(f"File size: {file_size} bytes")
    print(f"Hash value: {hash_value}")

    # Calculate the time taken to receive the file
    start_time = time.time()
    received_data = tcp_socket.recv(int(file_size))
    end_time = time.time()

    print(f"Time taken to receive file: {end_time - start_time} seconds")

    # Verify the hash value of the received file data
    if hashlib.sha256(received_data).hexdigest() == hash_value:
        # Send a confirmation message to the server
        tcp_socket.send(b"received")
        print(f"File received successfully.")
    else:
        # Send an error message to the server
        tcp_socket.send(b"error")
        print("Error: Hash value of received data does not match.")

    # Log everything to the log file
    log_file.write(f"File size: {file_size} bytes")
    log_file.write(f"Time taken to receive file: {end_time - start_time} seconds")
        
    # Close the socket
    tcp_socket.close()

# Close the log file
log_file.close()
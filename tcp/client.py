import socket
import hashlib

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_ip = "127.0.0.1" # Change this to the IP address of the server
server_port = 8001 # Change this to the port number that the server is listening on
client_socket.connect((server_ip, server_port))

# Receive a message from the server indicating that the connection was successful
message = client_socket.recv(1024)
print(message.decode())

# Send a message to the server indicating that the client is ready to receive the file
client_socket.send(b"ready")

# Receive the file size and hash value from the server
file_size = int(client_socket.recv(1024).decode())
hash_value = client_socket.recv(1024).decode()

# Initialize the received file data
file_data = b""

# Receive the file data from the server
while len(file_data) < file_size:
    chunk = client_socket.recv(1024)
    if not chunk:
        break
    file_data += chunk

# Calculate the hash value of the received file data
received_hash_value = hashlib.sha256(file_data).hexdigest()

# Send a confirmation message to the server indicating that the file was received successfully
if received_hash_value == hash_value:
    print("File received successfully.")
    client_socket.send(b"received")
else:
    print("File received with errors.")
    client_socket.send(b"error")

# Close the client socket
client_socket.close()

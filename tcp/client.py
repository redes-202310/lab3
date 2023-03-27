import socket

# Create a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
server_ip = "127.0.0.1" # Change this to the IP address of the server
server_port = 8000 # Change this to the port number that the server is listening on
tcp_socket.connect((server_ip, server_port))

# Send a message to the server to indicate that the client has successfully connected
message = tcp_socket.recv(1024)
print(message.decode())

# Send a "send_file" request to the server
tcp_socket.send(b"send_file")

# Receive the file data from the server
file_size = int(tcp_socket.recv(1024).decode())
file_data = tcp_socket.recv(file_size)

# Save the file to disk
with open("received_file.txt", "wb") as f:
    f.write(file_data)

# Close the socket
tcp_socket.close()

import socket

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the IP address and port number of the server
server_ip = "127.0.0.1" # Change this to the IP address of the server
server_port = 8000 # Change this to the port number used by the server

# Request a file from the server
filename = "file.txt" # Change this to the name of the file you want to request
udp_socket.sendto(filename.encode(), (server_ip, server_port))

# Receive the file data from the server
file_data, server_address = udp_socket.recvfrom(1024)

# Write the file data to disk
with open(filename, "wb") as f:
    f.write(file_data)

# with open(filename, "r") as f:
#     print(f.read())
import socket

# Create a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the IP address and port number of the server
server_ip = "127.0.0.1" # Change this to the IP address of the server
server_port = 8001 # Change this to the port number used by the server

# Connect to the server
tcp_socket.connect((server_ip, server_port))

# Request a file from the server
filename = "./filea.txt" # Change this to the name of the file you want to request
tcp_socket.sendall(filename.encode())

# Receive the file data from the server
file_data = b""
while True:
    data = tcp_socket.recv(1024)
    if not data:
        break
    file_data += data

# Check if the server sent an error message
if file_data == b"File not found":
    print("File not found on server")
else:
    print("Received file from server")
    # Write the file data to disk
    with open(filename, "wb") as f:
        f.write(file_data)
    
    # with open(filename, "r") as f:
    #     print(f.read())

    

# Close the socket
tcp_socket.close()

import socket
import threading

# Create a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
server_ip = "127.0.0.1" # Change this to the IP address of the server
server_port = 8000 # Change this to the port number that the server will listen on
tcp_socket.bind((server_ip, server_port))

# Listen for incoming connections
tcp_socket.listen(3)

# Initialize a list to store the connected clients
clients = []

# Wait for 25 clients to connect
while len(clients) < 3:
    # Accept a new client connection
    client_socket, client_address = tcp_socket.accept()
    
    # Add the new client to the list of connected clients
    clients.append(client_socket)
    
    # Send a message to the client to indicate that it has successfully connected
    client_socket.send(b"You have successfully connected to the server.")

# Wait for a "send_file" request from any client
while True:
    for client_socket in clients:
        # Receive a message from the client
        message = client_socket.recv(1024)
        
        # If the message is a "send_file" request, send the file data to all clients
        if message.decode() == "send_file":
            # Open the file to be sent
            with open("filea.txt", "rb") as f: # Change this to the name of the file to be sent
                file_data = f.read()

            # Send the file data to all connected clients
            for client_socket in clients:
                client_socket.send(str(len(file_data)).encode())
                client_socket.send(file_data)

# Close all client sockets
for client_socket in clients:
    client_socket.close()

# Close the server socket
tcp_socket.close()

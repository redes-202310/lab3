import socket

# Create a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP address and port number
ip_address = "127.0.0.1" # Change this to the IP address of your machine
port_number = 8001 # Change this to any available port number
tcp_socket.bind((ip_address, port_number))

# Listen for client connections
tcp_socket.listen()

# Function to send a file to a client
def send_file(client_socket, filename):
    # Open the requested file and read its data
    with open(filename, "rb") as f:
        file_data = f.read()

    # Send the file data to the client
    client_socket.sendall(file_data)
    print("Sent file to client")

# Serve files to clients
while True:
    # Accept a new client connection
    client_socket, address = tcp_socket.accept()

    # Receive a request for a file
    filename = client_socket.recv(1024).decode()

    # Check if the requested file exists
    try:
        with open(filename, "rb") as f:
            pass
    except FileNotFoundError:
        client_socket.sendall(b"File not found")
        client_socket.close()
        continue

    # Send the file to the client
    send_file(client_socket, filename)

    # Close the client connection
    client_socket.close()

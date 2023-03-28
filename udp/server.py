import socket

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific IP address and port number
ip_address = "127.0.0.1" # Change this to the IP address of your machine
port_number = 8000 # Change this to any available port number
udp_socket.bind((ip_address, port_number))

# Function to send a file to a client
def send_file(client_address, filename):
    # Open the requested file and read its data
    with open(filename, "rb") as f:
        file_data = f.read()

    # Send the file data to the client
    udp_socket.sendto(file_data, client_address)

# Serve files to clients
while True:
    # Receive a request for a file
    request_data, client_address = udp_socket.recvfrom(1024)
    filename = request_data.decode()

    # Check if the requested file exists
    try:
        with open(filename, "rb") as f:
            pass
    except FileNotFoundError:
        udp_socket.sendto(b"File not found", client_address)
        continue

    # Send the file to the client
    send_file(client_address, filename)
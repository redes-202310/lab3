import socket
import select
import os

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific IP address and port number
ip_address = "127.0.0.1" # Change this to the IP address of your machine
port_number = 8000 # Change this to any available port number
udp_socket.bind((ip_address, port_number))


file_paths = {"file_100MB": "data/file-100.txt", "file_250MB": "data/file-250.txt", "lorem": "data/lorem.txt"}
file_sizes = {"file_100MB": os.path.getsize(file_paths["file_100MB"]), "file_250MB": os.path.getsize(file_paths["file_250MB"]), "lorem": os.path.getsize(file_paths["lorem"])}

FRAGMENT_SIZE = 8000  # TODO: ask if KB is Kilo or Kibi

# Function to send a file to a client
def send_file(client_address, file_path):
    # Open the requested file and read its data
    with open(file_path, "rb") as f:
        data = f.read(FRAGMENT_SIZE)
        while data:
            if udp_socket.sendto(data, client_address):
                data = f.read(FRAGMENT_SIZE)


file_name = input("Enter the name of the file to send (file_100MB or file_250MB): ")
num_clients = int(input("Enter the number of clients to send the file to (1 or 2): ")) 
num_connected = 0
client_sockets = [udp_socket]

if file_name in file_paths:
    file_path = file_paths[file_name]
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    if 0 < num_clients <= 25:
        while num_connected < num_clients:
            read_socket, _, _ = select.select(client_sockets, [], [])

            for sock in read_socket:
                if sock == udp_socket:
                    request_data, client_address = udp_socket.recvfrom(1024)
                    print("received request from client", client_address)
                    client_sockets.append(client_address)
                    num_connected += 1
                else:
                    client_address = sock
                    send_file(client_address, file_path)
    else:
        print("Invalid number of clients")
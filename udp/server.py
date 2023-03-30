import socket
import threading
import os
import time

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific IP address and port number
ip_address = "127.0.0.1" 
port_number = 8000 
udp_socket.bind((ip_address, port_number))

FRAGMENT_SIZE = 8000  # TODO: ask if KB is Kilo or Kibi

file_paths = {"file_100MB": "data/file-100.txt", "file_250MB": "data/file-250.txt", "lorem": "data/lorem.txt"}
file_sizes = {"file_100MB": os.path.getsize(file_paths["file_100MB"]), "file_250MB": os.path.getsize(file_paths["file_250MB"]), "lorem": os.path.getsize(file_paths["lorem"])}


# Initialize the log file directory
log_dir = "udp/Logs/Server/"

# Create the log file directory if it does not exist
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Initialize the log file
current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
log_file = open(log_dir + current_time + ".log", "w")



# Function to send a file to a client
def send_file(client_address, client_num, file_path):
    print("Sending file to client", client_num)
    # Open the requested file and read its data
    start_time = time.time()
    with open(file_path, "rb") as f:
        data = f.read(FRAGMENT_SIZE)
        while data:
            if udp_socket.sendto(data, client_address):
                data = f.read(FRAGMENT_SIZE)
    end_time = time.time()
    execution_time = end_time - start_time
    log_file.write(f"Transfer time for client {client_num}: {execution_time}s\n")


file_name = input("Enter the name of the file to send (file_100MB or file_250MB): ")
num_clients = int(input("Enter the number of clients to send the file to (1 or 2): ")) 
num_connected = 0
client_sockets = [udp_socket]

if file_name in file_paths:
    file_path = file_paths[file_name]
    log_file.write(f"File name: {file_name}\n")
    log_file.write(f"File size: {file_sizes[file_name]} bytes\n")

    try:
        request_data, client_address = udp_socket.recvfrom(1024)
    except Exception as exp:
        request_data = False
    if request_data:
        if request_data == b"send_num_clients":
            udp_socket.sendto(num_clients.to_bytes(), client_address)
    try:
        request_data, client_address = udp_socket.recvfrom(1024)
    except Exception as exp:
        request_data = False
    if request_data:
        if request_data == b"send_file_name":
            udp_socket.sendto(file_name.encode(), client_address)
    try:
        request_data, client_address = udp_socket.recvfrom(1024)
    except Exception as exp:
        request_data = False
    if request_data:
        if request_data == b"send_file_size":
            udp_socket.sendto(file_sizes[file_name].to_bytes(length=64), client_address)


    with open(file_path, "rb") as f:
        file_data = f.read()
    if 0 < num_clients <= 25:
        

        while num_connected < num_clients:
            try:
                request_data, client_address = udp_socket.recvfrom(1024)
            except Exception as exp:
                request_data = False
            if request_data:
                print(request_data.decode())
                if request_data == b"send_file":
                    print("Received request from client", client_address, request_data)
                    client_sockets.append(client_address)
                    udp_socket.sendto(b"ACK", client_address)
                    num_connected += 1
                
        # all have connected
        print("All clients have connected, preparing to send file.")
        for client_address in client_sockets:
            if client_address != udp_socket:
                udp_socket.sendto(b"All clients have connected, preparing to send file.", client_address)
        
        client_num = 1
        
        for client_address in client_sockets:
            if client_address != udp_socket:
                thread = threading.Thread(target=send_file, args=(client_address, client_num, file_path))
                thread.start()
                client_num += 1
            # read_socket, _, _ = select.select(client_sockets, [], [])
        
        active_threads = threading.active_count()
        print("ACTIVE:", threading.active_count())
        while active_threads > 1:
            active_threads = threading.active_count()
        print("ACTIVE:", threading.active_count())
        print("All files sent")
        log_file.close()
        udp_socket.close()
    else:
        print("Invalid number of clients")
else:
    print("Invalid file name")
import socket
import os
import time
import threading

ip_address = "127.0.0.1" # Change this to the IP address of your machine
port_number = 8000

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

FRAGMENT_SIZE = 8000

# set up the directories to store the files and logs
files_dir = "udp/ArchivosRecibidos/"
if not os.path.exists(files_dir):
    os.makedirs(files_dir)

log_dir = "udp/Logs/Client/"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
log_file = open(log_dir + current_time + ".log", "w")


# send a request for the file
udp_socket.sendto(b"send_num_clients", (ip_address, port_number))

chunk_data, server_addr = udp_socket.recvfrom(FRAGMENT_SIZE)
print(f"Received {len(chunk_data)} bytes from {server_addr}")
print(f"Chunk data: {chunk_data}")
expected_clients = int.from_bytes(chunk_data, byteorder='big')
print("Expected clients:", expected_clients)

def handle_client_request(client_socket, client_num, test_num):
    
    client_socket.sendto(b"send_file", (ip_address, port_number)) # TODO: also send client number

    chunk_data, server_addr = client_socket.recvfrom(FRAGMENT_SIZE)
    print(f"{client_num}: Received {len(chunk_data)} bytes from {server_addr}")

    if chunk_data == b"ACK":
        print(f"{client_num}: You have succesfully connected to the server.")

    print("here")
    chunk_data, server_addr = client_socket.recvfrom(FRAGMENT_SIZE)
    print("here1")
    print(f"{client_num}: Received {len(chunk_data)} bytes from {server_addr}")
    print(f"{client_num}: Chunk data: {chunk_data}")

    if chunk_data == b"All clients have connected, preparing to send file.":
        print(f"{client_num}: All clients have connected, preparing to send file.")    

    file_name = f"{files_dir}Cliente{client_num}-Prueba{test_num}.txt"

    with open(file_name, 'wb') as file:
        while True:
            # receive a chunk of data
            
            chunk_data, server_addr = client_socket.recvfrom(FRAGMENT_SIZE)
            # write the chunk data to the file
            file.write(chunk_data)
            
            # send an acknowledgement to the server
            # udp_socket.sendto(b"ACK", server_addr)
            
            # break out of the loop if we have received the entire file
            print(len(chunk_data))
            if len(chunk_data) < FRAGMENT_SIZE:
                break

    print("File received successfully")


client_sockets = []
for i in range(1, expected_clients + 1):
    # create socket for client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sockets.append(client_socket)
    print(client_socket)
    # send request for file
    thread = threading.Thread(target=handle_client_request, args=(client_socket, i, 1))
    thread.start()

# close the socket

active_threads = threading.active_count()
print("ACTIVE:", threading.active_count())
while active_threads > 1:
    active_threads = threading.active_count()
print("ACTIVE:", threading.active_count())
print("All files recv")

# for client_socket in client_sockets:
#     client_socket.close()
# udp_socket.close()

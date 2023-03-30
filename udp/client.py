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

def handle_client_request(client_socket, client_num, test_num):
    
    client_socket.sendto(b"send_file", (ip_address, port_number)) # TODO: also send client number

    chunk_data, server_addr = client_socket.recvfrom(FRAGMENT_SIZE)
    print(f"{client_num}: Received {len(chunk_data)} bytes from {server_addr}")

    if chunk_data == b"ACK":
        print(f"{client_num}: You have succesfully connected to the server.")

    chunk_data, server_addr = client_socket.recvfrom(FRAGMENT_SIZE)
    print(f"{client_num}: Received {len(chunk_data)} bytes from {server_addr}")
    print(f"{client_num}: Chunk data: {chunk_data}")

    if chunk_data == b"All clients have connected, preparing to send file.":
        print(f"{client_num}: All clients have connected, preparing to send file.")    

    file_name = f"{files_dir}Cliente{client_num}-Prueba{test_num}.txt"

    start_time = time.time()
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
    execution_time = time.time() - start_time
    log_file.write(f"Transfer time for client {client_num}: {execution_time}s\n")
    print("File received successfully")


# send a request for the file
udp_socket.sendto(b"send_num_clients", (ip_address, port_number))

chunk_data, server_addr = udp_socket.recvfrom(FRAGMENT_SIZE)
expected_clients = int.from_bytes(chunk_data, byteorder='big')

udp_socket.sendto(b"send_file_name", (ip_address, port_number))
chunk_data, server_addr = udp_socket.recvfrom(FRAGMENT_SIZE)
file_name = chunk_data.decode()

udp_socket.sendto(b"send_file_size", (ip_address, port_number))
chunk_data, server_addr = udp_socket.recvfrom(FRAGMENT_SIZE)
file_size = int.from_bytes(chunk_data, byteorder='big')

log_file.write(f"File name: {file_name}\n")
log_file.write(f"File size: {file_size} bytes\n")


print("Expected clients:", expected_clients)
client_sockets = []
for i in range(1, expected_clients + 1):
    # create socket for client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sockets.append(client_socket)
    print(client_socket)
    # send request for file
    thread = threading.Thread(target=handle_client_request, args=(client_socket, i, 1))
    thread.start()


# TODO: como saber si es exitosa o no?
# log_file.write("Suceessful transfer: " + str(successful_transfer) + "\n")

active_threads = threading.active_count()
print("Active Clients:", threading.active_count())
while active_threads > 1:
    active_threads = threading.active_count()
print("All files received")

# close sockets
for client_socket in client_sockets:
    client_socket.close()
udp_socket.close()

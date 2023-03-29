import socket
import os
import time

ip_address = "127.0.0.1" # Change this to the IP address of your machine
port_number = 8000
# create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send a request for the file
udp_socket.sendto(b"send_file", (ip_address, port_number))

FRAGMENT_SIZE = 8000

files_dir = "udp/ArchivosRecibidos/"
if not os.path.exists(files_dir):
    os.makedirs(files_dir)

log_dir = "udp/Logs/Client/"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
log_file = open(log_dir + current_time + ".log", "w")

chunk_data, server_addr = udp_socket.recvfrom(FRAGMENT_SIZE)
print(f"Received {len(chunk_data)} bytes from {server_addr}")
print(f"Chunk data: {chunk_data}")

if chunk_data == b"ACK":
    print("You have succesfully connected to the server.")

chunk_data, server_addr = udp_socket.recvfrom(FRAGMENT_SIZE)
print(f"Received {len(chunk_data)} bytes from {server_addr}")
print(f"Chunk data: {chunk_data}")

if chunk_data == b"All clients have connected, preparing to send file.":
    print("All clients have connected, preparing to send file.")    



num_client = "XX" #TODO: get the client number from the server
test_num = "XX" #TODO: get the test number from the server

file_name = f"{files_dir}Cliente{num_client}-Prueba{test_num}.txt"

# open a file to write the received data to
with open(file_name, 'wb') as file:
    while True:
        # receive a chunk of data
        
        chunk_data, server_addr = udp_socket.recvfrom(FRAGMENT_SIZE)
        # write the chunk data to the file
        file.write(chunk_data)
        
        # send an acknowledgement to the server
        # udp_socket.sendto(b"ACK", server_addr)
        
        # break out of the loop if we have received the entire file
        if len(chunk_data) < FRAGMENT_SIZE:
            break

print("File received successfully")

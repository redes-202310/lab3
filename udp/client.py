import socket

ip_address = "127.0.0.1" # Change this to the IP address of your machine
port_number = 8000
# create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send a request for the file
udp_socket.sendto(b"send_file", (ip_address, port_number))

FRAGMENT_SIZE = 8000
# open a file to write the received data to
with open('received_file.txt', 'wb') as file:
    while True:
        # receive a chunk of data
        chunk_data, server_addr = udp_socket.recvfrom(FRAGMENT_SIZE)
        print(f"Received {len(chunk_data)} bytes from {server_addr}")
        print(f"Chunk data: {chunk_data}")
        # write the chunk data to the file
        file.write(chunk_data)
        
        # send an acknowledgement to the server
        # udp_socket.sendto(b"ACK", server_addr)
        
        # break out of the loop if we have received the entire file
        if len(chunk_data) < FRAGMENT_SIZE:
            break

print("File received successfully")

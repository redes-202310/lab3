import socket
import hashlib
import time
import os
import threading
import datetime

class Client(threading.Thread):

    def __init__(self, id, lock):
        threading.Thread.__init__(self)
        self.id = id
        self.lock = lock

    def run(self):
        with self.lock:
            # Create a TCP socket
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the server
            server_ip = "127.0.0.1" # Change this to the IP address of the server
            server_port = 8002 # Change this to the port number that the server is listening on
            tcp_socket.connect((server_ip, server_port))

            # Receive a message from the server to indicate successful connection
            message = tcp_socket.recv(1024)

            if message == b"You have successfully connected to the server.":
                # Send a message to the server to indicate readiness to receive the file
                tcp_socket.send(b"ready to receive")

                file_size = tcp_socket.recv(1024).decode()
                hash_value = tcp_socket.recv(int(file_size)).decode()

                print(f"File size: {file_size} bytes")
                print(f"Hash value: {hash_value}")

                # Calculate the time taken to receive the file
                start_time = time.time()
                self.receive_file("received.txt", tcp_socket)
                end_time = time.time()

                print(f"Time taken to receive file: {end_time - start_time} seconds")

                time.sleep(0.1)

                # Verify the hash value of the received file data
                calculated_hash = self.calculate_hash("received.txt")
                print(f"Calculated hash value: {calculated_hash}")

                success = False
                
                if calculated_hash == hash_value:
                    # Send a confirmation message to the server
                    time.sleep(0.1)
                    tcp_socket.send(b"received")
                    print(f"File received successfully.")
                    success = True
                else:
                    # Send an error message to the server
                    time.sleep(0.1)
                    tcp_socket.send(b"error")
                    print("Error: Hash value of received data does not match.")


                self.logging(file_size, end_time - start_time, success)
                    
                # Close the socket
                tcp_socket.close()


    def logging(self, file_size, time_taken, success):
        # Initialize the log file directory
        log_dir = "logs/"

        # Create the log file directory if it does not exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Initialize the log file
        log_file_name = f"client_{self.id+1}.log"
        with open(log_dir + log_file_name, "w") as log_file:
            # Log everything to the log file
            log_file.write(f"Date and time: {datetime.datetime.now()}\n")
            log_file.write(f"File size: {file_size} bytes\n")
            log_file.write(f"Time taken to receive file: {time_taken} seconds\n")
            log_file.write(f"Was the file received successfully? {success}\n")

    def calculate_hash(self, file_path):
        BLOCK_SIZE = 10 * 1024 * 1024
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BLOCK_SIZE)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()

    def receive_file(self, file_path, tcp_socket):
        BLOCK_SIZE = 10 * 1024 * 1024
        with open(file_path, 'wb') as f:
            while True:
                data = tcp_socket.recv(BLOCK_SIZE)
                if data.endswith(b"<EOF>"):
                    break
                f.write(data)
        

num_clients = input("Enter the number of clients: ")

for i in range(int(num_clients)):
    lock = threading.Lock()
    client = Client(i, lock)
    client.start()

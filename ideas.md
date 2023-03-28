threads to handle clients
``` python
def handle_client(client_socket):
    # open the file and read its contents
    with open(filename, 'rb') as f:
        file_contents = f.read()

    # send the file contents to the client
    client_socket.sendall(file_contents)

    # close the client socket
    client_socket.close()

# accept incoming client connections and start a new thread to handle each one
for i in range(num_clients):
    client_socket, client_address = server_socket.accept()
    print('Received connection from', client_address)

    # start a new thread to handle the client connection
    t = threading.Thread(target=handle_client, args=(client_socket,))
    t.start()
```
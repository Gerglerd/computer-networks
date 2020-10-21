import socket

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
serv_socket.bind(('0.0.0.0', 53210))
# socket to wait for connection, backlog - queue
serv_socket.listen(10)

# endlessly process incoming connections

while True:
    # accept() blocked until at least one connection appears in the queue of established connections
    client_socket, client_addr = serv_socket.accept()
    print('Address: ', client_addr)

    # until the client disconnects, we read the data transmitted to it and send it back

    while True:
        data = client_socket.recv(1024)
        if not data:
            # client off
            break
        client_socket.sendall(data)

    client_socket.close()

# You can connect to this server using the telnet console
# utility designed for text exchange of information over TCP
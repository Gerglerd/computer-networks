import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 5556))
sock.listen(10)
server_message = 'Hello'

while True:
    server_sock, server_addr = sock.accept()
    data = server_sock.recv(1024)
    if not data:
        break
    print('received message: ' + data.decode())
    data = data + server_message.encode()
    server_sock.send(data)

server_sock.close()
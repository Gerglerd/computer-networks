import socket

while True:
    # message = input()
    for i in range(500):
        message = i
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9091))
        sock.send(message.encode())
        message = sock.recv(1024)
        print('message from server: ' + message.decode())

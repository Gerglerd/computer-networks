import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9091))
while True:
    message = input()
    sock.send(message.encode())
    message = sock.recv(1024)
    print('message from server: ' + message.decode())

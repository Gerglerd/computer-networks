import socket
import time

message = 'Nice to meet u'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9091))
sock.send(message.encode())
time.sleep(2)
message = sock.recv(1024)
print('message from server: ' + message.decode())
sock.close()
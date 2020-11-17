import socket
from threading import Thread

serverAddress = ('localhost', 8017)


def disconnect(sock, login):
    print("closed: ", login)
    sock.send(bytes(login, 'utf8'))
    sock.close()
    exit(0)
    pass


def reciveMessage(sock, message):
    while True:
        message = sock.recv(1000)
        print(message.decode())


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(serverAddress)
    print("Enter login: ")
    login = input()
    print("Enter password: ")
    passwd = input()
    auth = login + '~' + passwd
    s.send(bytes(auth, 'utf8'))
    data = s.recv(1000)
    if data.decode('utf8') == 'correct':
        print('Correct!')
        break
    else:
        s.close()
        print('Incorrect login or password. Try again!')
try:
    recvThread = Thread(target=reciveMessage, args=(s, 'hello'))
    recvThread.start()

    while True:
        message = input()
        if message == "!disconnect":
            s.send(bytes(message, 'utf8'))
            disconnect(s, login)
        s.send(bytes(message, 'utf8'))

except KeyboardInterrupt:
    disconnect(s, login)

s.close()

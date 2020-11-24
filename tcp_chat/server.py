import socket
from threading import Thread

accounts = {
    '1': '1111',
    '2': '2222',
    '3': '3333'
}

online = {
    '1': False,
    '2': False,
    '3': False
}


def sendMessage(message, clientSockets):
    for clsock in clientSockets:
        clsock.send(bytes(message))
    pass


def autorization(clsock, clientSockets, online, accounts):
    while True:
        data = clsock.recv(1024)
        if checkUser(data, accounts, online):
            print('OK')
            clsock.send(bytes("correct", 'utf8'))
            clientSockets.append(clsock)
            print("client connected from: ", addr)
            break
        else:
            clsock.send(bytes("incorrect", 'utf8'))
    pass


def reciveMessage(clsock, clientSockets, online, accounts, message):
    autorization(clsock, clientSockets, online, accounts)
    while True:
        message = clsock.recv(1024)
        if len(message) == 0:
            user = clsock.recv(1024).decode()
            closeClient(clsock, clientSockets, online, user)
        else:
            if "!get" == message.decode():
                clsock.send(bytes(str(getOnlineUsers(online)), "utf8"))
            elif "!disconnect" == message.decode():
                usr = clsock.recv(1024).decode()
                closeClient(clsock, clientSockets, online, usr)
                break
            elif message:
                sendMessage(message, clientSockets)
                message = ''
    pass


def getOnlineUsers(online):
    onUsers = []
    for key, value in online.items():
        if value:
            onUsers.append(key)
    return onUsers


def isConnected(login, online):
    if online[login]:
        return True
    return False


def closeClient(clsock, clientSockets, online, user):
    online[user] = False
    clientSockets.remove(clsock)
    clsock.close()
    pass


def checkUser(authorization, account, online):
    loginPasswd = authorization.decode('utf8').split('~')
    if isConnected(loginPasswd[0], online):
        return False
    if loginPasswd[0] in account.keys():
        print('login ok')
        if loginPasswd[1] == account[loginPasswd[0]]:
            online[loginPasswd[0]] = True
            print('passwd ok')
            return True
    return False


clientSockets = []
MAX_CLIENTS = 10
address = ('localhost', 8017)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(address)
sock.listen(MAX_CLIENTS)

while True:
    conn, addr = sock.accept()
    print(conn)
    threadRecv = Thread(target=reciveMessage, args=(conn, clientSockets, online, accounts, 'hello'))
    threadRecv.start()

sock.close()

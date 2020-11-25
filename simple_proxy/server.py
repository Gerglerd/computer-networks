import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создание нового сокета и возвращение fd
sock.bind(('localhost', 5555))  # связать сокет с IP-адресом и портом
sock.listen(10)  # слушать порт и ожидать когда будет установлено соеденение
server_message = '(this message from server)\n'
conn, addr = sock.accept()  # запрос на установление соеденения с клиентом

while True:
    data = conn.recv(1024)  # получить данные из сети
    if not data:
        break
    print('received message: ' + data.decode())
    data = data + server_message.encode()
    conn.send(data)  # отправить данные по сети

print('Server closed')
conn.close()

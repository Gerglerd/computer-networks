import socket
import select
import time
import sys

buffer_size = 4096
delay = 0.0001
forward_to = ('localhost', 5556)  # connection with server


class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        self.forward.connect((host, port))
        return self.forward


class Server:
    input_list = []
    channel = {}

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(20)

    def mail_loop(self):
        self.input_list.append(self.server)

        while 1:
            time.sleep(delay)
            inputready, outputready, exceptready = select.select(self.input_list, [], [])

            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                self.data = self.s.recv(buffer_size)

                if len(self.data) == 0:
                    self.on_close()
                    break

                else:
                    self.on_recv()


    def on_accept(self):
        forward = Forward().start(forward_to[0], forward_to[1]) #socket connect to server
        client_socket, client_addr = self.server.accept()

        if forward:
            print(client_addr, "connected")
            self.input_list.append(client_socket)
            self.input_list.append(forward)
            self.channel[client_socket] = forward
            self.channel[forward] = client_socket

        else:
            print("Can't establish connection with remote server. "
                  "Closing connection with client side:", client_addr)
            client_socket.close()

    def on_close(self):
        print(self.s.getpeername(), "disconnected")
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        self.channel[out].close()
        self.channel[self.s].close()
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
        print(data.decode())
        self.channel[self.s].send(data)

if __name__ == '__main__':
    server = Server('localhost', 9091)
    try:
        server.mail_loop()
    except KeyboardInterrupt:
        print("Cntr+C to stop server")
        sys.exit(1)

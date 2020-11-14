import socket
import select
import sys
import queue

buffer_size = 4096
forward_to = ('localhost', 5556)  # connect to server


# Establishes a connection between the proxy server and the target server
class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        self.forward.connect((host, port))
        return self.forward


# main class
class TheServer:
    input_list = []
    output_list = []
    message_queue = {}

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(20)

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            readable, writable, exceptional = select.select(self.input_list, self.output_list, self.input_list)
            for self.s in readable:
                if self.s is self.server:
                    if self.s == self.server:
                        self.on_accept()
                        break
                    self.data = self.s.recv(buffer_size)
                    if len(self.data) == 0:
                        self.on_close()
                        break
                    else:
                        self.on_recv()
            for self.s in writable:
                try:
                    next_message = self.message_queue[self.s].get_nowait()
                except queue.Empty:
                    self.output_list.remove(self.s)
                else:
                    self.s.send(next_message)
            for self.s in exceptional:
                print(sys.stderr, 'handling exceptional condition for\n')
                self.input_list.remove(self.s)
                if self.s in self.output_list:
                    self.output_list.remove(self.s)
                self.on_close()

    def on_accept(self):
        forward = Forward().start(forward_to[0], forward_to[1])  # socket connect to server
        client_socket, client_addr = self.server.accept()  # proxy connect to client
        if forward:
            print(client_addr, "has connected")
            self.input_list.append(client_socket)
            self.input_list.append(forward)
            self.message_queue[client_socket] = forward
            self.message_queue[forward] = client_socket
        else:
            print("Can't establish connection with remote server.")
            print("Closing connection with client side: ", client_addr)
            client_socket.close()

    def on_close(self):
        print(self.s.getpeername(), " has disconnected")
        # remove objects from input_list
        self.input_list.remove(self.s)
        self.input_list.remove(self.message_queue[self.s])
        out = self.message_queue[self.s]
        # close the connection with client
        self.message_queue[out].close()  # equivalent to do self.s.close()
        # close the connection with remote server
        self.message_queue[self.s].close()
        # delete both objects from channel dict
        del self.message_queue[out]
        del self.message_queue[self.s]

    def on_recv(self):
        data = self.data
        # here we can parse and/or modify the data before send forward
        print(data.decode())
        self.message_queue[self.s].send(data)


if __name__ == '__main__':
    server = TheServer('', 9091)
    try:
        server.main_loop()
    except KeyboardInterrupt:
        print("Ctrl C - Stopping server")
        sys.exit(1)

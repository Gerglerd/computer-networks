import socket
import select
import sys
import queue

buffer_size = 4096
forward_to = ('localhost', 5556)


class Forward:

    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        self.forward.connect((host, port))
        return self.forward


class TheServer:
    inputs = []
    outputs = []
    message_queues = {}

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(20)

    def main_loop(self):

        self.inputs.append(self.server)

        while self.inputs:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)

            for self.s in readable:
                if self.s is self.server:
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
                    next_msg = self.message_queues[self.s].get_nowait()
                except queue.Empty:
                    # No messages waiting so stop checking for write.
                    print('output queue for ', s.getpeername(), ' is empty')
                    self.outputs.remove(s)
                else:
                    print('sending "%s" to %s ' % (next_msg, s.getpeername()))
                    s.send(next_msg)

            for s in exceptional:
                print('handling exceptional condition for ', s.getpeername())
                # Stop listening for input on the connection
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()

                # Remove message queue
                del self.message_queues[s]

    def on_accept(self):

        forward = Forward().start(forward_to[0], forward_to[1])  # socket conn to server
        clientsock, clientaddr = self.server.accept()  # proxy connects to client

        if forward:
            print(clientaddr, "connected")
            self.inputs.append(clientsock)
            self.inputs.append(forward)
            self.message_queues[clientsock] = forward
            self.message_queues[forward] = clientsock
        else:
            print("Can't establish connection with remote server. ", )
            print("Closing connection with client side", clientaddr)
            clientsock.close()

    def on_close(self):

        print(self.s.getpeername(), "disconnected")
        self.inputs.remove(self.s)
        self.inputs.remove(self.message_queues[self.s])
        out = self.message_queues[self.s]
        self.message_queues[out].close()
        self.message_queues[self.s].close()
        del self.message_queues[out]
        del self.message_queues[self.s]

    def on_recv(self):
        data = self.data
        print(data.decode())
        self.message_queues[self.s].send(data)


if __name__ == '__main__':
    server = TheServer('localhost', 9091)
    try:
        server.main_loop()
    except KeyboardInterrupt:
        print("Ctrl C - Stopping server")
        sys.exit(1)

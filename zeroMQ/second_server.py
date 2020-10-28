import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:4050")

while True:
    # wait next request
    message = socket.recv()
    print("Received request 2: %s" % message)
    # working
    time.sleep(2)
    # send reply back
    socket.send(message)

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5000")

while True:
    # wait next request
    message = socket.recv()
    print("Received request 1: %s" % message)
    # working
    time.sleep(1)
    # send reply back
    socket.send(message)

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    # wait next request
    message = socket.recv()
    print("Received request: %s" % message)
    # working
    time.sleep(0.5)
    # send reply back
    socket.send(message)

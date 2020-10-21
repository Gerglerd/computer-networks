import time
import zmq
from pip._vendor.distlib.compat import raw_input

context = zmq.Context()

# socket connect to server
print("Connecting to server...")
socket = context.socket(zmq.REQ)
n = raw_input('server number > ')
socket.bind("tcp://localhost:5000" + n)  # accept connections on a socket

while True:
    # wait next request
    message = socket.recv()
    print("Received request: %s" % message)
    # working
    time.sleep(0.5)
    # send reply back
    socket.send(message)
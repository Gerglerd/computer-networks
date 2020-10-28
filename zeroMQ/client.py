import zmq

context = zmq.Context()

print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5000")
socket.connect("tcp://127.0.0.1:4050")

# do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s ..." % request)
    socket.send(str.encode('message' + str(request)))

    # get reply
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))

socket.close()

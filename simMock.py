import socket
import zmq
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:8000")

fucku = {}
for i in range(80000):
    fucku[i] = 'suck it' + str(i)

while True:
    socket.send_string(str(fucku))
    for key in fucku:
        fucku[key] = 'suck it' + str(random.randint(0, 10))
    time.sleep(.1)

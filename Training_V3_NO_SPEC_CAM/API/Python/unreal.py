import zmq
import time
import random
import numpy as np
import cv2
import io

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:12345")
print("Connected")
while True:
    #sleep(1)
    print("Waiting for recv...")
    frame = socket.recv()
    print("Received frame: ")
    print(frame)
    #source = np.load(io.BytesIO(frame))
    #cv2.imshow(source)
    #cv2.waitKey(1)

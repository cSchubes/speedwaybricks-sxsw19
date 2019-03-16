import sys
import zmq
import cython_client as client
import cv2
context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect ("tcp://192.168.253.14:1000")
socket.setsockopt_string(zmq.SUBSCRIBE, '')
cnt = 0
while True:
    
    
    img_bytes = socket.recv(19200)
    
    img = client.proc(img_bytes)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow('aiiioi'+str(cnt%8),img)
    cv2.waitKey(1)
    cnt+=1

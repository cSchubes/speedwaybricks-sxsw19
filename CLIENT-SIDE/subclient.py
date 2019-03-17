import sys
import zmq
import sys
import cython_client as client
import cv2
import os

images=[[],[],[],[],[],[],[],[]]
context = zmq.Context()
socket = context.socket(zmq.SUB)
file = open('ip_set.txt')
lines = file.read().splitlines()

socket.connect ('tcp://'+lines[0]+':1007')
print('connected')
socket.setsockopt_string(zmq.SUBSCRIBE, str(''))

def client_thread():
    global socket
    cnt = 0
##    while True:
##        
##        check_var = socket.recv()
##        
##        if socket.recv() == b'\x0ff':
##            
##            break
    imgs = []
    for i in range(8):
        
        
        img_bytes = socket.recv(19200)
    ##    print(img_bytes)
        img = client.proc(img_bytes)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #cv2.imshow('aiiioi'+str(cnt%8),img)
        #cv2.waitKey(1)
        imgs.append(img)
    return imgs


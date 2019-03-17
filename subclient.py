import sys
import zmq
import sys
import cython_client as client
import cv2
import os
import numpy as np
from timeit import default_timer as timer

images=[[],[],[],[],[],[],[],[]]
context = zmq.Context()
socket = context.socket(zmq.SUB)
file = open('ip_set.txt')
lines = file.read().splitlines()
file.close()

socket.connect ('tcp://'+lines[0]+':1007')
print('connected')
socket.setsockopt_string(zmq.SUBSCRIBE, str(''))
imgs = [np.zeros((80,80,3)) for i in range(8)]

def client_thread():
    global socket
    global imgs
    cnt = 0
##    while True:
##        
##        check_var = socket.recv()
##        
##        if socket.recv() == b'\x0ff':
##            
##            break
    for i in range(8):
        img_bytes = socket.recv(19200)
        # print(img_bytes)
        img = client.proc(img_bytes)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # cv2.imshow('aiiioi'+str(cnt%8),img)
        #cv2.waitKey(1)
        # imgs.append(img)
        imgs[i] = img
    return imgs


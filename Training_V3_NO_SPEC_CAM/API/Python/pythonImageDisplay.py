import socket
import cv2
import cython_client as client
import cython_client360 as client360

from datetime import datetime as dt
from threading import Thread
import zmq
import io
import numpy as np
import traceback

context = zmq.Context()
socketer = context.socket(zmq.PUB)
socketer.bind("tcp://0.0.0.0:1007")

ready = [0,0,0,0,0,0,0,0]
bytearr  = ready.copy()
def zmq_PUB(socketer):
    global ready
    global bytearr
    while True:
        
        
        
        check = 1
        for i in ready:
            if i:
                
                continue
            else:
               check = 0
               break
        if check:
            #socketer.send(b'\x0ff')
            for i in bytearr:
               socketer.send(i)
               
            ready=[0,0,0,0,0,0,0,0]
        
def launchSocket(s, port, posX, posY, is360p):
    ##cv2.namedWindow(str(port))
    ##cv2.moveWindow(str(port), posX, posY)
    # times = []
    recvnum = 0
    global ready
    global bytearr
    #no termination characters are sent; just straight bytes
    while(True):
        try:
            
            tsum = 0
            # tbad = False
            size = 19200
            if is360p:
                size = 480*360*3
            someData = s.recv(size)
            bytearr[int((posX-100)/100)] = someData
            ready[int((posX-100)/100)]=1
            f = io.BytesIO()
            # t1 = dt.now().microsecond

            if is360p:
                img = client360.proc(someData)
            else:
                img = client.proc(someData)
        
            
            # t2 = dt.now().microsecond
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            #cv2.imshow(str(port), img)

            ### image saving: ###
            #cv2.imwrite("picOutput/im_" + str(port) + "_" + str(recvnum) + ".png", img)
            recvnum = recvnum + 1
            #cv2.waitKey(1)

            # if t2-t1 >3:
            #     tsum+= t2-t1
            # else:
            #     tbad=True
            # if not tbad:
            #     times.append(tsum)
        except Exception as e:
            print("ERROR: %s" % (e))
            traceback.print_exc()
            #print("RecvNum: " + str(recvnum))
publisher = Thread(target=zmq_PUB,args=(socketer,))
publisher.start()
for i in range(0, 8):
    port = 12300 + i
    s = socket.socket()
    address = '127.0.0.1'
    try:
        s.connect((address, port))
    except Exception as e:
        print("something's WRONG with %s:%d. Exception is %s" % (address, port, e))
        s.close()
        break

    print("CONNECTED TO PORT " + str(port))
    thread = Thread(target=launchSocket,args=(s, port, 100 + 100 * i, 200, i >= 8,))
    
    thread.start()

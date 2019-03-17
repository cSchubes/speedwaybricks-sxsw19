import numpy as np
import cv2
from datetime import datetime as dt
DTYPE = np.intc
img = np.zeros((80,80,3),dtype = DTYPE)
cdef int[:,:,:] img_view = img
#print(img)
cdef int num_pixels = 6400

def proc(pixelBytes):
    #t1 = dt.now().microsecond
    bytes_out = b''
    cdef int i = 0
    cdef int x = 0
    cdef int y = 0
    cdef int xy_cnt = 0
    cdef int num_bytes = 80*80*3
    #for i in range(int(num_pixels)):
    #    bytes_out+=input_bytes
    bytes_out=pixelBytes
    i=0
    xy_cnt = 0
    
    global img_view
    global img
    while i<num_bytes:
        x = int(xy_cnt/80)
        y = int(xy_cnt%80)
        #print(bytes_out[i],bytes_out[i+1],bytes_out[i+2])
        
        img_view[x,y,0] = bytes_out[i]
        img_view[x,y,1] = bytes_out[i+1]
        img_view[x,y,2] = bytes_out[i+2]
        i+=3
        xy_cnt+=1
    
    img = np.asarray(img_view,dtype = np.uint8)
    #print(img)
    return img
    #t2 = dt.now().microsecond
    
    #print('time',t2-t1)
    #cv2.imshow('a',img)

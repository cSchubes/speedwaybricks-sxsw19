import numpy as np
import cv2
from datetime import datetime as dt
input_bytes = b'\xff\x00\x00'
img_shape = (80,80,3)
img = np.zeros((80,80,3),dtype = np.uint8)
#print(img)
num_pixels = img_shape[0]*img_shape[1]
bytes_out = b''

for i in range(int(num_pixels)):
    bytes_out+=input_bytes
i=0
xy_cnt = 0
t1 = dt.now().microsecond
while i<len(bytes_out):
    y = int(xy_cnt/80)
    x = int(xy_cnt%80)
    #print(bytes_out[i],bytes_out[i+1],bytes_out[i+2])
    
    img[x,y,0] = bytes_out[i]
    img[x,y,1] = bytes_out[i+1]
    img[x,y,2] = bytes_out[i+2]
    i+=3
    xy_cnt+=1
t2 = dt.now().microsecond
print('time',t2-t1)
cv2.imshow('a',img)

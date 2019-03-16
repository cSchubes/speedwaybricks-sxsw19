import numpy as np
import io
import cv2
img2 = cv2.imread('cmp.jpg')
s = b'\x86\xbb\xc4\x85\xba\xc3\x84\xba\xc3\x84\xba\xc3\x83\xb9\xc2\x82\xb9\xc2\x82\xb9\xc2\x81\xb8\xc1\x81\xb9\xc1\x80\xb8\xc1\x80\xb8\xc0\x7f\xb7\xc0\x7f\xb7\xc0\x7f\xb7\xbf~\xb7\xc0~\xb7\xbf~\xb7\xbf~\xb6\xbf'
f = io.BytesIO()
bytes_boi=np.frombuffer(s, np.uint8)
total_no = len(bytes_boi)/3
bytes_boi = np.array_split(bytes_boi,len(bytes_boi)/3)
r=[]
b=[]
g=[]
for i in range(total_no):
    
print(np.reshape(bytes_boi,(3,int(total_no))))
print(img2)
##img = cv2.imdecode(np.frombuffer(s, np.uint8),
##print(img)

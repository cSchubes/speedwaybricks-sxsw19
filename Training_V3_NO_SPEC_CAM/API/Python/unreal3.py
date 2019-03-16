import cv2
import cython_client as client

recvnum = 0

#no termination characters are sent; just straight bytes
while(True):
    recvnum = recvnum + 1
    #print("RecvNum: " + str(recvnum))
    #cv2.imshow("This better work", client.proc(someData))
    cv2.imshow("This better work", client.proc())
    cv2.waitKey(1)

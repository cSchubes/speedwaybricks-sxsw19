import socket
import cv2
import cython_client as client
import matplotlib.pyplot as plt
from datetime import datetime as dt
s = socket.socket()
address = '127.0.0.1'
port = 12300  # port number is a number, not string
times = []
try:
    s.connect((address, port))
    # originally, it was
    # except Exception, e:
    # but this syntax is not supported anymore.
except Exception as e:
    print("something's wrong with %s:%d. Exception is %s" % (address, port, e))
    s.close()


recvnum = 0
#no termination characters are sent; just straight bytes
while(True):
    try:
        tsum = 0
        tbad = False
        recvnum = recvnum + 1
        #print("RecvNum: " + str(recvnum))
        for i in range(1):
            someData = s.recv(19200)
            t1 = dt.now().microsecond
            img = client.proc(someData)
            t2 = dt.now().microsecond
            cv2.imshow(str(port), img)
            cv2.waitKey(1)
            if t2-t1 >3:
                tsum+= t2-t1
            else:
                tbad=True
        if not tbad:
            times.append(tsum)
    except:
        print("RecvNum: " + str(recvnum))
        # plt.plot(times)
        # plt.xlabel('Iterations')
        # plt.ylabel('Time Taken (Microseconds)')
        # plt.title('Parsing Times')
        # axes = plt.gca()
        # axes.set_ylim([0,10000])
        # plt.show()

    #print(someData[-1])
    #cv2.imshow("This better work", client.proc(someData))
    #cv2.imshow("This better work", client.proc())
    #cv2.waitKey(1)

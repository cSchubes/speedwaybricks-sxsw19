import sys
import zmq
import ast
import socket
import time
# import subclient
import cv2
from threading import Thread
parameters = {}

def update_params(socket):
    global parameters
    while True:
        parameters = ast.literal_eval(socket.recv_string())

class rover:

    def __init__(self):
        file = open('ip_set.txt')
        lines = file.read().splitlines()
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        print(lines[0])
        self.socket.connect ('tcp://'+lines[0]+':2510')
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        self.port_conn = '2509'
        self.lines = lines
        #self.socket2.bind(('0.0.0.0',2505))
        param_thread = Thread(target = update_params,args = (self.socket,))
        param_thread.start()
        time.sleep(1)

        
    def isOverride(self):
        global parameters
        return bool(int(parameters['ManualOverride']))
    def isDeadZone(self):
        global parameters
        return bool(int(parameters['DeadZone']))
    def getSignalStrength(self):
        global parameters
        return parameters['SignalStrength']
    def getLidars(self):
        global parameters
        return parameters['LIDAR1'],parameters['LIDAR2'],parameters['LIDAR3']
    def getVelocity(self):
        global parameters
        return parameters['VelocityX'],parameters['VelocityY'],parameters['VelocityZ']
    def getWaypoint(self):
        global parameters
        return parameters['WaypointX'],parameters['WaypointY'],parameters['WaypointZ']
    def getCurrentHeading(self):
        global parameters
        return parameters['CurrentHeading']
    def getLocation(self):
        global parameters
        return parameters['LocationX'],parameters['LocationY'],parameters['LocationZ']
    def getRoll(self):
        global parameters
        return parameters['Roll']
    def getPitch(self):
        global parameters
        return parameters['Pitch']
    def getYaw(self):
        global parameters
        return parameters['Yaw']
    def getAcceleration(self):
        global parameters
        return parameters['AccelerationX'],parameters['AccelerationY'],parameters['AccelerationZ']
    def setTgtSpeed(self,tgt_speed):
        self.socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket2.connect ((self.lines[0],int(self.port_conn)))
        self.socket2.sendall(('TargetSpeed'+','+str(tgt_speed)).encode())
    def setTgtHeading(self,tgt_head):
        self.socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket2.connect ((self.lines[0],int(self.port_conn)))
        self.socket2.sendall(('TargetHeading'+','+str(tgt_head)).encode())
    def setTurnErr(self,tgt_err):
        self.socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket2.connect ((self.lines[0],int(self.port_conn)))
        self.socket2.sendall(('TurnError'+','+str(tgt_err)).encode())
    def stop(self):
        self.socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket2.connect ((self.lines[0],int(self.port_conn)))
        self.socket2.sendall(('AllStop'+','+str(1).encode()))
    def start(self):
        self.socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect (self.lines[0]+':'+self.port_conn)
        socket2.send_string('AllStop'+','+str(0))
    def getHeightAt(self,x,y,train = False):
        f = open('meta','r')
        lines = f.read().splitlines()
        meta = []
        if train:
            meta = lines[0].split()
        else:
            meta = lines[1].split()
        min_x = float(meta[0])
        max_x = float(meta[1])
        min_y = float(meta[2])
        max_y = float(meta[3])
        min_z = float(meta[4])
        min_z = float(meta[5])
        w = int(meta[6])
        h = int(meta[7])
        img_name = meta[8]
        img= cv2.imread(img_name)
        x = int(((abs(min_x)+x)/(max_x + abs(min_x)))*w)
        y = int(((abs(min_y)+y)/(max_y + abs(min_y)))*h)
        return img[x][y]
    
    # def getImgs(self):
    #     return subclient.client_thread()

if __name__=="__main__":
    rover_obj = rover()
    i=0
    while True:
        pass
        # print("Location ", rover_obj.getLocation())
        # print("RPY ", rover_obj.getRoll(), rover_obj.getPitch(), rover_obj.getYaw())
        # print("LIDARS ", rover_obj.getLidars())
        # rover_obj.setTgtSpeed(400)
        # print(dir(rover_obj))
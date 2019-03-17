import sys
import zmq
import ast
import socket
import time
import subclient
import cv2

def update_params(socket):
    return ast.literal_eval(socket.recv_string())
    
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
        
        self.params = ast.literal_eval(self.socket.recv_string())
        
    def update(self):
        # remake socket
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect ('tcp://'+self.lines[0]+':2510')
        socket.setsockopt_string(zmq.SUBSCRIBE, '')
        # update params
        self.params = ast.literal_eval(socket.recv_string())

    def isOverride(self):
        return bool(int(self.params['ManualOverride']))
    def isDeadZone(self):
        return bool(int(self.params['DeadZone']))
    def getSignalStrength(self):
        return self.params['SignalStrength']
    def getLIDARS(self):
        return self.params['LIDAR1'],self.params['LIDAR2'],self.params['LIDAR3']
    def getVelocity(self):
        return self.params['VelocityX'],self.params['VelocityY'],self.params['VelocityZ']
    def getWaypoint(self):
        return self.params['WaypointX'],self.params['WaypointY'],self.params['WaypointZ']
    def getCurrentHeading(self):
        return self.params['CurrentHeading']
    def getLocation(self):
        return self.params['LocationX'],self.params['LocationY'],self.params['LocationZ']
    def getRoll(self):
        return self.params['Roll']
    def getPitch(self):
        return self.params['Pitch']
    def getYaw(self):
        return self.params['Yaw']
    def getAcceleration(self):
        return self.params['AccelerationX'],self.params['AccelerationY'],self.params['AccelerationZ']
        
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
    def getImgs(self):
        return subclient.client_thread()
        
if __name__=="__main__":
    rover_obj = rover()
    i=0
    
    while True:
            pass
        
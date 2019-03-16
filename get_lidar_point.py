import numpy
import math

def find_robot_transform(robot_pos, robot_or):
    # robot_pos = [x, y, z], in meters in the globabl frame
    # robot_or = [roll, pitch, yaw] in degrees in globabl framw
    # returns a 4x4 array - the homogenous transformation matrix

    roll = math.radians(robot_or.r)
    pitch = math.radians(robot_or.p)
    yaw = math.radians(robot_or.y)

    R = numpy.array([[math.cos(yaw)*math.cos(pitch), math.cos(yaw)*math.sin(pitch)*math.sin(roll) - math.sin(yaw)*math.cos(roll), math.cos(yaw)*math.sin(pitch)*math.cos(roll) + math.sin(yaw)*math.sin(roll), robot_pos[0]],
                     [math.sin(yaw)*math.cos(pitch), math.sin(yaw)*math.sin(pitch)*math.sin(roll) + math.cos(yaw)*math.cos(roll), math.sin(yaw)*math.sin(pitch)*math.cos(roll) - math.cos(yaw)*math.sin(roll), robot_pos[1]],
                     [-1*math.sin(pitch), math.cos(pitch)*math.sin(roll), math.cos(pitch)*math.cos(roll), robot_pos[2]],
                     [0, 0, 0, 1]])

    return R

def find_lidar_point(robot_transform, lidar_yaw, lidar_dist):
    # robot_transform = 4x4 transform
    # lidar_yaw = one of {-30, 0, 30}, which lidar it is (degrees)
    # lidar_dist = the lidar range, in meters
    # returns a vector [x, y, z] in meters in the global frame.

    lidar_angle = math.radians(lidar_yaw)

    T = numpy.array([[math.cos(lidar_angle), -1*math.sin(lidar_angle), 0, 0],
                     [math.sin(lidar_angle), math.cos(lidar_angle), 0, 0,],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])
    
    

    D = numpy.array([[1, 0, 0, lidar_dist],
                     [0, 1, 0, 0,],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

    lidar_transform = numpy.matmul(robot_transform, numpy.matmul(T, D))
    lidar_point = [lidar_transform[0,3], lidar_transform[1,3], lidar_transform[2,3]]

    return lidar_point

class LidarTracker:
    prev_dist = float()
    new_dist = float()

    def __init__(self):
        self.prev_dist = 0

    def lidar_hit_object(self, new_data):
        # new_data is the newest lidar data (distance)
        # returns true if we want this new data to count (object, ground)
        # returns false if data is -1, or if its the same as last time

        if((abs(new_data - self.prev_dist) <= 0.001) or (new_data == -1)):
            return False
        else:
            # valid point, save this distance and get out
            self.prev_dist = new_data
            return True

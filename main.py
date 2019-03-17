import sys
import time
import math
from timeit import default_timer as timer
# api
from subapi import rover as RoverAPI
from multiprocessing import Process, Queue
# custom imports
from rover_lib import *
from parameters import deadzone_params
from classifier import Classify
from deadzone import GradientDescent
import obstacle_avoidance as oa
from get_lidar_point import *
from object_registry import ObjectRegistry

ARTIFACT_PATH='./models'
    
def get_state(rover: RoverAPI):
    state = RobotState(rover.getLocation(), rover.getCurrentHeading(), rover.getRoll(), rover.getPitch(), rover.getYaw())
    return state
    
def main(model='production.pkl'):
    # setup
    rover = RoverAPI()
<<<<<<< HEAD
    registry = ObjectRegistry()
    classify = Classify(ARTIFACT_PATH, model)
    DeadZoneController = None 
    classify_counter = 0
=======
    # registry = ObjectRegistry()
    classify = Classify(ARTIFACT_PATH, model)
    DeadZoneController = None 
    classify_counter = 0
    vel_counter = 0
    vel_buff = []
    avoid_obstacle = 0
    obs_timer = timer()
>>>>>>> 2f65c69cdf5c53c96f96cf158b47dcd4a11b2b1c
    
    # initial state
    rover.setTurnErr(0)
    rover.setTgtHeading(0)
    rover.setTgtSpeed(0)
    
    time.sleep(5)

    left_lidar_tracker = LidarTracker()
    middle_lidar_tracker = LidarTracker()
    right_lidar_tracker = LidarTracker()

    loc = rover.getLocation()
    waypoint = (loc[0] + 5000, loc[1] + 5000)
    # waypoint = rover.getWaypoint()
    
    camera_imgs = None
    while True:
        # run this guy at 1Hz
        start = timer()
        
        # CLASSIFY ##
        leftTerrain = -1
        rightTerrain = -1
        if classify_counter % 5 is 0:
            camera_imgs = rover.getImgs()
            camera_preds = []
            # may have to convert images here or change classify class
            for img in camera_imgs:
                camera_preds.append(classify.predict(img))
                
            leftPreds = [camera_preds[5][0], camera_preds[6][0], camera_preds[7][0]]
            rightPreds = [camera_preds[1][0], camera_preds[2][0], camera_preds[3][0]]
            
            leftTerrain = max(leftPreds, key=leftPreds.count)
            rightTerrain = max(rightPreds, key=rightPreds.count)
            
            print('--LEFT ' + str(leftTerrain))
            print('--RIGHT ' + str(rightTerrain))

        ## GET STATE ##
        rover.update()
        STATE = get_state(rover)
        dx = (waypoint[0] - STATE.location[0])
        dy = (waypoint[1] - STATE.location[1])
        dist = math.sqrt(dx*dx + dy*dy)

        ang = math.atan2(dy,dx) * 180 / math.pi
        spd = 0
        max_turn = 30

        delta_H = ang - STATE.heading
        if(delta_H <= -180):
            delta_H += 360
        elif(delta_H > 180):
            delta_H -= 360

        if abs(ang - STATE.heading) > 45:
            spd = 400
            rover.setTgtSpeed(spd)
            dH = max(-max_turn, min(delta_H,max_turn))
        elif abs(ang - STATE.heading) > 10:
            spd = 400
            rover.setTgtSpeed(spd)
            dH = max(-max_turn, min(delta_H,max_turn))
        else:
            spd = 400
            rover.setTgtSpeed(spd)
            dH = -1 * max(-max_turn, min(delta_H,max_turn))

        ## OBSTACLE CORRECTION ##
<<<<<<< HEAD
        lidar_points = list(rover.getLIDARS())
        if(left_lidar_tracker.lidar_hit_object(lidar_points[0])):
            obs_loc = location()
            obs_loc.setLocTup(find_lidar_point(find_robot_transform(STATE), 0, lidar_points[0]))
            registry.add((obs_loc.x, obs_loc.y, obs_loc.z))
        if(middle_lidar_tracker.lidar_hit_object(lidar_points[1])):
            obs_loc = location()
            obs_loc.setLocTup(find_lidar_point(find_robot_transform(STATE), 0, lidar_points[1]))
            registry.add((obs_loc.x, obs_loc.y, obs_loc.z))
        if(right_lidar_tracker.lidar_hit_object(lidar_points[2])):
            obs_loc = location()
            obs_loc.setLocTup(find_lidar_point(find_robot_transform(STATE), 0, lidar_points[2]))
            registry.add((obs_loc.x, obs_loc.y, obs_loc.z))
        # d = oa.obstacleCorrection(lidar_points, leftTerrain, rightTerrain)
        # d = oa.obstacleCorrection(lidar_points)
        # dH += d
        safe_heading = registry.determine_safe_heading(dH, STATE.location)
        print(dH)
        print(safe_heading)
        rover.setTgtHeading(safe_heading)
        # print(dH, dist)
        # print('D--%d'%d)
        # print(lidar_points)
        print(registry.purge(STATE.location, waypoint))
=======
        # lidar_points = list(rover.getLIDARS())
        # if(left_lidar_tracker.lidar_hit_object(lidar_points[0])):
        #     obs_loc = location()
        #     obs_loc.setLocTup(find_lidar_point(find_robot_transform(STATE), 0, lidar_points[0]))
        #     registry.add((obs_loc.x, obs_loc.y, obs_loc.z))
        # if(middle_lidar_tracker.lidar_hit_object(lidar_points[1])):
        #     obs_loc = location()
        #     obs_loc.setLocTup(find_lidar_point(find_robot_transform(STATE), 0, lidar_points[1]))
        #     registry.add((obs_loc.x, obs_loc.y, obs_loc.z))
        # if(right_lidar_tracker.lidar_hit_object(lidar_points[2])):
        #     obs_loc = location()
        #     obs_loc.setLocTup(find_lidar_point(find_robot_transform(STATE), 0, lidar_points[2]))
        #     registry.add((obs_loc.x, obs_loc.y, obs_loc.z))
            
        # print(lidar_points)    

        # if(not left_lidar_tracker.lidar_hit_object(lidar_points[0])): lidar_points[0] = 1000000
        # if(not middle_lidar_tracker.lidar_hit_object(lidar_points[1])): lidar_points[1] = 1000000
        # if(not right_lidar_tracker.lidar_hit_object(lidar_points[2])): lidar_points[2] = 1000000
        
        # print(lidar_points)

        # d = oa.obstacleCorrection(lidar_points, leftTerrain, rightTerrain)
        # d = oa.obstacleCorrection(lidar_points)
        # dH += d
        # safe_heading = registry.determine_safe_heading(dH, STATE.location)
        # print(dH)
        # print(safe_heading)
        
        vel = rover.getVelocity()
        if len(vel_buff) == 3:
            vel_buff[vel_counter%3] = sum([abs(num) for num in list(vel)])
            if timer() - obs_timer > 10:
                avoid_obstacle = 0
            if sum(vel_buff) / 3 < 10:
                avoid_obstacle += 1
        else:
            vel_buff.append(sum([abs(num) for num in list(vel)]))

        if avoid_obstacle == 0:
            rover.setTgtHeading(dH)
        else:
            obs_timer = timer()
            rover.setTgtHeading(dH+180)
            rover.setTgtSpeed(400)
            time.sleep(avoid_obstacle)
        # rover.setTgtHeading(STATE.heading + dH)
        # print(dH, dist)
        # print('D--%d'%d)
        # print(lidar_points)
        # print(registry.purge(STATE.location, waypoint))
>>>>>>> 2f65c69cdf5c53c96f96cf158b47dcd4a11b2b1c
        if dist < 1000:
            rov.setTgtSpeed(0)
            break

            
        ## WAYPOINT 2 WAYPOINT ##
        # if not rover.isDeadZone():
        #     # check for leaving dead zone
        #     if DeadZoneController is not None:
        #         DeadZoneController = None
            
        #     if not rover.isOverride():
        #         waypoint = rover.getWaypoint()
        #         print(waypoint)
        #         ### STUFF ###
                    
        # ## INSIDE DEADZONE ##
        # else:
        #     signal_strength = rover.getSignalStrength()
        #     # check for entering deadzone
        #     if DeadZoneController is None:
        #         DeadZoneController = GradientDescent(signal_strength, 
        #                                             STATE, deadzone_params)
        #         # rover.setWaypoint(-1, -1, -1)
        #     heading = DeadZoneController.get_next_step(STATE, signal_strength)
            ## STUFF
            
        # confirm we are running at 1Hz
        # and check if we are running over
        print(timer() - start)
        print('--------------')
        classify_counter += 1
<<<<<<< HEAD
=======
        vel_counter += 1
>>>>>>> 2f65c69cdf5c53c96f96cf158b47dcd4a11b2b1c
        while timer() - start < 0.25:
            pass

if __name__=='__main__':
    if len(sys.argv) > 1:
        main(model=sys.argv[1]) 
    else:
        main()

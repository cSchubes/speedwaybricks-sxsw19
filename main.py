import sys
import time
import math
from timeit import default_timer as timer
# api
from subapi import rover as RoverAPI
# custom imports
from rover_lib import *
from parameters import deadzone_params
from classifier import Classify
from deadzone import GradientDescent
import obstacle_avoidance as oa

ARTIFACT_PATH='./models'
    
def get_state(rover: RoverAPI):
    state = RobotState(rover.getLocation(), rover.getCurrentHeading())
    return state

def main(model='production.pkl'):
    # setup
    rover = RoverAPI()
    classify = Classify(ARTIFACT_PATH, model)
    DeadZoneController = None 
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
    while True:
        # run this guy at 1Hz
        start = timer()

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
        lidar_points = rover.getLIDARS()
        if(not left_lidar_tracker.lidar_hit_object()): lidar_points[0] = 1000000
        if(not middle_lidar_tracker.lidar_hit_object()): lidar_points[1] = 1000000
        if(not right_lidar_tracker.lidar_hit_object()): lidar_points[2] = 1000000
        dH += oa.obstacleCorrection(lidar_points)
        rover.setTgtHeading(STATE.heading + dH)
        # print(dH, dist, spd)

        if dist < 1000:
            rov.setTgtSpeed(0)
            break

        # CLASSIFY ##
        camera_imgs = rover.getImgs()
        camera_preds = []
        # may have to convert images here or change classify class
        for img in camera_imgs:
            camera_preds.append(classify.predict(img))
            
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
        while timer() - start < 0.5:
            pass

if __name__=='__main__':
    if len(sys.argv) > 1:
        main(model=sys.argv[1]) 
    else:
        main()

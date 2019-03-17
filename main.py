import sys
import time
from timeit import default_timer as timer
# api
# from subapi import rover as RoverAPI
import rover_mock as rover
from subapiTest import rover as RoverAPI
# custom imports
from rover_lib import *
from parameters import deadzone_params
from classifier import Classify
from deadzone import GradientDescent

ARTIFACT_PATH='./models'

def get_state(rover: RoverAPI):
    state = robot_state()
    # positions
    pose = rover.getLocation()
    pose += (rover.getRoll(),) # cast as tuples
    pose += (rover.getPitch(),)
    pose += (rover.getYaw(),)
    state.pose = poser(*pose) #tuple unpacking by position
    
    # velocity
    state.velocity = velocity_vect()
    state.velocity.setVelTup(rover.getVelocity())

    # acceleration
    state.acceleration = acceleration_vect()
    state.acceleration.setAccelTup(rover.getAcceleration())
    
    # heading
    state.heading = rover.getCurrentHeading()
    
    return state

def main(model='production.pkl'):
    # setup
    # rover = RoverAPI()
    classify = Classify(ARTIFACT_PATH, model)
    DeadZoneController = None 
    rov = RoverAPI()

    while True:
        # run this guy at 1Hz
        start = timer()
        rov.update()
        print(rov.test())

        ## GET STATE ##
        # STATE = get_state()
        
        ## CLASSIFY ##
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
        if timer() - start > 1:
            print('--BELOW 1HZ')
        print(timer() - start)
        while timer() - start < 1:
            pass

if __name__=='__main__':
    if len(sys.argv) > 1:
        main(model=sys.argv[1]) 
    else:
        main()
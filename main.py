import sys
import time
from timeit import default_timer as timer
# api
from subapi import rover as RoverAPI
# custom imports
from rover_lib import *
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
    rover = RoverAPI()
    classify = Classify(ARTIFACT_PATH, model)
    deadZoneHeading = None 

    while True:
        # run this guy at 1Hz
        start = timer()

        ## GET STATE ##
        STATE = get_state()
        
        ## CLASSIFY ##
        camera_imgs = rover.getImgs()
        camera_preds = []
        # may have to convert images here or change classify class
        for img in camera_imgs:
            camera_preds.append(classify.predict(img))
        
        ## WAYPOINT 2 WAYPOINT ##
        if not rover.isDeadZone():
            if not rover.isOverride():
                    
                waypoint = rover.getWaypoint()
                print(waypoint)
                ### STUFF ###
                    
        ## INSIDE DEADZONE ##
        else:
            if deadZoneHeading is None:
                deadZoneHeading = GradientDescent(...)
                # rover.setWaypoint(-1, -1, -1)
            signal_strength = rover.getSignalStrength()
            heading = deadZoneHeading.get_next_step(STATE, signal_strength)
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
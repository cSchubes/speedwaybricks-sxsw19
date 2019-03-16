import sys
import time
from classifier import Classify
from timeit import default_timer as timer
from subapi import rover as roverAPI
# import rover_mock as rover

ARTIFACT_PATH='./models'

def main(model='production.pkl'):
    # setup
    classify = Classify(ARTIFACT_PATH, model)
    rover = roverAPI()
    
    ## CONTROL LOOPS ##
    while not rover.isDeadZone():
        if not rover.isOverride():
            # run this guy at 1Hz
            start = timer()
            
            # classify camera images
            camera_imgs = rover.getImgs()
            print(timer() - start)
            camera_preds = []
            # may have to convert images here or change classify class
            for i in range(len(camera_imgs)):
                temp_img = camera_imgs[i]
                camera_preds.append(classify.predict(temp_img))
                
            # confirm we are onlyhot running at 1Hz
            # and check if we are running over
            if timer() - start > 1:
                print('--BELOW 1HZ')
            print(timer() - start)
            while timer() - start < 1:
                pass
    while rover.isDeadZone():
        # run this guy at 1Hz
        start = timer()
        
        # do stuff here
       
        signal = rover.getSignalStrength()
        
        while timer() - start < 1:
            pass

if __name__=='__main__':
    if len(sys.argv) > 1:
        main(model=sys.argv[1]) 
    else:
        main()
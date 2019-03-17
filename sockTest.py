from subapiTest import rover as RovAPI
import time

rover = RovAPI()

while True:
    print(rover.test())
    time.sleep(.5)
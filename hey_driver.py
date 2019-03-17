import subapi2 as api
import rover_lib as lib
import math
import numpy
from timeit import default_timer as timer
import obstacle_avoidance as oa

if __name__=="__main__":
    rov = api.rover()
    heading = rov.getCurrentHeading()
    loc = rov.getLocation()
    waypoint = (loc[0] + 5000, loc[1] + 5000)
    print(loc, waypoint)
    rov.setTurnErr(0)
    rov.setTgtHeading(0)
    rov.setTgtSpeed(0)
    start = timer()
    print("wait")
    while timer() - start < 5:
        pass
    while True:
        start = timer()

        loc = rov.getLocation()
        dx = (waypoint[0] - loc[0])
        dy = (waypoint[1] - loc[1])
        dist = math.sqrt(dx*dx + dy*dy)

        ang = math.atan2(dy,dx) * 180 / math.pi
        spd = 0
        max_turn = 30
        # get obstacle ang
        if abs(ang - rov.getCurrentHeading()) > 45:
            spd = 400
            rov.setTgtSpeed(spd)
            dH = max(-max_turn, min((ang - rov.getCurrentHeading()),max_turn))
        elif abs(ang - rov.getCurrentHeading()) > 10:
            spd = 400
            rov.setTgtSpeed(spd)
            dH = max(-max_turn, min((ang - rov.getCurrentHeading()),max_turn))
        else:
            spd = 400
            rov.setTgtSpeed(spd)
            dH = -1 * max(-max_turn, min((ang - rov.getCurrentHeading()),max_turn))

        dH += oa.obstacleCorrection(rov.getLIDARS())
        rov.setTgtHeading(rov.getCurrentHeading() + dH)
        print(dH, dist, spd)

        if dist < 1000:
            rov.setTgtSpeed(0)
            break

        while timer() - start < 0.25:
            pass


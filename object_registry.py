from rover_lib import location, relative_heading
import math

GAIN = 100
class ObjectRegistry:

    def __init__(self):
        self.registry = []

    def add(self, point):
        self.registry.append([point, 0])

    def determine_safe_heading(self, desired, rover_loc):
        des = int(desired)
        safe_heading = [i for i in range(0,360)]
        for ob in self.registry:
            obj = ob[0]
            heading = math.atan2((obj[1] - rover_loc[1]), (obj[0] - rover_loc[0])) * 180 / math.pi
            dist = math.sqrt( (obj[0] - rover_loc[0])**2 + (obj[1] - rover_loc[1])**2)
            GAIN = 0.1*dist
            radius = math.degrees(2*math.asin((GAIN/dist)))
            # radius = 180/(dist * math.pi)

            bound_l = int(heading - radius)
            bound_u = int(heading + radius)

            bounded = list(range(bound_l, bound_u))
            # print(bounded)
            safe_headings = [item for item in safe_heading if item not in bounded]
            safe_heading = safe_headings
            
            ob[1] += 1
            
        best_hdg = des+180
        for hdg in safe_heading:
            if abs(des - hdg) < abs(des - best_hdg):
                best_hdg = hdg

        return best_hdg

    def purge(self, rover_loc, waypoint):
        # call every step
        waypoint_vec = [waypoint[0]-rover_loc[0], 
                        waypoint[1]-rover_loc[1]]
        removeSet = []
        for i in range(len(self.registry)):
            obj = self.registry[i]
            print(obj)
            # if obj[0] - waypoint[0] < 0 and obj[1] - waypoint[1] < 0:
            if obj[1] > 15:
                removeSet.append(i)
                
        print(len(removeSet))
        for i in range(len(removeSet)-1, -1, -1):
            print(i)
            self.registry.pop(removeSet[i])
            
        return len(self.registry)



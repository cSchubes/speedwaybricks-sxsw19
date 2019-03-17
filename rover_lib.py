class location:
    x = float()
    y = float()
    z = float()

    def setLoc(self, xl, yl, zl):
        self.x = xl
        self.y = yl
        self.z = zl

    def setLocTup(self, loc_tuple):
        self.x = loc_tuple[0]
        self.y = loc_tuple[1]
        self.z = loc_tuple[2]

class acceleration_vect:
    x = float()
    y = float()
    z = float()

    def setAccel(self, xa, ya, za):
        self.x = xa
        self.y = ya
        self.z = za

    def setAccelTup(self, acc_tuple):
        self.x = acc_tuple[0]
        self.y = acc_tuple[1]
        self.z = acc_tuple[2]

class velocity_vect:
    x = float()
    y = float()
    z = float()
    
    def setVel(self, xv, yv, zv):
        self.x = xv
        self.y = yv
        self.z = zv

    def setVelTup(self, vel_tuple):
        self.x = vel_tuple[0]
        self.y = vel_tuple[1]
        self.z = vel_tuple[2]

class rotation:
    r = float()
    p = float()
    y = float()

    def setRot(self, roll, pitch, yaw):
        self.r = roll
        self.p = pitch
        self.y = yaw

    def setOrientTup(self, orient_tuple):
        self.r = orient_tuple[0]
        self.p = orient_tuple[1]
        self.y = orient_tuple[2]

class poser:
    position = location()
    orientation = rotation()

    def __init__(self, x, y, z, roll, pitch, yaw):
        self.position.x = x
        self.position.y = y
        self.position.z = z
        self.orientation.r = roll
        self.orientation.p = pitch
        self.orientation.y = yaw

    def setPose(self, x, y, z, roll, pitch, yaw):
        self.position.setLoc(x, y, z)
        self.orientation.setRot(roll, pitch, yaw)

    def setPoseTup(self, loc, roll, pitch, yaw):
        self.position.setLocTup(loc)
        self.orientation.setRot(roll, pitch, yaw)

class robot_command:
    speed = float()
    heading = float()
    heading_err = float()
    stop = bool()
    start = bool()

class RobotState:
    def __init__(self, location, heading):
        self.location = location
        self.heading = heading

def relative_heading(loc1, loc2):
    # Programmed to provide the relative heading vector from location 1 to location 2 where turning left is 0 -> -180 and right is 0 -> +180
    heading = math.atan2((loc2.y - loc1.y), (loc2.x - loc1.x)) * 180 / math.pi
    return heading

def xy_distance(loc1, loc2):
    distance = math.sqrt((loc2.x - loc1.x) * (loc2.x - loc1.x) + (loc2.y - loc1.y) * (loc2.y - loc1.y))
    return distance

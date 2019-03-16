import LowPassFilter


This basically just a filter to check to make sure the robot pitch
and roll angles do't change too fast. If they do, we probably hit an
obstacle.

## To implement: create one of these classes for pitch, and one for roll
## Then in every control loop cycle, get the new roll and pitch and call
## the "hit_object" funtion here with the new angle
## If it returns TRUE, take action (eg back up and turn)

class DetectObstacleCollision:
    def __init__(self, filter_coeff, first_angle, collision_delta):
        # filter_coeff = lowpass coefficient, reccomend like ... 2-10
        # first_angle = the initial robot state (no collisions at start)
        # colision_delta = angle change in 1 cycle that is considered collision
        self.angle_filter = LowPassFilter(filter_coeff)
        self.max_angle = collision_delta
        self.prev_angle = first_angle

    def hit_object(new_angle):
        delta_angle = angle_filter.filter(new_angle - self.prev_angle)
        self.prev_angle = new_angle

        if(abs(delta_angle) >= self.max_angle):
            return True

        return False

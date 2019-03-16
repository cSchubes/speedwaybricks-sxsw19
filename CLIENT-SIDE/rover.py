import waypoints
class Rover:
    
    def set_tgt_speed(self,tgt_speed):
        waypoints.setParam('TargetSpeed',tgt_speed)
    def set_tgt_heading(self,tgt_head):
        waypoints.setParam('TargetHeading',tgt_head)
    def set_turn_err(self,tgt_err):
        waypoints.setParam('TurnError',tgt_err)
    def stop(self):
        waypoints.setParam('AllStop',1)
    def start(self):
        waypoints.setParam('AllStop',0)
    def getVelocity(self):
        return waypoints.parameters['VelocityX'],waypoints.parameters['VelocityY'],waypoints.parameters['VelocityZ']
    def getWaypoint(self):
        return waypoints.parameters['WaypointX'],waypoints.parameters['WaypointY'],waypoints.parameters['WaypointZ']
    def getCurrentHeading(self):
        return waypoint.parameters['CurrentHeading']
    def getLocation(self):
        return waypoints.parameters['LocationX'],waypoints.parameters['LocationY'],waypoints.parameters['LocationZ']
    def getRoll(self):
        return waypoints.parameter['Roll']
    def getPitch(self):
        return waypoints.parameter['Pitch']
    def getYaw(self):
        return waypoints.paremeter['Yaw']
    def getAcceleration(self):
        return waypoints.parameters['AccelerationX'],waypoints.parameters['AccelerationY'],waypoints.parameters['AccelerationZ']
    



if __name__=="__main__":
    rover_obj = Rover()
    print(rover_obj.getLocation())

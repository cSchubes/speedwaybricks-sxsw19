import subapi as api
import rover_lib as lib
import math

if __name__=="__main__":
    rov = api.rover()
    goal_loc = lib.location(100, 100, 0)
    location = rov.getLocation()
    rov_state = lib.robot_state(lib.pose(location[0], location[1], location[2], rov.getRoll(), rov.getPitch(), rov.getYaw()))
    i=0

    while True:
        # Update robot state
        rov_state.pose.setPoseTup(rov.getLocation(), rov.getRoll(), rov.getPitch(), rov.getYaw())
        rov_state.heading = rov.getCurrentHeading()
        rov_state.acceleration.setAccelTup(rov.getAcceleration())
        rov_state.velocity.setVelTup(rov.getVelocity())

        print("Robot Heading ", rov_state.heading, " Robot Vel ", rov_state.velocity)

        # Obstacle calculations
        obs_dists = rov.getLidars()
        ######## call adam's range to point conversion 
        # for loc in obs_loc:
        #     obs_rel_heading[i] = relative_heading(rov_state.position, loc)
        for dist in obs_dists:
            obs_wt = numpy.sign(obs_dists.index(dist) - 1) * obs_gain / (dist*dist)
            tot_obs_wt += obs_wt

        print("Heading to goal ", lib.relative_heading(rov_state.position, goal), " Obstacle weight ", tot_obs_wt)

        # waypt_dist = lib.xy_distance(rov_state.position, goal_loc)
        # waypt_wt = (numpy.sign(lib.relative_heading(rov_state.position, goal) - rov_state.heading)) * waypt_wt / (waypt_dist * waypt_dist)
        goal_heading = lib.relative_heading(rov_state.position, goal) + tot_obs_wt

        rov.setTgtSpeed(50)
        rov.setTgtHeading(goal_heading)
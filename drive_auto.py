import subapi as api
import rover_lib as lib
import math
import numpy
import get_lidar_point

def get_desired_setpts(lidarMap, robot_pos, waypt):
	phi_des = 0
	# tuned parameters
	# a = 0; # higher a, higher need to keep current heading (avoid handling error)
	c = 10; # c controls dominance of obstacle
	u = 5; # u controls dominance of goal
	max_oa_rng = 2000; # cut-off repulsive distance

	for x in len(lidarMap)
		pt = lidarMap[x]
		euc_dist = (pt[0] - robot_pos[0])^2 + (pt[1] - robot_pos[1])^2 + (pt[2] - robot_pos[2])^2
		if euc_dist <= max_oa_rng:
			# find v_i of point
			v = c * (1/euc_dist^2)
		else:
			v = 0

		v_des_obs += v*[(pt[1]-robot_pos[1]) , (pt[0]-robot_pos[0])];

	v_des = u*[(waypt[1]-robot_pos[1]) , (waypt[0]-robot_pos[0])] - v_des_obs

	## TO DO +++++++++++++++++++++++++++
	# GET CURRENT TERRAIN - BOTTOM CAMERA [0] of terrainMap
	# terrain_curr = terrainMap[0]

	# Get SURROUNDING TERRAIN (AS SECTORS)
	# terrainMap.remove(terrainMap[0])
	# terrain_surr = terrainMap

	# LOOP THROUGH ALL SECTORS
	# DEFINE BETA_0 FOR EACH SECTOR BASED ON TERRAIN TYPE
	# BETA_0 = handling * exp(-del_phi) + velocity * gamma (tunable)
	# BETA IS ASSIGNED BASED ON GENERAL ATTRACTIVNESS OF TERRAIN

	phi_des = atan2( v_des[1] , v_des[0])
	vel_des = 200;

	# Find the terrain type in phi_des

	return [phi_des, vel_des]


if __name__=="__main__":
    rov = api.rover()
    # Set Waypoint
    way_pos = lib.location()
    way_pos.setLoc(1000, 1000, 0)
   
    rov_pos = rov.getLocation()
    rov_state = lib.robot_state(lib.poser(location[0], location[1], location[2], rov.getRoll(), rov.getPitch(), rov.getYaw()))

    # Euclidean distance to waypoint
    dist_way = math.sqrt( (way_pos[0] - rov_state.pose[0])^2 + (way_pos[1] - rov_state.pose[1])^2 +(way_pos[1] - rov_state.pose[1])^2 )

    while dist_way <= 0.1:
        # Update robot state
        rov_state.pose.setPoseTup(rov.getLocation(), rov.getRoll(), rov.getPitch(), rov.getYaw())
        rov_state.heading = rov.getCurrentHeading()
        rov_state.acceleration.setAccelTup(rov.getAcceleration())
        rov_state.velocity.setVelTup(rov.getVelocity())

        print("Robot Heading ", rov_state.heading, " Robot Vel ", rov_state.velocity)

        # Populate LIDAR map

        # Obstacle calculations
        R = find_robot_transform(robot_pos, robot_pitch)
        lidar_dst = getLidars()
        # Find LIDAR pts in map
		# NOTE: find_lidar_point doesn't take into account h of LIDAR
		lidar_left = LidarTracker();
		lidar_center = LidarTracker();
		lidar_right = LidarTracker();

		if lidar_left.lidar_hit_object(lidar_dst[0]):
			lidar_pts_pos[0] = find_lidar_point(R, -30, lidar_dst[0])

		if lidar_left.lidar_hit_object(lidar_dst[0]):
			lidar_pts_pos[1] = find_lidar_point(R, 0, lidar_dst[1])

		if lidar_left.lidar_hit_object(lidar_dst[0]):
			lidar_pts_pos[2] = find_lidar_point(R, 30, lidar_dst[2])

		lidarMap.extend(lidar_pts_pos[0], lidar_pts_pos[1], lidar_pts_pos[2])

		# CLASSIFER - TO ADD!
		# terrainMap = makeTerrainMap()

		## GET DESIRED PHI
		[phi_d, vel_d]= get_desired_setpts(lidarMap, robot_pos, waypoint)

        rov.setTgtSpeed(vel_d)
        rov.setTgtHeading(phi_d)

        print(rov.getLidars(), goal_heading)
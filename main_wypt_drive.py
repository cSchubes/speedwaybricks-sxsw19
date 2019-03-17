def get_desired_phi(lidarMap, terrainMap, robot_pos, waypt):
	phi_des = 0
	# tuned parameters
	# a = 0; # higher a, higher need to keep current heading (avoid handling error)
	c = 1; # c controls dominance of obstacle
	u = 5; # u controls dominance of goal
	max_oa_rng = 2000;

	for x in len(lidarMap)
		pt = lidarMap[x]
		euc_dist = (pt[0] - robot_pos[0])^2 + (pt[1] - robot_pos[1])^2 + (pt[2] - robot_pos[2])^2
		if euc_dist <= max_oa_rng:
			# find v_i of point
			v = c * (1/euc_dist^2)
		else:
			v = 0

		phi_des_obs += v*atan( (pt[1]-robot_pos[1]) / (pt[0]-robot_pos[0]))

	# Calculate a
	phi_des = u*atan( (waypt[1]-robot_pos[1]) / (waypt[0]-robot_pos[0])) - phi_des_obs


if __name__ == "__main__":
	# Define Robot Current Position
	robot_pos = getLocation()
	robot_roll = getRoll()
	robot_pitch = getPitch()
	robot_yaw = getYaw()

	# Get Waypoint
	waypoint = getWaypoint()

	while waypoint != robot_pos:
		## Populate LIDAR map
		R = find_robot_transform(robot_pos, robot_pitch)
		lidar_dst = getLidars()
		# Find LIDAR pts in map
		# NOTE: find_lidar_point doesn't take into account h of LIDAR
		lidar_pts_pos[0] = find_lidar_point(R, robot_yaw-30, lidar_dst[0])
		lidar_pts_pos[1] = find_lidar_point(R, robot_yaw, lidar_dst[1])
		lidar_pts_pos[2] = find_lidar_point(R, robot_yaw+30, lidar_dst[2])
		lidarMap.extend(lidar_pts_pos[0], lidar_pts_pos[1], lidar_pts_pos[2])
			
		# CLASSIFER - TO ADD!
		terrainMap = makeTerrainMap()

		## GET DESIRED PHI
		phi_d = get_desired_phi(lidarMap, terrainMap, robot_pos, waypoint)


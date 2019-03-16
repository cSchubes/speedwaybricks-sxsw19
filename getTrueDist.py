import numpy
import math

def find_robot_transform(robot_pos, robot_or):
    # robot_pos = [x, y, z], in meters in the globabl frame
    # robot_or = [roll, pitch, yaw] in degrees in globabl framw
    # returns a 4x4 array - the homogenous transformation matrix

    roll = math.radians(robot_or[0])
    pitch = math.radians(robot_or[1])
    yaw = math.radians(robot_or[2])

    R = numpy.array([[math.cos(yaw)*math.cos(pitch), math.cos(yaw)*math.sin(pitch)*math.sin(roll) - math.sin(yaw)*math.cos(roll), math.cos(yaw)*math.sin(pitch)*math.cos(roll) + math.sin(yaw)*math.sin(roll), robot_pos[0]],
                     [math.sin(yaw)*math.cos(pitch), math.sin(yaw)*math.sin(pitch)*math.sin(roll) + math.cos(yaw)*math.cos(roll), math.sin(yaw)*math.sin(pitch)*math.cos(roll) - math.cos(yaw)*math.sin(roll), robot_pos[1]],
                     [-1*math.sin(pitch), math.cos(pitch)*math.sin(roll), math.cos(pitch)*math.cos(roll), robot_pos[2]],
                     [0, 0, 0, 1]])

    return R

def find_lidar_point(robot_transform, lidar_yaw, lidar_dist):
    # robot_transform = 4x4 transform
    # lidar_yaw = one of {-30, 0, 30}, which lidar it is (degrees)
    # lidar_dist = the lidar range, in meters
    # returns a vector [x, y, z] in meters in the global frame.

    lidar_angle = math.radians(lidar_yaw)

    T = numpy.array([[math.cos(lidar_angle), -1*math.sin(lidar_angle), 0, 0],
                     [math.sin(lidar_angle), math.cos(lidar_angle), 0, 0,],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])
    
    

    D = numpy.array([[1, 0, 0, lidar_dist],
                     [0, 1, 0, 0,],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

    lidar_transform = numpy.matmul(robot_transform, numpy.matmul(T, D))
    lidar_point = [lidar_transform[0,3], lidar_transform[1,3], lidar_transform[2,3]]

    return lidar_point

def get_desired_setpts(lidarMap, terrainMap, robot_pos, waypt):
	phi_des = 0
	# tuned parameters
	# a = 0; # higher a, higher need to keep current heading (avoid handling error)
	c = 1; # c controls dominance of obstacle
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
	terrain_curr = terrainMap[0]

	# Get SURROUNDING TERRAIN (AS SECTORS)
	terrainMap.remove(terrainMap[0])
	terrain_surr = terrainMap

	# LOOP THROUGH ALL SECTORS
	# DEFINE BETA_0 FOR EACH SECTOR BASED ON TERRAIN TYPE
	# BETA_0 = handling * exp(-del_phi) + velocity * gamma (tunable)
	# BETA IS ASSIGNED BASED ON GENERAL ATTRACTIVNESS OF TERRAIN


	return [phi_des, vel_des]


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
		lidar_pts_pos[0] = find_lidar_point(R, -30, lidar_dst[0])
		lidar_pts_pos[1] = find_lidar_point(R, 0, lidar_dst[1])
		lidar_pts_pos[2] = find_lidar_point(R, 30, lidar_dst[2])
		lidarMap.extend([lidar_pts_pos[0], lidar_pts_pos[1], lidar_pts_pos[2]])
			
		# CLASSIFER - TO ADD!
		terrainMap = makeTerrainMap()

		## GET DESIRED PHI
		[phi_d, vel_d]= get_desired_setpts(lidarMap, terrainMap, robot_pos, waypoint)

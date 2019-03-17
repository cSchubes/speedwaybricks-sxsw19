def obstacleCorrection(lidarPts, leftTerrain=-1, rightTerrain=-1):

	left = lidarPts[0]
	center = lidarPts[1]
	right = lidarPts[2]

	del_phi_to_terrain = { '-1':'2000', '0':'3500', '1':'3000', '2':'2500', '3':'2000', '4':'2000', '5':'3500' }
	del_phi_max_to_terrain = { '-1':'30', '0':'10', '1':'20', '2':'20', '3':'40', '4':'40', '5':'10' }

	left_range = int(del_phi_to_terrain[str(leftTerrain)])
	left_max = int(del_phi_max_to_terrain[str(leftTerrain)])

	right_range = int(del_phi_to_terrain[str(rightTerrain)])
	right_max = int(del_phi_max_to_terrain[str(rightTerrain)])

	if left <= left_range or center <= center_range or right <= right_range:
		minLidar = min(lidarPts)
		minLidarType = lidarPts.index(minLidar)

		# get dist_lidar and scale accordingly
		if minLidarType == "left":
			del_phi = min(left_range/left, left_max)
		elif minLidarType == "right":
			del_phi =  - min(right_range/right, right_max)
		else:
			# GO LEFT IF OBSTACLE DEAD AHEAD
			if right < left:
				# GO LEFT
				del_phi = min(left_range/left, left_max)
			else:
				# GO RIGHT
				del_phi = - min(right_range/right, right_max)
			
	else:
		print "No valuable lidar data"
		del_phi = 0

	return del_phi



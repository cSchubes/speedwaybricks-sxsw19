def obstacleCorrection(lidarPts, leftTerrain=-1, rightTerrain=-1):
	left = lidarPts[0]
	center = lidarPts[1]
	right = lidarPts[2]

	del_phi_to_terrain = { '-1':'5', '0':'3', '1':'5', '2':'5', '3':'10', '4':'10', '5':'3' }

	if left <= 2000 or center <= 2000 or right <= 2000:
		minLidar = min(lidarPts)
		minLidarType = lidarPts.index(minLidar)

		if minLidarType == "left":
			del_phi = int(del_phi_to_terrain[str(leftTerrain)])
		elif minLidarType == "right":
			del_phi = - int(del_phi_to_terrain[str(rightTerrain)])
		else:
			# GO LEFT IF OBSTACLE DEAD AHEAD
			del_phi = int(del_phi_to_terrain[str(leftTerrain)])
	else:
		print("No valuable lidar data")
		del_phi = 0

	return del_phi



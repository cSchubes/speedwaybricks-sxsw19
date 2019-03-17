def obstacleCorrection(lidarPts, leftTerrain=-1, rightTerrain=-1):

    left = lidarPts[0]
    center = lidarPts[1]
    right = lidarPts[2]

    del_phi_to_terrain = { '-1':'3000', '0':'4500', '1':'4000', '2':'3500', '3':'3000', '4':'3000', '5':'4500' }
    del_phi_max_to_terrain = { '-1':'80', '0':'30', '1':'60', '2':'60', '3':'100', '4':'100', '5':'30' }

    left_range = int(del_phi_to_terrain[str(leftTerrain)])
    left_max = int(del_phi_max_to_terrain[str(leftTerrain)])

    right_range = int(del_phi_to_terrain[str(rightTerrain)])
    right_max = int(del_phi_max_to_terrain[str(rightTerrain)])

    if left <= left_range or center <= 2000 or right <= right_range:
        minLidar = min(lidarPts)
        print(minLidar)
        minLidarType = lidarPts.index(minLidar)
        print("MIN LIDAR", minLidarType)
        # get dist_lidar and scale accordingly
        if minLidarType == 0:
            del_phi = min(left_range/left, left_max)
            print("LEFT", del_phi)
        elif minLidarType == 2:
            del_phi =  -1 * min(right_range/right, right_max)
            print("RIGHT", del_phi)
        else:
            # GO LEFT IF OBSTACLE DEAD AHEAD
            if right < left:
                # GO LEFT
                print("CHOSE TO GO LEFT")
                # del_phi = min(left_range/center, left_max)
                del_phi = 80
            else:
                # GO RIGHT
                print("CHOSE TO GO RIGHT")
                # del_phi = -1 * min(right_range/center, right_max)
                del_phi = -80
            
    else:
        print("No valuable lidar data")
        del_phi = 0

    return del_phi



def obstacleCorrection(lidarPts, leftTerrain=-1, rightTerrain=-1):

    left = lidarPts[0]
    center = lidarPts[1]
    right = lidarPts[2]

<<<<<<< HEAD
    del_phi_to_terrain = { '-1':'3000', '0':'4500', '1':'4000', '2':'3500', '3':'3000', '4':'3000', '5':'4500' }
    del_phi_max_to_terrain = { '-1':'80', '0':'30', '1':'60', '2':'60', '3':'100', '4':'100', '5':'30' }

    left_range = int(del_phi_to_terrain[str(leftTerrain)])
    left_max = int(del_phi_max_to_terrain[str(leftTerrain)])

    right_range = int(del_phi_to_terrain[str(rightTerrain)])
    right_max = int(del_phi_max_to_terrain[str(rightTerrain)])

    if left <= left_range or center <= 2000 or right <= right_range:
=======
    c_to_terrain = { '-1':'5500', '0':'7750', '1':'7000', '2':'6250', '3':'5500', '4':'5500', '5':'7750' }
    del_phi_max_to_terrain = { '-1':'50', '0':'30', '1':'50', '2':'50', '3':'70', '4':'70', '5':'30' }

    c_left = int(c_to_terrain[str(leftTerrain)])
    left_max = int(del_phi_max_to_terrain[str(leftTerrain)])

    c_right = int(c_to_terrain[str(rightTerrain)])
    right_max = int(del_phi_max_to_terrain[str(rightTerrain)])

    if left <= 2000 or center <= 2000 or right <= 2000:
>>>>>>> 2f65c69cdf5c53c96f96cf158b47dcd4a11b2b1c
        minLidar = min(lidarPts)
        print(minLidar)
        minLidarType = lidarPts.index(minLidar)
        print("MIN LIDAR", minLidarType)
        # get dist_lidar and scale accordingly
        if minLidarType == 0:
<<<<<<< HEAD
            del_phi = min(left_range/left, left_max)
            print("LEFT", del_phi)
        elif minLidarType == 2:
            del_phi =  -1 * min(right_range/right, right_max)
=======
            if left != 0:
                del_phi = min(c_left/left, left_max)
            else:
                del_phi = left_max
            print("LEFT", del_phi)
        elif minLidarType == 2:
            if right != 0:
                del_phi =  -1 * min(c_right/right, right_max)
            else:
                del_phi = - right_max
>>>>>>> 2f65c69cdf5c53c96f96cf158b47dcd4a11b2b1c
            print("RIGHT", del_phi)
        else:
            # GO LEFT IF OBSTACLE DEAD AHEAD
            if right < left:
                # GO LEFT
                print("CHOSE TO GO LEFT")
                # del_phi = min(left_range/center, left_max)
<<<<<<< HEAD
                del_phi = 80
=======
                del_phi = -30
>>>>>>> 2f65c69cdf5c53c96f96cf158b47dcd4a11b2b1c
            else:
                # GO RIGHT
                print("CHOSE TO GO RIGHT")
                # del_phi = -1 * min(right_range/center, right_max)
<<<<<<< HEAD
                del_phi = -80
=======
                del_phi = 30
>>>>>>> 2f65c69cdf5c53c96f96cf158b47dcd4a11b2b1c
            
    else:
        print("No valuable lidar data")
        del_phi = 0

    return del_phi



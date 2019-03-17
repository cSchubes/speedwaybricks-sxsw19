import subapi as api
import rover_lib as lib
import math
import numpy
from get_lidar_point import *

def get_desired_setpts(lidarMap, robot_pos, waypt):
    phi_des = 0
    # tuned parameters
    # a = 0; # higher a, higher need to keep current heading (avoid handling error)
    c = 10000; # c controls dominance of obstacle
    u = 0.1; # u controls dominance of goal
    max_oa_rng = 100000; # cut-off repulsive distance
    v_des_obs = numpy.zeros(2)

    print(len(lidarMap))
    remove_list = []
    i = 0
    for pt in lidarMap:
        euc_dist = math.sqrt((pt[0] - robot_pos.x)**2 + (pt[1] - robot_pos.y)**2 )#(pt[2] - robot_pos.z)**2)
        # print('Euc Dist to Pt', euc_dist)
        if euc_dist <= max_oa_rng:
            # find v_i of point
            v = c * (1/euc_dist**2)
            v_des_obs = numpy.add([v*(pt[0]-robot_pos.x) , v*(pt[1]-robot_pos.y)], v_des_obs)
        else:
            # throw out point
            # remove_list.append(i)
            # lidarMap.remove(pt)
            v = 0
        i += 1

    # for i in remove_list:
        # lidarMap.pop(i)

    v_des = numpy.subtract([u*(waypt.x-robot_pos.x) , u*(waypt.y-robot_pos.y)], v_des_obs)
    print(math.sqrt( v_des[0]**2 + v_des[1]**2))
    # print(v_des)
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


    phi_des = math.atan2( v_des[1] , v_des[0]) * 180 / math.pi
    while phi_des < 0 or phi_des > 360:
        if phi_des < 0:
            phi_des = 360 + phi_des
        elif phi_des > 360:
            phi_des = phi_des - 360


    vel_des = 200

    print(phi_des)

    # Find the terrain type in phi_des
    return [phi_des, vel_des]


if __name__=="__main__":
    rov = api.rover()
    # Set Waypoint
    way_pos = lib.location()
    way_pos.setLoc(27000, -48000, 0)
    rov_pos = rov.getLocation()
    location = way_pos
    rov_state = lib.robot_state(lib.poser(rov_pos[0], rov_pos[1], rov_pos[2], rov.getRoll(), rov.getPitch(), rov.getYaw()))
    # Euclidean distance to waypoint
    dist_way = math.sqrt( (way_pos.x - rov_pos[0])**2 + (way_pos.y - rov_pos[1])**2 +(way_pos.z - rov_pos[2])**2 )
    # print(dist_way)
    lidarMap = []
    while dist_way >= 0.1:
        # Update robot state
        rov_state.pose.setPoseTup(rov.getLocation(), rov.getRoll(), rov.getPitch(), rov.getYaw())
        rov_state.heading = rov.getCurrentHeading()
        rov_state.acceleration.setAccelTup(rov.getAcceleration())
        rov_state.velocity.setVelTup(rov.getVelocity())

        # print("Robot Heading ", rov_state.heading, " Robot Vel ", rov_state.velocity.x)

        dist_way = math.sqrt( (way_pos.x - rov_pos[0])**2 + (way_pos.y - rov_pos[1])**2 +(way_pos.z - rov_pos[2])**2 )
        # print(dist_way)
        # Populate LIDAR map

        # Obstacle calculations
        R = find_robot_transform(rov_pos, rov_state.pose.orientation)
        lidar_dst = rov.getLIDARS()
        # Find LIDAR pts in map
        # NOTE: find_lidar_point doesn't take into account h of LIDAR
        lidar_left = LidarTracker()
        lidar_center = LidarTracker()
        lidar_right = LidarTracker()
        lidar_pts_pos = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        

        if lidar_left.lidar_hit_object(lidar_dst[0]):
            lidar_pts_pos[0] = find_lidar_point(R, -30, lidar_dst[0])
            print("found left")
        if lidar_center.lidar_hit_object(lidar_dst[1]):
            lidar_pts_pos[1] = find_lidar_point(R, 0, lidar_dst[1])
            print("found center")

        if lidar_right.lidar_hit_object(lidar_dst[2]):
            lidar_pts_pos[2] = find_lidar_point(R, 30, lidar_dst[2])
            print("found right")

        # print(lidar_dst[1])
        print(rov.getLocation())
        # lidarMap.extend(lidar_pts_pos)
        # print(lidarMap)

        # CLASSIFER - TO ADD!
        # terrainMap = makeTerrainMap()

        ## GET DESIRED PHI
        [phi_d, vel_d]= get_desired_setpts(lidar_pts_pos, rov_state.pose.position, way_pos)

        rov.setTgtSpeed(vel_d)
        rov.setTgtHeading(phi_d)

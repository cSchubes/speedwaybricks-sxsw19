

## This whole thing is based on the idea that the "handling" of a given terrain
## is based on the fiction of the floor, and thus for each terrain there is
## a max centripetal force that can be applied to turn.
##
## F = (m v^2)/r, but v = wr.
## So, F = m w r, we don't care about m.

valid_terrain = ["Acid Sludge", "Red Muddy", "Sand", "Grass", "Rock", "Ice"]

# A dictionary of the max centripetal force for each terrain.
# Units are [deg/s]*[m/s]
terrain_dict = {
    "Acid Sludge" : 100,
    "Red Muddy" : 100,
    "Sand" : 100,
    "Grass" : 100,
    "Rock" : 100,
    "Ice" : 100
}

def calc_turn_from_vel(terrain, des_vel):
    # terrain = string in valid_terrain
    # des_vel = desired linear velocity in m/s
    # returns a turning rate, in deg/s

    if (terrain == "Acid Sludge"):
        return -1
    elif (terrain == "Red Muddy"):
        return -1
    elif (terrain == "Sand"):
        return -1
    elif (terrain == "Grass"):
        return -1
    elif (terrain == "Rock"):
        return -1
    elif (terrain == "Ice"):
        return -1
    else:
        print("Invalid terrain type")
        return -1

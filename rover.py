# api mocker

import random
from data_loader import load_all

imgs, lbls, data_dict = load_all(9)

def isDeadZone():
    return False

def isOverride():
    return False

def getImgs():
    return random.sample(imgs, 8)

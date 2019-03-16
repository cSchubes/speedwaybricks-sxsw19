import cv2
import numpy as np
def get_labels(run_no):
    file = open('Run'+str(run_no)+'/picOutput/LABELS.txt')
    lines = file.read().splitlines()
    return lines
    #print(lines[0])
def parse_lbl(lbl):
    meta_data = lbl.split('LogTemp: RTMAT ')[1].split(' ')
    img_mat = meta_data[2]
    img_no = meta_data[1]
    cam_no = meta_data[0]
    return img_no,cam_no,img_mat

def load_img(lbl,extension = '/picOutput/im_1230'):
    return cv2.imread(extension+lbl[0]+'_'+lbl[1]+'.png')
def load_all(run_no,mode = 0):
    labels = get_labels(run_no)
    imgs = []
    lbls = []
    for lbl in labels:
        one_hot = [0,0,0,0,0,0]
        meta = parse_lbl(lbl)
        img = load_img((meta[1],meta[0]),'Run'+str(run_no)+'/picOutput/im_1230')
        if img is None:
            continue
        imgs.append(np.array(img))
        one_hot[int(meta[2])] = 1
        lbls.append(one_hot)
    if mode:
        np.save('numpy_saved',[imgs,lbls])
        
    return imgs,lbls

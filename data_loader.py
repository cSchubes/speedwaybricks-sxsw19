import cv2
import numpy as np
def get_labels(run_no):
    file = open('data/run'+str(run_no)+'/picOutput/LABELS.txt')
    lines = file.read().splitlines()
    # print(lines[0])
    return lines
def parse_lbl(lbl):
    meta_data = lbl.split('LogTemp: RTMAT ')[1].split(' ')
    img_mat = meta_data[2]
    img_no = meta_data[1]
    cam_no = meta_data[0]
    return img_no,cam_no,img_mat

def load_img(lbl,extension = '/picOutput/im_1230'):
    return cv2.imread(extension+lbl[0]+'_'+lbl[1]+'.png')

def build_dict(num_labels):
    label_dict = {}
    for i in range(num_labels):
        label_dict[i] = []
    return label_dict
    
def load_all(run_no,mode = 0):
    label_dict = build_dict(6)
    labels = get_labels(run_no)
    imgs = []
    lbls = []
    for lbl in labels:
        one_hot = [0,0,0,0,0,0]
        meta = parse_lbl(lbl)
        # meta: index 0: Image Index, Index 1: Image Page Index, Index 2: Label
        img = load_img((meta[1],meta[0]),'data/run'+str(run_no)+'/picOutput/im_1230')
        if img is None:
            continue
        imgs.append(np.array(img))
        one_hot[int(meta[2])] = 1
        lbls.append(one_hot)

        path_str = 'data/run'+str(run_no)+'/picOutput/im_1230'+str(meta[1])+'_'+str(meta[0])+'.png'
        label_dict[int(meta[2])].append(path_str)
    if mode:
        np.save('numpy_saved',[imgs,lbls])
        
    return label_dict
    
# imgs, labels, label_dict = load_all(9)
#print(imgs)
#print(labels)
# label_dict = load_all(9)
# print (label_dict)
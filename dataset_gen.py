from data_loader import load_all
from sklearn import model_selection
from shutil import copyfile
import os

SEED = 42

run9 = load_all(9)
run11 = load_all(11)

cnt = 0
for i in range(len(run9)):
    cnt += len(run9[i])
    
print(cnt)

merged = {}
for i in range(0,6):
    merged[i] = run9[i] + run11[i]

run9X = []
run9Y = []
run11X = []
run11Y = []
mergedX = []
mergedY = []
for i in range(0, 6):
    run9X += run9[i]
    run11X += run11[i]
    mergedX += merged[i]
    for j in range(0, len(run9[i])):
        run9Y.append(i)
    for j in range(0, len(run11[i])):
        run11Y.append(i)
    for j in range(0, len(merged[i])):
        mergedY.append(i)

cnt = {}
for item in run9Y:
    if item in cnt.keys():
        cnt[item] += 1
    else:
        cnt[item] = 1
    
print(cnt)
        
prefix = ['run9', 'run11', 'merged']
for i in range(6):
    for j in range(len(prefix)):
        os.makedirs('data/%s_terrain_dataset_find/train/%d'%(prefix[j], i))
        os.makedirs('data/%s_terrain_dataset_find/validate/%d'%(prefix[j], i))
        os.makedirs('data/%s_terrain_dataset_find/test/%d'%(prefix[j], i))
    
xSet = [run9X, run11X, mergedX]
ySet = [run9Y, run11Y, mergedY]

for i in range(len(xSet)):
    xt, xtest, yt, ytest = model_selection.train_test_split(xSet[i], ySet[i], test_size=.2, random_state=SEED, stratify=ySet[i])
    xtrain, xval, ytrain, yval = model_selection.train_test_split(xt, yt, test_size=.2, random_state=SEED, stratify=yt)
    for j in range(len(xtest)):
        copyfile(xtest[j], 'data/%s_terrain_dataset_find/test/%d/%s'%(prefix[i], ytest[j], xtest[j][xtest[j].rfind('/'):]))            
    for j in range(len(xval)):
        copyfile(xval[j], 'data/%s_terrain_dataset_find/validate/%d/%s'%(prefix[i], yval[j], xval[j][xval[j].rfind('/'):]))         
    for j in range(len(xtrain)):
        copyfile(xtrain[j], 'data/%s_terrain_dataset_find/train/%d/%s'%(prefix[i], ytrain[j], xtrain[j][xtrain[j].rfind('/'):]))    
    
            
    
# cnt = {}
# for item in yt:
#     if item in cnt.keys():
#         cnt[item] += 1
#     else:
#         cnt[item] = 1
    
# print(cnt)

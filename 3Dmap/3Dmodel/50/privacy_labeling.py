import numpy as np
import copy
import math
np.set_printoptions(threshold=np.inf)

point = np.loadtxt('exc.txt', delimiter=',', dtype=int)
# print(point)
maplabel = np.loadtxt('maplabel.txt', delimiter=' ', dtype=int)

## 50*50中每个点的label值[1,2,3,4]
maplabel_privacy = copy.deepcopy(maplabel)

## excel中每栋建筑物中心点所在50*50的位置
maplabel_index = np.zeros([50,50],dtype=int)

## 分组数
group_num = 110
for i in range(1,group_num+1):
    privacy_num = np.zeros([5,1], dtype=int)
    for j in range (len(point)):
        # print (point[j][3])
        if point[j][4] == i:
            print("j",j,point[j][3])
            privacy_num[point[j][3]] += 1
    print(privacy_num)
    maxindex = np.argmax(privacy_num)
    for m in range(50):
        for n in range(50):
            if maplabel[m][n] == i:
                maplabel_privacy[m][n] = maxindex

for j in range (len(point)):
    m = point[j][1]
    n = point[j][0]
    maplabel_privacy[m][n] = point[j][3]
    maplabel_index[m][n] = j + 1
    # if j == 318:
    #     print("testttt",m,n,maplabel_index[m][n])


print(maplabel_privacy)
print(maplabel_index)
np.savetxt("maplabel_privacy.txt", maplabel_privacy, fmt='%d', delimiter=' ')
np.savetxt("maplabel_index.txt", maplabel_index, fmt='%d', delimiter=' ')


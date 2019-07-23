import numpy as np
import os

a=np.loadtxt('map_10_1.txt')
occ_grid=np.reshape(a,(10,10,10))
# print(b)
# print(type(b))
occ_grid_name = "data/"+"occ_grid-50" + ".npy"
np.save(file=occ_grid_name, arr=occ_grid)

# occ_grid = np.load(file=occ_grid_name)
ground = np.zeros((50,50),dtype=int)
print(occ_grid.shape)
obstacle = 0
privacy = 0
privacy_num = np.zeros((5,1),dtype=int)
for i in range (occ_grid.shape[0]):
    for j in range (occ_grid.shape[1]):
        for k in range (occ_grid.shape[2]):
            if occ_grid[i][j][k] == 1:
                obstacle += 1
            elif occ_grid[i][j][k] == 2 or occ_grid[i][j][k] == 3 or occ_grid[i][j][k] == 4:
                privacy_num[int(occ_grid[i][j][k])] += 1
                privacy += 1
for j in range(occ_grid.shape[1]):
    for k in range(occ_grid.shape[2]):
        ground[j][k] = occ_grid[0][j][k]
obstacle_ratio = obstacle/(occ_grid.shape[0]*occ_grid.shape[1]*occ_grid.shape[2])
privacy_ratio = privacy/(occ_grid.shape[0]*occ_grid.shape[1]*occ_grid.shape[2])
print(obstacle, obstacle_ratio, privacy, privacy_ratio)
print(ground)
print (privacy_num)
np.savetxt("ground.txt", ground, fmt='%d', delimiter=' ')
np.save("ground.npy", ground)


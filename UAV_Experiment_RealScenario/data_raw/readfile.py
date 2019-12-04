import numpy as np
import os

# a=np.loadtxt('data/map0728-2.txt')
# occ_grid=np.reshape(a,(5,15,15))
# occ_grid=np.zeros((5,20,20),dtype=int)
# print(b)
# print(type(b))
# occ_grid_name =  "../data/occ_grid_known_Hybrid_temp26" + ".npy"
# occ_grid_name =  "occ_grid_0804" + ".npy"
occ_grid_name =  "../data2/plan_path_Hybrid_temp25" + ".npy"
# occ_grid_name =  "reference_path5" + ".npy"
# np.save(file=occ_grid_name, arr=occ_grid)

occ_grid = np.load(file=occ_grid_name)
print(occ_grid)
# ground = np.zeros((occ_grid.shape[1],occ_grid.shape[2]),dtype=int)
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
np.savetxt("ground_SA.txt", ground, fmt='%d', delimiter=' ')
# np.savetxt("ground_PP.txt", ground, fmt='%d', delimiter=' ')
# np.save("ground.npy", ground)

occ_grid_height = np.zeros((occ_grid.shape[1],occ_grid.shape[2]),dtype=int)
for i in range (occ_grid.shape[1]):
    for j in range (occ_grid.shape[2]):
        level = 0
        for k in range (occ_grid.shape[0]):
            if occ_grid[k][i][j] > 0:
                level += 1
        occ_grid_height[i][j] = level
print(occ_grid_height)
np.savetxt("occ_grid_height_SA.txt", occ_grid_height, fmt='%d', delimiter=' ')
# np.savetxt("occ_grid_height_PP.txt", occ_grid_height, fmt='%d', delimiter=' ')

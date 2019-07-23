import numpy as np
import os
import copy


occ_grid = np.load(file="occ_grid_known1.npy")
for m in range(10):
    print("The value of x: ", m)
    print(occ_grid[m])


path_grid = copy.deepcopy(occ_grid)
c = np.load(file="plan_path_Hybrid3.npy")
# print(c, len(c))
for i in range(len(c)):
    point = c[i]
    if point[3]== 2:
        path_grid[int(point[0])][int(point[1])][int(point[2])] = 10
    else:
        path_grid[int(point[0])][int(point[1])][int(point[2])] = 9
print("hybrid:",path_grid)


path_grid = copy.deepcopy(occ_grid)
c = np.load(file="plan_path_SC1.npy")
# print(c, len(c))
path_grid = copy.deepcopy(occ_grid)
for i in range(len(c)):
    point = c[i]
    if point[3]== 2:
        path_grid[int(point[0])][int(point[1])][int(point[2])] = 10
    else:
        path_grid[int(point[0])][int(point[1])][int(point[2])] = 9
print("sc:",path_grid)



path_grid = copy.deepcopy(occ_grid)
c = np.load(file="plan_path_PP1.npy")
# print(c, len(c))
path_grid = copy.deepcopy(occ_grid)
for i in range(len(c)):
    point = c[i]
    if point[3]== 2:
        path_grid[int(point[0])][int(point[1])][int(point[2])] = 10
    else:
        path_grid[int(point[0])][int(point[1])][int(point[2])] = 9
print("pp",path_grid)


path_grid = copy.deepcopy(occ_grid)
c = np.load(file="reference_path2.npy")
# print(c, len(c))
path_grid = copy.deepcopy(occ_grid)
for i in range(len(c)):
    point = c[i]
    if point[3]== 2:
        path_grid[int(point[0])][int(point[1])][int(point[2])] = 10
    else:
        path_grid[int(point[0])][int(point[1])][int(point[2])] = 9
print("ref:",path_grid)



path_grid = copy.deepcopy(occ_grid)
c = np.load(file="plan_path1.npy")
# print(c, len(c))
path_grid = copy.deepcopy(occ_grid)
for i in range(len(c)):
    point = c[i]
    if point[3]== 2:
        path_grid[int(point[0])][int(point[1])][int(point[2])] = 10
    else:
        path_grid[int(point[0])][int(point[1])][int(point[2])] = 9
print("plan:",path_grid)

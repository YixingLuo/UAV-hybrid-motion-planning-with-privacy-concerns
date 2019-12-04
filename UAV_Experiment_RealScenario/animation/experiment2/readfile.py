import numpy as np
import os

# a=np.loadtxt('data/map0728-2.txt')
# occ_grid=np.reshape(a,(5,15,15))
# occ_grid=np.zeros((5,10,10),dtype=int)
# print(b)
# print(type(b))
# occ_grid_name =  os.getcwd() + "/data3/occ_grid_known_Hybrid_temp26" + ".npy"
# occ_grid_name =  "occ_grid-0804" + ".npy"
# occ_grid_name =  "occ_grid_known_PP_temp18" + ".npy"
# np.save(file=occ_grid_name, arr=occ_grid)

# occ_grid = np.load(file=occ_grid_name)
# print(occ_grid)
# ground = np.zeros((occ_grid.shape[1],occ_grid.shape[2]),dtype=int)
# print(occ_grid.shape)


# for num in range (26):
#     path_num = os.getcwd() + "/data3/plan_path_Hybrid_temp" + str(num) + ".npy"
#     path = np.load(file=path_num)
#     for item in range(len(path)):
#         path[item][2] = 9
#     np.save(os.getcwd() + "/data3/plan_path_Hybrid_temp_2_" + str(num) + ".npy", path)


for num in range (26):
    occ = np.loadtxt(os.getcwd() + "/data3/ground" + str(num) + ".txt")
    occ = np.reshape(occ, (20, 20))
    for i in range(20):
        for j in range (20):
            if occ[i][j]==4:
                occ[i][j+9]=4
                occ[i][j]=0
    np.savetxt( os.getcwd() +"/data3/ground_2_" + str(num) + ".txt", occ, fmt='%d', delimiter=' ')


    occ_grid_height = np.loadtxt(os.getcwd() + "/data3/occ_grid_height" + str(num) + ".txt")
    occ_grid_height = np.reshape(occ_grid_height, (20, 20))
    for i in range(20):
        for j in range(20):
            if occ_grid_height[i][j] == 1:
                occ_grid_height[i][j + 9] = 1
                occ_grid_height[i][j] = 0
    np.savetxt( os.getcwd() +"/data3/occ_grid_height_2_" + str(num) + ".txt", occ_grid_height, fmt='%d', delimiter=' ')

# for num in range (27):
#     occ_grid_name = os.getcwd() + "/data3/occ_grid_known_Hybrid_temp" + str(num) + ".npy"
#     occ_grid = np.load(file=occ_grid_name)
#     ground = np.zeros((occ_grid.shape[1], occ_grid.shape[2]), dtype=int)
#
#     obstacle = 0
#     privacy = 0
#     privacy_num = np.zeros((5, 1), dtype=int)
#     for i in range(occ_grid.shape[0]):
#         for j in range(occ_grid.shape[1]):
#             for k in range(occ_grid.shape[2]):
#                 if occ_grid[i][j][k] == 1:
#                     obstacle += 1
#                 elif occ_grid[i][j][k] == 2 or occ_grid[i][j][k] == 3 or occ_grid[i][j][k] == 4:
#                     privacy_num[int(occ_grid[i][j][k])] += 1
#                     privacy += 1
#     for j in range(occ_grid.shape[1]):
#         for k in range(occ_grid.shape[2]):
#             ground[j][k] = occ_grid[0][j][k]
#     obstacle_ratio = obstacle / (occ_grid.shape[0] * occ_grid.shape[1] * occ_grid.shape[2])
#     privacy_ratio = privacy / (occ_grid.shape[0] * occ_grid.shape[1] * occ_grid.shape[2])
#     print(obstacle, obstacle_ratio, privacy, privacy_ratio)
#     print(ground)
#     print(privacy_num)
#     np.savetxt( os.getcwd() +"/data3/ground" + str(num) + ".txt", ground, fmt='%d', delimiter=' ')
#     # np.savetxt("ground_PP.txt", ground, fmt='%d', delimiter=' ')
#     # np.save("ground.npy", ground)
#
#     occ_grid_height = np.zeros((occ_grid.shape[1], occ_grid.shape[2]), dtype=int)
#     for i in range(occ_grid.shape[1]):
#         for j in range(occ_grid.shape[2]):
#             level = 0
#             for k in range(occ_grid.shape[0]):
#                 if occ_grid[k][i][j] > 0:
#                     level += 1
#             occ_grid_height[i][j] = level
#     print(occ_grid_height)
#     np.savetxt( os.getcwd() +"/data3/occ_grid_height" + str(num) + ".txt", occ_grid_height, fmt='%d', delimiter=' ')
#     # np.savetxt("occ_grid_height_PP.txt", occ_grid_height, fmt='%d', delimiter=' ')

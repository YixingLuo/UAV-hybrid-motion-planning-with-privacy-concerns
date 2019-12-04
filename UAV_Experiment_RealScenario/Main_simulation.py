"""
main function
"""
import sys
from Point2 import Point
import numpy as np
from Configure import configure
from HybridPlanning_SA_real import Astar_Hybrid_Planning_online

from flight_control import flight_control

from log import Log
import copy

from socket import *
import time

sys.setrecursionlimit(1000000)
np.set_printoptions(threshold=np.inf)

delay = 0

HOST = '192.168.1.105'
PORT = 7896
s = socket(AF_INET, SOCK_DGRAM)
s.connect((HOST, PORT))

colorflag = 1

sizeflag = 2

## time interval to send the flight control command
continue_time = 3

## experiment for group 1: 5*10*10 grid scale
occ_grid = np.load('data_raw/occ_grid_1.npy')
reference_path = np.load('data_raw/reference_path1.npy')
privacy_radius = [1, 1.5, 4]

## experiment for group 2: 5*20*20 grid scale
# occ_grid = np.load('data_raw/occ_grid_2.npy')
# reference_path = np.load('data_raw/reference_path2.npy')
# privacy_radius = [1, 1.5, 4]


print(occ_grid.shape, reference_path, len(reference_path))

log_tmp = Log(__name__, log_cate="results")
log = log_tmp.getlog()


grid_x = occ_grid.shape[0]
grid_y = occ_grid.shape[1]
grid_z = occ_grid.shape[2]

safety_threshold = 0.023
privacy_threshold = 0.02

## experiment for group 1: 5*10*10 grid scale
x1 = 0
x2 = 0
y1 = 0
y2 = 9
z1 = 0
z2 = 9
starting_point = Point(x1, y1, z1, 1)
end_point = Point(x2, y2, z2, 1)

## experiment for group 2: 5*20*20 grid scale
# x1 = 0
# x2 = 0
# y1 = 0
# y2 = 18
# z1 = 9
# z2 = 9
# starting_point = Point(x1, y1, z1, 1)
# end_point = Point(x2, y2, z2, 1)


config = configure(grid_x, grid_y, grid_z, safety_threshold, privacy_threshold, privacy_radius,
                                   starting_point,
                                   end_point, delay)
T_budget = config.T_budget
T_optimal = config.T_optimal

# print(occ_grid)
occ_grid_known = copy.deepcopy(occ_grid)
for i in range(occ_grid.shape[0]):
    for j in range(occ_grid.shape[1]):
        for k in range(occ_grid.shape[2]):
            if occ_grid_known[i][j][k] >1:
                occ_grid_known[i][j][k] = 1


## ref == 1 to show the initial results without self-adaptive motion planning
ref = 0
if ref == 1 :
    ## experiment for group 1: 5*10*10 grid scale
    reference_path = np.load('data_raw/reference_path1.npy')

    ## experiment for group 2: 5*20*20 grid scale
    # reference_path = np.load('data_raw/reference_path2.npy')

    print(reference_path)

    refpath = []
    for i in range(len(reference_path)):
        point = Point(int(reference_path[i][0]), int(reference_path[i][1]),
                      int(reference_path[i][2]),
                      int(reference_path[i][3]))
        refpath.append(point)

    for idx in range(len(refpath) - 1):
        print(refpath[idx], refpath[idx + 1])
        flight_control(idx, idx + 1, refpath, s, continue_time)

else :
    Astar_Hybrid_Planning_online(config, log, occ_grid_known, reference_path, occ_grid, s, colorflag, sizeflag,
                                 continue_time)




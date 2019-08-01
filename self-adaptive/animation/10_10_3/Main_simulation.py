
from Point2 import Point
import numpy as np
from Configure import configure
# from pathinitial import PathInitial
# from reference_path import PathInitial
# from PathPlanningOnline import Astar_Path_Planning_online
# from HybridPlanningOnline import Astar_Hybrid_Planning_online
from HybridPlanning_SA_real import Astar_Hybrid_Planning_online
# from SensorConfigOnline import Astar_Sensor_Config_online

from log import Log

from socket import *
import time

HOST = '192.168.0.101'
PORT = 7896
s = socket(AF_INET, SOCK_DGRAM)
s.connect((HOST, PORT))

log_tmp = Log(__name__, log_cate="results")
log = log_tmp.getlog()

reference_path = np.load('data/reference_path1.npy')
# print(reference_path)

occ_grid_known = np.load('data/occ_grid_known_initial1.npy')
# print(occ_grid_known)

occ_grid = np.load('data/occ_grid-10.npy')
# print(occ_grid)

grid_x = 10
grid_y = 10
grid_z = 10

safety_threshold = 0.039
privacy_threshold = 0.003
privacy_radius = [1, 1.5, 2]

x1 = 0
x2 = 0
y1 = 0
y2 = grid_y - 1
z1 = 0
z2 = grid_z - 1
starting_point = Point(x1, y1, z1, 1)
end_point = Point(x2, y2, z2, 1)
# alpha = 5 / 3
# beta = 4 / 3


config = configure(grid_x, grid_y, grid_z, safety_threshold, privacy_threshold, privacy_radius,
                                   starting_point,
                                   end_point)
T_budget = config.T_budget
T_optimal = config.T_optimal

Astar_Hybrid_Planning_online(config, log, occ_grid_known, reference_path, occ_grid, s)



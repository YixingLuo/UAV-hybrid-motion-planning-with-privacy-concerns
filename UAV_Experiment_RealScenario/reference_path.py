"""
reference path generation
"""
#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
from Point2 import Point
import copy
import numpy as np
from mapTools import privacy_init, hasprivacythreat2, initialmapwithknowngrid, initialmapwithknowngrid_ratio, caculate_privacy_surround
from Configure import configure
import math
import sys
from heapq import heappush
import os
import random

# from log import Log
# log = Log(__name__).getlog()

sys.setrecursionlimit(1000000)

def PathInitial(config, reinitial_flag, iteration, log, num):
    grid_x = config.grid_x
    grid_y = config.grid_y
    grid_z = config.grid_z
    grid = config.grid
    safety_threshold = config.safety_threshold
    privacy_threshold = config.privacy_threshold
    # privacy_radius = 1 ##
    privacy_radius = config.privacy_radius

    # drone parameter
    starting_point = config.starting_point
    end_point = config.end_point
    T_budget = config.T_budget
    T_optimal = config.T_optimal
    reinitial_flag = reinitial_flag

    # 全局信息，用作baseline
    # occ_grid_name = "occ_grid" + str(iteration) + ".npy"
    occ_grid_name = os.getcwd() +"/data_raw/"+"occ_grid_" +str(num) + ".npy"
    occ_grid = np.load(file=occ_grid_name)
    # occ_grid = np.load(file="occ_grid-1.npy")
    pri_grid, privacy_sum = privacy_init(grid_x, grid_y, grid_z, occ_grid, privacy_radius)


    refpath = []
    reference_path = []
    objective_list = []
    no_solution_flag = 1
    if reinitial_flag == 1:
        reference_path.append([0, 0, 0, 1])
        reference_path.append([1, 0, 0, 1])
        reference_path.append([2, 0, 0, 1])


        # objective_list.append([1, 0, 0])
        # objective_list.append([1, 0, 3])
        # objective_list.append([1, 4, 3])
        # objective_list.append([1, 4, 6])
        # objective_list.append([1, 9, 6])
        # objective_list.append([1, 9, 9])

        objective_list.append([3, 0, 0])
        objective_list.append([3, 0, 3])
        objective_list.append([3, 4, 3])
        objective_list.append([3, 4, 7])
        objective_list.append([3, 9, 7])
        objective_list.append([3, 9, 9])

        # objective_list.append([3, 18, 0])

        # y_list = [0, 12, 18, 31, 37, 43, 49]
        # x_list = [0, 16, 17, 24, 25, 33, 34 , 49]
        #
        # while objective_list[-1] != [1, 49, 49]:
        #     index = random.randint(0,1)
        #     if index == 0:
        #         now_x = objective_list[-1][1]
        #         if now_x == x_list[-1]:
        #             continue
        #         now_y = objective_list[-1][2]
        #         index_x = x_list.index(now_x)
        #         now_index_x = random.randint(index_x + 1, len(x_list)-1)
        #         objective_list.append([1, x_list[now_index_x], now_y])
        #     elif index == 1:
        #         now_x = objective_list[-1][1]
        #         now_y = objective_list[-1][2]
        #         if now_y == y_list[-1]:
        #             continue
        #         index_y = y_list.index(now_y)
        #         now_index_y = random.randint(index_y + 1, len(y_list) - 1)
        #         if y_list[now_index_y] == 0:
        #             continue
        #         objective_list.append([1, now_x, y_list[now_index_y]])

        print(objective_list)
        # objective_list = [[1, 0, 0],[1, 0, 12],[1, 25, 12],[1, 49, 12], [1, 49, 49]]
        for i in range(1, len(objective_list)):
            delta_x = objective_list[i][1]-objective_list[i-1][1]
            delta_y = objective_list[i][2]-objective_list[i-1][2]
            if delta_x > 0:
                for j in range(abs(delta_x)):
                    reference_path.append([3, objective_list[i-1][1] + j, objective_list[i-1][2], 1])
            elif delta_x < 0:
                for j in range(abs(delta_x)):
                    reference_path.append([3, objective_list[i-1][1] - j, objective_list[i-1][2], 1])
            elif delta_y > 0:
                for j in range(abs(delta_y)):
                    reference_path.append([3, objective_list[i - 1][1], objective_list[i - 1][2] + j, 1])
            elif delta_y < 0:
                for j in range(abs(delta_y)):
                    reference_path.append([3, objective_list[i - 1][1], objective_list[i - 1][2] - j, 1])

        # for i in range(38):
        #     reference_path.append([1, 0, i, 1])
        # for i in range (1, 35):
        #     reference_path.append([1,i,37,1])
        # for i in range (38, 50):
        #     reference_path.append([1,34,i,1])
        # for i in range (25, 34):
        #     reference_path.append([1,i,37,1])
        # for i in range (38,50):
        #     reference_path.append([1,33,i,1])
        # for i in range (35,50):
        #     reference_path.append([1,i,49,1])
        # reference_path.append([3, 9, 9, 1])

        reference_path.append([3, 9, 9, 1])
        reference_path.append([2, 9, 9, 1])
        reference_path.append([1, 9, 9, 1])
        reference_path.append([0, 9, 9, 1])

        # reference_path.append([3, 18, 0, 1])
        # reference_path.append([2, 18, 0, 1])
        # reference_path.append([1, 18, 0, 1])
        # reference_path.append([0, 18, 0, 1])

        # reference_path.append([2, 14, 14, 1])
        # reference_path.append([1, 14, 14, 1])
        # reference_path.append([0, 14, 14, 1])

        print(reference_path)

        for i in range(len(reference_path)):
            point = Point(int(reference_path[i][0]), int(reference_path[i][1]),
                          int(reference_path[i][2]),
                          int(reference_path[i][3]))
            refpath.append(point)

        # print(refpath)

        reference_path_name = os.getcwd() +"/data_raw/"+"reference_path" + str(iteration) + ".npy"
        np.save(file=reference_path_name, arr=reference_path)
    # b = np.load(file="reference_path.npy")
    # print(b, len(b))
    elif reinitial_flag == 2:
        reference_path_name = os.getcwd() + "/data_raw/" + "reference_path" + str(iteration) + ".npy"
        trajectory_ref_temp = np.load(file=reference_path_name)

        for i in range(len(trajectory_ref_temp)):
            point = Point(int(trajectory_ref_temp[i][0]), int(trajectory_ref_temp[i][1]),
                          int(trajectory_ref_temp[i][2]),
                          int(trajectory_ref_temp[i][3]))
            if occ_grid[point.x][point.y][point.z] != 0 :
                print("wrong")
            # refpath.append(point)

    # sum of privacy risk with occ_grid for reference path
    PR_sum_unknown_ref = 0
    # sum of privacy risk with occ_grid_known for reference path
    PR_sum_known_ref = 0


    num_ca = 0
    num_intruder = 0
    for point in refpath:
        # sum_ref += pri_grid[point.x][point.y][point.z] * math.exp(-(point.ca))
        # if pri_grid[point.x][point.y][point.z] > 0:
        # print(point, pri_grid_known[point.x][point.y][point.z])
        # print(point, caculate_privacy_surround(grid, point, occ_grid, privacy_radius), caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius))
        # print(caculate_privacy_surround(grid, point, occ_grid, privacy_radius))
        # print(caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius))
        PR_sum_unknown_ref += caculate_privacy_surround(grid, point, occ_grid, privacy_radius)
        PR_sum_known_ref += caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)

    print("\033[94m Fitness for reference path:\033[0m \n", len(refpath) - 1, PR_sum_unknown_ref,  PR_sum_known_ref)
    # print(privacy_sum)
    log.info("Initial_planning: Length of reference trajectory: %d" %(len(refpath) - 1))
    log.info("Initial_planning: Sum of privacy threat of reference trajectory(occ_grid): %f" %PR_sum_unknown_ref)
    log.info("Initial_planning: Sum of privacy threat of reference trajectory(occ_grid_known): %f" % PR_sum_known_ref)





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
    exploration_rate = config.exploration_rate

    # drone parameter
    starting_point = config.starting_point
    end_point = config.end_point
    T_budget = config.T_budget
    T_optimal = config.T_optimal
    viewradius = config.viewradius
    Kca = config.Kca
    threat_list = []
    reinitial_flag = reinitial_flag
    preference = config.preference

    # 全局信息，用作baseline
    # occ_grid_name = "occ_grid" + str(iteration) + ".npy"
    occ_grid_name = os.getcwd() +"/data/"+"occ_grid-" +str(num) + ".npy"
    occ_grid = np.load(file=occ_grid_name)
    # occ_grid = np.load(file="occ_grid-1.npy")
    pri_grid, privacy_sum = privacy_init(grid_x, grid_y, grid_z, occ_grid, privacy_radius)

    if reinitial_flag != 0:
        # occ_grid_known, pri_grid_known, privacy_sum_known = initialmapwithknowngrid_ratio(grid_x, grid_y, grid_z,
        #                                                                             privacy_threshold, privacy_radius,
        #                                                                             occ_grid, exploration_rate)
        # 最初始探索的地图
        occ_grid_known_name = os.getcwd() +"/data/"+"occ_grid_known_initial" + str(iteration) + ".npy"
        occ_grid_known = np.load(file=occ_grid_known_name)
        pri_grid_known, privacy_sum_known = privacy_init(grid_x, grid_y, grid_z, occ_grid_known, privacy_radius)
    else:
        # 本局地图信息，更新后的
        occ_grid_known_name = os.getcwd() +"/data/"+"occ_grid_known" + str(iteration) + ".npy"
        occ_grid_known = np.load(file=occ_grid_known_name)
        # occ_grid_known = np.load(file="occ_grid_known.npy")
        pri_grid_known, privacy_sum_known = privacy_init(grid_x, grid_y, grid_z, occ_grid_known, privacy_radius)

    refpath = []
    reference_path = []
    no_solution_flag = 1
    if reinitial_flag == 1:
        reference_path.append([0,0,0,1])
        # reference_path.append([1, 0, 0, 1])
        for i in range (17):
            reference_path.append([1,i,0,1])
        for i in range (1, 10):
            reference_path.append([1,16,i,1])
        for i in range (17, 25):
            reference_path.append([1,i,9,1])
        for i in range (10, 38):
            reference_path.append([1,24,i,1])
        for i in range (25, 34):
            reference_path.append([1,i,37,1])
        for i in range (38,50):
            reference_path.append([1,33,i,1])
        for i in range (34,50):
            reference_path.append([1,i,49,1])
        # reference_path.append([1, 49, 49, 1])
        reference_path.append([0, 49, 49, 1])
        print(reference_path)

        for i in range(len(reference_path)):
            point = Point(int(reference_path[i][0]), int(reference_path[i][1]),
                          int(reference_path[i][2]),
                          int(reference_path[i][3]))
            refpath.append(point)

        # print(refpath)

        reference_path_name = os.getcwd() +"/data/"+"reference_path" + str(iteration) + ".npy"
        np.save(file=reference_path_name, arr=reference_path)
    # b = np.load(file="reference_path.npy")
    # print(b, len(b))
    elif reinitial_flag == 2:
        reference_path_name = os.getcwd() + "/data/" + "reference_path" + str(iteration) + ".npy"
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





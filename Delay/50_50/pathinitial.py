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
from Astar import AStar

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
        # print(occ_grid_known)
        pri_grid_known, privacy_sum_known = privacy_init(grid_x, grid_y, grid_z, occ_grid_known, privacy_radius)
    else:
        # 本局地图信息，更新后的
        occ_grid_known_name = os.getcwd() +"/data/"+"occ_grid_known" + str(iteration) + ".npy"
        occ_grid_known = np.load(file=occ_grid_known_name)
        # occ_grid_known = np.load(file="occ_grid_known.npy")
        pri_grid_known, privacy_sum_known = privacy_init(grid_x, grid_y, grid_z, occ_grid_known, privacy_radius)

    trajectory_ref = []
    no_solution_flag = 0
    if reinitial_flag == 1:
        starttime = time.time()
        # aStar1 = AStar(occ_grid_known, pri_grid_known, grid, privacy_sum_known, starting_point, end_point, [1], T_budget,
        #                threat_list, T_optimal)
        aStar1 = AStar(occ_grid_known, pri_grid_known, grid, privacy_sum, starting_point, end_point, [1,2,3,4], T_budget,
                        threat_list, 0, T_optimal, preference, privacy_radius)
        #aStar1 = AStar(occ_grid_known, pri_grid_known, grid, privacy_sum, starting_point, end_point, [1], T_optimal,
        #           threat_list, T_optimal, preference)
        trajectory_ref = aStar1.start()

        endtime = time.time()
        dtime = endtime - starttime
        # print("程序运行时间：%.8s s" % dtime)

        if trajectory_ref == None:
            return no_solution_flag
        else:
            trajectory_ref = [starting_point] + trajectory_ref
            # no_solution_flag = 1


        refpath = np.zeros((len(trajectory_ref), 4))


        for i in range(len(trajectory_ref)):
            refpath[i] = [trajectory_ref[i].x, trajectory_ref[i].y, trajectory_ref[i].z, trajectory_ref[i].ca]
            # if occ_grid[trajectory_ref[i].x][trajectory_ref[i].y][trajectory_ref[i].z] != 0:
                # print("pi: wrong", trajectory_ref[i])

        reference_path_name = os.getcwd() +"/data/"+"reference_path" + str(iteration) + ".npy"
        np.save(file=reference_path_name, arr=refpath)
    # b = np.load(file="reference_path.npy")
    # print(b, len(b))
    elif reinitial_flag == 2:
        reference_path_name = os.getcwd() + "/data/" + "reference_path" + str(iteration) + ".npy"
        trajectory_ref_temp = np.load(file=reference_path_name)

        for i in range(len(trajectory_ref_temp)):
            point = Point(int(trajectory_ref_temp[i][0]), int(trajectory_ref_temp[i][1]),
                          int(trajectory_ref_temp[i][2]),
                          int(trajectory_ref_temp[i][3]))
            trajectory_ref.append(point)

    planpath = np.zeros((len(trajectory_ref), 4))
    # sum of privacy risk with occ_grid for reference path
    PR_sum_unknown_ref = 0
    # sum of privacy risk with occ_grid_known for reference path
    PR_sum_known_ref = 0

    # print("The occ_grid is: ")
    # for m in range(grid_x):
    #     print("The value of x: ", m)
    #     print(occ_grid[m])
    # print("The occ_grid_known is: ")
    # for m in range(grid_x):
    #     print("The value of x: ", m)
    #     print(occ_grid_known[m])

    num_ca = 0
    num_intruder = 0
    for point in trajectory_ref:
        # sum_ref += pri_grid[point.x][point.y][point.z] * math.exp(-(point.ca))
        # if pri_grid[point.x][point.y][point.z] > 0:
        # print(point, pri_grid_known[point.x][point.y][point.z])
        # print(point, caculate_privacy_surround(grid, point, occ_grid, privacy_radius), caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius))
        # print(caculate_privacy_surround(grid, point, occ_grid, privacy_radius))
        # print(caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius))
        PR_sum_unknown_ref += caculate_privacy_surround(grid, point, occ_grid, privacy_radius)
        PR_sum_known_ref += caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)

    print("\033[94m Fitness for reference path:\033[0m \n", len(trajectory_ref) - 1, PR_sum_unknown_ref,  PR_sum_known_ref)
    # print(privacy_sum)
    log.info("Initial_planning: Length of reference trajectory: %d" %(len(trajectory_ref) - 1))
    log.info("Initial_planning: Sum of privacy threat of reference trajectory(occ_grid): %f" %PR_sum_unknown_ref)
    log.info("Initial_planning: Sum of privacy threat of reference trajectory(occ_grid_known): %f" % PR_sum_known_ref)


    no_solution_flag = 0 ## 0628

    if reinitial_flag == 1:
        aStar2 = AStar(occ_grid, pri_grid, grid, privacy_sum, starting_point, end_point, [1,2,3,4], T_budget, threat_list, 0,
                       T_optimal, preference, privacy_radius)
        trajectory_plan = aStar2.start()

        if trajectory_plan == None: ## 0628
            return no_solution_flag
        else:
            trajectory_plan = [starting_point] + trajectory_plan
            no_solution_flag = 1

        # trajectory_plan = [starting_point] + trajectory_plan
        planpath = np.zeros((len(trajectory_plan), 4))

        for i in range(len(trajectory_plan)):
            planpath[i] = [trajectory_plan[i].x, trajectory_plan[i].y, trajectory_plan[i].z, trajectory_plan[i].ca]

        plan_path_name = os.getcwd() +"/data/"+"plan_path" + str(iteration) + ".npy"
        np.save(file=plan_path_name, arr=planpath)
        # c = np.load(file="plan_path.npy")
        # print(c, len(c))
        occ_grid_known = copy.deepcopy(occ_grid)

        # sum of privacy risk with occ_grid for best path
        PR_sum_unknown_plan = 0
        # sum of privacy risk with occ_grid_known for best path
        PR_sum_known_plan = 0

        num_intruder_plan = 0
        for point in trajectory_plan:
            # sum_plan += pri_grid[point.x][point.y][point.z] * math.exp(-(point.ca))
            # if pri_grid[point.x][point.y][point.z] > 0:
            # print(point, caculate_privacy_surround(grid, point, occ_grid, privacy_radius), caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius))
        # print(point, pri_grid_known[point.x][point.y][point.z])
            PR_sum_unknown_plan += caculate_privacy_surround(grid, point, occ_grid, privacy_radius)
            PR_sum_known_plan += caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)
        print("\033[94m Fitness for replanned path:\033[0m \n", len(trajectory_plan) - 1, PR_sum_unknown_plan, PR_sum_known_plan)
        # print(privacy_sum)
        log.info("Initial_planning: Length of best trajectory: %d" % (len(trajectory_plan) - 1))
        log.info("Initial_planning: Sum of privacy threat of best trajectory(occ_grid): %f" % PR_sum_unknown_plan)
        log.info("Initial_planning: Sum of privacy threat of best trajectory(occ_grid_known): %f" % PR_sum_known_plan)

    # if reinitial_flag:
    #     occ_grid_known_name = "occ_grid_known" + str(iteration) + ".npy"
    #     np.save(file=occ_grid_known_name, arr=occ_grid_known)
        # np.save(file="occ_grid_known.npy", arr=occ_grid_known)
        # c = np.load(file="occ_grid_known.npy")
        # for m in range(grid_x):
        #    print("The value of x: ", m)
        #    print(c[m])

    return  no_solution_flag


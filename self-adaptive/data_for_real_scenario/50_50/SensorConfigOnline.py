#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
add camera into searching space
"""
import time
from Point2 import Point
import numpy as np
from mapTools import privacy_init, hasprivacythreat2, initialmapwithknowngrid, initialmapwithknowngrid_ratio, caculate_privacy_surround
import copy
from Configure import configure
import math
from heapq import heappush
import sys
import os

# from log import Log
# log = Log(__name__).getlog()

sys.setrecursionlimit(1000000)


def Astar_Sensor_Config_online(config, iteration, log, num):

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
    viewradius = config.viewradius
    Kca = config.Kca
    threat_list = []

    #occ_grid, obstacle_num, occ_grid_known, pri_grid_known, privacy_sum_known = initialmap(grid_x, grid_y, grid_z,
    #                                                                                       starting_point, end_point,
    #                                                                                       safety_threshold,
    #                                                                                       privacy_threshold,
    #                                                                                       privacy_radius)
    # occ_grid_name = "occ_grid" + str(iteration) + ".npy"
    occ_grid_name = os.getcwd() + "/data/" + "occ_grid-" + str(num) + ".npy"
    occ_grid = np.load(file=occ_grid_name)
    # occ_grid = np.load(file="occ_grid-1.npy")
    pri_grid, privacy_sum = privacy_init(grid_x, grid_y, grid_z, occ_grid, privacy_radius)
    # occ_grid_known_name = "occ_grid_known" + str(iteration) + ".npy"
    occ_grid_known_name = os.getcwd() +"/data/"+"occ_grid_known_initial" + str(iteration) + ".npy"
    occ_grid_known = np.load(file=occ_grid_known_name)
    # occ_grid_known = np.load(file="occ_grid_known.npy")
    pri_grid_known, privacy_sum_known = privacy_init(grid_x, grid_y, grid_z, occ_grid_known, privacy_radius)
    #occ_grid_known, pri_grid_known, privacy_sum_known = initialmapwithknowngrid(grid_x, grid_y, grid_z,
    #                                                                            privacy_threshold, privacy_radius,
    #                                                                            occ_grid)
    #pri_grid, privacy_sum = privacy_init(grid_x, grid_y, grid_z, occ_grid, privacy_radius)
    # print("The occ_grid is: ")
    # for m in range(grid_x):
    #     print("The value of x: ", m)
    #     print(occ_grid[m])
    starttime = time.time()
    #aStar = AStar(occ_grid, pri_grid_known, grid, privacy_sum_known, starting_point, end_point, 1 , T_budget)
    # 开始寻路
    #trajectory_ref = aStar.start()
    #trajectory_ref_temp = np.load(file="plan_path.npy")
    # 导入初规划路径路径结果
    reference_path_name = os.getcwd() +"/data/"+"reference_path" + str(iteration) + ".npy"
    trajectory_ref_temp = np.load(file=reference_path_name)
    # trajectory_ref_temp = np.load(file="reference_path.npy")
    trajectory_ref = []
    for i in range (len(trajectory_ref_temp)):
        point = Point(int(trajectory_ref_temp[i][0]),int(trajectory_ref_temp[i][1]),int(trajectory_ref_temp[i][2]),int(trajectory_ref_temp[i][3]))
        trajectory_ref.append(point)

    endtime = time.time()
    dtime = endtime - starttime
    # print("程序运行时间：%.8s s" % dtime)

    path_grid = copy.deepcopy(occ_grid)

    # print(len(pathList))
    sum = 0
    if trajectory_ref == None:
        print("No solution!")
        exit(0)
    else:
        for point in trajectory_ref:
            #print(point)
            path_grid[point.x][point.y][point.z] = 9
            sum += pri_grid_known[point.x][point.y][point.z]
            # print(point, pri_grid_known[point.x][point.y][point.z])
        # print("----------------------", len(trajectory_ref))

    # 再次显示地图

    # print(path_grid, sum)
    #trajectory_ref = [starting_point] + trajectory_ref
    trajectory_plan = copy.deepcopy(trajectory_ref)
    # sensor_initial = np.zeros(len(trajectory_plan))
    # sensor_plan = copy.deepcopy(sensor_initial)
    time_step = 0
    # print("---------------------------------")
    # print("The length of original plan is: ", len(trajectory_plan))
    # for m in range(len(trajectory_plan)):
    #     print("The No.", m, " step: ", trajectory_plan[m])
    # print()

    idx = 0
    current_f = sum + len(trajectory_plan)
    replantime = 0

    while not (idx >= len(trajectory_plan)):
        current_p = trajectory_plan[idx]
        current_ca = trajectory_plan[idx].ca
        #print("currentnow:", current_p, idx)

        if current_p.x == end_point.x and current_p.y == end_point.y and current_p.z == end_point.z :
            # print("current:", current_p, idx)
            break

        next_p = trajectory_plan[idx+1]
        next_idx = idx + 1
        # print (current_p,next_p,next_idx)
        # print("The UAV would move a step: ")
        # print("The current point: ", current_p)
        # print("The next point: ", next_p)
        # print("The index of next point: ", next_idx, "\n")

        if current_ca == 2:  ## 1 = camera is open with high resolution, 2 = camera is off with lower resolution 0630
            time_step += 1
            current_p = next_p
            idx += 1
            # print("The UAV has finished this step.\n")
            continue

        # take picture
        # update occ_grid, pri_grid
        flag, occ_grid_known, pri_grid_known, privacy_sum_known, threat_list = hasprivacythreat2 (current_p, occ_grid_known, occ_grid, pri_grid_known, privacy_sum_known, config)
        # print("The length of privacy_list: ", len(threat_list))
        #for m in range(len(threat_list)):
        #    print(threat_list[m])

        if flag:
            # localization
            # p_threat, h_impact = privacy_modeling()
            # update occ_grid, pri_grid
            replan_flag = 0
            for j in range (idx+1, len(trajectory_plan)):
                if caculate_privacy_surround(grid, trajectory_plan[j], occ_grid_known, privacy_radius) > 0:
                # if pri_grid_known[trajectory_plan[j].x][trajectory_plan[j].y][trajectory_plan[j].z] > 0:
                    if trajectory_plan[j].ca != 2:
                        trajectory_plan[j].ca = 2
                        replan_flag = 1
                        # print("change sensor configuration for next point")
            if replan_flag :
                replantime += 1
            # print("replan_time:", replantime)
            # cam_off = 0
            # for ll in range(len(trajectory_plan)):
            #     sum += pri_grid_known[trajectory_plan[ll].x][trajectory_plan[ll].y][trajectory_plan[ll].z]
            #     cam_off += trajectory_plan[ll].ca
            #     print("now", trajectory_plan[ll])
            # print("The length of now_trajectory_plan: ", len(trajectory_plan), sum, cam_off)

            # current_f = sum + len(trajectory_plan) + cam_off

            # print("fitness", current_f)

        time_step += 1
        idx = idx + 1
        # print("The UAV has finished this step.\n")

    # print(occ_grid)
    path_grid2 = copy.deepcopy(occ_grid)

    ## log info
    # sum of privacy risk with pri_grid
    PR_sum_unknown_plan = 0
    # sum of privacy risk with pri_grid_knwon
    PR_sum_known_plan = 0
    # times of camera reconfigured
    num_ca_plan = 0
    # times of with intrusion of restricted area with pri_grid
    num_intruder_notknown_plan = 0
    # times of with intrusion of restricted area with pri_grid_knwon
    num_intruder_known_plan = 0
    # num_should_avoid_intruder_plan = 0
    # num_cannot_avoid_intruder_plan = 0

    for point in trajectory_plan:
        if point.ca == 1:
            path_grid2[point.x][point.y][point.z] = 7
        else:
            path_grid2[point.x][point.y][point.z] = 10
            num_ca_plan += 1
        # sum_unknown_plan += pri_grid[point.x][point.y][point.z] * math.exp(-(point.ca))
        # sum_known_plan += pri_grid_known[point.x][point.y][point.z] * math.exp(-(point.ca))
        PR_sum_unknown_plan += caculate_privacy_surround(grid, point, occ_grid, privacy_radius)
        PR_sum_known_plan += caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)
        if pri_grid[point.x][point.y][point.z] > 0 and occ_grid[point.x][point.y][point.z] == 0:
            num_intruder_notknown_plan += 1

        if pri_grid_known[point.x][point.y][point.z] > 0 and occ_grid_known[point.x][point.y][point.z] == 0:
            num_intruder_known_plan += 1

        # if occ_grid[point.x][point.y][point.z] == 2 or occ_grid[point.x][point.y][point.z] == 3 or occ_grid[point.x][point.y][point.z] == 4 :
        #     num_should_avoid_intruder_plan += 1
        #
        # if occ_grid_known[point.x][point.y][point.z] == 2 or occ_grid_known[point.x][point.y][point.z] == 3 or occ_grid_known[point.x][point.y][point.z] == 4:
        #     num_cannot_avoid_intruder_plan += 1
        # print(point, pri_grid_known[point.x][point.y][point.z])
    print("\033[94mFitness for replanned path:\033[0m \n ", len(trajectory_plan) - 1, PR_sum_unknown_plan,
          PR_sum_known_plan,
          num_ca_plan,
          num_intruder_notknown_plan, num_intruder_known_plan)
    log.info("Online_Sensor_Config: Length of replanned trajectory: %d" % (len(trajectory_plan) - 1))
    log.info("Online_Sensor_Config: Sum of privacy threat of replanned trajectory(occ_grid): %f" % PR_sum_unknown_plan)
    log.info("Online_Sensor_Config: Sum of privacy threat of replanned trajectory(occ_grid_known): %f" % PR_sum_known_plan)
    log.info("Online_Sensor_Config: Times of turning off camera of replanned trajectory: %d" % num_ca_plan)
    # log.info("Online_Sensor_Config: Times of intrusion of replanned trajectory: %d" % num_intruder_plan)
    log.info("Online_Sensor_Config: Times of intrusion of replanned trajectory(occ_grid): %d" % num_intruder_notknown_plan)
    log.info("Online_Sensor_Config: Times of intrusion of replanned trajectory(occ_grid_known): %d" % num_intruder_known_plan)
    # log.info(
    #     "Online_Sensor_Config: Times of intrusion of replanned trajectory(should avoid): %d" % num_should_avoid_intruder_plan)
    # log.info(
    #     "Online_Sensor_Config: Times of intrusion of replanned trajectory(cannot avoid): %d" % num_cannot_avoid_intruder_plan)


    # 再次显示地图
    PR_sum_unknown_ref = 0
    PR_sum_known_ref = 0
    num_ca_ref = 0
    num_intruder_notknown_ref = 0
    num_intruder_known_ref = 0
    # num_should_avoid_intruder_ref = 0
    # num_cannot_avoid_intruder_ref = 0

    for point in trajectory_ref:

        # sum_unknown_ref += pri_grid[point.x][point.y][point.z] * math.exp(-(point.ca))
        # sum_known_ref += pri_grid_known[point.x][point.y][point.z] * math.exp(-(point.ca))
        PR_sum_unknown_ref += caculate_privacy_surround(grid, point, occ_grid, privacy_radius)
        PR_sum_known_ref += caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)
        if point.ca == 2:
            num_ca_ref += 1
        # print(point, pri_grid_known[point.x][point.y][point.z])
        if pri_grid[point.x][point.y][point.z] > 0 and occ_grid[point.x][point.y][point.z] == 0:
            num_intruder_notknown_ref += 1

        if pri_grid_known[point.x][point.y][point.z] > 0 and occ_grid_known[point.x][point.y][point.z] == 0:
            num_intruder_known_ref += 1

    # if  occ_grid[point.x][point.y][point.z] == 2 or occ_grid[point.x][point.y][point.z] == 3 or occ_grid[point.x][point.y][point.z] == 4 :
        #     num_should_avoid_intruder_ref += 1
        #
        # if occ_grid_known[point.x][point.y][point.z] == 2 or occ_grid_known[point.x][point.y][point.z] == 3 or occ_grid_known[point.x][point.y][point.z] == 4:
        #     num_cannot_avoid_intruder_ref += 1
    # print("\033[94m Fitness for reference path:\033[0m \n", len(trajectory_ref) - 1, sum_ref, num_ca_ref,
    #       num_intruder_ref)
    print("\033[94mFitness for replanned path:\033[0m \n ", len(trajectory_plan) - 1, PR_sum_unknown_ref, PR_sum_known_ref,
          num_ca_ref,
          num_intruder_notknown_ref, num_intruder_known_ref)
    log.info("Online_Sensor_Config: Length of preplanned trajectory: %d" % (len(trajectory_ref) - 1))
    log.info("Online_Sensor_Config: Sum of privacy threat of preplanned trajectory(occ_grid): %f" % PR_sum_unknown_ref)
    log.info("Online_Sensor_Config: Sum of privacy threat of preplanned trajectory(occ_grid_known): %f" % PR_sum_known_ref)
    log.info("Online_Sensor_Config: Times of turning off camera of preplanned trajectory: %d" % num_ca_ref)
    # log.info("Online_Sensor_Config: Times of intrusion of preplanned trajectory: %d" % num_intruder_ref)
    log.info(
        "Online_Sensor_Config: Times of intrusion of preplanned trajectory(occ_grid): %d" % num_intruder_notknown_ref)
    log.info("Online_Sensor_Config: Times of intrusion of preplanned trajectory(occ_grid_known): %d" % num_intruder_known_ref)
    # log.info(
    #     "Online_Sensor_Config: Times of intrusion of preplanned trajectory(should avoid): %d" % num_should_avoid_intruder_ref)
    # log.info(
    #     "Online_Sensor_Config: Times of intrusion of preplanned trajectory(cannot avoid): %d" % num_cannot_avoid_intruder_ref)
    

    #print(path_grid2, sum)
    # print("---------------------------------")
    # print("The last plan is finished!")
    # print("The length of last plan is: ", len(trajectory_plan))
    # for m in range(len(trajectory_plan)):
    #     print("The No.", m, " step: ", trajectory_plan[m])
    end = time.time()
    dtime = end - starttime
    # print("程序运行时间：%.8s s" % dtime)
    print("\033[94m Replan times: \033[0m", replantime)
    log.info("Online_Sensor_Config: Replanning times: %d" % replantime)
    #grid_visualization(occ_grid, starting_point, end_point, trajectory_plan, trajectory_ref)

    occ_grid_known_name = os.getcwd() +"/data/"+"occ_grid_known" + str(iteration) + ".npy"
    np.save(file=occ_grid_known_name, arr=occ_grid_known)
    # np.save(file="occ_grid_known.npy", arr=occ_grid_known)
    # b = np.load(file="occ_grid_known.npy")
    # for m in range(grid_x):
    #     print("The value of x: ", m)
    #     print(b[m])

    plan_path = np.zeros((len(trajectory_plan), 4))
    for i in range(len(trajectory_plan)):
        plan_path[i] = [trajectory_plan[i].x, trajectory_plan[i].y, trajectory_plan[i].z, trajectory_plan[i].ca]

    plan_path_SC_name = os.getcwd() +"/data/"+"plan_path_SC" + str(iteration) + ".npy"
    np.save(file=plan_path_SC_name, arr=plan_path)
    # np.save(file="plan_path_SC.npy", arr=plan_path)
    # c = np.load(file="plan_path_SC.npy")
    # print(c, len(c))

    exploration_rate = 0

    for i in range(grid_x):
        for j in range(grid_y):
            for k in range(grid_z):
                if occ_grid_known[i][j][k]!=occ_grid[i][j][k]:
                    exploration_rate += 1
    exploration_rate =  1 -  exploration_rate/(grid_x * grid_y * grid_z * privacy_threshold)
    print("\033[94m exploration rate: \033[0m", exploration_rate)
    log.info("Online_Sensor_Config: Exploration rate: %f" % exploration_rate)

    return 




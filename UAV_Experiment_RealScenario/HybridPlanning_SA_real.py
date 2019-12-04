#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
add camera into searching space
"""
import time
from Point2 import Point
import numpy as np
from mapTools import privacy_init, initialmapwithknowngrid, initialmapwithknowngrid_ratio, caculate_privacy_surround
import copy
from Configure import configure
import math
# from quickSort import quick_sort
import sys
import os
from heapq import heappush
from Astar_real import AStar
from flight_control import flight_control
from demo6 import hasprivacythreat_real

# from log import Log
# log = Log(__name__).getlog()

sys.setrecursionlimit(1000000)

def Astar_Hybrid_Planning_online(config, log, occ_grid_known, reference, occ_grid, socket, colorflag, sizeflag, continue_time):

    s = socket

    grid_x = config.grid_x
    grid_y = config.grid_y
    grid_z = config.grid_z
    grid = config.grid

    privacy_threshold = config.privacy_threshold
    privacy_radius = config.privacy_radius

    # drone parameter
    starting_point = config.starting_point
    end_point = config.end_point
    T_budget = config.T_budget
    T_optimal = config.T_optimal
    threat_list = []
    replantime = 0
    delay = config.delay


    occ_grid = copy.deepcopy(occ_grid)
    occ_grid_known = copy.deepcopy(occ_grid_known)

    starttime = time.time()
    trajectory_ref_temp = reference
    trajectory_ref = []
    for i in range(len(trajectory_ref_temp)):
        point = Point(int(trajectory_ref_temp[i][0]), int(trajectory_ref_temp[i][1]), int(trajectory_ref_temp[i][2]),
                      int(trajectory_ref_temp[i][3]))
        trajectory_ref.append(point)

    trajectory_plan = copy.deepcopy(trajectory_ref)



    time_step = 0

    idx = 0
    num_of_no_solution = 0

    while not (idx >= len(trajectory_plan)):
        current_p = trajectory_plan[idx]
        current_ca = trajectory_plan[idx].ca

        print("current position of UAV:", current_p)
        log.info("current position of UAV: [%d, %d, %d, %d]" %(current_p.x, current_p.y, current_p.z, current_p.ca))

        if current_p.x == end_point.x and current_p.y == end_point.y and current_p.z == end_point.z:
            plan_path = np.zeros((len(trajectory_plan), 4))
            for i in range(len(trajectory_plan)):
                plan_path[i] = [trajectory_plan[i].x, trajectory_plan[i].y, trajectory_plan[i].z,
                                trajectory_plan[i].ca]
            plan_path_Hybrid_name = os.getcwd() + "/data/" + "plan_path_Hybrid_temp" + str(idx) + ".npy"
            np.save(file=plan_path_Hybrid_name, arr=plan_path)
            occ_grid_known_name = os.getcwd() + "/data/" + "occ_grid_known_Hybrid_temp" + str(idx) + ".npy"
            np.save(file=occ_grid_known_name, arr=occ_grid_known)

            break

        next_p = trajectory_plan[idx + 1]
        next_idx = idx + 1

        if current_ca == 2: ## 1 = camera is open with high resolution, 2 = camera is off with lower resolution
            time_step += 1
            current_p = next_p
            plan_path = np.zeros((len(trajectory_plan), 4))
            for i in range(len(trajectory_plan)):
                plan_path[i] = [trajectory_plan[i].x, trajectory_plan[i].y, trajectory_plan[i].z,
                                trajectory_plan[i].ca]
            plan_path_Hybrid_name = os.getcwd() + "/data/" + "plan_path_Hybrid_temp" + str(idx) + ".npy"
            np.save(file=plan_path_Hybrid_name, arr=plan_path)
            occ_grid_known_name = os.getcwd() + "/data/" + "occ_grid_known_Hybrid_temp" + str(idx) + ".npy"
            np.save(file=occ_grid_known_name, arr=occ_grid_known)

            """
            move a step
            """
            flight_control(idx, idx + 1, trajectory_plan, s, continue_time)

            idx += 1

            continue

        flag = 0


        flag, occ_grid_known = hasprivacythreat_real(current_p, occ_grid_known, config, idx, colorflag, sizeflag, log)


        if flag:
            ## 0702
            point = trajectory_plan[next_idx]

            affect_path = []

            start = idx + 1 + delay
            start = math.ceil(start)

            start_idx = 0
            end_idx = 0

            while start <= len(trajectory_plan) - (math.ceil(delay) + 1):
                affect_path = []
                point = trajectory_plan[start]
                # print(start, point)
                if (caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)) > 0:
                    start_idx = start
                    end_idx = start_idx
                    # print(start_idx)
                    for k in range (start_idx, len(trajectory_plan)):
                        point = trajectory_plan[k]
                        if (caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)) > 0:
                            end_idx = k
                            # print(end_idx)
                    end_idx = min(end_idx + 1, len(trajectory_plan))
                    start_idx = max(0, start_idx - 1)
                    # print(start_idx, end_idx)
                    affect_path.append([start_idx, end_idx])
                    start = end_idx + 1

                    # 开始寻路
                    ## 0628
                    print("affect_path", affect_path)

                    # log.info ("affect_path [%d, %d]" % (affect_path[0], affect_path[1]))
                    print("producing local planning")
                    log.info ("producing local planning")
                    current_p = trajectory_plan[affect_path[0][0]]
                    original_index = affect_path[0][0]
                    if affect_path[0][1] >= len(trajectory_plan):
                        next_idx = len(trajectory_plan)-1
                        next_p = trajectory_plan[-1]
                    else:
                        next_idx = affect_path[0][1]
                        next_p = trajectory_plan[affect_path[0][1]]

                    print(next_p, next_idx, current_p, original_index)
                    log.info ("affect_path:[from: %d (%d, %d, %d, %d) to: %d (%d, %d, %d, %d)]" % (original_index, current_p.x, current_p.y, current_p.z, current_p.ca, next_idx, next_p.x, next_p.y, next_p.z, next_p.ca))


                    T_plan = T_budget - (len(trajectory_plan) - 1) + (next_idx - original_index)
                    T_plan_optimal = T_optimal - (len(trajectory_plan) - 1) + (next_idx - original_index)

                    distance = abs(trajectory_plan[next_idx].x - trajectory_plan[original_index].x) + abs(
                        trajectory_plan[next_idx].y - trajectory_plan[original_index].y) + abs(
                        trajectory_plan[next_idx].z - trajectory_plan[original_index].z)

                    ## have enough time for planning
                    if T_plan >= distance:
                        replantime += 1
                        aStar_pp = AStar(occ_grid_known, grid, current_p, next_p, T_plan, threat_list, 0, T_plan_optimal, privacy_radius)
                        trajectory_optimal_pp = aStar_pp.start()

                        temp_sum = 0
                        PR_temp_sum_unknown = 0
                        PR_temp_sum_known = 0
                        length_PP = 0
                        no_solution_flag = 0
                        if trajectory_optimal_pp != None:
                            length_PP = len(trajectory_optimal_pp)
                            for jj in range(len(trajectory_optimal_pp)):
                                point = trajectory_optimal_pp[jj]
                                PR_temp_sum_unknown += caculate_privacy_surround(grid, point, occ_grid, privacy_radius)
                                PR_temp_sum_known += caculate_privacy_surround(grid, point, occ_grid_known,
                                                                               privacy_radius)
                                # print("privacy risk:", caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius), "point:", point)
                            if PR_temp_sum_known > 0:
                                no_solution_flag = 1
                            elif len(trajectory_optimal_pp) > T_plan_optimal:
                                no_solution_flag = 2
                        else:
                            length_PP = 0
                            no_solution_flag = 3

                        ## 如果找不到没有侵犯隐私的可行解，或者规划出的可行解超出了时间的约束，说明只进行路径规划不可行
                        if no_solution_flag > 0:
                            num_of_no_solution += 1
                            # print(occ_grid_known)
                            print(
                                "Online_Hybrid_Planning: No solution for local planning: from [%d, %d, %d] to [%d, %d, %d]. No solution flag is %d, PR for PP is %f. length of PP is %d, T plan optimal is %d"
                                % (
                                    current_p.x, current_p.y, current_p.z, next_p.x, next_p.y, next_p.z,
                                    no_solution_flag,
                                    PR_temp_sum_known, length_PP, T_plan_optimal))
                            log.info(
                                "Online_Hybrid_Planning: No solution for local planning: from [%d, %d, %d] to [%d, %d, %d]. No solution flag is %d, PR for PP is %f. length of PP is %d, T plan optimal is %d"
                                % (
                                    current_p.x, current_p.y, current_p.z, next_p.x, next_p.y, next_p.z,
                                    no_solution_flag,
                                    PR_temp_sum_known, length_PP, T_plan_optimal))
                            aStar = AStar(occ_grid_known, grid, current_p, next_p, T_plan, threat_list, 1, T_plan_optimal, privacy_radius)
                            trajectory_optimal = aStar.start()
                        else:
                            trajectory_optimal = copy.deepcopy(trajectory_optimal_pp)

                        if trajectory_optimal != None:

                            first_part = trajectory_plan[0:original_index + 1]
                            if next_idx == len(trajectory_plan) - 1:
                                following_part = []
                            else:
                                following_part = trajectory_plan[next_idx + 1:]

                            for m in range(len(trajectory_optimal)): ## force camera configuration
                                trajectory_optimal[m].ca = 2

                            now_trajectory = first_part + trajectory_optimal + following_part

                            trajectory_plan = copy.deepcopy(now_trajectory)

                        else:
                            pass

                    else:
                        pass

                else:
                    start += 1

        ## try
        for j in range(idx+1, len(trajectory_plan)):
            if caculate_privacy_surround(grid, trajectory_plan[j], occ_grid_known, privacy_radius) > 0:
                # if pri_grid_known[trajectory_plan[j].x][trajectory_plan[j].y][trajectory_plan[j].z] > 0:
                if trajectory_plan[j].ca != 2:
                    trajectory_plan[j].ca = 2
                    print("\033[94m force camera configuration \033[0m")

        plan_path = np.zeros((len(trajectory_plan), 4))
        for i in range(len(trajectory_plan)):
            plan_path[i] = [trajectory_plan[i].x, trajectory_plan[i].y, trajectory_plan[i].z,
                            trajectory_plan[i].ca]
        plan_path_Hybrid_name = os.getcwd() + "/data/" + "plan_path_Hybrid_temp" + str(idx) + ".npy"
        np.save(file=plan_path_Hybrid_name, arr=plan_path)

        occ_grid_known_name = os.getcwd() + "/data/" + "occ_grid_known_Hybrid_temp" + str(idx) + ".npy"
        np.save(file=occ_grid_known_name, arr=occ_grid_known)

        """
        move a step
        """
        flight_control(idx, idx + 1, trajectory_plan, s, continue_time)

        time_step += 1
        idx = idx + 1



    end = time.time()
    dtime = end - starttime
    # print("程序运行时间：%.8s s" % dtime)
    # print("sumpri:", sum)
    # print("num_ca:", num_ca)
    print("\033[94m Replan times: \033[0m", replantime)
    log.info("Online_Hybrid_Planning: Replanning times: %d" % replantime)
    print("\033[94m No solution times: \033[0m", num_of_no_solution)
    log.info("Online_Hybrid_Planning: No solution times: %d" % num_of_no_solution)
    print("\033[94m Execution time: \033[0m",  dtime)
    log.info("Online_Hybrid_Planning: Execution time: %f" %  dtime)
    # grid_visualization(occ_grid, starting_point, end_point, trajectory_plan, trajectory_ref)

    # occ_grid_known_name = os.getcwd() +"/data/"+"occ_grid_known" + ".npy"
    # np.save(file=occ_grid_known_name, arr=occ_grid_known)


    plan_path = np.zeros((len(trajectory_plan), 4))
    for i in range(len(trajectory_plan)):
        plan_path[i] = [trajectory_plan[i].x, trajectory_plan[i].y, trajectory_plan[i].z, trajectory_plan[i].ca]

    # plan_path_Hybrid_name = os.getcwd() +"/data/"+"plan_path_Hybrid" + ".npy"
    # np.save(file=plan_path_Hybrid_name, arr=plan_path)


    exploration_rate = 0

    for i in range(grid_x):
        for j in range(grid_y):
            for k in range(grid_z):
                if occ_grid_known[i][j][k] != occ_grid[i][j][k]:
                    exploration_rate += 1
    exploration_rate = 1 - exploration_rate / (grid_x * grid_y * grid_z * privacy_threshold)
    print("\033[94m exploration rate: \033[0m", exploration_rate)
    log.info("Online_Hybrid_Planning: Exploration rate: %f" % exploration_rate)


    PR_sum_unknown_plan = 0
    PR_sum_known_plan = 0
    num_ca_plan = 0

    for point in trajectory_plan:
        if point.ca == 1:
            pass
        else:
            num_ca_plan += 1
        PR_sum_unknown_plan += caculate_privacy_surround(grid, point, occ_grid, privacy_radius)
        PR_sum_known_plan += caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)

    print("\033[94mFitness for replanned path:\033[0m \n ", len(trajectory_plan) - 1, PR_sum_unknown_plan,
          PR_sum_known_plan, num_ca_plan)
    log.info("Online_Hybrid_Planning: Length of replanned trajectory: %d" % (len(trajectory_plan) - 1))
    log.info(
        "Online_Hybrid_Planning: Sum of privacy threat of replanned trajectory(occ_grid): %f" % PR_sum_unknown_plan)
    log.info(
        "Online_Hybrid_Planning: Sum of privacy threat of replanned trajectory(occ_grid_known): %f" % PR_sum_known_plan)
    log.info("Online_Hybrid_Planning: Times of turning off camera of replanned trajectory: %d" % num_ca_plan)


    # 再次显示地图
    PR_sum_unknown_ref = 0
    PR_sum_known_ref = 0
    num_ca_ref = 0

    for point in trajectory_ref:
        PR_sum_unknown_ref += caculate_privacy_surround(grid, point, occ_grid, privacy_radius)
        PR_sum_known_ref += caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)
        if point.ca == 2:
            num_ca_ref += 1
    print("\033[94mFitness for preplanned path:\033[0m \n ", len(trajectory_plan) - 1, PR_sum_unknown_ref,
          PR_sum_known_ref, num_ca_ref)
    log.info("Online_Hybrid_Planning: Length of preplanned trajectory: %d" % (len(trajectory_ref) - 1))
    log.info(
        "Online_Hybrid_Planning: Sum of privacy threat of preplanned trajectory(occ_grid): %f" % PR_sum_unknown_ref)
    log.info(
        "Online_Hybrid_Planning: Sum of privacy threat of preplanned trajectory(occ_grid_known): %f" % PR_sum_known_ref)
    log.info("Online_Hybrid_Planning: Times of turning off camera of preplanned trajectory: %d" % num_ca_ref)


    return



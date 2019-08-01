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
# from quickSort import quick_sort
import sys
import os
from heapq import heappush
from Astar import AStar

# from log import Log
# log = Log(__name__).getlog()

sys.setrecursionlimit(1000000)

def Astar_Hybrid_Planning_online(config, iteration, log, num):

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
    replantime = 0
    preference = config.preference


    # occ_grid_name = "occ_grid" + str(iteration) + ".npy"
    # num is the number of the grid
    occ_grid_name = os.getcwd() + "/data/" + "occ_grid-" + str(num) + ".npy"
    occ_grid = np.load(file=occ_grid_name)
    # occ_grid = np.load(file="occ_grid-1.npy")
    pri_grid, privacy_sum = privacy_init(grid_x, grid_y, grid_z, occ_grid, privacy_radius)
    # occ_grid_known_name = "occ_grid_known" + str(iteration) + ".npy"
    occ_grid_known_name = os.getcwd() +"/data/"+"occ_grid_known_initial" + str(iteration) + ".npy"
    occ_grid_known = np.load(file=occ_grid_known_name)
    # occ_grid_known = np.load(file="occ_grid_known.npy")
    pri_grid_known, privacy_sum_known = privacy_init(grid_x, grid_y, grid_z, occ_grid_known, privacy_radius)
    a = 0
    for i in range(grid_x):
        for j in range(grid_y):
            for k in range(grid_z):
                if occ_grid_known[i][j][k] != occ_grid[i][j][k]:
                    a += 1
    # print(restricted_area_num, a, (grid_x * grid_y * grid_z * privacy_threshold))
    exp_rate = 1 - a / (grid_x * grid_y * grid_z * privacy_threshold)
    # print("exp_rate ",exp_rate , a)

    # print("The occ_grid is: ")
    # for m in range(grid_x):
    #     print("The value of x: ", m)
    #     print(occ_grid[m])
    starttime = time.time()
    # aStar = AStar(occ_grid, pri_grid_known, grid, privacy_sum_known, starting_point, end_point, [1], T_budget, threat_list, 0)
    # 开始寻路
    # trajectory_ref = aStar.start()
    reference_path_name = os.getcwd() +"/data/"+"reference_path" + str(iteration) + ".npy"
    trajectory_ref_temp = np.load(file=reference_path_name)
    # trajectory_ref_temp = np.load(file="reference_path.npy")
    # trajectory_ref_temp = np.load(file="plan_path_Hybrid.npy")
    trajectory_ref = []
    for i in range(len(trajectory_ref_temp)):
        point = Point(int(trajectory_ref_temp[i][0]), int(trajectory_ref_temp[i][1]), int(trajectory_ref_temp[i][2]),
                      int(trajectory_ref_temp[i][3]))
        # if (pri_grid_known[point.x][point.y][point.z] > 0):
        #     print(point)
        trajectory_ref.append(point)

    # endtime = time.time()
    # dtime = endtime - starttime
    # print("程序运行时间：%.8s s" % dtime)

    path_grid = copy.deepcopy(occ_grid)

    sum = 0
    if trajectory_ref == None:
        print("No solution!")
        exit(0)
    else:
        for point in trajectory_ref:
            # for ii in range(len(trajectory_ref)):
            # print(point)
            path_grid[point.x][point.y][point.z] = 9
            sum += pri_grid_known[point.x][point.y][point.z]
            # print(point, pri_grid_known[point.x][point.y][point.z])
        # print("----------------------\n", len(trajectory_ref))

    # 再次显示地图

    # print(path_grid, sum)
    # trajectory_ref = [starting_point] + trajectory_ref
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
    num_of_no_solution = 0
    current_f = sum + len(trajectory_plan)

    while not (idx >= len(trajectory_plan)):
        current_p = trajectory_plan[idx]
        current_ca = trajectory_plan[idx].ca

        if current_p.x == end_point.x and current_p.y == end_point.y and current_p.z == end_point.z:
            plan_path = np.zeros((len(trajectory_plan), 4))
            for i in range(len(trajectory_plan)):
                plan_path[i] = [trajectory_plan[i].x, trajectory_plan[i].y, trajectory_plan[i].z,
                                trajectory_plan[i].ca]
            plan_path_Hybrid_name = os.getcwd() + "/data/" + "plan_path_Hybrid_temp" + str(idx) + ".npy"
            np.save(file=plan_path_Hybrid_name, arr=plan_path)
            break

        next_p = trajectory_plan[idx + 1]
        next_idx = idx + 1
        # print("The UAV would move a step: ")
        # print("The current point: ", current_p)
        # print("The next point: ", next_p)
        # print("The index of next point: ", next_idx, "\n")

        if current_ca == 2: ## 1 = camera is open with high resolution, 2 = camera is off with lower resolution
            time_step += 1
            current_p = next_p
            plan_path = np.zeros((len(trajectory_plan), 4))
            for i in range(len(trajectory_plan)):
                plan_path[i] = [trajectory_plan[i].x, trajectory_plan[i].y, trajectory_plan[i].z,
                                trajectory_plan[i].ca]
            plan_path_Hybrid_name = os.getcwd() + "/data/" + "plan_path_Hybrid_temp" + str(idx) + ".npy"
            np.save(file=plan_path_Hybrid_name, arr=plan_path)

            idx += 1
            # print("The UAV has finished this step.\n")
            continue

        # take picture
        # update occ_grid, pri_grid
        flag, occ_grid_known, pri_grid_known, privacy_sum_known, threat_list = hasprivacythreat2(current_p,
                                                                                                 occ_grid_known,
                                                                                                 occ_grid,
                                                                                                 pri_grid_known,
                                                                                                 privacy_sum_known,
                                                                                                 config)
        # print("flag",flag)
        print(trajectory_plan[idx])
        num = 0
        # for i in range(grid_x):
        #     for j in range(grid_y):
        #         for k in range(grid_z):
        #             if pri_grid[i][j][k] != pri_grid_known[i][j][k]:
        #                 num +=1
        # print("$$$$$_current", num)
        # print("occ_grid_known",occ_grid_known)
        # print("pri_grid_known",pri_grid_known)
        # print("prigrid", pri_grid)
        # print("The length of privacy_list: ", len(threat_list))
        for m in range(len(threat_list)):
            print(threat_list[m])

        # if flag:
        #     ## 0622
        #     for j in range(idx + 1, len(trajectory_plan)):
        #         point = trajectory_plan[j]
        #         if  (caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)) > 0:
        #             # print("have privacy risk!!")
        #             next_p = trajectory_plan[j]
        #             next_idx = j
        #         # if (pri_grid_known[trajectory_plan[j].x][trajectory_plan[j].y][trajectory_plan[j].z] * math.exp(
        #         #         -(trajectory_plan[j].ca) )) > 0:
        #         #     next_p = trajectory_plan[j]
        #         #     next_idx = j
        #         else:
        #             break
        #
        #     # print("---------------------------------")
        #     # print("The UAV produce a temporory plan!")
        #     # print("The index of current point: ", idx)
        #     # print("The current point: ", current_p)
        #     # print("The index of next point: ", next_idx)
        #     # print("The next point: ", next_p, "\n")
        #
        #     # if  (next_idx == idx + 1)  and (pri_grid_known[trajectory_plan[next_idx].x][trajectory_plan[next_idx].y][trajectory_plan[next_idx].z] > 0) :
        #     #    trajectory_plan[next_idx].ca = 1
        #     #    print ("change sensor configuration for next point")
        #
        #     if next_idx != idx + 1:  # no need for motion planning
        #
        #         """删除冗余路径"""
        #         if current_p.x == next_p.x and current_p.y == next_p.y and current_p.z == next_p.z: # 0623
        #         # if current_p == next_p:
        #             # print("delete redundant route", current_p, next_p)
        #             first_part = trajectory_plan[:idx]
        #             next_part = trajectory_plan[next_idx + 1:]
        #             trajectory_plan = first_part + next_part
        #             break
        #
        #         # print("The length of trajectory_plan: ", len(trajectory_plan))
        #         T_plan = T_budget - (len(trajectory_plan) - 1) + (next_idx - idx)
        #         T_plan_optimal = T_optimal - (len(trajectory_plan) - 1) + (next_idx - idx)
        #         # print("The time limit: ", T_plan, "\n")
        #         # if T_plan < (abs(trajectory_plan.points[next_idx].x - trajectory_plan.points[idx].x) + abs(trajectory_plan.points[next_idx].y - trajectory_plan.points[idx].y) + \
        #         #        abs(trajectory_plan.points[next_idx].z - trajectory_plan.points[idx].z)):
        #         #    print("no solution!")
        #         # print(T_plan, current_p,  next_p)
        #
        #         distance = abs(trajectory_plan[next_idx].x - trajectory_plan[idx].x) + abs(
        #             trajectory_plan[next_idx].y - trajectory_plan[idx].y) + abs(
        #             trajectory_plan[next_idx].z - trajectory_plan[idx].z)
        #
        #         ## have enough time for planning
        #         if T_plan >= distance:
        #             # 开始寻路
        #             start1 = time.time()
        #             # aStar = AStar(occ_grid, pri_grid_known, grid, privacy_sum_known, current_p, next_p, [1], T_plan,
        #             #               threat_list, 1, T_plan_optimal)
        #
        #             ## 0628
        #             print("producing local planning")
        #             replantime += 1 ## 0701
        #             aStar_pp = AStar(occ_grid, pri_grid_known, grid, privacy_sum, current_p, next_p, [1, 2, 3, 4],
        #                              T_plan, threat_list, 0, T_plan_optimal, preference, privacy_radius)
        #             trajectory_optimal_pp = aStar_pp.start()
        #
        #             temp_sum = 0
        #             PR_temp_sum_unknown = 0
        #             PR_temp_sum_known = 0
        #             length_PP = 0
        #             no_solution_flag = 0
        #             if trajectory_optimal_pp != None:
        #                 length_PP = len(trajectory_optimal_pp)
        #                 for jj in range(len(trajectory_optimal_pp)):
        #                     point = trajectory_optimal_pp[jj]
        #                     # print(point)
        #                     # temp_sum += pri_grid_known[point.x][point.y][point.z]
        #                     PR_temp_sum_unknown += caculate_privacy_surround(grid, point, occ_grid, privacy_radius)
        #                     PR_temp_sum_known += caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)
        #                 if PR_temp_sum_known > 0:
        #                     no_solution_flag = 1
        #                 elif len(trajectory_optimal_pp) > T_plan_optimal:
        #                     no_solution_flag = 2
        #             else:
        #                 length_PP = 0
        #                 no_solution_flag = 3
        #
        #             ## 如果找不到没有侵犯隐私的可行解，或者规划出的可行解超出了时间的约束，说明只进行路径规划不可行
        #             if no_solution_flag > 0:
        #                 num_of_no_solution += 1
        #                 print("Online_Hybrid_Planning: No solution for local planning: from [%d, %d, %d] to [%d, %d, %d]. No solution flag is %d, PR for PP is %f. length of PP is %d, T plan optimal is %d, T_plan is %d"
        #                     % (current_p.x, current_p.y, current_p.z, next_p.x, next_p.y, next_p.z, no_solution_flag, PR_temp_sum_known, length_PP, T_plan_optimal, T_plan))
        #                 log.info("Online_Hybrid_Planning: No solution for local planning: from [%d, %d, %d] to [%d, %d, %d]. No solution flag is %d, PR for PP is %f. length of PP is %d, T plan optimal is %d, T_plan is %d"
        #                     % (current_p.x, current_p.y, current_p.z, next_p.x, next_p.y, next_p.z, no_solution_flag, PR_temp_sum_known, length_PP, T_plan_optimal, T_plan))
        #                 aStar = AStar(occ_grid, pri_grid_known, grid, privacy_sum, current_p, next_p, [1, 2, 3, 4],
        #                               T_plan, threat_list, 1, T_plan_optimal, preference, privacy_radius)
        #                 trajectory_optimal = aStar.start()
        #             else:
        #                 trajectory_optimal = copy.deepcopy(trajectory_optimal_pp)
        #
        #             # trajectory_optimal = copy.deepcopy(trajectory_optimal_pp)
        #             #
        #             #
        #             # aStar = AStar(occ_grid, pri_grid_known, grid, privacy_sum, current_p, next_p, [1,2,3,4], T_plan,
        #             #               threat_list, 1, T_plan_optimal, preference)
        #
        #             # print('\033[94m finding solution for local planning... \033[0m')
        #             # trajectory_optimal = aStar.start()
        #
        #             previous_trajectory = copy.deepcopy(trajectory_plan[:idx])
        #             following_trajectory = copy.deepcopy(trajectory_plan[next_idx + 1:])
        #
        #             now_trajectory = []
        #             print(trajectory_plan)
        #             first_part = copy.deepcopy(trajectory_plan[:idx + 1])
        #             following_part = copy.deepcopy(trajectory_plan[next_idx + 1:])
        #             now_trajectory = first_part + trajectory_optimal + following_part
        #
        #             # replan_flag = 0
        #             # for m in range(idx + 1, next_idx + 1):
        #             #     # print("original， The No.", m, " step: ", trajectory_plan[m])
        #             #     if (len(trajectory_optimal) != (next_idx - idx)):
        #             #         replan_flag = 1
        #             #         break
        #             #     if (trajectory_plan[m] != trajectory_optimal[m - idx - 1]):
        #             #         replan_flag = 1
        #             #         break
        #             #
        #             # if replan_flag:
        #             #     replantime += 1  ## 排除重复规划的相同路径 0620
        #
        #             trajectory_plan = copy.deepcopy(now_trajectory)
        #
        #             if trajectory_optimal == None:
        #                 print('\033[94mNo solution for local planning... \033[0m')
        #
        #
        #             # if trajectory_optimal == None:
        #             #     # print('\033[94mNo solution for local planning... \033[0m')
        #             #     # print()
        #             #     for kk in range(idx + 1, next_idx + 1):
        #             #         trajectory_plan[kk].ca = 1
        #             #
        #             # else:
        #             #     # print("The length of local planning: ", len(trajectory_optimal))
        #             #     # print()
        #             #     previous_trajectory = copy.deepcopy(trajectory_plan[:idx])
        #             #     following_trajectory = copy.deepcopy(trajectory_plan[next_idx + 1:])
        #             #
        #             #     now_trajectory = []
        #             #     first_part = trajectory_plan[0:idx + 1]
        #             #     following_part = trajectory_plan[next_idx + 1:]
        #             #     now_trajectory = first_part + trajectory_optimal + following_part
        #             #
        #             #     replan_flag = 0
        #             #     for m in range(idx + 1, next_idx + 1):
        #             #         # print("original， The No.", m, " step: ", trajectory_plan[m])
        #             #         if (len(trajectory_optimal) != (next_idx - idx)):
        #             #             replan_flag = 1
        #             #             break
        #             #         if (trajectory_plan[m] != trajectory_optimal[m - idx - 1]):
        #             #             replan_flag = 1
        #             #
        #             #     if replan_flag:
        #             #         replantime += 1  ## 排除重复规划的相同路径 0620
        #
        #
        #                 # trajectory_plan = copy.deepcopy(now_trajectory)
        #
        #         # turn off camera never exist
        #         else:
        #             # print("sensor reconfigured for the next points in the path!!!")
        #             for kk in range(idx + 1, next_idx + 1):
        #                 trajectory_plan[kk].ca = 2
        #         sum = 0
        #         cam_off = 0
        #         for ll in range(len(trajectory_plan)):
        #             sum += pri_grid_known[trajectory_plan[ll].x][trajectory_plan[ll].y][trajectory_plan[ll].z]
        #             cam_off += trajectory_plan[ll].ca
        #             # print("now", trajectory_plan[ll])
        #         # print("The length of now_trajectory_plan: ", len(trajectory_plan), sum, cam_off)
        #
        #
        #     # elif pri_grid_known[trajectory_plan[next_idx].x][trajectory_plan[next_idx].y][trajectory_plan[next_idx].z] > 0:
        #     elif (caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)) > 0:
        #         trajectory_plan[next_idx].ca = 2  ## camera reconfiguration
        #         # print("change sensor configuration for next point")


        if flag:
            ## 0702
            point = trajectory_plan[next_idx]
            if (caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)) == 0:
                pass
            else:
                for j in range(idx + 1, len(trajectory_plan)):
                    point = trajectory_plan[j]
                    if  (caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)) > 0:
                        print("have privacy risk!!")
                        next_p = trajectory_plan[j]
                        next_idx = j
                        # print(next_p)
                    # if (pri_grid_known[trajectory_plan[j].x][trajectory_plan[j].y][trajectory_plan[j].z] * math.exp(
                    #         -(trajectory_plan[j].ca) )) > 0:
                    #     next_p = trajectory_plan[j]
                    #     next_idx = j
                    else:
                        break
                if next_idx == len(trajectory_plan)-1:
                    next_p = trajectory_plan[next_idx]
                    if (caculate_privacy_surround(grid, next_p , occ_grid_known, privacy_radius)) > 0:
                        next_p.ca = 2
                else:
                    next_idx += 1
                    next_p = trajectory_plan[next_idx]
                """删除冗余路径"""
                if current_p.x == next_p.x and current_p.y == next_p.y and current_p.z == next_p.z:  # 0623
                    # if current_p == next_p:
                    # print("delete redundant route", current_p, next_p)
                    first_part = trajectory_plan[:idx]
                    if next_idx == len(trajectory_plan)-1:
                        next_part = []
                    else:
                        next_part = trajectory_plan[next_idx + 1:]
                    trajectory_plan = first_part + next_part
                    break

                # print("The length of trajectory_plan: ", len(trajectory_plan))
                T_plan = T_budget - (len(trajectory_plan) - 1) + (next_idx - idx)
                T_plan_optimal = T_optimal - (len(trajectory_plan) - 1) + (next_idx - idx)
                # print("The time limit: ", T_plan, "\n")
                # if T_plan < (abs(trajectory_plan.points[next_idx].x - trajectory_plan.points[idx].x) + abs(trajectory_plan.points[next_idx].y - trajectory_plan.points[idx].y) + \
                #        abs(trajectory_plan.points[next_idx].z - trajectory_plan.points[idx].z)):
                #    print("no solution!")
                # print(T_plan, current_p,  next_p)

                distance = abs(trajectory_plan[next_idx].x - trajectory_plan[idx].x) + abs(
                    trajectory_plan[next_idx].y - trajectory_plan[idx].y) + abs(
                    trajectory_plan[next_idx].z - trajectory_plan[idx].z)

                ## have enough time for planning
                if T_plan >= distance:
                    # 开始寻路
                    start1 = time.time()
                    ## 0628
                    print("producing local planning", idx)
                    replantime += 1
                    aStar_pp = AStar(occ_grid, pri_grid_known, grid, privacy_sum, current_p, next_p, [1, 2, 3, 4],
                                     T_plan, threat_list, 0, T_plan_optimal, preference, privacy_radius)
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
                            # print(point)
                            # temp_sum += pri_grid_known[point.x][point.y][point.z]
                            PR_temp_sum_unknown += caculate_privacy_surround(grid, point, occ_grid, privacy_radius)
                            PR_temp_sum_known += caculate_privacy_surround(grid, point, occ_grid_known,
                                                                           privacy_radius)
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
                                current_p.x, current_p.y, current_p.z, next_p.x, next_p.y, next_p.z, no_solution_flag,
                                PR_temp_sum_known, length_PP, T_plan_optimal))
                        log.info(
                            "Online_Hybrid_Planning: No solution for local planning: from [%d, %d, %d] to [%d, %d, %d]. No solution flag is %d, PR for PP is %f. length of PP is %d, T plan optimal is %d"
                            % (
                                current_p.x, current_p.y, current_p.z, next_p.x, next_p.y, next_p.z, no_solution_flag,
                                PR_temp_sum_known, length_PP, T_plan_optimal))
                        aStar = AStar(occ_grid, pri_grid_known, grid, privacy_sum, current_p, next_p, [1, 2, 3, 4],
                                      T_plan, threat_list, 1, T_plan_optimal, preference, privacy_radius)
                        trajectory_optimal = aStar.start()
                    else:
                        trajectory_optimal = copy.deepcopy(trajectory_optimal_pp)

                    now_trajectory = []
                    # for m in range(idx + 1, next_idx + 1):
                    #     print("original， The No.", m, " step: ", trajectory_plan[m])
                    first_part = trajectory_plan[0:idx + 1]
                    if next_idx == len(trajectory_plan)-1:
                        following_part = []
                    else:
                        following_part = trajectory_plan[next_idx + 1:]
                    # following_part = trajectory_plan[next_idx + 1:]
                    now_trajectory = first_part + trajectory_optimal + following_part

                    # replan_flag = 0
                    # for m in range(len(trajectory_optimal)):
                    #     print("plan， The No.", m, " step: ", trajectory_optimal[m])
                    #     if (len(trajectory_optimal) != (next_idx - idx)):
                    #         replan_flag = 1
                    #         break
                    #     if (trajectory_plan[m] != trajectory_optimal[m - idx - 1]):
                    #         replan_flag = 1
                    #
                    # if replan_flag:
                    #     replantime += 1  ## 排除重复规划的相同路径 0620

                    trajectory_plan = copy.deepcopy(now_trajectory)
                    # print(trajectory_plan[idx])
                    # plan_path = np.zeros((len(trajectory_plan), 4))
                    # for i in range(len(trajectory_plan)):
                    #     plan_path[i] = [trajectory_plan[i].x, trajectory_plan[i].y, trajectory_plan[i].z,
                    #                     trajectory_plan[i].ca]
                    # plan_path_Hybrid_name = os.getcwd() + "/data/" + "plan_path_Hybrid_temp" + str(idx) + ".npy"
                    # np.save(file = plan_path_Hybrid_name, arr = plan_path)

                # for ll in range(len(trajectory_plan)):
                    # sum += pri_grid_known[trajectory_plan[ll].x][trajectory_plan[ll].y][trajectory_plan[ll].z]
                    # cam_off += trajectory_plan[ll].ca
                    # print("now", trajectory_plan[ll])
                # print("The length of now_trajectory_plan: ", len(trajectory_plan), sum, cam_off)

        plan_path = np.zeros((len(trajectory_plan), 4))
        for i in range(len(trajectory_plan)):
            plan_path[i] = [trajectory_plan[i].x, trajectory_plan[i].y, trajectory_plan[i].z,
                            trajectory_plan[i].ca]
        plan_path_Hybrid_name = os.getcwd() + "/data/" + "plan_path_Hybrid_temp" + str(idx) + ".npy"
        np.save(file=plan_path_Hybrid_name, arr=plan_path)

        time_step += 1
        idx = idx + 1
        # print("The UAV has finished this step.\n")

        # if idx == 4:
        #    print("the debug begin!")
        # print("next point", idx,time_step, len(trajectory_plan))
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
        # sum_unknown_plan += pri_grid[point.x][point.y][point.z] * math.exp(-(point.ca) )
        # sum_known_plan += pri_grid_known[point.x][point.y][point.z] * math.exp(-(point.ca) )
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
    print("\033[94mFitness for replanned path:\033[0m \n ", len(trajectory_plan) - 1, PR_sum_unknown_plan, PR_sum_known_plan, num_ca_plan,
          num_intruder_notknown_plan, num_intruder_known_plan)
    # print("occ_grid", occ_grid)
    # print("occ_grid_known", occ_grid_known)

    log.info("Online_Hybrid_Planning: Length of replanned trajectory: %d" %(len(trajectory_plan) - 1))
    log.info("Online_Hybrid_Planning: Sum of privacy threat of replanned trajectory(occ_grid): %f" % PR_sum_unknown_plan)
    log.info("Online_Hybrid_Planning: Sum of privacy threat of replanned trajectory(occ_grid_known): %f" % PR_sum_known_plan)
    log.info("Online_Hybrid_Planning: Times of turning off camera of replanned trajectory: %d" % num_ca_plan)
    # log.info("Online_Hybrid_Planning: Times of intrusion of replanned trajectory: %d" % num_intruder_plan)
    log.info("Online_Hybrid_Planning: Times of intrusion of replanned trajectory(occ_grid): %d" % num_intruder_notknown_plan)
    log.info("Online_Hybrid_Planning: Times of intrusion of replanned trajectory(occ_grid_known): %d" % num_intruder_known_plan)
    # log.info("Online_Hybrid_Planning: Times of intrusion of replanned trajectory(should avoid): %d" % num_should_avoid_intruder_plan)
    # log.info("Online_Hybrid_Planning: Times of intrusion of replanned trajectory(cannot avoid): %d" % num_cannot_avoid_intruder_plan)

    # 再次显示地图
    PR_sum_unknown_ref = 0
    PR_sum_known_ref = 0
    num_ca_ref = 0
    num_intruder_notknown_ref = 0
    num_intruder_known_ref = 0
    # num_should_avoid_intruder_ref = 0
    # num_cannot_avoid_intruder_ref = 0
    for point in trajectory_ref:
        # sum_unknown_ref += pri_grid[point.x][point.y][point.z] * math.exp(-(point.ca) )
        # sum_known_ref += pri_grid_known[point.x][point.y][point.z] * math.exp(-(point.ca))
        PR_sum_unknown_ref += caculate_privacy_surround(grid, point, occ_grid, privacy_radius)
        PR_sum_known_ref += caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)
        if point.ca == 2:
            num_ca_ref += 1
        # if pri_grid[point.x][point.y][point.z] != pri_grid_known[point.x][point.y][point.z]:
        #     print("$$$$$$$$$")

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
    print("\033[94mFitness for preplanned path:\033[0m \n ", len(trajectory_plan) - 1,  PR_sum_unknown_ref ,  PR_sum_known_ref, num_ca_ref,
          num_intruder_notknown_ref, num_intruder_known_ref)
    log.info("Online_Hybrid_Planning: Length of preplanned trajectory: %d" % (len(trajectory_ref) - 1))
    log.info("Online_Hybrid_Planning: Sum of privacy threat of preplanned trajectory(occ_grid): %f" %  PR_sum_unknown_ref )
    log.info("Online_Hybrid_Planning: Sum of privacy threat of preplanned trajectory(occ_grid_known): %f" %  PR_sum_known_ref)
    log.info("Online_Hybrid_Planning: Times of turning off camera of preplanned trajectory: %d" % num_ca_ref)
    # log.info("Online_Hybrid_Planning: Times of intrusion of preplanned trajectory: %d" % num_intruder_ref)
    log.info("Online_Hybrid_Planning: Times of intrusion of preplanned trajectory(occ_grid): %d" % num_intruder_notknown_ref)
    log.info("Online_Hybrid_Planning: Times of intrusion of preplanned trajectory(occ_grid_known): %d" % num_intruder_known_ref)
    # log.info("Online_Hybrid_Planning: Times of intrusion of preplanned trajectory(should avoid): %d" % num_should_avoid_intruder_ref)
    # log.info("Online_Hybrid_Planning: Times of intrusion of preplanned trajectory(cannot avoid): %d" % num_cannot_avoid_intruder_ref)

    # 再次显示地图

    # print(path_grid2, sum)
    # print("---------------------------------")
    # print("The last plan is finished!")
    # print("The length of last plan is: ", len(trajectory_plan))
    # for m in range(len(trajectory_plan)):
    #     print("The No.", m, " step: ", trajectory_plan[m])
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

    plan_path_Hybrid_name = os.getcwd() +"/data/"+"plan_path_Hybrid" + str(iteration) + ".npy"
    np.save(file=plan_path_Hybrid_name, arr=plan_path)
    # np.save(file=os.getcwd() +"/data/"+"plan_path_Hybrid.npy", arr=plan_path)
    # c = np.load(file=os.getcwd() +"/data/"+"plan_path_Hybrid.npy")
    # print(c, len(c))

    exploration_rate = 0

    for i in range(grid_x):
        for j in range(grid_y):
            for k in range(grid_z):
                if occ_grid_known[i][j][k] != occ_grid[i][j][k]:
                    exploration_rate += 1
    exploration_rate = 1 - exploration_rate / (grid_x * grid_y * grid_z * privacy_threshold)
    print("\033[94m exploration rate: \033[0m", exploration_rate)
    log.info("Online_Hybrid_Planning: Exploration rate: %f" % exploration_rate)

    return



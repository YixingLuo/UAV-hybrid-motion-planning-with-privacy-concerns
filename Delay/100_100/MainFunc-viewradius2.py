import os
import time
from Point2 import Point
import numpy as np
from random import randint
from mapTools import privacy_init, hasprivacythreat2, initialmapwithknowngrid, SaveMap, initialmapwithknowngrid_ratio
import copy
from Configure import configure
import math
import sys
from heapq import heappush
# from pathinitial import PathInitial
from reference_path import PathInitial
from PathPlanningOnline import Astar_Path_Planning_online
# from HybridPlanningOnline import Astar_Hybrid_Planning_online
# from HybridPlanning_SA import Astar_Hybrid_Planning_online
from HybridPlanning_SA_delay import Astar_Hybrid_Planning_online
from SensorConfigOnline import Astar_Sensor_Config_online

from log import Log

from log import Log

# num_of_occ_grid = 2
num_list = [100]
for round in range(len(num_list)):
    # num = round + 1
    num = num_list[round]
    # num = 10
    #
    # viewradius_list = [1, 1.5, 2, 2.5, 3]
    viewradius_list = [4]
    # viewradius_list.reverse()
    for vr in range (len(viewradius_list)):

        viewradius = viewradius_list[vr]
        # viewradius = 2
        preference = 1
        delay = 0
        log_tmp = Log(__name__, log_cate="results-delay0-viewradius"+ str(viewradius) + "-data" + str(num))
        log = log_tmp.getlog()

        exploration_rate_list = [0]
        for j in range(len(exploration_rate_list)):
            # exploration_rate_list = [0, 0.2, 0.4, 0.6, 0.8]
            exploration_rate = exploration_rate_list[j]
            # exploration_rate = 0.9
            # exploration_rate = 0
            # viewradius = 2.5
            # for j in range(10):
            #     preference_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
            #     preference = preference_list[j]
            #     exploration_rate = 0.2

            # if exploration_rate == 0 or exploration_rate == 1:
            #     rangek = 2
            # else:
            #     rangek = 3
            rangek = 11
            for i in range(1, rangek):

                iteration = i
                grid_x = 10
                grid_y = 100
                grid_z = 100

                # delay = 0

                # safety_threshold, privacy_threshold 固定 0.3 最佳
                # safety_threshold_list = [0.2, 0.3, 0.4]
                # safety_threshold = safety_threshold_list[i%3]
                # privacy_threshold_list = [0.05, 0.1, 0.15]
                # privacy_threshold = privacy_threshold_list[i % 3]
                # privacy_radius = [0.5, 1, 2]

                safety_threshold = 0.05472
                privacy_threshold = 0.05415
                privacy_radius = [1, 1.5, 2]

                x1 = 0
                x2 = 0
                y1 = 0
                y2 = grid_y - 1
                z1 = 0
                z2 = grid_z - 1
                starting_point = Point(x1, y1, z1, 1)
                end_point = Point(x2, y2, z2, 1)

                # alpha ,beta 固定
                # alpha_list = [4/2, 5/3, 6/4, 7/5, 8/6, 9/7, 10/8, 11/9, 12/10, 13/11]
                # alpha = alpha_list[i % 10]
                # beta_list = [3/2, 4/3, 5/4, 6/5, 7/6, 8/7, 9/8, 10/9, 11/10, 12/11]
                # beta = beta_list[i % 10]
                alpha = 12 / 10
                beta = 11 / 10
                # alpha = 10
                # beta = 10

                Kca = 10

                config = configure(grid_x, grid_y, grid_z, safety_threshold, privacy_threshold, privacy_radius,
                                   starting_point,
                                   end_point, viewradius, alpha, beta, exploration_rate, preference, delay)
                T_budget = config.T_budget
                T_optimal = config.T_optimal
                log.info(
                    "Iteration: %d; Configuration: grid: %d, safety_threshold: %f, privacy_threshold: %f, the starting point: [%d, %d, %d]; the end point: [%d, %d, %d]; T_budget(alpha): "
                    "%f (%f); "
                    "T_optimal(beta): %f (%f); Exploration_rate: %f; Preference: %f; View_radius: %f"
                    % (
                        iteration, grid_x, safety_threshold, privacy_threshold, x1, y1, z1, x2, y2, z2, T_budget, alpha,
                        T_optimal,
                        beta, exploration_rate, preference, viewradius))
                SaveMap(config, iteration, exploration_rate, num)

                reinitial_flag = 1
                # refpath = []
                # planpath = []
                PathInitial(config, reinitial_flag, iteration, log, num)
                # print(no_solution_flag)
                # if no_solution_flag != 1:
                #     log.info("Error for no initial solution!")
                #     print("error for no initial solution")
                #     i -= 1
                #     continue

                # Hybrid
                Astar_Hybrid_Planning_online(config, iteration, log, num)
                reinitial_flag = 2
                PathInitial(config, reinitial_flag, iteration, log, num)

                # SC
                #
                Astar_Sensor_Config_online(config, iteration, log, num)
                reinitial_flag = 2
                PathInitial(config, reinitial_flag, iteration, log, num)

                # PP
                Astar_Path_Planning_online(config, iteration, log, num)
                reinitial_flag = 2
                PathInitial(config, reinitial_flag, iteration, log, num)

            log_tmp.clear()
    # num = 0
    # # while sum_ref_initial > sum_plan_last:
    # while num == 0:
    #     num += 1
    #     refpath, len_refpath, sum_ref, planpath, len_planpath, sum_plan,  no_solution_flag = PathInitial(config, reinitial_flag, iteration,
    #                                                                                   log)
    #     sum_online_plan, len_trajectory_plan, num_intruder_plan, sum_pre, len_trajectory_ref, num_intruder_ref = Astar_Hybrid_Planning_online(
    #         config, iteration, log)
    #     reinitial_flag = 0
    #     sum_ref_initial = sum_ref
    #     if num > 30:
    #         log.info("Error to be trapped!")
    #         break
    #
    # reinitial_flag = 1
    # refpath, len_refpath, sum_ref_initial, planpath, len_planpath, sum_plan_last,  no_solution_flag  = PathInitial(config, reinitial_flag,
    #                                                                                            iteration, log)
    # num = 0
    # # while sum_ref_initial > sum_plan_last:
    # while num == 0:
    #     num += 1
    #
    #     refpath, len_refpath, sum_ref, planpath, len_planpath, sum_plan,  no_solution_flag  = PathInitial(config, reinitial_flag, iteration,
    #                                                                                   log)
    #     sum_online_plan, len_trajectory_plan, num_intruder_plan, sum_pre, len_trajectory_ref, num_intruder_ref = Astar_Sensor_Config_online(
    #         config, iteration, log)
    #     reinitial_flag = 0
    #     sum_ref_initial = sum_ref
    #     if num > 30:
    #         log.info("Error to be trapped!")
    #         break
    #
    # reinitial_flag = 1
    # refpath, len_refpath, sum_ref_initial, planpath, len_planpath, sum_plan_last,  no_solution_flag  = PathInitial(config, reinitial_flag,
    #                                                                                            iteration, log)
    #
    # num = 0
    # # while sum_ref_initial > sum_plan_last:
    # while num == 0:
    #     num += 1
    #
    #     refpath, len_refpath, sum_ref, planpath, len_planpath, sum_plan,  no_solution_flag  = PathInitial(config, reinitial_flag, iteration,
    #                                                                                   log)
    #     sum_online_plan, len_trajectory_plan, num_intruder_plan, sum_pre, len_trajectory_ref, num_intruder_ref = Astar_Path_Planning_online(
    #         config, iteration, log)
    #     reinitial_flag = 0
    #     sum_ref_initial = sum_ref
    #     if num > 30:
    #         log.info("Error to be trapped!")
    #         break
from Point2 import Point
import numpy as np
import os
from mapTools import privacy_init, hasprivacythreat2, initialmapwithknowngrid, initialmapwithknowngrid_ratio, caculate_privacy_surround
from Configure import configure

reference_path = os.getcwd() + "/data/reference_path1" + ".npy"
# reference_path = os.getcwd() + "/data2/plan_path_Hybrid_temp36" + ".npy"
trajectory_ref = np.load(file = reference_path)
occ_grid_path = os.getcwd() + "/data/occ_grid_known_temp35" + ".npy"
occ_grid_known = np.load(file=occ_grid_path)
occ_grid_path2 = os.getcwd() + "/data/occ_grid_0731" + ".npy"
occ_grid = np.load(file=occ_grid_path2)

privacy_radius = [1, 1.5, 4]
grid = [5, 15, 15]
# 再次显示地图
PR_sum_unknown_ref = 0
PR_sum_known_ref = 0
num_ca_ref = 0
num_intruder_notknown_ref = 0
num_intruder_known_ref = 0
# num_should_avoid_intruder_ref = 0
# num_cannot_avoid_intruder_ref = 0
for i in range(len(trajectory_ref)):
    point = Point(int(trajectory_ref[i][0]), int(trajectory_ref[i][1]), int(trajectory_ref[i][2]),
                  int(trajectory_ref[i][3]))
    # sum_unknown_ref += pri_grid[point.x][point.y][point.z] * math.exp(-(point.ca) )
    # sum_known_ref += pri_grid_known[point.x][point.y][point.z] * math.exp(-(point.ca))
    PR_sum_unknown_ref += caculate_privacy_surround(grid, point, occ_grid, privacy_radius)
    PR_sum_known_ref += caculate_privacy_surround(grid, point, occ_grid_known, privacy_radius)
    if point.ca == 2:
        num_ca_ref += 1
    # if pri_grid[point.x][point.y][point.z] != pri_grid_known[point.x][point.y][point.z]:
    #     print("$$$$$$$$$")

    # print(point, pri_grid_known[point.x][point.y][point.z])
    # if pri_grid[point.x][point.y][point.z] > 0 and occ_grid[point.x][point.y][point.z] == 0:
    #     num_intruder_notknown_ref += 1
    #
    # if pri_grid_known[point.x][point.y][point.z] > 0 and occ_grid_known[point.x][point.y][point.z] == 0:
    #     num_intruder_known_ref += 1

    # if  occ_grid[point.x][point.y][point.z] == 2 or occ_grid[point.x][point.y][point.z] == 3 or occ_grid[point.x][point.y][point.z] == 4 :
    #     num_should_avoid_intruder_ref += 1
    #
    # if occ_grid_known[point.x][point.y][point.z] == 2 or occ_grid_known[point.x][point.y][point.z] == 3 or occ_grid_known[point.x][point.y][point.z] == 4:
    #     num_cannot_avoid_intruder_ref += 1
# print("\033[94m Fitness for reference path:\033[0m \n", len(trajectory_ref) - 1, sum_ref, num_ca_ref,
#       num_intruder_ref)
print("\033[94mFitness for preplanned path:\033[0m \n ", len(trajectory_ref) - 1,  PR_sum_unknown_ref ,  PR_sum_known_ref, num_ca_ref,
      num_intruder_notknown_ref, num_intruder_known_ref)
# log.info("Online_Hybrid_Planning: Length of preplanned trajectory: %d" % (len(trajectory_ref) - 1))
# log.info("Online_Hybrid_Planning: Sum of privacy threat of preplanned trajectory(occ_grid): %f" %  PR_sum_unknown_ref )
# log.info \
#     ("Online_Hybrid_Planning: Sum of privacy threat of preplanned trajectory(occ_grid_known): %f" %  PR_sum_known_ref)
# log.info("Online_Hybrid_Planning: Times of turning off camera of preplanned trajectory: %d" % num_ca_ref)
# # log.info("Online_Hybrid_Planning: Times of intrusion of preplanned trajectory: %d" % num_intruder_ref)
# log.info \
#     ("Online_Hybrid_Planning: Times of intrusion of preplanned trajectory(occ_grid): %d" % num_intruder_notknown_ref)
# log.info \
#     ("Online_Hybrid_Planning: Times of intrusion of preplanned trajectory(occ_grid_known): %d" % num_intruder_known_ref)
# log.info("Online_Hybrid_Planning: Times of intrusion of preplanned trajectory(should avoid): %d" % num_should_avoid_intruder_ref)
# log.info("Online_Hybrid_Planning: Times of intrusion of preplanned trajectory(cannot avoid): %d" % num_cannot_avoid_intruder_ref)
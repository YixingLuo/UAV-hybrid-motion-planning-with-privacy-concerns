#!/usr/bin/env python
# main function
import numpy as np
from path import Path
from point import Point
import geneticAlgorithm as gA
from quickSort import quick_sort
from gridVisualization import grid_visualization
from mapTools import privacy_init, map_generate
#from global_planning import initialmap
import copy

path = []
grid_x = 5
grid_y = 5
grid_z = 5

occ_grid = None
population = 500
generation = 30
selection_size = 50

objectives = []
no_of_objectives = 1
obstacles_per_axis = 1
starting_point = Point(0, 0, 0, 0)
end_point = Point(4, 4, 4, 0)


safety_threshold = 0.5
privacy_threshold = 0.1
privacy_radius = 1
# the tolerance of the times of camera off
Kca = 3

Tbudget = 100

class GA_class(object):
    def __init__(self, population, generation, selection_size):
        # population 种群数量
        self.population = population
        # generation 种群进化代数
        self.generation = generation
        # 选择个数
        self.selection_size = selection_size

    def initialsolution(occ_grid, pri_grid, privacy_sum, obstacle_num, starting_point, end_point, Tbudget, Kca=0):
        objectives = [end_point]
        Kca = 0
        T_budget = Tbudget
        occ_grid = occ_grid
        pri_grid = pri_grid
        privacy_sum = privacy_sum
        obstacle_num = obstacle_num
        starting_point = starting_point
        end_point = end_point

        alg = gA.GeneticAlgorithm(self.population, self.generation)
        print('\033[94m Generating random initial solutions... \033[0m')
        paths = alg.init_population(starting_point, objectives, Kca)

        for p in range(len(paths)):
            paths[p].fitness = alg.get_fitness(paths[p], occ_grid, pri_grid,
                                               starting_point, end_point, privacy_sum, obstacle_num)

        max_p = max(paths, key=lambda x: x.fitness)

        max_f = -5
        max_path = []

        for i in range(self.generation):
            quick_sort(paths)
            if max_f < paths[0].fitness:
                max_f = paths[0].fitness
                max_path = copy.deepcopy(paths[0])
                print('\033[94m Current maximum fitness:\033[0m\033[92m ' + str(
                    max_f) + '\033[0m\033[94m, Generation:\033[0m\033[92m ' + str(i) + ' \033[0m')
                for j in range(len(paths[0].points)):
                    print(paths[0].points[j])
                print("the generation", i, len(paths[0].points))
                alg.get_fitness(paths[0], occ_grid, pri_grid, starting_point, end_point, privacy_sum, obstacle_num)
                # 选择
                selected_path_list = alg.select(paths, self.selection_size, occ_grid, pri_grid, starting_point,
                                                end_point, privacy_sum, obstacle_num)
                # 形成couple, 交叉， 变异
                new_path_list = []
                for j in range(self.selection_size):
                    for k in range(j + 1, self.selection_size):
                        new_path1 = alg.cross_over(paths[j].points, paths[k].points, objectives, Kca)
                        new_path2 = alg.cross_over(paths[k].points, paths[j].points, objectives, Kca)

                        new_path1_mutated = alg.mutate(new_path1, objectives, Kca)
                        new_path1_mutated.fitness = alg.get_fitness(new_path1_mutated, occ_grid, pri_grid,
                                                                    starting_point, end_point, privacy_sum,
                                                                    obstacle_num)
                        new_path_list.append(new_path1_mutated)

                        new_path2_mutated = alg.mutate(new_path2, objectives, Kca)
                        new_path2_mutated.fitness = alg.get_fitness(new_path2_mutated, occ_grid, pri_grid,
                                                                    starting_point, end_point, privacy_sum,
                                                                    obstacle_num)
                        new_path_list.append(new_path2_mutated)

                # 重插入
                paths = alg.reinsert(paths, new_path_list, population)

        if len(max_path) < T_budget:
            return max_f, max_path
        else:
            print("No Solution!")
            return max_f, max_path

    def motionplan (occ_grid_known, pri_grid_known, privacy_sum, obstacle_num,  current_p, next_p, T_plan, Kca):
        objectives = [next_p]
        Kca = Kca
        T_budget = T_plan
        occ_grid = occ_grid_known
        pri_grid = pri_grid_known
        privacy_sum = privacy_sum
        obstacle_num = obstacle_num
        starting_point = current_p
        end_point =  next_p

        alg = gA.GeneticAlgorithm(self.population, self.generation)
        print('\033[94m Generating random initial solutions... \033[0m')
        paths = alg.init_population(starting_point, objectives, Kca)

        for p in range(len(paths)):
            paths[p].fitness = alg.get_fitness(paths[p], occ_grid, pri_grid,
                                               starting_point, end_point, privacy_sum, obstacle_num)

        max_p = max(paths, key=lambda x: x.fitness)

        max_f = -5
        max_path = []

        for i in range(self.generation):
            quick_sort(paths)
            if max_f < paths[0].fitness:
                max_f = paths[0].fitness
                max_path = copy.deepcopy(paths[0])
                print('\033[94m Current maximum fitness:\033[0m\033[92m ' + str(
                    max_f) + '\033[0m\033[94m, Generation:\033[0m\033[92m ' + str(i) + ' \033[0m')
                for j in range(len(paths[0].points)):
                    print(paths[0].points[j])
                print("the generation", i, len(paths[0].points))
                alg.get_fitness(paths[0], occ_grid, pri_grid, starting_point, end_point, privacy_sum, obstacle_num)
                # 选择
                selected_path_list = alg.select(paths, self.selection_size, occ_grid, pri_grid, starting_point,
                                                end_point, privacy_sum, obstacle_num)
                # 形成couple, 交叉， 变异
                new_path_list = []
                for j in range(self.selection_size):
                    for k in range(j + 1, self.selection_size):
                        new_path1 = alg.cross_over(paths[j].points, paths[k].points, objectives, Kca)
                        new_path2 = alg.cross_over(paths[k].points, paths[j].points, objectives, Kca)

                        new_path1_mutated = alg.mutate(new_path1, objectives, Kca)
                        new_path1_mutated.fitness = alg.get_fitness(new_path1_mutated, occ_grid, pri_grid,
                                                                    starting_point, end_point, privacy_sum,
                                                                    obstacle_num)
                        new_path_list.append(new_path1_mutated)

                        new_path2_mutated = alg.mutate(new_path2, objectives, Kca)
                        new_path2_mutated.fitness = alg.get_fitness(new_path2_mutated, occ_grid, pri_grid,
                                                                    starting_point, end_point, privacy_sum,
                                                                    obstacle_num)
                        new_path_list.append(new_path2_mutated)

                # 重插入
                paths = alg.reinsert(paths, new_path_list, population)

        if len(max_path) < T_budget:
            return max_f, max_path
        else:
            print("No Solution!")
            return max_f, max_path


# import global map
def initialmap (grid_x, grid_y, grid_z, starting_point, end_point, safety_threshold, privacy_threshold, privacy_radius):
    #print("start")
    occ_grid, obstacle_num = map_generate(grid_x, grid_y, grid_z, starting_point, end_point, safety_threshold, privacy_threshold)
    pri_grid, privacy_sum = privacy_init(grid_x, grid_y, grid_z, occ_grid, privacy_radius)

    occ_grid_known = copy.deepcopy(occ_grid)
    for i in range (grid_x-1):
        for j in range (grid_y-1):
            for k in range (grid_z-1):
                if occ_grid_known[i][j][k] == 2 or occ_grid_known[i][j][k] == 3 or occ_grid_known[i][j][k] == 4:
                    occ_grid_known[i][j][k] = 0
    pri_grid_known, privacy_sum_known = privacy_init(grid_x, grid_y, grid_z, occ_grid_known, privacy_radius)
    #print (occ_grid, obstacle_num, occ_grid_known, pri_grid_known, privacy_sum_known)
    return occ_grid, obstacle_num, occ_grid_known, pri_grid_known, privacy_sum_known

occ_grid, obstacle_num, occ_grid_known, pri_grid_known, privacy_sum_known = initialmap (grid_x, grid_y, grid_z, starting_point, end_point, safety_threshold, privacy_threshold, privacy_radius)

print (occ_grid, obstacle_num, occ_grid_known, pri_grid_known, privacy_sum_known)

max_f, max_path = ga.initialsolution(occ_grid, pri_grid, privacy_sum, obstacle_num, starting_point, end_point, Tbudget, Kca=0)
print(max_f)
for j in range(len(max_path.points)):
    print(max_path.points[j])



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

# from log import Log
# log = Log(__name__).getlog()

sys.setrecursionlimit(1000000)


class AStar:
    """
    AStar算法的Python3.x实现
    """

    class Node:  # 描述AStar算法中的节点数据
        def __init__(self, point, endPoint, ideallength, g=0):
            self.point = point  # 自己的坐标
            self.father = None  # 父节点
            self.g = g  # g值，g值在用到的时候会重新算
            self.step = 0
            self.cam = 0
            # self.h = abs(endPoint.x - point.x) + abs(endPoint.y - point.y) + abs(endPoint.z - point.z) # 计算h值 曼哈顿距离
            self.h = 0

        def __str__(self):
            return "point as the node: x:" + str(self.point.x) + ",y:" + str(self.point.y) + ",z:" + str(self.point.z) + ",ca:" + str(self.point.ca)

        # 堆需要节点与节点之间的比较，因此必须实现这个魔术方法
        def __lt__(self, other):
            if self.g + self.h ==  other.g + other.h:
                return self.step < other.step
            else:
                return self.g + self.h < other.g + other.h

    def __init__(self, occ_grid, pri_grid, grid, sum_privacy, startPoint, endPoint, passTag, Tbudget, threat_list, flag, Toptimal, preference, pri_radius):
        """
        构造AStar算法的启动条件
        :param map3d: Array2D类型的寻路数组
        :param startPoint: Point或二元组类型的寻路起点
        :param endPoint: Point或二元组类型的寻路终点
        :param passTag: int类型的可行走标记（若地图数据!=passTag即为障碍）
        :param threatlist: privacy restricted area affected
        """
        # 开启表
        self.openList = []
        # 关闭表
        self.closeList = []
        # 寻路地图
        self.map3d = occ_grid
        self.grid = grid
        self.prigrid = pri_grid
        self.sumpri = sum_privacy
        self.ideallength = abs(endPoint.x - startPoint.x) + abs(endPoint.y - startPoint.y) + abs(endPoint.z - startPoint.z)
        self.Tbudget = Tbudget
        self.Toptimal = Toptimal
        # print("Time limit: ", self.Tbudget)
        self.threatlist = threat_list
        self.timestep = 0
        #self.startPoint = startPoint
        self.flag = flag
        self.preference = preference
        self.pri_radius = pri_radius


        # 起点终点
        if isinstance(startPoint, Point) and isinstance(endPoint, Point):
            self.startPoint = startPoint
            self.endPoint = endPoint
        else:
            self.startPoint = Point(*startPoint)
            self.endPoint = Point(*endPoint)

        ## 结束点的第二种可能性 - 0615
        self.endPoint2 = Point(endPoint.x, endPoint.y, endPoint.z, 1-endPoint.ca)

        # 障碍物标记
        self.passTag = [1,2,3,4]

        #print("endpoint",self.endPoint, self.endPoint2)

    """new function"""

    def updateNodeHvalue(self):
        for i in range(len(self.openList)):
            node = self.openList[i]
            rou1 = 1- (abs(node.point.x - self.endPoint.x) +
                       abs(node.point.y - self.endPoint.y) +
                       abs(node.point.z - self.endPoint.z)) / self.ideallength
            rou2 = node.step / self.Tbudget
            adaptive1 = math.exp(1 - rou1 / rou2)
            adaptive2 = math.exp(rou1 / rou2 - 1)
            # print(rou1,rou2, adaptive1, adaptive2)
            fathernode = node.father
            delta_h = 0

            temp_sum = 0
            for x in range(node.point.x - 1, node.point.x + 2):
                for y in range(node.point.y - 1, node.point.y + 2):
                    for z in range(node.point.z - 1, node.point.z + 2):
                        if x >= 0 and x < self.grid[0] and y >= 0 and y < self.grid[1] and z >= 0 and z < self.grid[2]:
                            if x != node.point.x or y != node.point.y or z != node.point.z:
                                temp_sum += self.prigrid[x][y][z]
            pri1 = self.prigrid[node.point.x][node.point.y][node.point.z]
            dis1 = abs(node.point.x - self.endPoint.x) + abs(node.point.y - self.endPoint.y) + abs(
                            node.point.z - self.endPoint.z)

            ## type 1
            # node.h = dis1   ## 0625

            ## type 2
            # node.h = dis1
            # adapt_list = [math.exp(0), math.exp(1)]
            # if rou1 / rou2 < 1:
            #     delta_h = adapt_list[1 - node.point.ca]
            #     node.h = node.h * self.preference + delta_h * (pri1 + temp_sum)
            # else:
            #     delta_h = adapt_list[node.point.ca]
            #     node.h = node.h * self.preference + delta_h * (pri1 + temp_sum)

            ## type 3
            # node.h = dis1 * self.preference + pri1 + temp_sum

            ## type 4
            # for j in range(len(self.threatlist)):
            #     # far away, oppisite
            #     threat = self.threatlist[j]
            #
            #     if (abs(node.point.x - threat[0]) + abs(node.point.y - threat[1]) + abs(node.point.z - threat[2])) > (
            #             abs(fathernode.point.x - threat[0]) + abs(fathernode.point.y - threat[1]) +
            #             abs(fathernode.point.z - threat[2])):
            #         delta_h += adaptive1 * self.map3d[threat[0]][threat[1]][threat[2]] ## 绕路
            #     else:
            #         delta_h += adaptive2 * self.map3d[threat[0]][threat[1]][threat[2]]
            # node.h = (abs(self.endPoint.x - node.point.x) + abs(self.endPoint.y - node.point.y) + abs(self.endPoint.z - node.point.z))
            # node.h = node.h * self.preference  +  delta_h

            ## type 4.2
            # node.h = node.h = node.h * delta_h




    # def getMinNode(self):
    #     """
    #     获得openlist中F值最小的节点
    #     :return: Node
    #     """
    #     """
    #     currentNode = self.openList[0]
    #     for node in self.openList:
    #         if node.g + node.h < currentNode.g + currentNode.h:
    #             currentNode = node
    #     return currentNode
    #     """
    #     # currentNode = self.openList[0]
    #     # for node in self.openList:
    #     #     if node.g + node.h < currentNode.g + currentNode.h: ## 0615 why not <=, but <?????
    #     #         if node.step <= self.Tbudget:
    #     #             currentNode = node
    #     # if currentNode.point != self.startPoint:
    #     #     print("MinF: " , currentNode.father.step, currentNode.father.point, currentNode.step, currentNode.point)
    #     # if currentNode.step <= self.Tbudget:
    #     #     return currentNode
    #     # else:
    #     #     return None
    #
    #     quick_sort(self.openList)
    #     self.openList = list(reversed(self.openList))
    #     # currentNode = self.openList[0]
    #     for node in self.openList:
    #         if node.step <= self.Tbudget:
    #             return node
    #     return None

    def pointInCloseList(self, point):
        for node in self.closeList:
            if node.point == point:
                return True
        return False

    def point_in_close_list(self, point, step_num):
        for node in self.closeList:
            if node.point == point and node.step == step_num:
                return True
        return False

    def pointInOpenList(self, point):
        for node in self.openList:
            if node.point == point:
                return node
        return None

    def the_same_points_in_open_list(self, point):
        same_points_list = []
        for node in self.openList:
            if node.point == point:
                same_points_list.append(node)
        return same_points_list

    def endPointInCloseList(self):
        for node in self.closeList: ## 0615
            if node.point == self.endPoint or node.point == self.endPoint2:
                return node
        return None

    def endPointInOpenList(self):
        for node in self.openList:
            if node.point == self.endPoint or node.point == self.endPoint2: # 0615
                return node
        return None

    def searchNear(self, minF, offsetX, offsetY, offsetZ, cam):
        """
        搜索节点周围的点
        :param minF:F值最小的节点
        :param offsetX:坐标偏移量
        :param offsetY:
        :return:
        """
        # 越界检测
        if (minF.point.x + offsetX < 0 or minF.point.x + offsetX > self.grid[0] - 1 or
                minF.point.y + offsetY < 0 or minF.point.y + offsetY > self.grid[1] - 1 or
                minF.point.z + offsetZ < 0 or minF.point.z + offsetZ > self.grid[2] - 1):
            return
        # 如果是障碍，就忽略
        # if self.map3d[minF.point.x + offsetX][minF.point.y + offsetY][minF.point.z + offsetZ] != self.passTag:
        # if self.map3d[minF.point.x + offsetX][minF.point.y + offsetY][minF.point.z + offsetZ] in self.passTag:
        # print("$$$$$$$$$", currentPoint, minF, minF.step)
        if self.map3d[minF.point.x + offsetX][minF.point.y + offsetY][minF.point.z + offsetZ] in self.passTag:
            return
        # 如果在关闭表中，就忽略
        currentPoint = Point(minF.point.x + offsetX, minF.point.y + offsetY, minF.point.z + offsetZ, cam)
        # print("##########", currentPoint, minF, minF.step)
        # if self.pointInCloseList(currentPoint):
        #     return
        if self.point_in_close_list(currentPoint, minF.step + 1):
            return

        """new setting for time limit"""
        # print()
        if minF.step + 1 > self.Tbudget:
            # print("time limit", minF, minF.step, currentPoint )
            return

        # 设置单位花费

        # step = 1/ self.Toptimal  ## 0625

        # step = 1
        #
        # if self.sumpri == 0:
        #     privacy_threat = 0
        # else:
        #     # privacy_threat = (self.prigrid[minF.point.x + offsetX][minF.point.y + offsetY][minF.point.z + offsetZ] * math.exp(-(cam))) / self.sumpri ## 0625
        #     privacy_threat = self.prigrid[minF.point.x + offsetX][minF.point.y + offsetY][
        #                          minF.point.z + offsetZ] * math.exp(-(cam))


        ## 0628 h_i*exp((-1/2)*ws*dis^2)
        privacy_threat = caculate_privacy_surround(self.grid, currentPoint, self.map3d, self.pri_radius)
        # privacy_threat = 0
        # grid_x = self.grid[0]
        # grid_y = self.grid[1]
        # grid_z = self.grid[2]
        # r = max(self.pri_radius)
        # current_x = minF.point.x + offsetX
        # current_y = minF.point.y + offsetY
        # current_z = minF.point.z + offsetZ
        #
        # min_x = max(current_x - r, 0)
        # min_x = math.floor(min_x)
        # max_x = min(current_x + r, grid_x - 1)
        # max_x = math.ceil(max_x)
        # min_y = max(current_y - r, 0)
        # min_y = math.floor(min_y)
        # max_y = min(current_x + r, grid_y - 1)
        # max_y = math.ceil(max_y)
        # min_z = max(current_z - r, 0)
        # min_z = math.floor(min_z)
        # max_z = min(current_z + r, grid_z - 1)
        # max_z = math.ceil(max_z)
        # for m in range(min_x, max_x + 1):
        #     for n in range(min_y, max_y + 1):
        #         for l in range(min_z, max_z + 1):
        #             if self.map3d[m][n][l] == 2 or self.map3d[m][n][l] == 3 or self.map3d[m][n][l] == 4:
        #                 dis = np.sqrt(np.power((current_x - m), 2) + np.power((current_y - n), 2) + np.power((current_z - l), 2))
        #                 h = 0
        #                 if dis <= self.pri_radius[int(self.map3d[m][n][l]) - 2]:
        #                     if self.map3d[m][n][l] == 2:
        #                         h = 1
        #                     elif self.map3d[m][n][l] == 3:
        #                         h = 10
        #                     elif self.map3d[m][n][l] == 4:
        #                         h = 100
        #                     privacy_threat += h * math.exp((-1 / 2) * np.power(dis, 2) * cam)

        ## 加入时间的约束惩罚
        time_punishment = 1
        # if self.Toptimal < 0:
        #     self.Toptimal = 0
        if minF.step + 1 > self.Toptimal:
            # print("punishment:",math.exp((minF.step + 1 - self.Toptimal) / (self.Tbudget - self.Toptimal)))
            alpha = 1
            time_punishment = alpha * math.exp((minF.step + 1 - self.Toptimal) / (self.Tbudget - self.Toptimal))
            if privacy_threat == 0:
                delta_g = time_punishment
            else:
                delta_g = time_punishment * privacy_threat
        else:
            delta_g = time_punishment * privacy_threat
        #
        # delta_g = time_punishment * privacy_threat

        # type1
        # print ("delta_g :", time_punishment * privacy_threat)
        # delta_g =  math.exp(time_punishment * privacy_threat)
        # delta_g = time_punishment * math.exp(privacy_threat)  ## 0703
        # type2
        # delta_g = privacy_threat
        # delta_g = step + cam_off + privacy_threat

        # 如果不在openList中，就把它加入openlist
        # currentNode = self.pointInOpenList(currentPoint)
        # 用一个列表来收集相同的点
        same_point_list = self.the_same_points_in_open_list(currentPoint)
        if not same_point_list:
            # print("currentPoint:", currentPoint, currentNode)
            currentNode = AStar.Node(currentPoint, self.endPoint, self.ideallength, g=minF.g + delta_g)
            currentNode.father = minF
            currentNode.cam = minF.cam + cam
            currentNode.step = minF.step + 1
            # self.openList.append(currentNode)
            heappush(self.openList, currentNode)

            #print("MinF$$$$$: ", minF.step, minF.point, currentNode.step, currentNode.point)
            return
        # # 如果在openList中，判断minF到当前点的G是否更小
        # if minF.g + delta_g < currentNode.g:  # 如果更小，就重新计算g值，并且改变father
        #     currentNode.g = minF.g + delta_g
        #     currentNode.father = minF
        #     currentNode.step = minF.step + 1
        #     currentNode.cam = minF.cam
        #     # print("MinF#####: ", currentNode.father.step, currentNode.father.point, currentNode.step, currentNode.point)

        # 检查这些相同的点的step值，如果有相同的，就更新相同的
        # 如果没有相同的，就看看当前的step值和最小的step值
        # 如果最小的step值小，说明当前的step没用
        # 如果当前的step小，说明当前的step值有用，添加到openlist中
        smallest_step_num = self.Tbudget
        same_step_in_list = False
        same_node = None
        for node in same_point_list:
            if minF.step + 1 == node.step:
                same_step_in_list = True
                same_node = node
                break
            if smallest_step_num > node.step:
                smallest_step_num = node.step
        if same_step_in_list:
            if minF.g + delta_g < same_node.g:  # 如果更小，就重新计算g值，并且改变father
                same_node.g = minF.g + delta_g
                same_node.father = minF
                same_node.step = minF.step + 1
                same_node.cam = minF.cam
        else:
            if minF.step+1 < smallest_step_num:
                currentNode = AStar.Node(currentPoint, self.endPoint, self.ideallength, g=minF.g + delta_g)
                currentNode.father = minF
                currentNode.cam = minF.cam + cam
                currentNode.step = minF.step + 1
                # self.openList.append(currentNode)
                heappush(self.openList, currentNode)
        # currentNode = AStar.Node(currentPoint, self.endPoint, self.ideallength, g=minF.g + delta_g)
        # currentNode.father = minF
        # currentNode.cam = minF.cam + cam
        # currentNode.step = minF.step + 1
        # heappush(self.openList, currentNode)

    def start(self):
        """
        开始寻路
        :return: None或Point列表（路径）
        """
        # 判断寻路终点是否是障碍
        #if self.map3d[self.endPoint.x][self.endPoint.y][self.endPoint.z] != self.passTag:
        #if self.map3d[self.endPoint.x][self.endPoint.y][self.endPoint.z] in self.passTag:
        if self.map3d[self.endPoint.x][self.endPoint.y][self.endPoint.z] in self.passTag:
            return None
        # 1.将起点放入开启列表
        startNode = AStar.Node(self.startPoint, self.endPoint, self.ideallength)
        # self.openList.append(startNode)
        heappush(self.openList, startNode)
        # 2.主循环逻辑
        while True:
            # 找到F值最小的点
            # minF = self.getMinNode()
            minF = self.openList[0]
            # # print("minF: ", minF.point, minF.step)
            # if minF == None :
            #     print("no solution for minF!")
            #     return None
            # minF = None
            # if len(self.openList) == 0:
            #     print("No solution for minF!")
            #     return None
            # else:
            #     minF = self.openList[0]
            # 把这个点加入closeList中，并且在openList中删除它
            self.closeList.append(minF)
            self.openList.remove(minF)

            # 判断这个节点的上下左右节点
            # turn on camera
            # actions = [[0, -1, 0, 0],[0, 1, 0, 0],[-1, 0, 0, 0],[1, 0, 0, 0],[0, 0, 1, 0],[0, 0, -1, 0],[0, -1, 0, 1],[0, 1, 0, 1],
            #  [-1, 0, 0, 1],[0, 0, 1, 1],[0, 0, -1, 1],[1, 0, 0, 1]]
            # actionlist = [0,1,2,3,4,5,6,7,8,9,10,11]
            # np.random.shuffle(actionlist)
            # #
            # for i in range (len(actionlist)):
            #     self.searchNear(minF, actions[actionlist[i]][0], actions[actionlist[i]][1], actions[actionlist[i]][2], actions[actionlist[i]][3])
             #"""
            # turn on camera
            if self.flag == 0:
               # self.searchNear(minF, 1, 0, 0, 1)
               # self.searchNear(minF, 0, -1, 0, 1)
               # self.searchNear(minF, -1, 0, 0, 1)
               # self.searchNear(minF, 0, 0, 1, 1)
               # self.searchNear(minF, 0, 1, 0, 1)
               # self.searchNear(minF, 0, 0, -1, 1)
               actions = [[-1, 0, 0, 1],[1, 0, 0, 1],[0, -1, 0, 1],[0, 1, 0, 1],[0, 0, -1, 1],[0, 0, 1, 1]]
               actionlist = [0,1,2,3,4,5]
               np.random.shuffle(actionlist)

               for i in range (len(actionlist)):
                   self.searchNear(minF, actions[actionlist[i]][0], actions[actionlist[i]][1], actions[actionlist[i]][2], actions[actionlist[i]][3])

            else:
               # self.searchNear(minF, 1, 0, 0, 1)
               # self.searchNear(minF, 0, -1, 0, 1)
               # self.searchNear(minF, -1, 0, 0, 1)
               # self.searchNear(minF, 0, 0, 1, 1)
               # self.searchNear(minF, 0, 1, 0, 1)
               # self.searchNear(minF, 0, 0, -1, 1)
               # self.searchNear(minF, 1, 0, 0, 2)
               # self.searchNear(minF, 0, -1, 0, 2)
               # self.searchNear(minF, -1, 0, 0, 2)
               # self.searchNear(minF, 0, 0, 1, 2)
               # self.searchNear(minF, 0, 1, 0, 2)
               # self.searchNear(minF, 0, 0, -1, 2)

               actions = [[-1, 0, 0, 1], [1, 0, 0, 1], [0, -1, 0, 1], [0, 1, 0, 1], [0, 0, -1, 1], [0, 0, 1, 1],
                          [-1, 0, 0, 2], [1, 0, 0, 2], [0, -1, 0, 2], [0, 1, 0, 2], [0, 0, -1, 2], [0, 0, 1, 2]]
               actionlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
               np.random.shuffle(actionlist)
            #
               for i in range(len(actionlist)):
                   self.searchNear(minF, actions[actionlist[i]][0], actions[actionlist[i]][1], actions[actionlist[i]][2],
                                actions[actionlist[i]][3])
              #"""
            # self.updateNodeHvalue()

            # 判断是否终止
            point = self.endPointInCloseList()
            if point:  # 如果终点在关闭表中，就返回结果
                # print("The plan found!")
                cPoint = point
                pathList = []
                while True:
                    if cPoint.father:
                        pathList.append(cPoint.point)
                        cPoint = cPoint.father
                    else:
                        # print(pathList)
                        # print(list(reversed(pathList)))
                        # print(pathList.reverse())
                        return list(reversed(pathList))
            if len(self.openList) == 0:
                print("No plan could meet the time limit!")
                return None
#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
A-star for trajectory planning
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

    def __init__(self, occ_grid, grid,  startPoint, endPoint, Tbudget, threat_list, flag, Toptimal, pri_radius):
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
        self.ideallength = abs(endPoint.x - startPoint.x) + abs(endPoint.y - startPoint.y) + abs(endPoint.z - startPoint.z)
        self.Tbudget = Tbudget
        self.Toptimal = Toptimal
        self.threatlist = threat_list
        self.timestep = 0
        self.flag = flag
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

        if self.map3d[minF.point.x + offsetX][minF.point.y + offsetY][minF.point.z + offsetZ] in self.passTag:
            return
        # 如果在关闭表中，就忽略
        currentPoint = Point(minF.point.x + offsetX, minF.point.y + offsetY, minF.point.z + offsetZ, cam)
        if self.point_in_close_list(currentPoint, minF.step + 1):
            return

        """new setting for time limit"""
        # print()
        if minF.step + 1 > self.Tbudget:
            return

        # 设置单位花费

        privacy_threat = caculate_privacy_surround(self.grid, currentPoint, self.map3d, self.pri_radius)
        # if currentPoint.x == 2 and currentPoint.y == 3 and currentPoint.z == 2:
            # print("grid:", self.map3d)
            # print("privacy risk:", privacy_threat)

        ## 加入时间的约束惩罚
        # time_punishment = 1
        # # if self.Toptimal < 0:
        # #     self.Toptimal = 0
        # if minF.step + 1 > self.Toptimal:
        #     alpha = 1
        #     time_punishment = alpha * math.exp((minF.step + 1 - self.Toptimal) / (self.Tbudget - self.Toptimal))
        #     if privacy_threat == 0:
        #         delta_g = time_punishment
        #     else:
        #         delta_g = time_punishment * privacy_threat
        # else:
        #     delta_g = time_punishment * privacy_threat

        delta_g = privacy_threat

        # 用一个列表来收集相同的点
        same_point_list = self.the_same_points_in_open_list(currentPoint)
        if not same_point_list:
            currentNode = AStar.Node(currentPoint, self.endPoint, self.ideallength, g=minF.g + delta_g)
            currentNode.father = minF
            currentNode.cam = minF.cam + cam
            currentNode.step = minF.step + 1
            # self.openList.append(currentNode)
            heappush(self.openList, currentNode)

            return

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
               self.searchNear(minF, 1, 0, 0, 1)
               self.searchNear(minF, 0, -1, 0, 1)
               self.searchNear(minF, -1, 0, 0, 1)
               self.searchNear(minF, 0, 0, 1, 1)
               self.searchNear(minF, 0, 1, 0, 1)
               self.searchNear(minF, 0, 0, -1, 1)
               # actions = [[-1, 0, 0, 1],[1, 0, 0, 1],[0, -1, 0, 1],[0, 1, 0, 1],[0, 0, -1, 1],[0, 0, 1, 1]]
               # actionlist = [0,1,2,3,4,5]
               # np.random.shuffle(actionlist)
               #
               # for i in range (len(actionlist)):
               #     self.searchNear(minF, actions[actionlist[i]][0], actions[actionlist[i]][1], actions[actionlist[i]][2], actions[actionlist[i]][3])

            else:

                self.searchNear(minF, 1, 0, 0, 2)
                self.searchNear(minF, 0, -1, 0, 2)
                self.searchNear(minF, 0, 0, -1, 2)
                self.searchNear(minF, 0, 1, 0, 2)
                self.searchNear(minF, 0, 0, 1, 2)
                self.searchNear(minF, -1, 0, 0, 2)

                self.searchNear(minF, 1, 0, 0, 1)
                self.searchNear(minF, 0, -1, 0, 1)
                self.searchNear(minF, 0, 0, -1, 1)
                self.searchNear(minF, 0, 1, 0, 1)
                self.searchNear(minF, 0, 0, 1, 1)
                self.searchNear(minF, -1, 0, 0, 1)
            #
            #    actions = [[-1, 0, 0, 1], [1, 0, 0, 1], [0, -1, 0, 1], [0, 1, 0, 1], [0, 0, -1, 1], [0, 0, 1, 1],
            #               [-1, 0, 0, 2], [1, 0, 0, 2], [0, -1, 0, 2], [0, 1, 0, 2], [0, 0, -1, 2], [0, 0, 1, 2]]
            #    actionlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            #    np.random.shuffle(actionlist)
            # #
            #    for i in range(len(actionlist)):
            #        self.searchNear(minF, actions[actionlist[i]][0], actions[actionlist[i]][1], actions[actionlist[i]][2],
            #                     actions[actionlist[i]][3])
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
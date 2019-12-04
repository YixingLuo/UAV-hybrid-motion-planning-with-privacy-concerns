"""
privacy region detection
"""
#!/usr/bin/python
# -*- coding:utf-8 -*-
# map generation tools

import numpy as np
from random import randint
import math
import copy
from Point2 import Point
from Configure import configure
import time
import os
import cv2



#################################
circlelen=20  #圆形的直径，单位为cm
boxlen=52   #箱子的长度，单位为cm

cellLength=200 #cm

centerX=2000
centerY=1125
# blueLower = np.array([80, 22, 130])
# blueUpper = np.array([145, 180, 255])

blueLower = np.array([80, 55, 160])
blueUpper = np.array([120, 120, 255])

yellowLower = np.array([26, 43, 46])
yellowUpper = np.array([34, 255, 255])

redLower = np.array([170, 43, 46])
redUpper = np.array([180, 255, 255])
#################################

## read the latest picture in the folder
def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                L.append(int(file[:-4]))
                # print(max(L)-1)
    return max(L) - 1


# 隐私部分的初始化
def privacy_init(grid_x, grid_y, grid_z, occ_grid, radius):
    #print(radius[0])
    # print(occ_grid)
    pri_grid = np.zeros((grid_x, grid_y, grid_z))
    for i in range(grid_x):
        for j in range(grid_y):
            for k in range(grid_z):
                # 这里隐私等级分为三级，数字越大，级别越高
                if (occ_grid[i][j][k] == 2) or (occ_grid[i][j][k] == 3) or (occ_grid[i][j][k] == 4):
                    # different level of privacy restricted area has different affecting radius:
                    temp = int (occ_grid[i][j][k])
                    r = radius[temp-2]
                    min_x = max(i - r, 0)
                    min_x = math.floor(min_x)
                    max_x = min(i + r, grid_x - 1)
                    max_x = math.ceil(max_x)
                    min_y = max(j - r, 0)
                    min_y = math.floor(min_y)
                    max_y = min(j + r, grid_y - 1)
                    max_y = math.ceil(max_y)
                    min_z = max(k - r, 0)
                    min_z = math.floor(min_z)
                    max_z = min(k + r, grid_z - 1)
                    max_z = math.ceil(max_z)
                    for m in range(min_x, max_x + 1):
                        for n in range(min_y, max_y + 1):
                            for l in range(min_z, max_z + 1):
                                dis = np.sqrt(np.power((i - m), 2) + np.power((j - n), 2) + np.power((k - l), 2))
                                h = 0
                                if dis <= r:
                                    if occ_grid[i][j][k] == 2:
                                        h = 1
                                    elif occ_grid[i][j][k] == 3:
                                        h = 2
                                        # h = 4
                                    elif occ_grid[i][j][k] == 4:
                                        h = 3
                                        # h = 8
                                    # print (dis, np.power(dis, 2),math.exp((-1/2)*np.power(dis, 2)),i,j,k,m,n,l)
                                    # print (pri_grid[m][n][l])
                                    pri_grid[m][n][l] += h * math.exp((-1 / 2) * np.power(dis, 2))
                                    # pri_grid[m][n][l] += h /( np.power(dis, 2))
                                    # print(pri_grid[m][n][l])
    sum_privacy = 0
    for i in range(grid_x):
        for j in range(grid_y):
            for k in range(grid_z):
                sum_privacy += pri_grid[i][j][k]
    return pri_grid, sum_privacy


def caculate_privacy_surround(grid, point, occ_grid, privacy_radius ):
    privacy_threat = 0
    grid_x = grid[0]
    grid_y = grid[1]
    grid_z = grid[2]
    r = max(privacy_radius)

    current_x = point.x
    current_y = point.y
    current_z = point.z
    cam = point.ca

    min_x = max(current_x - r, 0)
    min_x = math.floor(min_x)
    max_x = min(current_x + r, grid_x - 1)
    max_x = math.ceil(max_x)
    min_y = max(current_y - r, 0)
    min_y = math.floor(min_y)
    max_y = min(current_y + r, grid_y - 1)
    max_y = math.ceil(max_y)
    min_z = max(current_z - r, 0)
    min_z = math.floor(min_z)
    max_z = min(current_z + r, grid_z - 1)
    max_z = math.ceil(max_z)
    # if current_x == 0 and current_y == 3 and current_z == 1:
    #     print("current_point",point)
    #     print(min_x,max_x,min_y,max_y,min_z,max_z)
    for m in range(min_x, max_x + 1):
        for n in range(min_y, max_y + 1):
            for l in range(min_z, max_z + 1):
                if occ_grid[m][n][l] == 2 or occ_grid[m][n][l] == 3 or occ_grid[m][n][l] == 4:
                    dis = np.sqrt(np.power((current_x - m), 2) + np.power((current_y - n), 2) + np.power((current_z - l), 2))
                    h = 0
                    if dis <= privacy_radius[int(occ_grid[m][n][l]) - 2]:
                        # print("privacy",m,n,l, point)
                        # if self.pri_radius[int(self.map3d[m][n][l]) - 2]
                        # print(self.pri_radius[int(self.map3d[m][n][l]) - 2])
                        if occ_grid[m][n][l] == 2:
                            h = 1
                        elif occ_grid[m][n][l] == 3:
                            h = 2
                            # h = 4
                        elif occ_grid[m][n][l] == 4:
                            h = 3
                            # h = 8
                        privacy_threat += h * math.exp((-1 / 2) *(1/2)* np.power(dis, 2) * cam)  ## 规约到0-1之间
    return privacy_threat

#################################################

def isInside(box, x, y):
    # A = Point()
    # B = Point()
    # C = Point()
    # D = Point()
    A_x = box[0][0]
    A_y = box[0][1]
    B_x = box[1][0]
    B_y = box[1][1]
    C_x = box[2][0]
    C_y = box[2][1]
    D_x = box[3][0]
    D_y = box[3][1]

    a = (B_x - A_x) * (y - A_y) - (B_y - A_y) * (x - A_x)
    b = (C_x - B_x) * (y - B_y) - (C_y - B_y) * (x - B_x)
    c = (D_x - C_x) * (y - C_y) - (D_y - C_y) * (x - C_x)
    d = (A_x - D_x) * (y - D_y) - (A_y - D_y) * (x - D_x)
    # print("dd", a,b,c,d,x,y,box)
    if (a > 0 and b > 0 and c > 0 and d > 0) or (a < 0 and b < 0 and c < 0 and d < 0):
        return 1
    else:
        return 0

def hasprivacythreat_real (position, occ_grid_known, config, index, colorflag, sizeflag, log):
    # picture_index = np.zeros((30, 1), dtype=int)
    # picture_index = [12,17,21,41,50,55,60,70,81,86,94,99,106,113,119,126,132,140,148,155,160,166]
    # picture_index = [15, 22, 27, 31, 33, 36, 45, 48, 92, 110, 118, 122, 127, 129, 134, 136, 145, 146, 147, 148, 149, 150,151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164]
    # picture_list = [1, 2, 5, 7, 10, 13, 17, 18, 21, 24, 27, 28, 30, 33, 37, 41, 45, 49, 53, 56, 59, 62, 65, 67, 69, 73,
    #                 74, 76, 80, 82, 86, 88, 92, 93, 95, 99, 103]
    """
    :param position: current position of drone
    :param occ_grid_known: current environment map
    :param config: system configurations
    :param colorflag: detect blue or red
    :param sizeflag: split the picture into 3*3 or 5*5 to locate the center of privacy region
    :return: flag: if privacy region is detected, return the updated occ_grid_known
    """
    ## try this for offline testing with settled picture index
    picture_list_1 = [5, 10, 16, 22, 30, 38, 46, 56, 66, 76, 86, 96, 106, 116, 126, 136, 146, 152, 159, 166, 173, 180, 187, 194, 199, 205, 216]
    picture_list_2 = [3, 8, 13, 18, 25, 31, 37, 44, 55, 60, 65, 70, 75, 80, 85, 99, 102, 107, 112, 118, 124, 134, 139, 142, 143, 144, 150]

    ## when camera is on: position.ca==1, launch privacy region detection
    flag = 0
    if position.ca==1:
        # flag=1
        x = position.x
        y = position.y
        z = position.z

        # print("position:", position)
        # log.info("current position [%d, %d, %d, %d]" % (position.x, position.y, position.z, position.ca))

        ## try this for online
        # num = file_name('D:/1')
        # img1 = 'D:/1/' + str(num) + '.jpg'

        ## try this for offline testing with settled picture index
        # picture_index = picture_list_1[index]
        # img1 = os.getcwd() + '/pic5-1/'+str(picture_index)+".jpg"

        picture_index = picture_list_2[index]
        img1 = os.getcwd() + '/pic5-3/' + str(picture_index) + ".jpg"

        print("\033[92m image index: %s \033[0m" % (img1))
        log.info("image index %s" % (img1))
        img = cv2.imread(img1)
        # print(img)
        img = cv2.resize(img,(4000,2250),)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        if colorflag == 1:
            mask = cv2.inRange(hsv, blueLower, blueUpper)
        elif colorflag == 2:
            mask = cv2.inRange(hsv, redLower, redUpper)

        ret, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(binary, kernel, iterations=1)
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        arr_x = []
        arr_y = []
        # size_num = 5

        if sizeflag == 1:
            size_num = 3
        elif sizeflag == 2:
            size_num = 5
        elif sizeflag == 3:
            if x >= 3:
                size_num = 5
            else:
                size_num = 3

        x_start = 4000 / (size_num * 2)
        y_start = 2250 / (size_num * 2)
        for i in range(size_num):
            arr_x.append(x_start + i * x_start * 2)
            arr_y.append(y_start + i * y_start * 2)

        center_x = 4000 / 2
        center_y = 2250 / 2
        # print("center", center_x, center_y)
        # print(arr_x, arr_y)

        if contours:

            c = max(contours, key=cv2.contourArea)
            array = cv2.minAreaRect(c)
            box = cv2.boxPoints(array)
            box = np.int0(box)
            # print (box)

            length = abs(box[0][0] - box[2][0])
            width = abs(box[0][1] - box[1][1])
            area = length * width

            if area > 0.001 * 4000 * 2250:

                for xx in range(len(arr_x)):
                    for yy in range(len(arr_y)):
                        # print("fffff", (center_x - arr_x[xx]) / (4000 / 3), center_y - arr_y[yy])
                        y_ = round((center_x - arr_x[xx]) / (4000 / size_num))
                        x_ = round((center_y - arr_y[yy]) / (2250 / size_num))
                        # print(x_, y_)
                        if isInside(box, arr_x[xx], arr_y[yy]) == 1:
                            # print("inside", isInside(box, arr_x[xx], arr_y[yy]), arr_x[xx], arr_y[yy])
                            # x_ = int ((center_x - arr_x[xx]) / (4000 / 3))
                            # y_ = int ((center_y - arr_y[yy]) / (2250 / 3))
                            # print(x_, y_, y + x_, z + y_)
                            if y + x_ <= occ_grid_known.shape[1] - 1 and y + x_ >= 0 and z + y_ <= \
                                    occ_grid_known.shape[2] - 1 and z + y_ >= 0:
                                delta_y = y + x_
                                delta_z = z + y_
                                # if occ_grid_known[0][delta_y][delta_z] != 4:
                                flag = 1
                                occ_grid_known[0][delta_y][delta_z] = 4
                                print("\033[92m threat position: [%d, %d] \033[0m" % (delta_y, delta_z))
                                log.info("threat position: [%d, %d]" % (delta_y, delta_z))

                # cv2.drawContours(img, [box], 0, (0, 0, 0), 8)
                # cv2.imwrite(savepath, img)

                M = cv2.moments(c)
                # 得到物体中心点坐标
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

                # print("box center", cx, cy)

                y_ = math.ceil(size_num / 2) - math.ceil(cx / (4000 / size_num))
                x_ = math.ceil(size_num / 2) - math.ceil(cy / (2250 / size_num))
                # print(y_, x_)

                if y + x_ <= occ_grid_known.shape[1] - 1 and y + x_ >= 0 and z + y_ <= \
                        occ_grid_known.shape[2] - 1 and z + y_ >= 0:
                    delta_y = y + x_
                    delta_z = z + y_
                    # if occ_grid_known[0][delta_y][delta_z] != 4:
                    flag = 1
                    occ_grid_known[0][delta_y][delta_z] = 4
                    print("\033[92m center threat position: [%d, %d] \033[0m" % (delta_y, delta_z))
                    log.info("center threat position: [%d, %d]" % (delta_y, delta_z))



            else:
                flag = 0

        return flag, occ_grid_known
    else:
        flag = 0
        return flag, occ_grid_known
            
                
        


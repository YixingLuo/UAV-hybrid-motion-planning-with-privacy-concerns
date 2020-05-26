# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 08:59:57 2019

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 21:05:11 2019

@author: Administrator
"""
import cv2
import numpy as np
import os
redLower = np.array([150, 43, 46])
redUpper = np.array([180, 255, 255])

blueLower = np.array([90, 55, 160])
blueUpper = np.array([120, 200, 255])

list_i = [38, 39, 40, 41, 42, 43, 44]

from PIL import Image


for i in range(219):

    # if i in list_i:
    #     continue
    i +=1
    path = os.getcwd() + '/pic5-3/' + str(i)+'.jpg'
    print(path)
    img1 = cv2.imread(path)
    savepath = os.getcwd() + '/pic5-3/' + str(i)+ '_2.jpg'
    img = np.copy(img1)
    # img=cv2.resize(img,(4000,2250),)

    # print(img.shape)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, blueLower, blueUpper)
    # print('mask',mask)
    ret, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
    # print(ret, binary)
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(binary, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        print(i, img[cy][cx], cx, cy)
        # hsv  = cv2.cvtColor(img[cy][cx], cv2.COLOR_BGR2HSV)
        # print(hsv)



        array = cv2.minAreaRect(c)
        box = cv2.boxPoints(array)
        box = np.int0(box)

        length = abs (box[0][0]-box[2][0])
        width = abs (box [0][1]-box[1][1])

        print(path, img[cy][cx], cx, cy)
        cv2.drawContours(img, [box], 0, (0, 0, 0), 8)
        # cv2.imshow('Maximage', img)
        cv2.imwrite(savepath, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        area = length * width
        print(area)
        if area > 0.001 * 4000 * 2250:
            print(path, img[cy][cx], cx, cy)
            cv2.drawContours(img, [box], 0, (0, 0, 0), 8)
            # cv2.imshow('Maximage', img)
            cv2.imwrite(savepath, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()



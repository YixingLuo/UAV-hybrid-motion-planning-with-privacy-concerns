# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 15:55:16 2019

@author: Administrator
"""

import cv2
import os
 
# 读取图片并缩放方便显示
# path = 'D:/1/' + str(51) + '.jpg'
path = os.getcwd() + '/pic1_1/' + '25.jpg'
img = cv2.imread(path)
height, width = img.shape[:2]
size = (int(width * 0.2), int(height * 0.2))
# 缩放
img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
 
# BGR转化为HSV
HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
 
# 鼠标点击响应事件
def getposHsv(event, x, y, flags, param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print("HSV is", HSV[y, x])
 
 
def getposBgr(event, x, y, flags, param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print("Bgr is", img[y, x])
 
 
cv2.imshow("imageHSV", HSV)
cv2.imshow('image', img)
cv2.setMouseCallback("imageHSV", getposHsv)
cv2.setMouseCallback("image", getposBgr)
cv2.waitKey(0)

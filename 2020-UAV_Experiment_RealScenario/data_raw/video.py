# -*- coding: UTF-8 -*-
import os
import cv2
import time
import numpy as np

picture_list = [1,2,5,7,10,13,17,18,21,24,27,28,30,33,56,67,69,73,74,76,80,82,88,92,93,95,99,102]
index_list =   [0,1,2,3,4,5,6,7,8,9,10,11,12,13,19,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
# picture_list = [103]
# index_list = [36]

# 图片合成视频

path = os.getcwd() + "/pic2/"


# for i in range(37):
#     if i in index_list:
#         pass
#     else:
#         print(i)
#         # np.zeros()  返回来一个给定形状和类型的用0填充的数组
#
#         img = np.ones([1080,1920,3], dtype=np.uint8)*255
#
#         name = path2 = os.getcwd()+ "/pic2/used/" + str(i) + ".jpg"
#         print(name)
#         cv2.imwrite(name,img)







def readimg (path):
    for i in range (len(picture_list)):
        item = path + str(picture_list[i]) + '.jpg'
        print(item)
        img = cv2.imread(item)
        img = cv2.resize(img, (1920, 1080), )
        path2 = os.getcwd()+ "/pic2/used/" + str(index_list[i]) + ".jpg"
        print(path2)
        cv2.imwrite(path2, img)


def picvideo(path):
    # path = r'C:\Users\Administrator\Desktop\1\huaixiao\\'#文件路径
    filelist = os.listdir(path)  # 获取该目录下的所有文件名

    '''
    fps:
    帧率：1秒钟有n张图片写进去[控制一张图片停留5秒钟，那就是帧率为1，重复播放这张图片5次] 
    如果文件夹下有50张 534*300的图片，这里设置1秒钟播放5张，那么这个视频的时长就是10秒
    '''
    fps = 1
    # size = (1200, 924) #图片的分辨率片
    size = (1920,1080)
    # file_path = os.getcwd() + "/" + "10_10.mp4"  # 导出路径
    file_path = os.getcwd() + "/" + "10_10_pic.mp4"  # 导出路径
    print(file_path)
    # fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    # 不同视频编码对应不同视频格式（例：'I','4','2','0' 对应avi格式）
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    video = cv2.VideoWriter(file_path, fourcc, fps, size)

    # path = os.getcwd() + "\pic\\"
    # path = os.getcwd() + "/pic2/"  # 待读取的文件夹

    # print(path)

    # for i in range(len(picture_list)):
    for i in range(37):
    #     item = path + str(picture_list[i]) + '.jpg'
        item = os.getcwd() + "/pic2/used/" + str(i) + '.jpg'
        print(item)
        img = cv2.imread(item)  # 使用opencv读取图像，直接返回numpy.ndarray 对象，通道顺序为BGR ，注意是BGR，通道值默认范围0-255。
        img = cv2.resize(img, (1920,1080), )
        # print(img)
        video.write(img)  # 把图片写进视频


    video.release()  # 释放

# path = os.getcwd()
picvideo(path)


# readimg(path)

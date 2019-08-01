# -*- coding: UTF-8 -*-
import os
import cv2
import time


# 图片合成视频
def picvideo(path, size):
    # path = r'C:\Users\Administrator\Desktop\1\huaixiao\\'#文件路径
    filelist = os.listdir(path)  # 获取该目录下的所有文件名

    '''
    fps:
    帧率：1秒钟有n张图片写进去[控制一张图片停留5秒钟，那就是帧率为1，重复播放这张图片5次] 
    如果文件夹下有50张 534*300的图片，这里设置1秒钟播放5张，那么这个视频的时长就是10秒
    '''
    fps = 1
    size = (1200, 924) #图片的分辨率片
    file_path = os.getcwd() + "/" + "10_10.mp4"  # 导出路径
    print(file_path)
    # fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')  # 不同视频编码对应不同视频格式（例：'I','4','2','0' 对应avi格式）
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    video = cv2.VideoWriter(file_path, fourcc, fps, size)

    path = os.getcwd() + "\pic\\"  # 待读取的文件夹

    for i in range(27):
        item = path + str(i) + '.png'
        print(item)
        img = cv2.imread(item)  # 使用opencv读取图像，直接返回numpy.ndarray 对象，通道顺序为BGR ，注意是BGR，通道值默认范围0-255。
        print(img)
        video.write(img)  # 把图片写进视频


    video.release()  # 释放

path = os.getcwd()
picvideo(path, (1200, 924))




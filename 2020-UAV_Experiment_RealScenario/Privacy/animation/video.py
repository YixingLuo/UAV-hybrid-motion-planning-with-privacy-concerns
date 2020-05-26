# -*- coding: UTF-8 -*-
import os
import cv2
import time

list_i = [1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 160, 161, 162, 163, 164, 165, 166, 167, 168]

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
    size = (1920, 1080) #图片的分辨率片
    # file_path = os.getcwd() + "/" + "exp_model.mp4"  # 导出路径
    # file_path = os.getcwd() + "/" + "exp_model_ref.mp4"  # 导出路径
    file_path = os.getcwd() + "/" + "exp_pic_ref.mp4"  # 导出路径
    # file_path = os.getcwd() + "/" + "exp_pic_plan.mp4"  # 导出路径
    print(file_path)
    # fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')  # 不同视频编码对应不同视频格式（例：'I','4','2','0' 对应avi格式）
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    video = cv2.VideoWriter(file_path, fourcc, fps, size)
    #
    # path = os.getcwd() + "\pic_ref\\"  # 待读取的文件夹
    path = os.getcwd() + "\pic5-4\\"  # 待读取的文件夹
    # path = os.getcwd() + "\pic5-3\\"  # 待读取的文件夹
    # print(path)

    # for i in range(1,152):
    for i in range(len(list_i)):
        # print(len(L))
    # for i in range(25):
        item = path + str(list_i[i]) + '.jpg'
        # item = path + str(i) + '.jpg'
    #     print(item)

        img = cv2.imread(item)  # 使用opencv读取图像，直接返回numpy.ndarray 对象，通道顺序为BGR ，注意是BGR，通道值默认范围0-255。

        img = cv2.resize(img, (1920, 1080), )
            # print(img)
        video.write(img)  # 把图片写进视频


    video.release()  # 释放

path = os.getcwd()
picvideo(path, (1920, 1080))

#
#
# for root, dirs, files in os.walk(os.getcwd() + "\pic5-4\\"):
#     L = []
#     for file in files:
#         if os.path.splitext(file)[1] == '.jpg':
#             L.append(int(file[:-4]))
#     L.sort()
#     print(len(L))
#     print(L)




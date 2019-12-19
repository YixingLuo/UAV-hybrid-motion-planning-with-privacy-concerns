# -*- coding: UTF-8 -*-
import os
import cv2
import time

list_i = [1, 4, 6, 9, 11, 14, 16, 19, 21, 24, 28, 32, 37, 40, 41, 47, 49, 51, 55, 60, 69, 70, 71, 74, 76, 77, 80, 86, 90, 97, 100, 103, 108, 109, 114, 115, 116, 117, 118, 119, 120, 121, 122, 124, 126, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144]

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
    # file_path = os.getcwd() + "/" + "exp_model_1.mp4"  # 导出路径
    # file_path = os.getcwd() + "/" + "exp_model_ref_1.mp4"  # 导出路径
    # file_path = os.getcwd() + "/" + "exp_pic_ref.mp4"  # 导出路径
    file_path = os.getcwd() + "/" + "exp_pic_plan_1.mp4"  # 导出路径
    print(file_path)
    # fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')  # 不同视频编码对应不同视频格式（例：'I','4','2','0' 对应avi格式）
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    video = cv2.VideoWriter(file_path, fourcc, fps, size)
    #
    # path = os.getcwd() + "\pic_ref\\"  # 待读取的文件夹
    path = os.getcwd() + "\pic5-1\\"  # 待读取的文件夹
    # path = os.getcwd() + "\pic5-2\\"  # 待读取的文件夹

    for i in range(1,220):
    # for i in range(len(list_i)):
        # print(len(L))
    # for i in range(25):
    #     item = path + str(list_i[i]) + '.jpg'
        item = path + str(i) + '.jpg'
        print(item)

        img = cv2.imread(item)  # 使用opencv读取图像，直接返回numpy.ndarray 对象，通道顺序为BGR ，注意是BGR，通道值默认范围0-255。

        img = cv2.resize(img, (1920, 1080), )
            # print(img)
        video.write(img)  # 把图片写进视频


    video.release()  # 释放

path = os.getcwd()
picvideo(path, (1920, 1080))



# for root, dirs, files in os.walk(os.getcwd() + "\pic5-2\\"):
#     L = []
#     for file in files:
#         if os.path.splitext(file)[1] == '.jpg':
#             L.append(int(file[:-4]))
#     L.sort()
#     print(len(L))
#     print(L)




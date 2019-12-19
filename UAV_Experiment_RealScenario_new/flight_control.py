"""
flight control of UAV
"""
# 无人机方向锁定，x轴正方向

# 前一个状态
#x_pri, y_pri, h_pri, rs_pri

# 后一个状态
#x_next, y_next, h_next, rs_next

#左手坐标系，中指为z正，大拇指为y正，食指为x正

from socket import *
import time
import numpy as np
import random

#HOST = '192.168.31.105'
HOST = '192.168.0.100'
PORT = 7896
s = socket(AF_INET, SOCK_DGRAM)
s.connect((HOST, PORT))

# x_pri = 0
#
# y_pri = 0
#
# z = 0
#
# h = 1
#
# xl = 0


def flight_control (previous, next, trajectory, socket, continue_time):

    s = socket
    index_list = []
    for i in range(previous, next+1):
        index_list.append(i)

    # print(index_list)
    for i in range(len(index_list)-1):
        previous_point = trajectory[index_list[i]]
        next_point = trajectory[index_list[i+1]]

        x_pri = previous_point.y
        y_pri = previous_point.z
        z_pri = previous_point.x
        camera_pri = previous_point.ca

        x_next = next_point.y  # 前后
        y_next = next_point.z  # 左右
        z_next = next_point.x  # 上下
        camera = next_point.ca  # 分辨率

        h = 1 + z_pri

        print("from:", previous_point, "to:", next_point)

        # x方向变化
        if x_next - x_pri != 0:

            # 向x轴正方向移动(向前)
            if x_next - x_pri == 1:
                message = str(str(0) + ',' + str(0.5) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
                # print(message)
                s.sendall(message.encode('utf-8'))
                print("向前")

                time.sleep(continue_time)

                # message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
                # print(message)
                # s.sendall(message.encode('utf-8'))
                # print(message)
                # print("停止")

                # message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
                # # print(message)
                # s.sendall(message.encode('utf-8'))

                # time.sleep(5)

            else:
                message = str(str(0) + ',' + str(-0.5) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
                # print(message)
                s.sendall(message.encode('utf-8'))
                print("向后")

                time.sleep(continue_time)

                message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
                # print(message)
                s.sendall(message.encode('utf-8'))
                print("停止")

                # message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
                # # print(message)
                # s.sendall(message.encode('utf-8'))

                time.sleep(5)

        # y方向变化
        elif y_next - y_pri != 0:
            if y_next - y_pri == 1:
                message = str(str(-0.5) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
                # print(message)
                s.sendall(message.encode('utf-8'))
                print("向左")

                time.sleep(continue_time)

                message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
                # print(message)
                s.sendall(message.encode('utf-8'))
                print("停止")

                # message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
                # # print(message)
                # s.sendall(message.encode('utf-8'))

                time.sleep(5)


            else:
                message = str(str(0.5) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
                # print(message)
                s.sendall(message.encode('utf-8'))
                print("向右")

                time.sleep(continue_time)

                message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
                s.sendall(message.encode('utf-8'))
                print("停止")

                # message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
                # s.sendall(message.encode('utf-8'))

                time.sleep(5)


        elif z_next - z_pri != 0:
            if z_next - z_pri == 1:
                message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(z_next + 1) + ',' + str(camera))
                # print(message)
                s.sendall(message.encode('utf-8'))
                print("升至" + str(z_next + 1) + "米")

                message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(z_next + 1) + ',' + str(camera))
                # print(message)
                s.sendall(message.encode('utf-8'))

                # message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(z_next + 1) + ',' + str(camera))
                # print(message)
                # s.sendall(message.encode('utf-8'))

                time.sleep(8)

            if z_pri - z_next == 1:
                message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(z_next + 1) + ',' + str(camera))
                # print(message)
                s.sendall(message.encode('utf-8'))
                print("降至" + str(z_next + 1) + "米")

                message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(z_next + 1) + ',' + str(camera))
                # print(message)
                s.sendall(message.encode('utf-8'))

                # message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(z_next + 1) + ',' + str(camera))
                # print(message)
                # s.sendall(message.encode('utf-8'))

                time.sleep(8)

        if camera != camera_pri:
            print("\033[95m camera configuration: from %d to %d \033[0m" % (camera_pri, camera))





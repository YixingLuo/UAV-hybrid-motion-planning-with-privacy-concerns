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
HOST = '192.168.0.101'
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


#txt
# list = [[0,0,0,1],
# [0,0,1,1],
# [0,1,1,1],
# [0,1,2,1],
# [1,1,2,1],
# [1,2,2,1],
# [1,3,2,1],
# [0,3,2,1],
# [0,3,3,1],
# [1,3,3,1],
# [1,3,4,1],
# [1,3,5,1],
# [0,3,5,1],
# [0,3,6,1],
# [0,3,7,1],
# [0,4,7,1],
# [1,4,7,1],
# [1,5,7,1],
# [1,6,7,1],
# [0,6,7,1],
# [0,7,7,1],
# [0,8,7,1],
# [0,8,8,1],
# [0,8,9,1],
# [0,9,9,1]]

h = 1

def flight_control (previous, next, trajectory, socket):

    s = socket
    previous_point = trajectory[previous]
    next_point = trajectory[next]

    x_pri = previous_point.y
    y_pri = previous_point.z
    z_pri = previous_point.x
    camera_pri  = previous_point.ca

    x_next = next_point.y  # 前后
    y_next = next_point.z  # 左右
    z_next = next_point.x  # 上下
    camera = next_point.ca  # 分辨率

    h = 1 + z_pri

    print(previous, next, previous_point,next_point,h)

    # x方向变化
    if x_next - x_pri != 0:

        # 向x轴正方向移动(向前)
        if x_next - x_pri == 1:
            message = str(str(0) + ',' + str(1) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))
            print("向前")

            time.sleep(2)

            message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))
            print("停止")

            message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))

            # time.sleep(5)

        else:
            message = str(str(0) + ',' + str(-1) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))
            print("向后")

            time.sleep(2)

            message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))
            print("停止")

            message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))

            # time.sleep(5)

    # y方向变化
    elif y_next - y_pri != 0:
        if y_next - y_pri == 1:
            message = str(str(-1) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))
            print("向左")

            time.sleep(2)

            message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))
            print("停止")

            message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))

            # time.sleep(5)


        else:
            message = str(str(1) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))
            print("向右")

            time.sleep(2)

            message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))
            print("停止")

            message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))

            # time.sleep(5)


    elif z_next - z_pri != 0:
        if z_next - z_pri == 1:

            message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(z_next + 1) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))
            print("升至" + str(z_next  + 1) + "米")

            time.sleep(1)

        if z_pri - z_next == 1:

            message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(z_next + 1) + ',' + str(camera))
            s.sendall(message.encode('utf-8'))
            print("降至" + str(z_next  + 1) + "米")

            time.sleep(1)

    if camera != camera_pri:
        print("camera configuration: from %d to %d" % (camera_pri, camera))


# for item in list:
#
#     x_next = item[1]  #前后
#     y_next = item[2]  #左右
#     z = item[0]  #上下
#     camera = item[3]  #分辨率
#
#
#
#     # x方向变化
#     if x_next - x_pri != 0:
#
#     # 向x轴正方向移动(向前)
#         if x_next-x_pri == 1:
#             message = str(str(0) + ',' + str(0.5) + ',' + str(0) + ',' + str(h)+ ',' +str(camera))
#             s.sendall(message.encode('utf-8'))
#             print("向前")
#
#             time.sleep(1)
#
#             message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h)+ ',' +str(camera))
#             s.sendall(message.encode('utf-8'))
#             print("停止")
#
#             time.sleep(1.5)
#
#             message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
#             s.sendall(message.encode('utf-8'))
#
#             x_pri = x_next
#
#         else:
#             message = str(str(0) + ',' + str(-0.5) + ',' + str(0) + ',' + str(h)+ ',' +str(camera))
#             s.sendall(message.encode('utf-8'))
#             print("向后")
#
#             time.sleep(1)
#
#             message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h)+ ',' +str(camera))
#             s.sendall(message.encode('utf-8'))
#             print("停止")
#
#             time.sleep(1.5)
#
#             message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
#             s.sendall(message.encode('utf-8'))
#
#             x_pri = x_next
#
#
#     # y方向变化
#     elif y_next - y_pri != 0:
#         if y_next-y_pri == 1:
#             message = str(str(-0.5) + ',' + str(0) + ',' + str(0) + ',' + str(h)+ ',' +str(camera))
#             s.sendall(message.encode('utf-8'))
#             print("向左")
#
#             time.sleep(1)
#
#             message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h)+ ',' +str(camera))
#             s.sendall(message.encode('utf-8'))
#             print("停止")
#
#             time.sleep(1.5)
#
#             message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
#             s.sendall(message.encode('utf-8'))
#
#             y_pri = y_next
#
#         else :
#             message = str(str(0.5) + ',' + str(0) + ',' + str(0) + ',' + str(h)+ ',' +str(camera))
#             s.sendall(message.encode('utf-8'))
#             print("向右")
#
#             time.sleep(1)
#
#             message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h)+ ',' +str(camera))
#             s.sendall(message.encode('utf-8'))
#             print("停止")
#
#             time.sleep(1.5)
#
#             message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(h) + ',' + str(camera))
#             s.sendall(message.encode('utf-8'))
#
#             y_pri = y_next
#
#     else:
#
#
#
#         message = str(str(0) + ',' + str(0) + ',' + str(0) + ',' + str(z+1) + ',' + str(camera))
#         s.sendall(message.encode('utf-8'))
#         print("升至"+str(z+1)+"米")
#
#         time.sleep(8)
#
#         h = z+1







####################################
#功能：场景可视化
#输入：maplabel_height_update.txt、reference_path2.npy、plan_path_Hybrid3.npy
#输出：i.txt、可视化

import numpy as np
import mayavi.mlab as mlab
import copy
import matplotlib.pyplot as plt

'''
t= np.mgrid[-np.pi:np.pi:100j]
mlab.plot3d(np.cos(t), np.sin(3 * t), np.cos(5 * t), color=(0.23, 0.6, 1), colormap='Spectral')
mlab.colorbar()
mlab.show()
'''
'''
def map(map_array):

    mlab.barchart(A/10)
    #mlab.plot3d(x, y, z, color=(0.23, 0.6, 1), colormap='Spectral')
    mlab.plot3d(x, y, z, color=(0.5, 0, 0),tube_radius=None, colormap='Spectral')
    mlab.plot3d(x1, y1, z1, color=(0, 1, 0), opacity=1,tube_radius=None, colormap='Spectral')


    #mlab.plot3d(x2, y2, z2, color=(0, 0, 1), opacity=1, tube_radius=None, colormap='Spectral')
    #mlab.plot3d(x3, y3, z3, color=(0, 0, 1), opacity=1, tube_radius=None, colormap='Spectral')

    mlab.vectorbar()
    mlab.xlabel('x')
    mlab.ylabel('y')
    mlab.zlabel('z')
    mlab.show()
'''
# occ_grid = np.load("occ_grid-50.npy")
# obstaclex = []
# obstacley = []
# obstaclez = []
# privacy2x = []
# privacy2y = []
# privacy2z = []
# privacy3x = []
# privacy3y = []
# privacy3z = []
# privacy4x = []
# privacy4y = []
# privacy4z = []
# v1 = []
# v2 = []
# v3 = []
# v4 = []
# for i in range(10):
#     for j in range(50):
#         for k in range(50):
#             if occ_grid[i][j][k] == 1:
#                 obstaclex.append(j)
#                 obstacley.append(k)
#                 obstaclez.append(i)
#                 v1.append(1 - occ_grid[i][j][k])
#             if occ_grid[i][j][k] == 2:
#                 privacy2x.append(j)
#                 privacy2y.append(k)
#                 privacy2z.append(i)
#                 v2.append(1 - occ_grid[i][j][k])
#             if occ_grid[i][j][k] == 3:
#                 privacy3x.append(j)
#                 privacy3y.append(k)
#                 privacy3z.append(i)
#                 v3.append(1 - occ_grid[i][j][k])
#             if occ_grid[i][j][k] == 4:
#                 privacy4x.append(j)
#                 privacy4y.append(k)
#                 privacy4z.append(i)
#                 v4.append(1 - occ_grid[i][j][k])
#
# mlab.points3d(obstaclex, obstacley, obstaclez, v1, mode='cube', color=(0,0,0), scale_mode='none', scale_factor='1')
# mlab.points3d(privacy2x, privacy2y, privacy2z, v2, mode='cube', color=(0.5,0,1), scale_mode='none', scale_factor='1')
# mlab.points3d(privacy3x, privacy3y, privacy3z, v3, mode='cube', color=(0.75,0,1), scale_mode='none', scale_factor='1')
# mlab.points3d(privacy4x, privacy4y, privacy4z, v4, mode='cube', color=(1,0,1), scale_mode='none', scale_factor='1')



#将所有建筑物可视化过程
A=np.loadtxt('maplabel_height_update.txt',delimiter=',')
print("打印带高度信息的地图\n")
print(A)

Label = np.loadtxt('maplabel_privacy.txt',delimiter=' ')
A1 = np.zeros((50,50),dtype=int)
A2 = copy.deepcopy(A1)
A2 = copy.deepcopy(A1)
A3 = copy.deepcopy(A1)
A4 = copy.deepcopy(A1)

for i in range(50):
    for j in range (50):
        label = Label[i][j]
        if label == 1:
            A1[i][j] = A[i][j]
        if label == 2:
            A2[i][j] = A[i][j]
        if label == 3:
            A3[i][j] = A[i][j]
        if label == 4:
            A4[i][j] = A[i][j]





#参考路径可视化过程
reference_path1 = "reference_path1" + ".npy"
reference = np.load(file=reference_path1)
print("参考路径数组类型输出：",reference.shape)
print("输出参考路径：\n")
print(reference)
print("x=0时：")
print(reference[0])
print("测试...取第一维高度：")
print(reference[:,0])
x=reference[:,1]
y=reference[:,2]
z=reference[:,0]
print(x)
#综合路径可视化过程
plan_path_Hybrid1="plan_path_Hybrid1"+ ".npy"
plan_path_Hybrid=np.load(file=plan_path_Hybrid1)
print("综合规划路径数组类型输出：",plan_path_Hybrid.shape)
print("输出Hybird路径：\n")
print(plan_path_Hybrid)
print("x=0时：")
print(plan_path_Hybrid[0])
print("测试...取第一维高度：")
print(plan_path_Hybrid[:,0])
x1=plan_path_Hybrid[:,1]
y1=plan_path_Hybrid[:,2]
z1=plan_path_Hybrid[:,0]

#camera状态改变可视化过程
camera_path="plan_path_Hybrid1"+ ".npy"
camera_path=np.load(file=camera_path)
'''
x2=camera_path[71:75,1]
y2=camera_path[71:75,2]
z2=camera_path[71:75,0]
x3=camera_path[75:77,1]
y3=camera_path[75:77,2]
z3=camera_path[75:77,0]
'''
print("测试...取摄像机开关状态：")
c=plan_path_Hybrid[:,3]
#print(c)
#print(len(c))
#print(c[0])
cc=[]#cc表示改变摄像机状态的点的位置集合
for i in range(len(c)):
    if c[i]!=c[i-1]:
        print(i-1,c[i-1])
        cc.append(i-1)
print("改变摄像机状态的点的位置集合：",cc)
ccc=[]
n=2
for i in range(0, len(cc), n):

    print(cc[i:i + n])
    ccc.append(cc[i:i + n])
print("将状态的位置集合拆分成两两的线段：",ccc)
print("改变camera状态的线段的条数：",len(ccc))
print("####",np.shape(ccc)[0])

#总体可视化函数
# mlab.barchart(A / 10)
mlab.barchart(A1 / 10)
mlab.barchart(A2 / 10)
mlab.barchart(A3 / 10)
mlab.barchart(A4 / 10)

# mlab.plot3d(x, y, z, color=(0.23, 0.6, 1), colormap='Spectral')
mlab.plot3d(x, y, z, color=(1, 0, 0),opacity=1, tube_radius=None, colormap='Spectral')
mlab.plot3d(x1, y1, z1, color=(0, 0, 1), opacity=1, tube_radius=None, colormap='Spectral')

for i in range(np.shape(ccc)[0]):
    c1=plan_path_Hybrid[ccc[i][0]:(ccc[i][1]+1),0:3]
    print("******",c1)
    np.savetxt("c" + str(i) + ".txt", c1, fmt='%d', delimiter=' ')
    camera_path_1 = np.loadtxt("c"+str(i)+".txt", delimiter=' ', dtype=int)
    print("@@@@@@@@@",camera_path_1)
    X = camera_path_1[:, 1]
    Y = camera_path_1[:, 2]
    Z = camera_path_1[:, 0]
    for i in range(np.shape(ccc)[0]):
        mlab.plot3d(X, Y, Z, color=(0, 1, 0), opacity=1, tube_radius=None, colormap='Spectral')

mlab.points3d(0, 0, 0,mode='cube', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')
mlab.points3d(49, 49, 0,mode='cube', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')
# mlab.axes(extent=[0, 50, 0, 50, 0, 10])
# mlab.vectorbar()
mlab.xlabel('x')
mlab.ylabel('y')
mlab.zlabel('z')
mlab.show()
#map(A)
'''
cccc=np.zeros([np.shape(ccc)[0]*np.shape(ccc)[1],3])
m=0
for i in range(np.shape(ccc)[0]):
    for j in range(np.shape(ccc)[1]):
        print("原规划路径摄像机改变的集合：")
        print(plan_path_Hybrid[ccc[i][j]])
        cccc[m][:]=plan_path_Hybrid[ccc[i][j]][0:3]
        m+=1
print("开关变化的点集合\n",cccc)
ccccc=[]
for i in range(0, len(cccc), n):

    #print(cccc[i:i + n])
    ccccc.append(cccc[i:i + n])
print("两两线段切分：\n",ccccc[1])
'''














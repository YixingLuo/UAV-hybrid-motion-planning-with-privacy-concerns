import numpy as np
import mayavi.mlab as mlab
import matplotlib.pyplot as plt

'''
t= np.mgrid[-np.pi:np.pi:100j]
mlab.plot3d(np.cos(t), np.sin(3 * t), np.cos(5 * t), color=(0.23, 0.6, 1), colormap='Spectral')
mlab.colorbar()
mlab.show()
'''
def map(map_array):

    mlab.barchart(A/10)
    #mlab.plot3d(x, y, z, color=(0.23, 0.6, 1), colormap='Spectral')
    mlab.plot3d(x, y, z, color=(0.5, 0, 0),tube_radius=None, colormap='Spectral')
    mlab.plot3d(x1, y1, z1, color=(0, 1, 0), opacity=1,tube_radius=None, colormap='Spectral')
    mlab.plot3d(x2, y2, z2, color=(0, 0, 1), opacity=1, tube_radius=None, colormap='Spectral')
    mlab.plot3d(x3, y3, z3, color=(0, 0, 1), opacity=1, tube_radius=None, colormap='Spectral')

    mlab.vectorbar()
    mlab.xlabel('x')
    mlab.ylabel('y')
    mlab.zlabel('z')
    mlab.show()
A=np.loadtxt('maplabel_height_update.txt',delimiter=',')
print("打印带高度信息的地图\n")
print(A)





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

#camera_path=np.loadtxt('c0.txt',delimiter=' ',dtype=int)
camera_path="plan_path_Hybrid1"+ ".npy"
camera_path=np.load(file=camera_path)
x2=camera_path[71:75,1]
y2=camera_path[71:75,2]
z2=camera_path[71:75,0]
x3=camera_path[75:77,1]
y3=camera_path[75:77,2]
z3=camera_path[75:77,0]
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
print(ccc[0][0])
cccc=np.zeros([4,3])
m=0
for i in range(2):
    for j in range(2):
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
for i in range(2):
    #保存切好的线段
    np.savetxt("c"+str(i)+".txt", ccccc[i], fmt='%d', delimiter=' ')


#mlab.plot3d(x, y, z, color=(0.5, 0, 0), tube_radius=None, colormap='Spectral')




map(A)




print("......")

'''
np.savetxt("occ_grid_0.txt",occ_grid[0],fmt='%d',delimiter=' ')
np.savetxt("occ_grid_1.txt",occ_grid[1],fmt='%d',delimiter=' ')
x=occ_grid[0]
y=occ_grid[:,1,:]
z=occ_grid[:,:,2]
mlab.barchart(y,z,x)
mlab.xlabel('x')
mlab.ylabel('y')
mlab.zlabel('z')
mlab.show()
'''
#s=occ_grid
#mlab.barchart(s)
#mlab.vectorbar()
#mlab.show()

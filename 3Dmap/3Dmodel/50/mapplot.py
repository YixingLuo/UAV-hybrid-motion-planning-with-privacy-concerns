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
    mlab.barchart(A)
    #mlab.plot3d(x, y, z, color=(0.23, 0.6, 1), colormap='Spectral')
    mlab.plot3d(x, y, z, color=(0.5, 0, 0),tube_radius=0.1, colormap='Spectral')
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
x=reference[:,1]+1
y=reference[:,2]+1
z=reference[:,0]+1
print(x)

hybrid_path1 = "plan_path_Hybrid1" + ".npy"
hybrid = np.load(file=hybrid_path1)
print("规划径数组类型输出：",reference.shape)
print("输出规划路径：\n")
print(hybrid, len(hybrid))
print("x=0时：")
print(hybrid[0])
print("测试...取第一维高度：")
print(hybrid[:,0])
x=hybrid[:,1]+1
y=hybrid[:,2]+1
z=hybrid[:,0]+1
print(x)


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

####################################
#功能：10*10的场景可视化
#输入：maplabel_height_update.txt、reference_path1.npy、plan_path_Hybrid1.npy
#输出：i.txt、可视化

import numpy as np
import mayavi.mlab as mlab
import matplotlib.pyplot as plt
import moviepy.editor as mpy
import copy
import  os

duration = 37

#将所有建筑物可视化过程
# A=np.loadtxt('occ_grid_height_PP.txt',delimiter=' ')
A=np.loadtxt('occ_grid_height_SA.txt',delimiter=' ')
print("打印带高度信息的地图\n")
# print(A)

# Label = np.loadtxt('ground_PP.txt',delimiter=' ')
Label = np.loadtxt('ground_SA.txt',delimiter=' ')
print(Label)
A1 = np.zeros((A.shape[0], A.shape[1]),dtype=int)
#A2 = copy.deepcopy(A1)
A2 = copy.deepcopy(A1)
A3 = copy.deepcopy(A1)
A4 = copy.deepcopy(A1)

for i in range(A.shape[0]):
    for j in range (A.shape[1]):
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
# reference_path = "reference_path1" + ".npy"
reference_path = "reference_path3" + ".npy"
reference = np.load(file = reference_path)
print(reference)
# reference  = np.loadtxt('reference.txt',delimiter=' ')

# print("参考路径数组类型输出：",reference.shape)
# print("输出参考路径：\n")
# print(reference)
# print("x=0时：")
# print(reference[0])
# print("测试...取第一维高度：")
# print(reference[:,0])
# 为保证可视化的美观性，在起点出插入【0，0，0】，在终点追加【9，9，0】
x=reference[:,1]
x=np.insert(x,0,0)
x=np.append(x,A.shape[0]-1)
# print("x的内容",x)
y=reference[:,2]
y=np.insert(y,0,0)
y=np.append(y,A.shape[1]-1)
z=reference[:,0]+0.5
z=np.insert(z,0,0)
z=np.append(z,0)
# print("高度：",type(z))

# mlab.barchart(A1)
# mlab.barchart(A2)
# mlab.barchart(A3)
# mlab.barchart(A4)
# #
# mlab.points3d(0, 0, 0,mode='cube', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')
# mlab.points3d(14, 14, 0,mode='cube', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')
#
# mlab.plot3d(x, y, z, color=(0, 0, 0), opacity=1, tube_radius=None, colormap='Spectral')
# mlab.show()

# vol = mlab.contour3d(volumes_data[:,:,:,0], contours = 10, opacity=0.8, colormap='jet', figure = fig3)

def make_frame(t):
    # x = volumes_data[:, :, :, int(t * 100/5/2)]
    # vol.mlab_source.set(scalars=x)
    mlab.clf(figure=None)
    print(int(t * 100 /5/2))
    mlab.barchart(A1)
    mlab.barchart(A2)
    mlab.barchart(A3)
    mlab.barchart(A4)

    mlab.points3d(0, 0, 0, mode='cube', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')
    mlab.points3d(A.shape[0]-1, A.shape[1]-1, 0, mode='cube', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')
    num = int(t)
    # plan_path_Hybrid1 = "plan_path_Hybrid_temp" + str(num) + ".npy"
    plan_path_Hybrid1 = "plan_path_PP_temp" + str(num) + ".npy"
    plan_path_Hybrid = np.load(file=plan_path_Hybrid1)
    # print("综合规划路径数组类型输出：",plan_path_Hybrid.shape)
    # print("输出Hybird路径：\n")
    # print(plan_path_Hybrid)
    # print("x=0时：")
    # print(plan_path_Hybrid[0])
    # print("测试...取第一维高度：")
    # print(plan_path_Hybrid[:,0])
    x1 = plan_path_Hybrid[:, 1]
    x1 = np.insert(x1, 0, 0)
    x1 = np.append(x1, A.shape[0]-1)
    y1 = plan_path_Hybrid[:, 2]
    y1 = np.insert(y1, 0, 0)
    y1 = np.append(y1, A.shape[1]-1)
    z1 = plan_path_Hybrid[:, 0] + 0.5
    z1 = np.insert(z1, 0, 0)
    z1 = np.append(z1, 0)

    # camera状态改变可视化过程
    # camera_path = "plan_path_Hybrid_temp" + str(num) + ".npy"
    camera_path = "plan_path_PP_temp" + str(num) + ".npy"
    camera_path = np.load(file=camera_path)

    # print("测试...取摄像机开关状态：")
    c = plan_path_Hybrid[:, 3]
    # print(c)
    # print(len(c))
    # print(c[0])
    cc = []  # cc表示改变摄像机状态的点的位置集合
    for i in range(len(c)):
        if c[i] != c[i - 1]:
            # print(i-1,c[i-1])
            cc.append(i - 1)
    # print("改变摄像机状态的点的位置集合：",cc)
    ccc = []
    n = 2
    for i in range(0, len(cc), n):
        # print(cc[i:i + n])
        ccc.append(cc[i:i + n])
    # print("将状态的位置集合拆分成两两的线段：",ccc)
    # print("改变camera状态的线段的条数：",len(ccc))
    # print("####",np.shape(ccc)[0])

    # mlab.plot3d(x, y, z, color=(0.23, 0.6, 1), colormap='Spectral')
    mlab.plot3d(x1, y1, z1, color=(0, 0, 1), opacity=1, tube_radius=None, colormap='Spectral')
    mlab.plot3d(x, y, z, color=(0, 0, 0), opacity=1, tube_radius=None, colormap='Spectral')

    for i in range(np.shape(ccc)[0]):
        c1 = plan_path_Hybrid[ccc[i][0]:(ccc[i][1] + 1), 0:3]
        # print("******",c1)
        np.savetxt("c" + str(i) + ".txt", c1, fmt='%d', delimiter=' ')
        camera_path_1 = np.loadtxt("c" + str(i) + ".txt", delimiter=' ', dtype=int)
        # print("@@@@@@@@@",camera_path_1)
        X = camera_path_1[:, 1]
        Y = camera_path_1[:, 2]
        Z = camera_path_1[:, 0] + 0.5
        for i in range(np.shape(ccc)[0]):
            mlab.plot3d(X, Y, Z, color=(0, 1, 0), opacity=1, tube_radius=None, colormap='Spectral')

    a = plan_path_Hybrid[num][0]
    b = plan_path_Hybrid[num][1]
    c = plan_path_Hybrid[num][2]
    # print(c, a, b)
    mlab.points3d(b, c, a + 0.5, mode='cube', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')

    s = mlab.gcf()
    s.scene.background = (1, 1, 1)
    source = s.children[0]
    colors = source.children[0]
    # colors = manager.children[0]
    # print(colors)
    colors.scalar_lut_manager.lut_mode = "Blues"
    colors = s.children[1].children[0]
    colors.scalar_lut_manager.lut_mode = "Wistia"
    colors = s.children[2].children[0]
    colors.scalar_lut_manager.lut_mode = "RdYlBu"
    colors = s.children[3].children[0]
    colors.scalar_lut_manager.lut_mode = "OrRd"
    mlab.move(forward=-4, right=-4)

    mlab.savefig('abc.png', figure=mlab.gcf(), magnification=2)

    # mlab.show()

    # return mlab.screenshot(antialiased=True)
    print(mlab.screenshot(figure=None, mode='rgb', antialiased=False))
    return mlab.screenshot(figure=None, mode='rgb', antialiased=False)


# animation = mpy.VideoClip(make_frame, duration=duration).resize(0.5)  # 一定要resize，否则会出错
# animation = mpy.VideoClip(make_frame, duration=duration)
# animation.write_gif("4Dfmri.gif",fps=3)  # 需要通过控制duration和fps的大小来，操控显示
# animation.write_videofile("./target.mp4", fps=3)

# @mlab.animate(delay=500)
def anim():
    f = mlab.gcf()
    print("showing map")

    mlab.barchart(A1)
    mlab.barchart(A2)
    mlab.barchart(A3)
    mlab.barchart(A4)

    s = mlab.gcf()
    s.scene.background = (1, 1, 1)
    source = s.children[0]
    colors = source.children[0]
    # colors = manager.children[0]
    # print(colors)
    colors.scalar_lut_manager.lut_mode = "Blues"
    colors = s.children[1].children[0]
    colors.scalar_lut_manager.lut_mode = "Wistia"
    colors = s.children[2].children[0]
    colors.scalar_lut_manager.lut_mode = "RdYlBu"
    colors = s.children[3].children[0]
    colors.scalar_lut_manager.lut_mode = "OrRd"
    mlab.points3d(0, 0, 0, mode='cube', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')
    mlab.points3d(9, 9, 0, mode='cube', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')

    for scene_cnt in range(0, 27):
        print('Updating scene...  the number is ', scene_cnt)
        # mlab.clf(figure=None)
        num = scene_cnt
        plan_path_Hybrid1 = "plan_path_Hybrid_temp" + str(num) + ".npy"
        plan_path_Hybrid = np.load(file=plan_path_Hybrid1)
        # print("综合规划路径数组类型输出：",plan_path_Hybrid.shape)
        # print("输出Hybird路径：\n")
        # print(plan_path_Hybrid)
        # print("x=0时：")
        # print(plan_path_Hybrid[0])
        # print("测试...取第一维高度：")
        # print(plan_path_Hybrid[:,0])
        x1 = plan_path_Hybrid[:, 1]
        x1 = np.insert(x1, 0, 0)
        x1 = np.append(x1, 9)
        y1 = plan_path_Hybrid[:, 2]
        y1 = np.insert(y1, 0, 0)
        y1 = np.append(y1, 9)
        z1 = plan_path_Hybrid[:, 0] + 0.5
        z1 = np.insert(z1, 0, 0)
        z1 = np.append(z1, 0)

        # camera状态改变可视化过程
        camera_path = "plan_path_Hybrid_temp" + str(num) + ".npy"
        camera_path = np.load(file=camera_path)

        # print("测试...取摄像机开关状态：")
        c = plan_path_Hybrid[:, 3]
        # print(c)
        # print(len(c))
        # print(c[0])
        cc = []  # cc表示改变摄像机状态的点的位置集合
        for i in range(len(c)):
            if c[i] != c[i - 1]:
                # print(i-1,c[i-1])
                cc.append(i - 1)
        # print("改变摄像机状态的点的位置集合：",cc)
        ccc = []
        n = 2
        for i in range(0, len(cc), n):
            # print(cc[i:i + n])
            ccc.append(cc[i:i + n])
        # print("将状态的位置集合拆分成两两的线段：",ccc)
        # print("改变camera状态的线段的条数：",len(ccc))
        # print("####",np.shape(ccc)[0])

        # mlab.plot3d(x, y, z, color=(0.23, 0.6, 1), colormap='Spectral')
        mlab.plot3d(x1, y1, z1, color=(0, 0, 1), opacity=1, tube_radius=None, colormap='Spectral')
        mlab.plot3d(x, y, z, color=(0, 0, 0), opacity=1, tube_radius=None, colormap='Spectral')

        for i in range(np.shape(ccc)[0]):
            c1 = plan_path_Hybrid[ccc[i][0]:(ccc[i][1] + 1), 0:3]
            # print("******",c1)
            np.savetxt("c" + str(i) + ".txt", c1, fmt='%d', delimiter=' ')
            camera_path_1 = np.loadtxt("c" + str(i) + ".txt", delimiter=' ', dtype=int)
            # print("@@@@@@@@@",camera_path_1)
            X = camera_path_1[:, 1]
            Y = camera_path_1[:, 2]
            Z = camera_path_1[:, 0] + 0.5
            for i in range(np.shape(ccc)[0]):
                mlab.plot3d(X, Y, Z, color=(0, 1, 0), opacity=1, tube_radius=None, colormap='Spectral')

        a = plan_path_Hybrid[num][0]
        b = plan_path_Hybrid[num][1]
        c = plan_path_Hybrid[num][2]
        # print(c, a, b)
        mlab.points3d(b, c, a + 0.5, mode='sphere', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')
        # mlab.view(focalpoint='auto')
        yield


# anim()
# mlab.show()

if __name__ == '__main__' :

    # for num in range(18,19):
    for num in range(27):
        mlab.clf(figure=None)

        # 将所有建筑物可视化过程
        # A = np.loadtxt("occ_grid_height" + str(num) + ".txt", delimiter=' ')
        # print("打印带高度信息的地图\n")
        # print(A)

        # Label = np.loadtxt("ground" + str(num) + ".txt", delimiter=' ')
        # print(Label)
        A1 = np.zeros((A.shape[0], A.shape[1]), dtype=int)
        # A2 = copy.deepcopy(A1)
        A2 = copy.deepcopy(A1)
        A3 = copy.deepcopy(A1)
        A4 = copy.deepcopy(A1)

        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                label = Label[i][j]
                if label == 1:
                    A1[i][j] = A[i][j]
                if label == 2:
                    A2[i][j] = A[i][j]
                if label == 3:
                    A3[i][j] = A[i][j]
                if label == 4:
                    A4[i][j] = A[i][j]



        mlab.barchart(A1)
        # mlab.barchart(A2)
        # mlab.barchart(A3)
        mlab.barchart(A4)
        s = mlab.gcf()
        s.scene.background = (1, 1, 1)
        source = s.children[0]
        colors = source.children[0]
        colors.scalar_lut_manager.lut_mode = "Blues"
        colors = s.children[1].children[0]
        colors.scalar_lut_manager.lut_mode = "OrRd"
        # colors = s.children[2].children[0]
        # colors.scalar_lut_manager.lut_mode = "RdYlBu"
        # colors = s.children[3].children[0]
        # colors.scalar_lut_manager.lut_mode = "Wistia"

        mlab.points3d(0, 0, 0, mode='cube', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')
        mlab.points3d(A.shape[0]-1, A.shape[1]-1, 0, mode='cube', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')

        plan_path_Hybrid1 = "../data/plan_path_Hybrid_temp" + str(num) + ".npy"
        # plan_path_Hybrid1 = "plan_path_PP_temp" + str(num) + ".npy"
        plan_path_Hybrid = np.load(file=plan_path_Hybrid1)
        # print("综合规划路径数组类型输出：",plan_path_Hybrid.shape)
        # print("输出Hybird路径：\n")
        print(plan_path_Hybrid)
        # print("x=0时：")
        # print(plan_path_Hybrid[0])
        # print("测试...取第一维高度：")
        # print(plan_path_Hybrid[:,0])
        x1 = plan_path_Hybrid[:, 1]
        x1 = np.insert(x1, 0, 0)
        x1 = np.append(x1, A.shape[0]-1)
        y1 = plan_path_Hybrid[:, 2]
        y1 = np.insert(y1, 0, 0)
        y1 = np.append(y1, A.shape[1]-1)
        z1 = plan_path_Hybrid[:, 0] + 0.5
        z1 = np.insert(z1, 0, 0)
        z1 = np.append(z1, 0)

        # camera状态改变可视化过程
        camera_path = "../data/plan_path_Hybrid_temp" + str(num) + ".npy"
        # camera_path = "plan_path_PP_temp" + str(num) + ".npy"
        camera_path = np.load(file=camera_path)

        # print("测试...取摄像机开关状态：")
        c = plan_path_Hybrid[:, 3]
        print(c)
        # print(len(c))
        # print(c[0])
        cc = []  # cc表示改变摄像机状态的点的位置集合
        for i in range(1, len(c)):
            if c[i] != c[i - 1]:
                # print(i-1,c[i-1])
                cc.append(i - 1)
        # print("改变摄像机状态的点的位置集合：",cc)
        ccc = []
        n = 2
        for i in range(0, len(cc), n):
            # print(cc[i:i + n])
            ccc.append(cc[i:i + n])
        print("将状态的位置集合拆分成两两的线段：",ccc)
        # print("改变camera状态的线段的条数：",len(ccc))
        # print("####",np.shape(ccc)[0])

        # mlab.plot3d(x, y, z, color=(0.23, 0.6, 1), colormap='Spectral')
        mlab.plot3d(x1, y1, z1, color=(0, 0, 1), opacity=1, tube_radius=None, colormap='Spectral', line_width = 5)
        mlab.plot3d(x, y, z, color=(0, 0, 0), opacity=1, tube_radius=None, colormap='Spectral', line_width = 5)

        for i in range(np.shape(ccc)[0]):
            c1 = plan_path_Hybrid[ccc[i][0]:(ccc[i][1] + 1), 0:3]
            # print("******",c1)
            np.savetxt("c" + str(i) + ".txt", c1, fmt='%d', delimiter=' ')
            camera_path_1 = np.loadtxt("c" + str(i) + ".txt", delimiter=' ', dtype=int)
            # print("@@@@@@@@@",camera_path_1)
            X = camera_path_1[:, 1]
            Y = camera_path_1[:, 2]
            Z = camera_path_1[:, 0] + 0.5
            for i in range(np.shape(ccc)[0]):
                mlab.plot3d(X, Y, Z, color=(0, 1, 0), opacity=1, tube_radius=None, colormap='Spectral', line_width = 5)

        a = plan_path_Hybrid[num][0]
        b = plan_path_Hybrid[num][1]
        c = plan_path_Hybrid[num][2]
        # print(c, a, b)
        mlab.points3d(b, c, a + 0.5, mode='sphere', color=(1, 1, 0), scale_mode='none', scale_factor='0.5')
        mlab.show()
        #
        # mlab.savefig(os.getcwd() + '/pic/' + str(num)+'.jpg', size = (1920,1080), figure=mlab.gcf(), magnification=2)
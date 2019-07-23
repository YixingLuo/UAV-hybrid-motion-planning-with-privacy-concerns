import xlrd
import math
import xlwt
from convertion import millerToXY
from xlutils.copy import copy
import numpy as np

maplabel=np.loadtxt('maplabel.txt',delimiter=' ',dtype=int)

def extract(inpath):
    data = xlrd.open_workbook(inpath, encoding_override='utf-8')
    table = data.sheets()[0]  # 选定表
    nrows = table.nrows  # 获取行号
    ncols = table.ncols  # 获取列号
    point = np.zeros([331, 4],dtype=int)
    '''
    newbook = copy(data)
    newsheet = newbook.get_sheet(0)
    # 在末尾增加新行
    str = 'point'
    newsheet.write(ncols, 0, str)
    #newbook.save(inpath)
    '''
    count=0
    for i in range(1, nrows):  # 第0行为表头
        alldata = table.row_values(i)  # 循环输出excel表中每一行，即所有数据
        lon = alldata[3]  # 取出表中第4列数据
        lat = alldata[2]  # 取出表中第3列数据
        # print(alldata[1])
        y =round(alldata[1])
        privacy_type = alldata[4]
        xz = []
        xz = millerToXY(lon, lat)

        #print(result1,result2)
        '''
        math.ceil(f)  # 向上取整
        math.floor(f)  # 向下取整
        round(f)  # 四舍五入'''

        x = round(abs(xz[0][1]-g1xy[1])/LONG_y)
        z = round(abs(xz[0][0]-g1xy[0])/LAT_x)

        if i == 1:
            print(xz, lon, lat, x, z)

        x_1 = round(abs(lon - g1[1]) / LONG)
        z_1 = round(abs(lat - g1[0]) / LAT)

        #point=[x,z,y]
        # if x != x_1 or z != z_1:
        #     print("ssss",  x,z,x_1,z_1)
        # if alldata[2] == 12:
        #     print("aaaa", x, z, x_1, z_1, maplabel[z][x])

        point[i-1]=[x,z,y,privacy_type]
        #print(type(point[2]))


        #alldata[5]=point
        #print(alldata[5])
        count+=1
        #newsheet.write(ncols,5)
       # newbook.save(inpath)
    print(count)
    #print(type(point))
    #print(point)
    return point



# g1=[45.5348,-122.6940]
# g2=[45.5348,-122.6876]
# g3=[45.5302,-122.6940]
# g4=[45.5302,-122.6876]
#print(round(g1[0]-g3[0],4))

g1=[45.5193, -122.6536]
g1xy = [6301606, 6387010]
g2=[45.5193, -122.6455]
g2xy = [6301606, 6387912]
g3=[45.51506, -122.6536]
g3xy = [6302006, 6387010]
g4=[45.51506, -122.6455]
g4xy = [6302006, 6387912]

LAT=round(abs(g1[0]-g3[0])/50,6)

LONG=round(abs(g1[1]-g2[1])/50,6)
print(LAT,LONG)

# g1xy = [6300140, 6382510]
# g2xy = [6300140, 6383223]
# g3xy = [6300575, 6382510]
# g4xy = [6300575, 6383223]

LAT_x = round(abs(g1xy[0]-g3xy[0])/50,6)
LONG_y = round(abs(g1xy[1]-g2xy[1])/50,6)
print(LAT_x, LONG_y)


inpath = '2.xlsx'  # excel文件所在路径
point=extract(inpath)
print(point)
# print(point[116])

buildings = np.zeros((331, 5),dtype=int)

buildings[:, 0] = point[:, 0]
buildings[:, 1] = point[:, 1]
buildings[:, 2] = point[:, 2]
buildings[:, 3] = point[:, 3] #privacy_level

temp = []
for i in range(331):
    if maplabel[buildings[i][1]][buildings[i][0]] == 1:
        print(buildings[i][1], buildings[i][0])
    buildings[i][4] = maplabel[buildings[i][1]][buildings[i][0]]

np.savetxt("exc.txt",buildings,fmt='%d',delimiter=',')
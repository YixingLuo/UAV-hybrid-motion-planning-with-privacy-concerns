import os
import cv2
from pylab import *
from PIL import Image
array_of_img = [] # this if for store all of the image data
# this function is for read image,the input is directory name
map1=np.zeros((50,50),dtype=int)
#map2=np.zeros((50,50),dtype=int)
#print(map1)
def read_directory(directory_name):
    files= os.listdir(r"./"+directory_name)
    files.sort(key=lambda x: int(x.split('.')[0]))
    # this loop is for read each image in this foder,directory_name is the foder name with images.
    for filename in files:
        #print(filename) #just for test
        #img is used to store the image data
        #img = cv2.imread(directory_name + "/" + filename)
        img = Image.open(directory_name + "/" + filename).convert('1')
        img0=array(img)
        array_of_img.append(img0)
    return array_of_img

        #print(img)
    #print(array_of_img[2475:2478])
    #print(array_of_img[51])
def count(array_of_img):
    n=0
    num_of_obstacle = 0
    #print(array_of_img[1].shape)
    for i in range(50):
        for j in range(50):
            T = np.sum(array_of_img[n])
            F = array_of_img[n].shape[0]*array_of_img[n].shape[1] - T
            print(T,F)#白色和黑色的数量比较
            alpha = 1
            if F >= alpha * T:
            #if F>0:
                map1[i, j] = 1
                num_of_obstacle += 1
                #map2[i, j] = 2
            else:
                map1[i, j] = 0
                #map2[i, j] = 0

            n+=1
    print(num_of_obstacle)
    #print(map1)
    return map1
    #return map2

    #print(map[0,0])
    #print("\n")
'''
def Writedata(data):
    #filename = 'map1.txt'  #数据文件保存位置
    filename = 'map2.txt'  # 数据文件保存位置
    row = np.array(data).shape[0]   #获取行数n
    print(row)
    print(type(data))
    with open(filename,'w') as f: # 若filename不存在会自动创建，写之前会清空文件
        for i in range(0,row):
            f.write(str(data[i][0:]))
            f.write("\n")
'''
def Writedata(data):
    np.savetxt("map1.txt",data,fmt='%d',delimiter=' ')

array_of_img=read_directory("map")

map1=count(array_of_img)
#map2=count(array_of_img)
#print(map2)
Writedata(map1)
#Writedata(map2)

#print(shape(map1))
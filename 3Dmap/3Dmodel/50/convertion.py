import numpy
import math
# xy_coordinate = []
# 转换后的XY坐标集
def millerToXY (lon, lat):
    xy_coordinate = []
    L = 6381372*math.pi*2
    W = L
    H = L/2
    mill = 2.3
    x = lon*math.pi/180
    y = lat*math.pi/180
    y = 1.25*math.log(math.tan(0.25*math.pi+0.4*y))
    x = (W/2)+(W/(2*math.pi))*x
    y = (H/2)-(H/(2*mill))*y
    xy_coordinate.append([round(y), round(x)])
    return xy_coordinate

g1=[45.5193, -122.6536]
g1xy = [6301606, 6387010]
g2=[45.5193, -122.6455]
g2xy = [6301606, 6387912]
g3=[45.51506, -122.6536]
g3xy = [6302006, 6387010]
g4=[45.51506, -122.6455]
g4xy = [6302006, 6387912]



g5 = [45.51537434, -122.65013474]

lon = g5[1]
lat = g5[0]
xy = millerToXY(lon,lat)

print(xy)
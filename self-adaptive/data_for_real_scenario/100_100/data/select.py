import numpy as np
import os

a=np.loadtxt('maplabel_privacy.txt')
occ_grid=np.reshape(a,(100,100))

x_list =[]
y_list = []

sum = 0
for i in range(100):
    sum  = 0
    for j in range(100):
        sum += a[i][j]
    if sum == 0:
        x_list.append(i)

for j in range(100):
    sum  = 0
    for i in range(100):
        sum += a[i][j]
    if j == 99:
        print(sum)
    if sum == 0:
        y_list.append(j)

print(x_list, y_list)

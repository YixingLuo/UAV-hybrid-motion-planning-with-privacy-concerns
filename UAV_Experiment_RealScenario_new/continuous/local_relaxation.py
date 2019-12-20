import numpy as np
from scipy.optimize import minimize
import math
start_point = [3, 4, 7]
end_point = [3, 10, 7]
time = 8
privacy_list = [[0, 6, 9],[0, 6, 8]]

def objective(x, privacy_list):
    x_list = []
    y_list = []
    z_list = []
    for i in range (time-1):
        x_list.append(x[i])
        y_list.append(x[time-1 + i])
        z_list.append(x[2*(time-1)+i])
    # print(privacy_list)
    privacy_threat = 0
    privacy_list = np.array(privacy_list)
    for i in range(privacy_list.shape[0]):
        for j in range (len(x_list)):
            distance = math.sqrt(math.pow(x_list[j]-privacy_list[i][0],2) + math.pow(y_list[j]-privacy_list[i][1],2) + math.pow(z_list[j]-privacy_list[i][2],2))
            privacy_threat += 1 - distance/4

    return privacy_threat


def constraint(a, b):
    distance = math.sqrt(math.pow(a[0]-b[0],2) + math.pow(a[1]-b[1],2) + math.pow(a[2]-b[2],2))
    return distance - math.sqrt(3)


# initial guesses
x0 = np.zeros(3 * (time-1))

# show initial objective
print('Initial SSE Objective: ' + str(objective(x0,privacy_list)))

# optimize
b = (0, 4)
bnds = []
for i in range (3 * (time-1)):
    bnds.append(b)
bnds = tuple(bnds)
# bnds = (b, b, b, b)
point_list = [start_point]
for i in range (time - 1):
    point_list.append([x0[i], x0[time - 1 + i], x0[2 * (time-1) + i]])
point_list.append(end_point)
# print(point_list)
point_list = np.array(point_list)
cons = []
for i in range (point_list.shape[0] - 1):
    # print(i)
    # print(point_list[i], point_list[i + 1])
    cons_temp = {'type': 'ineq', 'fun': constraint(point_list[i], point_list[i + 1])}
    cons.append(cons_temp)
# cons = tuple(cons)
print(cons)
solution = minimize(objective, x0, method='SLSQP', \
                    bounds=bnds, constraints=cons)
x = solution.x

# show final objective
# print('Final SSE Objective: ' + str(objective(x,privacy_list)))
print(x)
# print solution
# print('Solution')
# print('x1 = ' + str(x[0]))
# print('x2 = ' + str(x[1]))
# print('x3 = ' + str(x[2]))
# print('x4 = ' + str(x[3]))
import numpy

# affect_path=[[1,3], [4,5]]
# affect_path = [[1,4], [2,6]]
# affect_path = [[1,4], [2, 3]]
# affect_path = [[1,4], [1, 3]]
affect_path = [[1,4]]

left = affect_path[0][0]
right = affect_path[0][1]
affect_path_update = [[left, right]]

for item in range(1, len(affect_path)):
    left_now = affect_path[item][0]
    right_now = affect_path[item][1]
    if left_now <= affect_path_update[-1][1]:
        affect_path_update[-1][1] = max(affect_path_update[-1][1], right_now)
    else:
        affect_path_update.append([left_now, right_now])

print("affect_path_update",affect_path_update)
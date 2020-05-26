import numpy as np
import os


# reference_path = [[ 0,  0,  9,  1],
#  [ 1,  0,  9,  1],
#  [ 2,  0,  9,  1],
#  [ 3,  0,  9,  1],
#  [ 3,  1,  9,  1],
#  [ 3,  2,  9,  1],
#  [ 3,  3,  9,  1],
#  [ 3,  4,  9,  1],
#  [ 3,  5,  9,  1],
#  [ 3,  6,  9,  1],
#  [ 3,  7,  9,  1],
#  [ 3,  8,  9,  1],
#  [ 3,  9,  9,  1],
#  [ 3, 10,  9,  1],
#  [ 3, 11,  9,  1],
#  [ 3, 12,  9,  1],
#  [ 3, 13,  9,  1],
#  [ 3, 14,  9,  1],
#  [ 3, 15,  9,  1],
#  [ 3, 16,  9,  1],
#  [ 3, 17,  9,  1],
#  [ 3, 18,  9,  1],
#  [ 2, 18,  9,  1],
#  [ 1, 18,  9,  1],
#  [ 0, 18,  9,  1]]
#
# reference_path_name = os.getcwd() + "/data_raw/" + "reference_path" + ".npy"
# np.save(file=reference_path_name, arr=reference_path)
#
# reference_path = np.load('data_raw/reference_path.npy')
# print(reference_path)

occ_grid = np.zeros((10, 20, 20))


occ_grid_name = os.getcwd() + "/data_raw/" + "occ_grid" + ".npy"
np.save(file=occ_grid_name, arr=occ_grid)

occ_grid = np.load('data_raw/occ_grid.npy')
print(occ_grid)
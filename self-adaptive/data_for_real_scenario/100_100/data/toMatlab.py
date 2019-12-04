from scipy import io
import numpy as np

mat = np.load('occ_grid-100.npy')
# print(mat)
io.savemat('occ_grid-100.mat', mat)

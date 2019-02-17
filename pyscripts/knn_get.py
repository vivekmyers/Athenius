import sys
import numpy as np
import data_loader
from random import shuffle
from user_score import nearestNeighbors

args = np.array([float(x) for x in sys.argv[1:]])
nn = nearestNeighbors(np.ones([20]))
for i in nn:
    print(i)


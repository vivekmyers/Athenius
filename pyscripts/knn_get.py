import sys
import numpy as np
import data_loader
from random import shuffle
from user_score import nearestNeighbors

args = np.array([float(x) for x in sys.argv[1:]])
for i in nearestNeighbors(args):
    print(i[0][0])


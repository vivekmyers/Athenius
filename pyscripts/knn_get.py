import sys
import numpy as np
import data_loader
from random import shuffle
from user_score import nearestNeighbors

args = np.array([float(x) for x in sys.argv[1:]])
senate, house = nearestNeighbors(args)

for i in senate:
    print(i[0])

for i in house:
    print(i[0])


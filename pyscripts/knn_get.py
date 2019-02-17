import sys
import data_loader
from random import shuffle

arr, reps, bills = data_loader.senate_records(1)
shuffle(reps)

for i in reps[:3]:
    print(i[0])


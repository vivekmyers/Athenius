import sys
import data_loader

arr, reps, bills = data_loader.senate_records(1)

for i in reps[:3]:
    print(i)


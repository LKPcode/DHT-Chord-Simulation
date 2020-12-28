import matplotlib.pyplot as plt
import numpy as np
import statistics
from dht import DHT
from config import *
import math
from hash import *


def stabilize_and_fix_fingers(dht):
    dht.fix_all_fingers_of_all_nodes()
    dht.stabilize()
    dht.fix_all_fingers_of_all_nodes()
    dht.stabilize()


# Number of pionts on the plot
steps = 8
# Creates an array that defines the number of nodes in the simulation on every step
num_of_nodes_per_step = [2 ** (4 + step) for step in range(0, steps)]
print(num_of_nodes_per_step)

x = num_of_nodes_per_step
y = []
dy = 0

for amount in num_of_nodes_per_step:
    dht = DHT()
    # nodes is in config.py
    for i in range(0, amount):
        dht.join()

    stabilize_and_fix_fingers(dht)

    # insert real values here
    dht.insert_values(data, hashedData)

    allKeys = []
    for key in dht.nodeDict:
        allKeys.append(len(dht.nodeDict[key].hashTable))

    # y.append(statistics.median(dht.hopsOfFindSuccessor))
    y.append(sum(allKeys) / len(allKeys))

    print(y)
    print(math.log(amount, 2) / 2 + 0.02)

    del dht


plt.style.use('seaborn-whitegrid')


plt.plot(x, y)
plt.xlabel("Number of Nodes")
plt.ylabel("Average Num of keys in Node")
plt.title("Average Number of Keys per num of Nodes in the Network")

plt.show()

#
# print(f"\nMedian num of hops: {statistics.median(dht.hopsOfFindSuccessor)}")
# print(
#    f"\nAverage num of hops: {sum(dht.hopsOfFindSuccessor) / len(dht.hopsOfFindSuccessor)}")
#
# print(f"\nPerfect Average num of hops: {   math.log(nodes , 2) / 2  + 0.02 }")
#

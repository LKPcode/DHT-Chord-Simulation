import random
from config import *

# The node Structure


class Node:

    def __init__(self, id):
        self.hashTable = {}
        self.ID = id  # random.randint(0, 2 ** M)
        self.suc = None
        self.pre = None
        self.fingerTable = [None] * M

    def print_finger_table(self):
        i = 0
        for finger in self.fingerTable:
            print(f"{i} : {finger}")
            i += 1

    def __str__(self):
        return f"Node: ID: {self.ID} with successor {self.suc} and predecessor {self.pre} ."

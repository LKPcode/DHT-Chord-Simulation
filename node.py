import random
from config import *

# The node Structure


class Node:

    def __init__(self):
        self.hashTable = {}
        self.ID = random.randint(0, 2 ** M)
        self.suc = None
        self.pre = None
        self.fingerTable = [None] * M

    def __str__(self):
        return f"Node: ID: {self.ID} with successor {self.suc} and predecessor {self.pre} ."

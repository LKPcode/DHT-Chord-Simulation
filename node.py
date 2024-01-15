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

    def transfer_hash_table(self,table):
        for item in table.items():
            self.save_key_value_pair(item[0],item[1])

    def save_key_value_pair(self,key,value):
        # If key does not exist then create a empty list and append the first value
        if key not in self.hashTable:
            self.hashTable[key] = []
            self.hashTable[key].append(value)
        else:
            self.hashTable[key].append(value)

    def print_hash_table(self):
        print("Hash Table of node",self.ID)
        for key in self.hashTable:
            print(key, '->', self.hashTable[key])

    def __str__(self):
        return f"Node: ID: {self.ID} with successor {self.suc} and predecessor {self.pre} ."

    
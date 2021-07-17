import random
from node import Node
import config
from hash import *


# The Allmighty God that controls Everything

class DHT:

    def __init__(self):
        self.nodeDict = {}
        self.nodeNum = 0
        self.hopsOfFindSuccessor = []

    # Get a random id that does not already exist
    def get_random_id(self):
        id = hash_data(random.randint(0, 2 ** M))

        while True:
            if id in self.nodeDict:
                id = hash_data(random.randint(0, 2 ** M))
            else:
                break
        return id

    # Adds a new node in the network
    def join(self):
        # First check is the network is not full
        if self.nodeNum >= 2 ** M:
            print(
                "Cannot add another node in the network because it reached maximum capacity -> 2**M ")
            quit()
        newNode = Node(self.get_random_id())
        # print("Node Joined: ", newNode.ID)

        # Add the first node of the network
        if self.nodeNum == 0:
            self.nodeDict[newNode.ID] = newNode
            # print(f"Joined: {self.nodeDict[newNode.ID]}")

        # Add a second node in the network
        elif self.nodeNum == 1:
            # its actually not random because only one node is in the dict
            otherID = random.choice(list(self.nodeDict.keys()))
            # Update succsessor and predecessor of the other node
            self.nodeDict[otherID].pre = newNode.ID
            self.nodeDict[otherID].suc = newNode.ID
            self.nodeDict[otherID].fingerTable[0] = newNode.ID

            # Update succsessor and predecessor of the newNode
            newNode.suc = otherID
            newNode.fingerTable[0] = otherID
            newNode.pre = otherID
            self.nodeDict[newNode.ID] = newNode

            # print(f"Joined: {self.nodeDict[newNode.ID]}")

        # Add an node in the network if there are more than 2 already.
        else:
            # Ask a random node who is its successor
            randID = random.choice(list(self.nodeDict.keys()))
            sucNode = self.findSuccessor(self.nodeDict[randID], newNode.ID)
            # Initialize newNode's successor
            newNode.suc = sucNode.ID
            newNode.fingerTable[0] = sucNode.ID

            # self.nodeDict[sucNode.ID].pre = newNode.ID

            # Notify newNode's successor about its existance
            self.notify(newNode)
            # Add newNode to the network
            self.nodeDict[newNode.ID] = newNode

            # print(f"Joined: {self.nodeDict[newNode.ID]}")

            # Call stabilize so we dont have to do it manually

            self.stabilize()

        # Increment the number of nodes in the network by one
        self.nodeNum += 1

    def removeNodeAbruptly(self):
        randID = random.choice(list(self.nodeDict.keys()))
        self.nodeDict.pop(randID)

    def removeNodeSafely(self):
        # find a random node
        randID = random.choice(list(self.nodeDict.keys()))
        deletedNode = self.nodeDict[randID]
        # assign the successor of deleted node to the successor of the predecessor node of the deleted node
        self.nodeDict[deletedNode.pre].suc = deletedNode.suc
        self.nodeDict[deletedNode.pre].fingerTable[0] = deletedNode.suc

        # assign the predecessor of deleted node to the predecessor of the successor node of the deleted node
        self.nodeDict[deletedNode.suc].pre = deletedNode.pre

        self.nodeDict[deletedNode.suc].transfer_hash_table(
            deletedNode.hashTable)

        # and remove deleted node from nodes dictionary
        self.nodeDict.pop(randID)
        # self.fix_all_fingers_of_all_nodes()
        self.stabilize()

        self.nodeNum -= 1
        print("Deleted Node: ", randID)

    # Notifies a node's successor about its existance so that it can update its predecessor

    def notify(self, node):
        self.nodeDict[node.suc].pre = node.ID

    # Runs the stabilization algorithm for a specified node
    def stabilizeNode(self, node):
        if self.nodeDict[node.suc].pre != node.ID:
            node.suc = self.nodeDict[node.suc].pre
            self.nodeDict[node.suc].pre = node.ID

    # Stabilization for all the nodes in the network
    def stabilize(self):
        for item in self.nodeDict.items():
            self.stabilizeNode(item[1])

    # Finds the successor of any given key iteratively
    def findSuccessor(self, node, key, recordHops=False):
        # node.fingerTable[0] == node.suc
        currentNode = node
        hops = 0
        count = 0

        while True:
            # print("Find Successor")
            # if the key is in the range of the current node's predecessor and its own id then return its own id
            if currentNode.pre is not None and between(currentNode.pre, currentNode.ID, key):
                if count != 0:
                    hops += 1
                if recordHops == True:
                    self.hopsOfFindSuccessor.append(hops)
                return self.nodeDict[currentNode.ID]
            # elif currentNode.fingerTable[0] is not None and between(currentNode.ID, currentNode.suc , key):
            #     return self.nodeDict[currentNode.suc]
            else:  # Search the finger table
                for i in range(M-1, 0, -1):
                    try:
                        if currentNode.fingerTable[i] is not None and not between(currentNode.ID, currentNode.fingerTable[i], key):
                            currentNode = self.nodeDict[currentNode.fingerTable[i]]
                            hops += 1
                            break
                    except:
                        continue
                currentNode = self.nodeDict[currentNode.suc]
                # hops += 1
                count += 1

    def fix_finger(self, node, i):
        ith_finger = (node.ID + 2**i) % 2**M
        node.fingerTable[i] = self.findSuccessor(node, ith_finger).ID

    def fix_all_fingers_of_node(self, node):
        for i in range(0, M):
            self.fix_finger(node, i)

    def fix_all_fingers_of_all_nodes(self):
        for pair in self.nodeDict.items():
            for i in range(0, M):
                self.fix_finger(pair[1], i)

    def send_random_exact_match_queries(self, amount):
        for i in range(0, amount):
            randKey = random.randint(0, 2 ** M)
            randID = random.choice(list(self.nodeDict.keys()))
            self.findSuccessor(self.nodeDict[randID], randKey, True)

    # inserting values and keys into nodes
    def insert_key_value_pair(self, key, value):
        randNodeID = random.choice(list(self.nodeDict.keys()))
        targetNode = self.findSuccessor(self.nodeDict[randNodeID], key)
        targetNode.save_key_value_pair(key, value)
        return targetNode

    # inserting data and hashed data as value and key of the node
    def insert_values(self, value, hashedValue):
        for i, j in zip(hashedValue, value):
            self.insert_key_value_pair(i, j)

    # deleting key value pair using the key
    def delete_pair(self, key):
        randID = random.choice(list(self.nodeDict.keys()))
        node = self.findSuccessor(self.nodeDict[randID], key)
        if node.hashTable[key] is not None:
            node.hashTable.pop(key)
            return True
        return False

    # Print the network in human readable form

    def print(self):
        for item in self.nodeDict.items():
            print(item[1])

    def print_density(self):
        network = ["_"] * 2**M
        for id in self.nodeDict:
            network[id] = "#"
        print("".join(network))

    def search_ft(self, id):
        for node in self.nodeDict:
            for finger in self.nodeDict[node].fingerTable:
                if finger == id:
                    return "ID Found in a finger tables"
        return "Finger NOT Found in finger Tables"

    def search_ft_none(self):
        for node in self.nodeDict:
            for finger in self.nodeDict[node].fingerTable:
                if finger is None:
                    return "there is a none value in fingertables"
        return "no None value found in finger tables"


# The Great Enigma :)
def between(ID1, ID2, key):
    # ID1 is smaller value, #ID2 is larger value
    if ID1 == ID2:
        return True
    wrap = ID1 > ID2  # Boolean to see if wrapping occured.
    if not wrap:
        return True if key > ID1 and key <= ID2 else False
    else:
        return True if key > ID1 or key <= ID2 else False


dht = DHT()

# nodes is in config.py
for i in range(0, nodes):
    dht.join()

randID = random.choice(list(dht.nodeDict.keys()))

dht.fix_all_fingers_of_all_nodes()
# print(dht.nodeNum)
# dht.send_random_exact_match_queries(1000)

dht.insert_values(data, hashedData)
# dht.insert_key_value_pair(32,222).print_hash_table()


# allKeys list will gather every key from every node
allKeys = []
# key is the node actuzally
for key in dht.nodeDict:
    # print (len(dht.nodeDict[key].hashTable))
    allKeys.append(len(dht.nodeDict[key].hashTable))
print("the average keys per node is", sum(allKeys)/len(dht.nodeDict))
print("the perfect average is", len(hashedData)/nodes)
print(dht.nodeNum)
#     f"\nAverage num of hops: {sum(dht.hopsOfFindSuccessor) / len(dht.hopsOfFindSuccessor)}")
# print(hash_integer(2))

# for key in dht.nodeDict:
#     print ("node: ", key)
#     dht.nodeDict[key].print_hash_table()

# print (randID)
for i in range(0, 100):
    dht.removeNodeSafely()

dht.fix_all_fingers_of_all_nodes()

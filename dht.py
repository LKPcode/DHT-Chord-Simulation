import random
from node import Node
from config import *

# The Almighty God that controls Everything


class DHT:

    def __init__(self):
        self.nodeDict = {}
        self.nodeNum = 0
        self.hopsOfFindSuccessor = []

    # Get a random id that does not already exist
    def get_random_id(self):
        id = random.randint(0, 2 ** M)
        while True:
            if id in self.nodeDict:
                id = random.randint(0, 2 ** M)
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
        # Add the first node of the network
        if self.nodeNum == 0:
            self.nodeDict[newNode.ID] = newNode
            print(f"Joined: {self.nodeDict[newNode.ID]}")

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

            print(f"Joined: {self.nodeDict[newNode.ID]}")

        # Add an node in the network if there are more than 2 already.
        else:
            # Ask a random node who is its successor
            randID = random.choice(list(self.nodeDict.keys()))
            sucNode = self.findSuccessor(self.nodeDict[randID], newNode.ID)
            # Initialize newNode's successor
            newNode.suc = sucNode.ID
            newNode.fingerTable[0] = sucNode.ID

            #self.nodeDict[sucNode.ID].pre = newNode.ID

            # Notify newNode's successor about its existance
            self.notify(newNode)
            # Add newNode to the network
            self.nodeDict[newNode.ID] = newNode

            print(f"Joined: {self.nodeDict[newNode.ID]}")

            # Call stabilize so we dont have to do it manually
            self.stabilize()
            self.stabilize()

        # Increment the number of nodes in the network by one
        self.nodeNum += 1

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
        while True:
            #print("Find Successor")
            # if the key is in the range of the current node's predecessor and its own id then return its own id
            if currentNode.pre is not None and between(currentNode.pre, currentNode.ID, key):
                if recordHops == True:
                    self.hopsOfFindSuccessor.append(hops)

                return self.nodeDict[currentNode.ID]
            # If the key is between the current node and its successor then we return the successor as the node that holds that key
            elif currentNode.fingerTable[0] is not None and between(currentNode.ID, currentNode.suc, key):
                if recordHops == True:
                    self.hopsOfFindSuccessor.append(hops)

                return self.nodeDict[currentNode.suc]

            else:  # Search the finger table
                for i in range(M-1, 1, -1):
                    if currentNode.fingerTable[i] is not None and not between(currentNode.ID, currentNode.fingerTable[i], key):
                        currentNode = self.nodeDict[currentNode.fingerTable[i]]
                        hops += 1
                        continue

                # This might be stupid ( Maybe we should be returning the last node in the fingertable instead of the first one)
                currentNode = self.nodeDict[currentNode.suc]
                hops += 1

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

    # Print the network in human readable form

    def print(self):
        for item in self.nodeDict.items():
            print(item[1])

    def print_density(self):
        network = ["_"] * 2**M
        for id in self.nodeDict:
            network[id] = "#"
        print("".join(network))


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

for i in range(0, 1024):
    dht.join()


randID = random.choice(list(dht.nodeDict.keys()))

dht.fix_all_fingers_of_all_nodes()

dht.send_random_exact_match_queries(100000)

print(
    f"\nAverage num of hops: {sum(dht.hopsOfFindSuccessor) / len(dht.hopsOfFindSuccessor)}")

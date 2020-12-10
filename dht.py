import random
from node import Node
from config import *

# The Almighty God that controls Everything


class DHT:

    def __init__(self):
        self.nodeDict = {}
        self.nodeNum = 0

    # Adds a new node in the network
    def join(self):
        newNode = Node()
        # Add the first node of the network
        if self.nodeNum == 0:
            self.nodeDict[newNode.ID] = newNode
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

    # Finds the successor of any given key recursively
    def findSuccessor(self, node, key):

        # node.fingerTable[0] == node.suc

        # If the key is between this node and its successor then we return the successor as the node that holds that key
        if node.fingerTable[0] is not None and between(node.ID, node.suc, key):
            return self.nodeDict[node.suc]

        else:  # Search the finger table
            for i in range(1, M-1):
                if node.fingerTable[i] is not None and between(node.fingerTable[i-1], node.fingerTable[i], key):
                    return self.findSuccessor(self.nodeDict[node.fingerTable[i-1]], key)

            # This might be stupid ( Maybe we should be returning the last node in the fingertable and not the first one)
            return self.findSuccessor(self.nodeDict[node.fingerTable[0]], key)

    # Print the network in human readable form
    def print(self):
        for item in self.nodeDict.items():
            print(item[1])


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

dht.join()

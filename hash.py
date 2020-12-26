import hashlib
from config import *
import random


#just a function for md5 hashing 
def hash_data(element):
    result = hashlib.md5(str(element).encode())
    #digest as hex and append as decimal
    return int(result.hexdigest(),16)%2**M

#plain data
data = []
with open('airports.dat', 'r') as a:
    for line in a:
        data.append(line)

#list to store hashed data
hashedData = []

#hashing data [] and store in hashedData []
for line in data:
    hashedData.append(hash_data(line))
# for line in hashedData:
#     print (line)
# for i,j in zip (hashedData, data):
#     print (i,j)
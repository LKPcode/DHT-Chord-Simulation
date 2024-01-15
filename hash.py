import hashlib
from config import *
import random
import csv
import csv


#just a function for md5 hashing 
def hash_data(element):
    result = hashlib.md5(str(element).encode())
    #digest as hex and append as decimal
    return int(result.hexdigest(),16)%2**M




# for line in hashedData:
#     print (line)
# for i,j in zip (hashedData, data):
#     print (i,j)
def read_csv_file(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_list.append(row)
    return data_list

data = read_csv_file('merged_file.txt')


#list to store hashed data
hashedData = []
#hashing data [] and store in hashedData []
for column in data:
    # print(column["university"])
    hashedData.append(hash_data(column["university"]))
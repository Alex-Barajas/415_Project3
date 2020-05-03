# CS415 Spring 2020
# Alex Barajas | Alondra Lona
import glob
import os
import math
import time

class basicOp:
    def __init__(self):
        self.dict = {}

    def operations(self, name):
        if name not in self.dict:
            self.dict[name] = [1]
        temp = self.dict[name]
        temp += 1
        self.dict[name] = temp

    def tasktotal(self, name):
        if name not in self.dict:
            print("doesn't exist bro")
            return
        return self.dict[name]



def task1a(c, v, w):
    t0 = time.time()
    table = [[0] * (c + 1) for i in range(len(v) + 1)]
    opt_subset = []
    # padding
    v.insert(0, 0)
    w.insert(0, 0)

    size = len(v)
    for i in range(1, size):
        for j in range(1, c + 1):
            if j - w[i] >= 0:
                table[i][j] = max(table[i - 1][j], v[i] + table[i - 1][j - w[i]])
            else:
                table[i][j] = table[i - 1][j]

    print("Traditional Dynamic Programming Optimal value: ", table[size - 1][c])  # size - 1 because the padding
    i = len(v) - 1
    j = c
    start = table[i][j]
    while j > 0 and i > 0:
        other = table[i - 1][j]
        if start > other:
            opt_subset.append(i)
            j -= w[i]
            start = table[i - 1][j]
        else:
            start = table[i - 1][j]
            i -= 1
    t1 = time.time()
    print("Traditional Dynamic Programming Time Taken: ", t1 - t0)
    print("Traditional Dynamic Programming Optimal subset: ", opt_subset[::-1])


# Hash Table Implementation
class HashTable:
    def __init__(self, k):
        self.hash_table = [{} for _ in range(k)]
        self.k = k
        self.space = 0

    def insert(self, key, i, j, value):
        valueKey = (i, j)
        hash_key = int(key) % self.k
        hash_bucket = self.hash_table[hash_key]
        if valueKey not in hash_bucket:
            hash_bucket[valueKey] = value

    def print_hash_table(self):
        print(self.hash_table)

    def print(self, val):
        print(val)

    def search(self, key, i, j):
        hash_key = int(key) % self.k
        dict_key = (i, j)
        bucket = self.hash_table[hash_key]
        for k, v in bucket.items():
            if k == dict_key:
                return v
        return 0

    def size(self):
        total = 0
        for elem in self.hash_table:
            total += len(elem)
            if len(elem) == 0: # we still include 1 because the hash table saved a spot
                total += 1
        return total



def binFormat(c, v, i, j):
    bn = math.ceil(math.log2(len(v) + 1))
    bw = math.ceil(math.log2(c + 1))
    ri = format(i, "0%sb" % bn)
    rj = format(j, "0%sb" % bw)
    rij = '1' + ri + rj
    return rij


def task1b(c, v, w):
    t0 = time.time()
    k = math.floor((c * len(v)) * .45)
    a = HashTable(k)
    i = len(v) - 1
    j = c
    opt_subset = []

    def MFKnapsnack(i, j):
        rij = binFormat(c, v, i, j)
        g = a.search(rij, i, j)
        if i > 0 and j > 0:
            if j < w[i]:
                value = MFKnapsnack(i - 1, j)
            else:
                value = max(MFKnapsnack(i - 1, j), v[i] + MFKnapsnack(i - 1, j - w[i]))
            a.insert(rij, i, j, value)
        a.insert(rij, i, j, 0)
        return a.search(rij, i, j)

    print("Space-efficient Dynamic Programming Optimal value: ", MFKnapsnack(i, j))

    # back track
    start = a.search(binFormat(c, v, i, j), i, j)

    while j > 0 and i > 0:
        other = a.search(binFormat(c, v, i - 1, j), i - 1, j)
        if start > other:
            opt_subset.append(i)
            j -= w[i]
            start = a.search(binFormat(c, v, i - 1, j), i - 1, j)
        else:
            start = a.search(binFormat(c, v, i - 1, j), i - 1, j)
            i -= 1
    t1 = time.time()
    print("Space-efficient Dynamic Programming Time Taken: ", t1 - t0)
    print("Space-efficient Dynamic Programming Optimal subset: ", opt_subset[::-1])
    print("Space-efficient Dynamic Programming Space Taken: ", a.size())



#TASK 2-A g Greedy Approach using Quick-Sort
def knap_greedy(cap, weight, values, knap_sack):

    total_weight = 0
    total_value = 0
    for i in range(len(values)):
        if (total_weight + weight[i]) <= cap[0]:
           # i += 1
            total_value += values[i]
            total_weight += weight[i]
            knap_sack.append(values[i]) #i append but i dont think i am doing anything with this

    return total_value

def partition(values, weights, low, high):
    i = low - 1 # index of small element

    pivot = values[high]/weights[high]

    for j in range(low, high):

        #basic_operations+=1 would go here

        # If current element is smaller than the pivot
        if pivot >= values[j]/weights[j]:
            i += 1 #increment indx of smaller element
            #swap weights
            weights_temp = weights[i]
            weights[j] = weights[i]
            weights[j] = weights_temp

            #swap values
            values_temp = values[i]
            values[j] = values[i]
            values[j] = values_temp

        weights_temp = weights[i+1]
        weights[i+1] = values[high]
        weights[high] = weights_temp


        values_temp = values[i+1]
        values[i+1] = values[high]
        values[high] = values_temp

        return(i + 1)

def quickSort(values, weights, low, high):
    if low < high :
        part= partition(values, weights, low, high)
        quickSort(values, weights,  low, part-1)
        quickSort(values, weights, part + 1, high)


def main():
    x = input("Enter range of files you want to be read: ").split(',')
    for i in range(int(x[0]), int(x[1])+1):
        filec = []
        filev = []
        filew = []
        if i < 9:
            for j in ['c', 'v', 'w']:
                cwd = os.getcwd()
                filestring = cwd + '/KnapsackTestData/p0%s_' % i + j + '.txt'  # change directory
                file = open(filestring, 'r')
                if j == 'c':
                    filec = file.readlines()
                    filec = [x.strip() for x in filec]  # removes chars we dont want
                    filec = list(map(int, filec))  # maps the strings to ints
                    # print(filec)
                if j == 'v':
                    filev = file.readlines()
                    filev = [x.strip() for x in filev]
                    filev = list(map(int, filev))
                    # print(filev)
                if j == 'w':
                    filew = file.readlines()
                    filew = [x.strip() for x in filew]
                    filew = list(map(int, filew))
        else:
            for j in ['c', 'v', 'w']:
                cwd = os.getcwd()
                filestring = cwd + '/KnapsackTestData/p%s_' % i + j + '.txt'  # change directory
                file = open(filestring, 'r')
                if j == 'c':
                    filec = file.readlines()
                    filec = [x.strip() for x in filec]  # removes chars we dont want
                    filec = list(map(int, filec))  # maps the strings to ints
                    # print(filec)
                if j == 'v':
                    filev = file.readlines()
                    filev = [x.strip() for x in filev]
                    filev = list(map(int, filev))
                    # print(filev)
                if j == 'w':
                    filew = file.readlines()
                    filew = [x.strip() for x in filew]
                    filew = list(map(int, filew))
                
        report = basicOp()
        #### our code here #####
        # print('Task1a')
        print('----------------------')
        print("Knapsack capacity = ", filec[0], " -- Total number of items = ", len(filev))
        print()
        task1a(filec[0], filev, filew)
        print()
        # print('Task1b')
        task1b(filec[0], filev, filew)


        filev.pop(0)
        filew.pop(0)
        #2A Greedy using sort
        greedy_optimal_set = []
        greedy_optimal_values = []
        len_values = len(filev)


        quickSort(filev, filew, 0, len_values-1)
        greedy_result = knap_greedy(filec, filew, filev, greedy_optimal_values)

        print("\nGreedy Approach Optimal value:", greedy_result)
       #print("Greedy Approach Optimal subset:", greedy_optimal_values)
        #print("Greedy Approach Number of Operations:", greedy_operations)


main()














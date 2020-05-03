# CS415 Spring 2020
# Alex Barajas | Alondra Lona
import glob
import os
import math
import time


class basicOp:
    def __init__(self):
        self.dict = {}
        self.basic_operations_greedy = 0
        self.basic_operations_heap = 0

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
    #def addCount(self):

    def getOperationsHeap(self):
        return self.basic_operations_heap
    def getOperationSort(self):
        return self.basic_operations_greedy

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



#TASK 2-A g Greedy Approach
def knap_greedy(cap, weight, values, knap_sack):

    total_w = 0
    total_v = 0
    for i in range(len(values)):
        if (total_w + weight[i]) >= cap:
            break
        else:
            total_v += values[i]
            total_w += weight[i]
            knap_sack.append(values[i]) #i append values
    return total_v

def partition(values, weights, low, high,operations):
    i = (low-1) # index of small element

    pivot = (values[high])/(weights[high])
    for j in range(low, high):

        #basic_operations
        operations.basic_operations_greedy += 1


        # If current element is greater than the pivot
        if values[j]/weights[j] > pivot:
            i = i + 1 #increment indx of smaller element

            #swap weights
            weights_temp = weights[i]
            weights[i] = weights[j]
            weights[j] = weights_temp

            #swap values
            values_temp = values[i]
            values[i] = values[j]
            values[j] = values_temp

    weights_temp = weights[i+1]
    weights[i+1] = weights[high]
    weights[high] = weights_temp

    values_temp = values[i+1]
    values[i+1] = values[high]
    values[high] = values_temp

    return i + 1

def quickSort(values, weights, low, high, operations):
    if low < high:
        # create partition
        #basic ops
        operations.basic_operations_greedy += 1

        #print(operations.basic_operations_greedy)

        part = partition(values, weights, low, high, operations)
        quickSort( values, weights,  low, part-1, operations)
        quickSort(values, weights, part + 1, high, operations)


# TASK 2B
def heap_build(values, weights, n, i, operations):
    largest = i # intialize as root

    left_child = 2 * i + 1
    right_child = 2 * i + 2
    # of basic ops
    operations.basic_operations_heap += 1
    # if left child of root exists and is greater than root
    if left_child < n and (values[i]/weights[i] > values[left_child]/weights[left_child]):
        largest = left_child

    # if right child of root exists and is greater than root
    if right_child < n and (values[largest]/weights[largest] > values[right_child]/weights[right_child]):
        largest = right_child

    # change root if need 2
    if largest != i:
        swap = values[i]
        values[i] = values[largest]
        values[largest] = swap

        swap_w = weights[i]
        weights[i] = weights[largest]
        weights[largest] = swap_w

        #recursively heapify
        heap_build(values, weights, n, largest, operations)

def deleteMax(weights, values, operations):
    # get last element
    operations.basic_operations_heap += 0
    total_v = len(values)
    last = total_v - 1 #values - 1 if i use index when i call

    weights_temp = weights[0]
    weights[0] = weights[last]
    weights[last] = weights_temp

    values_temp = values[0]
    values[0] = values[last]
    values[last] = values_temp

    #delete
    values.pop()
    weights.pop()

    #call total values again
    total_v = len(values)
    #heapify
    heap_sort(values, weights, total_v, operations)

def heap_sort(values, weights, total, operations):
    #build max heap
    operations.basic_operations_heap += 0
    for i in range(total, -1, -1):
        heap_build(values, weights, total, i, operations)

    for i in range(total-1, 0, -1):
        #swap values and weights
        swap_v = values[i]
        values[i] = values[0]
        values[0] = swap_v

        swap_w = weights[i]
        weights[i] = weights[0]
        weights[0] = swap_w

        #build
        heap_build(values, weights, i, 0, operations)


def greedy_heap(weights, values, cap, heap_sack, operations):
    # calculates total values
    operations.basic_operations_greedy += 0 # this will just add 0 since we need it to pass operations
    total_value = 0
    total_weight = 0
    for i in range(len(values)):
        if (total_weight + weights[0]) >= cap:
            break
        else:
            total_weight += weights[0]
            total_value += values[0]
            heap_sack.append(values[0])
        deleteMax(weights, values, operations)

    return total_value

  
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
        print()

        filev.pop(0)
        filew.pop(0)

        # copies for heaping
        heap_v2 = []
        heap_v2.extend(filev)
        heap_w = []
        heap_w.extend(filew)
        unSorted = []
        unSorted.extend(filev)

        #2A Greedy using quicKsort

        greedy_optimal_values = []
        len_values = len(filev)

        # create instance
        operations_greedy = basicOp()
        # sort the values
        quickSort(filev, filew, 0, len_values-1, operations_greedy)
        greedy_result = knap_greedy(filec[0], filew, filev, greedy_optimal_values)

        num = operations_greedy.getOperationSort() # get total number of operations

        print("Greedy Approach Optimal value:", greedy_result)
        greedy_set = []
        for w in range(len(greedy_optimal_values)):
            for g in range(len(unSorted)):
                if (greedy_optimal_values[w] == unSorted[g]):
                    greedy_set.append(g + 1)
        greedy_set.sort()
        print("Greedy Approach Optimal subset:", greedy_set)
        print("Greedy Approach Number of Operations:", num)
        print()

        # TASK 2B Using Heap Based

        operations_heap = basicOp() # create instance of class
        heap_result = []
        heap_optimal_value = []
        heap_sort(heap_v2, heap_w, len_values, operations_heap)
        heap_result = greedy_heap(heap_w, heap_v2, filec[0], heap_optimal_value, operations_heap)
        num2 = operations_heap.getOperationsHeap() # call getOper to get total num of operations


        print("Heap-based Greedy Approach Optimal values:", heap_result)
        heap_set = []
        for x in range(len(heap_optimal_value)):
            for v in range(len(unSorted)):
                if (heap_optimal_value[x] == unSorted[v]):
                    heap_set.append(v + 1)
        heap_set.sort()
        print("Heap-based Greedy Approach Optimal subset:", heap_set)
        print("Heap-based Greedy Approach Number of Operations: ", num2)



main()














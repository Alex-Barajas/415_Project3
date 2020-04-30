# CS415 Spring 2020
# Alex Barajas | Alondra Lona
import glob
import os
import numpy


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
    print(" Project 3 415 :^)")
    for i in range(7,8):
        filec = []
        filev = []
        filew = []
        for j in ['c', 'v', 'w']:
            cwd = os.getcwd()
            filestring = cwd + '/KnapsackTestData/p0%s_' % i + j + '.txt' # change directory current working directory
            file = open(filestring, 'r')
            if j == 'c':
                filec = file.readlines() # reads
                filec = [x.strip() for x in filec] # strips characters of any special chars
                filec = list(map(int, filec)) # maps strings to integers
                print(filec)
            if j == 'v':
                filev = file.readlines()
                filev = [x.strip() for x in filev]
                filev = list(map(int, filev))
                print(filev)
            if j == 'w':
                filew = file.readlines()
                filew = [x.strip() for x in filew]
                filew = list(map(int, filew))
                print(filew)


    #2A Greedy using sort
    greedy_optimal_set = []
    greedy_optimal_values = []
    len_values = len(filev)


    quickSort(filev, filew, 0, len_values-1)
    greedy_result = knap_greedy(filec, filew, filev, greedy_optimal_values)

    print("Greedy Approach Optimal value:", greedy_result)
    #print("Greedy Approach Optimal subset:", greedy_optimal_values)
    #print("Greedy Approach Number of Operations:", greedy_operations)


main()














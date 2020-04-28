# CS415 Spring 2020
# Alex Barajas | Alondra Lona
import glob
import os
import numpy

def task1a(c, v, w):

    # initalize table with buffer
    # table = numpy.zeros(c, len(v))
    table = [[0] * (c+1) for i in range(len(v) + 1)]

    sizeofv= len(v)
    for i in range(1, sizeofv + 1):
        a = i
        for j in range(1, c + 1):
            if j - w[i - 1] >= 0:
                table[i][j] = max(table[i-1][j], v[i-1] + table[i-1][j - w[i-1]])
            else:
                table[i][j] = table[i - 1][j]
    return table[sizeofv][c]

def task1b():


def main():
    for i in range(1):
        filec = []
        filev = []
        filew = []
        for j in ['c', 'v', 'w']:
            cwd = os.getcwd()
            filestring = cwd + '/KnapsackTestData/p0%s_' % i + j + '.txt' # change directory
            file = open(filestring, 'r')
            if j == 'c':
                filec = file.readlines()
                filec = [x.strip() for x in filec]
                filec = list(map(int, filec))
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



        #### our code here #####
        print(task1a(filec[0], filev, filew))

main()

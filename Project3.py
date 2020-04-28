# CS415 Spring 2020
# Alex Barajas | Alondra Lona
import glob
import os


def main():
    print(" Project 3 415 :^)")
    for i in range(3):
        filec = []
        filev = []
        filew = []
        for j in ['c', 'v', 'w']:
            filestring = '/Users/tank/Desktop/415_Project3/KnapsackTestData/p0%s_' % i + j + '.txt' # change directory
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

main()

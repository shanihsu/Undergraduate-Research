import pandas as pd
import random
import numpy as np

def initial(): #random initial gene
    Gene = []
    for i in range(100):
        Gene.append(random.random())
    return Gene
    #print(Gene)

def findmachine(Gene,dm): #find random gene correspond to machine
    Mommac = []
    for i in range(100):
        machinenum = 0
        min = 0.0
        max = 1.0
        range1 = max/dm[i][0]
        max = min + range1
        while (not(Gene[i]>=min and Gene[i]<=max)) and max<=1 and machinenum<dm[i][0]:
            machinenum += 1
            min = max
            max += range1
        Mommac.append(dm[i][machinenum+1])
    return Mommac

def findMachineTime(Mommac, dt, dm):
    Momtime = []
    for i in range(100):
        Momtime.append(dt[i][dm[i].index(Mommac[i])])
    print(Momtime)
    return Momtime

if __name__ == '__main__':
    data = pd.read_excel('data.xlsx',sheet_name= [0,1,2,3])

    #create CANRUN_machine
    datamachine = []
    for i in range(100):
        datamachine.append(data[0].values[i][9].split("EQP"))
        datamachine[i][0] = len(datamachine[i])-1
    #print(datamachine)
    
    #create CANRUN_process time
    datatime = []
    for i in range(100):
        datatime.append(data[0].values[i][9].split("EQP"))
        datatime[i][0] = len(datatime[i])-1
    for i in range(100):
        for j in range(1, len(datatime[i])):
            datatime[i][j] = data[1].values[10*(int(datamachine[i][j])-1) + int(data[0].values[i][8][1])-1][2] * int(data[0].values[i][3])/25
    #print(datatime)

    gene = initial()
    mommac = findmachine(gene, datamachine)
    momtime = findMachineTime(mommac, datatime, datamachine)
    print(gene)
    print(mommac)
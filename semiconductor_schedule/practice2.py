import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt # import matplotlib相關套件

class machine(): #answer map
    def __init__(self): 
        self.start = []
        self.end = []
        self.assignjob = []

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

def findMachineTime(Mommac, dt, dm): #find random gene correspond to process time
    Momtime = []
    for i in range(100):
        Momtime.append(dt[i][dm[i].index(Mommac[i])])
    return Momtime

def createmap(Mommac, Data, Momtime): #find correspond machine from random genes ,find start time and end time in each machine, and add setup_time file and Tool file as condition
    Machine = []
    for i in range(10):
        Machine.append(machine())
    for i in range(100):
        if len(Machine[int(Mommac[i])-1].start) == 0:
            Machine[int(Mommac[i])-1].assignjob.append(i+1)
            Machine[int(Mommac[i])-1].start.append(Data[3].values[int(Mommac[i])-1][2])
            Machine[int(Mommac[i])-1].end.append(Momtime[i]+Machine[int(Mommac[i])-1].start[0])
        else:
            tmp = Machine[int(Mommac[i])-1].assignjob[-1]
            Machine[int(Mommac[i])-1].assignjob.append(i+1)
            Machine[int(Mommac[i])-1].start.append(Machine[int(Mommac[i])-1].end[-1] + Data[2].values[tmp-1][Machine[int(Mommac[i])-1].assignjob[-1]])
            Machine[int(Mommac[i])-1].end.append(Momtime[i]+Machine[int(Mommac[i])-1].start[-1])
    return Machine

# def orderjob(Machine): #order job from random gene to correspond machine by rules
#     for i in range(10):
#         for j in range(len(Machine[i].assignjob)):
#             if 

    
    

if __name__ == '__main__':
    data = pd.read_excel('data.xlsx',sheet_name= [0,1,2,3])

    #create CANRUN_machine
    datamachine = []
    for i in range(100):
        datamachine.append(data[0].values[i][9].split("EQP"))
        datamachine[i][0] = len(datamachine[i])-1
    
    #create CANRUN_process time
    datatime = []
    for i in range(100):
        datatime.append(data[0].values[i][9].split("EQP"))
        datatime[i][0] = len(datatime[i])-1
    for i in range(100):
        for j in range(1, len(datatime[i])):
            if int(data[0].values[i][8][1]) != 0:
                datatime[i][j] = data[1].values[10*(int(datamachine[i][j])-1) + int(data[0].values[i][8][1])-1][2] * int(data[0].values[i][3])/25
            else:
                datatime[i][j] = data[1].values[10*(int(datamachine[i][j])-1) + int(data[0].values[i][8][1])-1+10][2] * int(data[0].values[i][3])/25

    gene = initial()
    mommac = findmachine(gene, datamachine)
    momtime = findMachineTime(mommac, datatime, datamachine)
    Mach = createmap(mommac, data, momtime)
    for i in range(10):    
        print(Mach[i].assignjob)
        print(Mach[i].start)
        print(Mach[i].end)
    #print(gene)
    #print(mommac)

    #draw
    #draw barh
    for i in range(10):
        for j in range(len(Mach[i].assignjob)):
            plt.barh(i,Mach[i].end[j]-Mach[i].start[j],left=Mach[i].start[j])
            plt.text(Mach[i].start[j]+(Mach[i].end[j]-Mach[i].start[j])/4,i,'J%s'%(Mach[i].assignjob[j]),color="white")
    plt.yticks(np.arange(10),np.arange(1,11))
    plt.show()
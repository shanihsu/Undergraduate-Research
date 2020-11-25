import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt # import matplotlib相關套件

class machine(): #answer map
    def __init__(self): 
        self.start = []
        self.end = []
        self.assignjob = []
        self.urgent = []
    def __repr__(self):
        return repr((self.start, self.end, self.assignjob, self.urgent))

class jobdata: #some data in xlsx[0]
    def __init__(self, assignjob, urgent):
        self.assignjob = assignjob
        self.urgent = urgent
    def __repr__(self):
        return repr((self.assignjob, self.urgent))

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

def createmap(Mommac, Data, Momtime): #find 10 machine which correpond to random genes ,find start time and end time in each machine, and add setup_time file and Tool file as condition
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

def orderjob(Machine, Data, dt, dm): #order job from random gene to correspond machine by rules
    machtmp = []
    for i in range(10):
        machtmp.append(machine())
    #sort jobs in each machine by urgent
    for i in range(10):
        tmp = []
        for j in range(len(Machine[i].assignjob)):
            Machine[i].urgent.append(Data[0].values[Machine[i].assignjob[j]-1][7])
            tmp.append(jobdata(Machine[i].assignjob[j], Machine[i].urgent[j]))
        tmp = sorted(tmp, key=lambda jobdata: jobdata.urgent, reverse=True)
    #assign sorted result to map
        for j in range(len(Machine[i].assignjob)):
            if len(machtmp[i].start) == 0:
                machtmp[i].assignjob.append(tmp[j].assignjob)
                machtmp[i].start.append(Data[3].values[i][2])
                t = np.array(dm[tmp[j].assignjob-1])
                d = t.astype(int).tolist()
                machtmp[i].end.append(machtmp[i].start[0] + dt[tmp[j].assignjob-1][d.index(i+1)])
            else:
                temp = machtmp[i].assignjob[-1]
                machtmp[i].assignjob.append(tmp[j].assignjob)
                machtmp[i].start.append(machtmp[i].end[-1] + Data[2].values[temp-1][machtmp[i].assignjob[-1]])
                t = np.array(dm[tmp[j].assignjob-1])
                d = t.astype(int).tolist()
                machtmp[i].end.append(machtmp[i].start[-1] + dt[tmp[j].assignjob-1][d.index(i+1)])
    return machtmp            


    

    
    

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
    Mach = orderjob(Mach, data, datatime, datamachine)
    # for i in range(10):    
    #     print(Mach[i].assignjob)
    #     print(Mach[i].start)
    #     print(Mach[i].end)
    #print(gene)
    #print(mommac)

    #draw
    #draw barh
    color_barh = ['r','g','b','c','m','y','navy','coral', 'brown', 'orange']
    for i in range(10):
        for j in range(len(Mach[i].assignjob)): 
            plt.barh(i,Mach[i].end[j]-Mach[i].start[j],left=Mach[i].start[j], color = color_barh[int(data[0].values[Mach[i].assignjob[j]-1][8][1])])
            plt.text(Mach[i].start[j]+(Mach[i].end[j]-Mach[i].start[j])/4,i,'%s'%(Mach[i].assignjob[j]),color="white")
    plt.yticks(np.arange(10),np.arange(1,11))
    plt.show()
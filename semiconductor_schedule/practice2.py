import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt # import matplotlib相關套件


#mach100 = []

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

class selectdata: #data of 50 genemom and 50 geneson
    def __init__(self, genenum, time):
        self.genenum = genenum
        self.time = time
    def __repr__(self):
        return repr((self.genenum, self.time))

class answer:
    def __init__(self, genedata, mach, gene, geneson, sortgene, sortgeneson):
        self.genedata = genedata
        self.mach = mach
        self.gene = gene
        self.geneson = geneson
        self.sortgene = sortgene
        self.sortgeneson = sortgeneson
    def __repr__(self):
        return repr((self.genedata, self.mach, self.gene, self.geneson, self.sortgene, self.sortgeneson))

def initial(): #random initial gene
    Gene = [[0]*100 for i in range(50)]
    for i in range(50):
        for j in range(100):
            Gene[i][j] = random.random()
    return Gene
    
def findmachine(Gene,dm): #find random gene correspond to machine
    Mommac = [[0]*100 for i in range(50)]
    for i in range(50):
        for j in range(100):
            machinenum = 0
            min = 0.0
            max = 1.0
            range1 = max/dm[j][0]
            max = min + range1
            while (not(Gene[i][j]>=min and Gene[i][j]<=max)) and max<=1 and machinenum<dm[j][0]:
                machinenum += 1
                min = max
                max += range1
            Mommac[i][j] = dm[j][machinenum+1]
    return Mommac

def findMachineTime(Mommac, dt, dm): #find random gene correspond to process time
    Momtime = [[0]*100 for i in range(50)]
    for i in range(50):
        for j in range(100):
            Momtime[i][j] = dt[j][dm[j].index(Mommac[i][j])]
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

def randomorder(Sortgene, Machine, Data, k, dt, dm): #order gene from random sort number 0~1  
    machtmp = []
    for i in range(10):
        machtmp.append(machine())
    #sort jobs in each machine by sortgene
    for i in range(10):
        tmp = []
        erasetmp = []
        for j in range(len(Machine[i].assignjob)):
            erasetmp.append(0)
            Machine[i].urgent.append(Sortgene[k][Machine[i].assignjob[j]-1])# urgent here means sortgene
            tmp.append(jobdata(Machine[i].assignjob[j], Machine[i].urgent[j]))
        tmp = sorted(tmp, key=lambda jobdata: jobdata.urgent, reverse=True)
        if i == 0:
            print(tmp[0])
        #modify genes by arrival time
        for j in range(len(Machine[i].assignjob)):
            if int(Data[0].values[Machine[i].assignjob[j]-1][4]) == 999:
                tmp.append(jobdata(Machine[i].assignjob[j], Machine[i].urgent[j]))
                erasetmp[j] = -1
        #print(tmp)
        for j in range(len(Machine[i].assignjob)-1, -1, -1):
            if erasetmp[j] == -1:
                del tmp[j]
        if i == 0:
            print("a", tmp[0])
        #print(tmp)
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
    

def mating(mtnum, genemom): #mate gene and generate two sons once
    geneson = [[0]*100 for i in range(50)]
    for num in range(int(mtnum)):
        sonnum1 = num * 2
        sonnum2 = num * 2 + 1
        # random select gene
        rdgene = random.sample(range(0,49),2)
        rdgene.sort()
        #print(rdgene)
        # random select two point to mate
        rdpt = random.sample(range(0,99),2)
        rdpt.sort()
        #print(rdpt)
        #mating
        for i in range(rdpt[0]):
            geneson[sonnum1][i] = genemom[rdgene[0]][i]
            geneson[sonnum2][i] = genemom[rdgene[1]][i]
        for i in range(rdpt[0],rdpt[1]+1):
            geneson[sonnum1][i] = genemom[rdgene[1]][i]
            geneson[sonnum2][i] = genemom[rdgene[0]][i]
        for i in range(rdpt[1]+1,100):
            geneson[sonnum1][i] = genemom[rdgene[0]][i]
            geneson[sonnum2][i] = genemom[rdgene[1]][i]
    return geneson

def motation(geneson, mtonum, genemom): #motate gene and generate one son once 
    for num in range(int(mtonum), 50):
        #random select gene
        rdgene = random.randint(0,49)
        #random select two point to motate
        rdpt = random.sample(range(0,99),2)
        rdpt.sort()
        #motate
        for i in range(rdpt[0]):
            geneson[num][i] = genemom[rdgene][i]
        for i in range(rdpt[0],rdpt[1]+1):
            geneson[num][i] = random.random()
        for i in range(rdpt[1]+1,100):
            geneson[num][i] = genemom[rdgene][i]
    return geneson

def findtime(map): #find max time in 10 machine
    maptime = map[0].end[-1]
    for i in range(10):
        if len(map[i].end) != 0:
            if map[i].end[-1] > maptime:
                maptime = map[i].end[-1]
    return maptime        
    
def select(Genedata, Gene, Geneson, Sortgene, Sortgeneson): # select 50 gene as mom and return it
    #Genedata = sorted(Genedata, key=lambda selectdata: selectdata.time)
    newgene = [[0]*200 for i in range(50)]
    for i in range(10):
        if Genedata[i].genenum < 50:
            for j in range(100):
                newgene[i][j] = Gene[Genedata[i].genenum][j]
            for j in range(100, 200):
                newgene[i][j] = Sortgene[Genedata[i].genenum][j-100]
        elif Genedata[i].genenum >= 50:
            for j in range(100):
                newgene[i][j] = Geneson[Genedata[i].genenum-50][j]
            for j in range(100, 200):
                newgene[i][j] = Sortgeneson[Genedata[i].genenum-50][j-100]    
    for i in range(10,50):
        rd = random.randint(10,99)
        if Genedata[rd].genenum < 50:
            for j in range(100):
                newgene[i][j] = Gene[Genedata[rd].genenum][j]
            for j in range(100, 200):
                newgene[i][j] = Sortgene[Genedata[rd].genenum][j-100]
        elif Genedata[rd].genenum >= 50:
            for j in range(100):
                newgene[i][j] = Geneson[Genedata[rd].genenum-50][j]
            for j in range(100, 200):
                newgene[i][j] = Sortgeneson[Genedata[rd].genenum-50][j-100]
    return newgene
    
def geneAlgorithm(genedata, Gene, Geneson, datamachine, datatime, mate, motate, Sortgene, Sortgeneson):  
    genetmp = select(genedata, Gene, Geneson, Sortgene, Sortgeneson)
    for i in range(50):
        for j in range(100):
            gene[i][j] = genetmp[i][j]
        for j in range(100, 200):
            sortgene[i][j-100] = genetmp[i][j]
    matenum = 50 * mate / 2
    motatenum = 50 * motate
    sontmp = mating(matenum, gene)
    geneson = motation(sontmp, 50*mate, gene)
    sortsontmp = mating(matenum, sortgene) #sort gene
    sortgeneson = motation(sortsontmp, 50*mate, sortgene) #sotr gene

    mommac = findmachine(gene, datamachine)
    momtime = findMachineTime(mommac, datatime, datamachine)
    sonmac = findmachine(geneson, datamachine)
    sontime = findMachineTime(sonmac, datatime, datamachine)
    
    #global mach100
    mach100 = []
    genedata = []
    for i in range(50):
        Machtmp = createmap(mommac[i], data, momtime[i])
        Machtmp = randomorder(sortgene, Machtmp, data, i, datatime, datamachine)
        #Machtmp = orderjob(Machtmp, data, datatime, datamachine)
        genedata.append(selectdata(i, findtime(Machtmp)))
        mach100.append(Machtmp)
    for i in range(50):
        Machtmp = createmap(sonmac[i], data, sontime[i])
        Machtmp = randomorder(sortgeneson, Machtmp, data, i, datatime, datamachine)
        #Machtmp = orderjob(Machtmp, data, datatime, datamachine)
        genedata.append(selectdata(i+50, findtime(Machtmp)))
        mach100.append(Machtmp)
    genedata = sorted(genedata, key=lambda selectdata: selectdata.time)
    #print(genedata)
    return answer(genedata, mach100, gene, geneson, sortgene, sortgeneson)

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
    #define mate and motate
    mate = 0.8 #mate rate
    motate = 0.2 #motate rate
    runtime = 0 #execute time of geneAlgorithm

    #first time gene algorithm
    gene = initial() #select gene
    sortgene = initial() #sort gene
    matenum = 50 * mate / 2
    motatenum = 50 * motate
    sontmp = mating(matenum, gene) #select gene
    geneson = motation(sontmp, 50*mate, gene) #select gene
    sortsontmp = mating(matenum, sortgene) #sort gene
    sortgeneson = motation(sortsontmp, 50*mate, sortgene) #sotr gene

    mommac = findmachine(gene, datamachine)
    momtime = findMachineTime(mommac, datatime, datamachine)
    sonmac = findmachine(geneson, datamachine)
    sontime = findMachineTime(sonmac, datatime, datamachine)
    
    mach100 = []
    genedata = []
    for i in range(50):
        Machtmp = createmap(mommac[i], data, momtime[i])
        Machtmp = randomorder(sortgene, Machtmp, data, i, datatime, datamachine)
        #Machtmp = orderjob(Machtmp, data, datatime, datamachine)
        genedata.append(selectdata(i, findtime(Machtmp)))
        mach100.append(Machtmp)
    for i in range(50):
        Machtmp = createmap(sonmac[i], data, sontime[i])
        Machtmp = randomorder(sortgeneson, Machtmp, data, i, datatime, datamachine)
        #Machtmp = orderjob(Machtmp, data, datatime, datamachine)
        genedata.append(selectdata(i+50, findtime(Machtmp)))
        mach100.append(Machtmp)
    genedata = sorted(genedata, key=lambda selectdata: selectdata.time)
    #print(genedata)
    ans = geneAlgorithm(genedata, gene, geneson, datamachine, datatime,mate, motate, sortgene, sortgeneson)
    #print(ans.genedata)
    #select(genedata, gene, geneson)
    runtime += 1
    """
    for i in range(20):
        ans = geneAlgorithm(ans.genedata, ans.gene, ans.geneson, datamachine, datatime,mate, motate, ans.sortgene, ans.sortgeneson)
        runtime += 1
    for i in range(20):
        ans = geneAlgorithm(ans.genedata, ans.gene, ans.geneson, datamachine, datatime,0.7, 0.3, ans.sortgene, ans.sortgeneson)
        runtime += 1
    for i in range(20):
        ans = geneAlgorithm(ans.genedata, ans.gene, ans.geneson, datamachine, datatime,0.6, 0.4, ans.sortgene, ans.sortgeneson)
        runtime += 1
    """
    #print(ans)
    #print(mach100[0][0].assignjob)
    #print(ans.genedata[0].genenum)
    
    Mach = ans.mach[ans.genedata[0].genenum]
    
    print("answer")
    for i in range(10):
        print("machine",i+1)
        print(Mach[i].end[-1])
    print("runtime = ",runtime)
    #draw
    #draw barh
    color_barh = ['r','g','b','c','m','y','navy','coral', 'brown', 'orange']
    for i in range(10):
        for j in range(len(Mach[i].assignjob)): 
            if (data[0].values[Mach[i].assignjob[j]-1][4]*60) < Mach[i].end[j]:
                colorsave = 'black'
            else:
                colorsave = color_barh[int(data[0].values[Mach[i].assignjob[j]-1][8][1])]
            plt.barh(i,Mach[i].end[j]-Mach[i].start[j],left=Mach[i].start[j], color = colorsave)
            plt.text(Mach[i].start[j]+(Mach[i].end[j]-Mach[i].start[j])/4,i,'%s'%(Mach[i].assignjob[j]),color="white")
    plt.yticks(np.arange(10),np.arange(1,11))
    plt.show()
    
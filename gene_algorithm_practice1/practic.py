import matplotlib.pyplot as plt # import matplotlib相關套件
import random
import numpy as np
import time


job = [[80, -1, 60],
    [75, 86, 94],
    [25, -1, 96],
    [78, 95, 89],
    [45, 78, -1],
    [12, -1, 65],
    [55, 99, 87],
    [11, -1, 16],
    [-1, 16, 45],
    [43, 56, 21]]
	


class machine(): #answer map
    def __init__(self, start=0, end=0, assignjob=0): 
        self.start = start
        self.end = end
        self.assignjob = assignjob

class genedata():
    def __init__(self, time=0, genenum=0):
        self.time = time
        self.genenum = genenum

genemom = [[0]*10 for i in range(50)] #random number 0~1
geneson = [[0]*10 for i in range(50)] #number 0~1 from mating and motating
mommac = [[0]*10 for i in range(50)] #the machine number which corresponds to random number 0~1 in genemom
sonmac = [[0]*10 for i in range(50)] #the machine number which corresponds to random number 0~1 in geneson
data = [] #each gene will cost time
for i in range(100):
	data.append(genedata())
sortdata = [] #sort data
for i in range(100):
	sortdata.append(genedata())
ansmachine = []  #min time of 100 gene, save its all data
for i in range(3):
	a = []
	for j in range(10):
		a.append(machine())
	ansmachine.append(a)
anscount = [0]*3 #count how many job in each machine 
plotans = [] #save sortdata[0].time to plot

def initial(): #random initial 50 gene
    global genemom
    for i in range(50):
        for j in range(10):
            genemom[i][j] = random.random()
            #print(genemom[i][j])

def mating(num): #mate gene and generate two sons once
	global genemom
	global geneson
	sonnum1 = num * 2
	sonnum2 = num * 2 + 1
    # random select gene
	rdgene = random.sample(range(0,49),2)
	rdgene.sort()
	#print(rdgene)
	# random select two point to mate
	rdpt = random.sample(range(0,9),2)
	rdpt.sort()
	#print(rdpt)
	#mating
	for i in range(rdpt[0]):
		geneson[sonnum1][i] = genemom[rdgene[0]][i]
		geneson[sonnum2][i] = genemom[rdgene[1]][i]
	for i in range(rdpt[0],rdpt[1]+1):
		geneson[sonnum1][i] = genemom[rdgene[1]][i]
		geneson[sonnum2][i] = genemom[rdgene[0]][i]
	for i in range(rdpt[1]+1,10):
		geneson[sonnum1][i] = genemom[rdgene[0]][i]
		geneson[sonnum2][i] = genemom[rdgene[1]][i]

def motation(num): #motate gene and generate one son once 
	global genemom
	global geneson
	#random select gene
	rdgene = random.randint(0,9)
	#random select two point to motate
	rdpt = random.sample(range(0,9),2)
	rdpt.sort()
	#motate
	for i in range(rdpt[0]):
		geneson[num][i] = genemom[rdgene][i]
	for i in range(rdpt[0],rdpt[1]+1):
		geneson[num][i] = random.random()
	for i in range(rdpt[1]+1,10):
		geneson[num][i] = genemom[rdgene][i]

def findMachine(): #find correspond machine number of genemom and geneson's random number 
	global genemom
	global geneson
	global mommac
	global sonmac
	global job
	#find genemom
	for i in range(50):
		for j in range(10):
			x = genemom[i][j]
			num = j
			cando = 3
			machinenum = 0
			min = 0.0
			max = 1.0
			for k in range(3):
				if job[num][k] < 0:
					cando -= 1
			range1 = max / cando
			max = min + range1
			while job[num][machinenum] < 0:
				machinenum += 1
			while (not(x>=min and x<=max)) and max<=1 and machinenum<3:
				machinenum += 1
				while job[num][machinenum] < 0:
					machinenum += 1
				min = max
				max += range1
			mommac[i][j] = machinenum
    #find geneson
	for i in range(50):
		for j in range(10):
			x = geneson[i][j]
			num = j
			cando = 3
			machinenum = 0
			min = 0.0
			max = 1.0
			for k in range(3):
				if job[num][k] < 0:
					cando -= 1
			range1 = max / cando
			max = min + range1
			while job[num][machinenum] < 0:
				machinenum += 1
			while (not(x>=min and x<=max)) and max<=1 and machinenum<3:
				machinenum += 1
				while job[num][machinenum] < 0:
					machinenum += 1
				min = max
				max += range1
			sonmac[i][j] = machinenum

def findTime(num): #find each gene total time
	max = -1 #each gene cost time
	judge = 0 #if judge == 1, num >= 50
	#int (*maptmp)[10]; #copy mommac or sonmac
	tmp = []  #record each job in its corresponse machine data
	for i in range(3):
		a = []
		for j in range(10):
			a.append(machine())
		tmp.append(a)
	countmp = [0]*3 #count how many job in each machine
	#copy mommac or sonmac
	if num < 50:
		maptmp = mommac.copy()
	else:
		maptmp = sonmac.copy()
		num -= 50
		judge = 1
	#initial
	for i in range(3):
		countmp[i] = 0
		for j in range(10):
			tmp[i][j].start = 0
			tmp[i][j].end = 0
			tmp[i][j].assignjob = 0
	#calculate time of each machine cost
	for i in range(10):
		tmp[maptmp[num][i]][countmp[maptmp[num][i]]].assignjob = i+1
		if countmp[maptmp[num][i]] == 0:
			tmp[maptmp[num][i]][countmp[maptmp[num][i]]].end += job[i][maptmp[num][i]]
		else:
			tmp[maptmp[num][i]][countmp[maptmp[num][i]]].start = tmp[maptmp[num][i]][countmp[maptmp[num][i]]-1].end
			tmp[maptmp[num][i]][countmp[maptmp[num][i]]].end = tmp[maptmp[num][i]][countmp[maptmp[num][i]]].start + job[i][maptmp[num][i]]
		
		countmp[maptmp[num][i]] += 1
	#find max time which machine cost and it will be this gene total time
	for i in range(3):
		if countmp[i] > 0:
			if tmp[i][countmp[i]-1].end > max:
				max = tmp[i][countmp[i]-1].end
	#save the result
	if judge == 1:
		num += 50
	data[num].time = max
	data[num].genenum = num			

def sortGene(): #copy data and sort data
	#copy data to sortdata
	for i in range(100):
		sortdata[i].time = data[i].time
		sortdata[i].genenum = data[i].genenum
	#sort sortdata
	for i in range(99):
		for j in range(11,100):
			if sortdata[i].time > sortdata[j].time:
				tmp1 = sortdata[i].time
				tmp2 = sortdata[i].genenum
				sortdata[i].time = sortdata[j].time
				sortdata[i].genenum = sortdata[j].genenum
				sortdata[j].time = tmp1
				sortdata[j].genenum = tmp2

def answer(): #find the min answer which correspond to gene
	num = sortdata[0].genenum #the min gene
	countmp = [0]*3 #count how many job in each machine
	#copy mommac or sonmac
	if num < 50:
		maptmp = mommac.copy()
	else:
		maptmp = sonmac.copy()
		num -= 50
	#initial
	for i in range(3):
		anscount[i] = 0
		for j in range(10):
			ansmachine[i][j].start = 0
			ansmachine[i][j].end = 0
			ansmachine[i][j].assignjob = 0
	#calculate time of each machine cost and save to ansmachine and anscount
	for i in range(10):
		ansmachine[maptmp[num][i]][anscount[maptmp[num][i]]].assignjob = i+1
		if anscount[maptmp[num][i]] == 0:
			ansmachine[maptmp[num][i]][anscount[maptmp[num][i]]].end += job[i][maptmp[num][i]]
		else:
			ansmachine[maptmp[num][i]][anscount[maptmp[num][i]]].start = ansmachine[maptmp[num][i]][anscount[maptmp[num][i]]-1].end
			ansmachine[maptmp[num][i]][anscount[maptmp[num][i]]].end = ansmachine[maptmp[num][i]][anscount[maptmp[num][i]]].start + job[i][maptmp[num][i]]
		anscount[maptmp[num][i]] += 1

def select(): #select the better 50 genes from 100 genes to replace mother
	genemomtmp = [[0]*10 for i in range(50)] #save temp mom, and when it select completed, genemomtmp will be assign to genemom
	#select the better 10 gene and save to genemomtmp
	for i in range(10):
		for j in range(10):
			if sortdata[i].genenum < 50:
				genemomtmp[i][j] = genemom[sortdata[i].genenum][j]
			elif sortdata[i].genenum >= 50:
				genemomtmp[i][j] = geneson[sortdata[i].genenum-50][j]
	exist = [0]*100 #check gene whether selected or not,selected:1,not selected:0
	#initial
	for i in range(10):
		exist[i] = 1
	sn = (1+90)*90/2 #sum of denominator in rate
	#select remainder 40 genes
	for i in range(40):
		#circle plate select
		rdnum = random.random()
		rdcal = rdnum * sn #numerator
		levelsum = 0
		randnum = 0
		for k in range(90,0,-1):
			levelsum += k
			if levelsum >= rdcal:
				randnum = 101-k-1
				break
		#check whether selected or not
		while exist[randnum] == 1:
			rdnum = random.random()
			rdcal = rdnum*sn
			levelsum = 0
			randnum = 0
			for k in range(90,0,-1):
				levelsum += k
				if levelsum >= rdcal:
					randnum = 101-k-1
					break
		exist[randnum] = 1
		#copy selected data
		if sortdata[randnum].genenum < 50:
			for j in range(10):
				genemomtmp[i+10][j] = genemom[sortdata[randnum].genenum][j]
		elif sortdata[randnum].genenum >= 50:
			for j in range(10):
				genemomtmp[i+10][j] = geneson[sortdata[randnum].genenum-50][j]
	#copy completed genemomtmp to genemom
	for i in range(50):
		for j in range(10):
			genemom[i][j] = genemomtmp[i][j]

def printans(): #print answer
	plotans.append(sortdata[0].time)
	print("ans=",sortdata[0].time)

def geneAlgorithm(mate,motate, startcal): #completed gene algorithm and recursive
	judgefunc = 0
	matenum = 50 * mate / 2
	motatenum = 50 * motate
	select()
	for i in range(int(matenum)):
		mating(i)
	for i in range(int(50*mate),50):
		motation(i)
	findMachine()
	for i in range(100):
		findTime(i)
	sortGene()
	answer()
	printans()
	loopend = time.time()
	if (loopend - startcal) > 10:
		judgefunc = 1
	return judgefunc


def draw(): #draw picture
	plt.plot(plotans,color = 'b')
	plt.show()



if __name__ == '__main__':
	tStart = time.time()#計時開始
	judge = 0
	mate = 0.8 #mate rate
	motate = 0.2 #motate rate
	runtime = 0 #execute time of geneAlgorithm
	#first time gene algorithm
	initial()
	matenum = 50 * mate / 2
	motatenum = 50 * motate
	for i in range(int(matenum)):
		mating(i)
	for i in range(int(50*mate), 50):
		motation(i)
	findMachine()
	for i in range(100):
		findTime(i)
	sortGene()
	answer()
	printans()
	runtime += 1
	#recursive algoruthm
	for i in range(7):
		if plotans[-1] == 158:
			break
		geneAlgorithm(mate,motate, tStart)
		runtime += 1
		if i%3 == 0:
			mate -= 0.1
			motate += 0.1
	for i in range(100000):
		if plotans[-1] == 158:
			break
		judge = geneAlgorithm(mate, motate, tStart)
		runtime += 1
		mate = 0.2
		motate = 0.8
		if judge == 1:
			break
	"""
	while plotans[-1] != 158:
		mate = 0.5
		motate = 0.5
		geneAlgorithm(mate,motate)
		runtime += 1
	"""
	print ("runtime=",runtime)
	tEnd = time.time()
	print("it cost ", tEnd-tStart, "sec")
	
	#draw picture
	draw()
	#print final answer
	print("answer")
	for i in range(3):
		print("machine",i+1)
		for j in range(anscount[i]):
			print("job",ansmachine[i][j].assignjob,"\tST=",ansmachine[i][j].start,"\tCT=",ansmachine[i][j].end)
	#draw barh
	for i in range(3):
		for j in range(anscount[i]):
			plt.barh(i,ansmachine[i][j].end-ansmachine[i][j].start,left=ansmachine[i][j].start)
			plt.text(ansmachine[i][j].start+(ansmachine[i][j].end-ansmachine[i][j].start)/4,i,'Job%s'%(ansmachine[i][j].assignjob),color="white")
	plt.yticks(np.arange(3),np.arange(1,4))
	plt.show()
	
"""
for i in range(50):
    print(i,"",end = "")
    for j in range(10):
        print("%.6f" % (genemom[i][j]),"",end = "")
        #print("{:.2f}".format(genemom[i][j]),"",end = "")
    print("\n")
print("----------------------")
for i in range(50):
    print(i,"",end = "")
    for j in range(10):
        print("%.6f" % (geneson[i][j]),"",end = "")
        #print("{:.2f}".format(genemom[i][j]),"",end = "")
    print("\n")
#print(geneson)
print(mommac)
"""
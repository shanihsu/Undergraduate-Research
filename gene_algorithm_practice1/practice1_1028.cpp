#include <iostream>
#include <cstdlib>
#include <time.h>
#include <iomanip>
#include <vector>
#include <fstream>

using namespace std;

typedef struct machine{  //answer map
	int start;
	int end;
	int assignjob;
};

typedef struct genedata{
	int time;
	int genenum;
};


int job[10][3] = {
		{80, -1, 60},
		{75, 86, 94},
		{25, -1, 96},
		{78, 95, 89},
		{45, 78, -1},
		{12, -1, 65},
		{55, 99, 87},
		{11, -1, 16},
		{-1, 16, 45},
		{43, 56, 21}
};

float genemom[50][10]; //random number 0~1
float geneson[50][10]; //number 0~1 from mating and motating
int mommac[50][10];  //the machine number which corresponds to random number 0~1 in genemom
int sonmac[50][10];  //the machine number which corresponds to random number 0~1 in geneson
genedata data[100];  //each gene will cost time
genedata sortdata[100];  //sort data
machine ansmachine[3][10]; //min time of 100 gene, save its all data
int anscount[3]; // count how many job in each machine 
vector<int> plotans; //save sortdata[0].time to plot


void initial(){ // random initial 50 gene
	for(int i = 0; i < 50; ++i){
		for(int j = 0; j < 10; ++j){
			genemom[i][j] = ((double) rand() / (RAND_MAX + 1.0));
		}
	}
}

void mating(int num){  //mate gene and generate two sons once
	int sonnum1 = num * 2;
	int sonnum2 = num * 2 + 1;
	//random select gene
	int rdgene1 = rand() % 50; 
	int rdgene2 = rand() % 50;
	while(rdgene1 == rdgene2){
		rdgene2 = rand() % 50;
	}
	if(rdgene2 < rdgene1){
		int tmp = rdgene2;
		rdgene2 = rdgene1;
		rdgene1 = tmp;
	}
	//random select two point to mate
	int rdpt1 = rand() % 10; 
	int rdpt2 = rand() % 10;
	while(rdpt1 == rdpt2){
		rdpt2 = rand() % 10;
	}
	if(rdpt2 < rdpt1){
		int tmp = rdpt2;
		rdpt2 = rdpt1;
		rdpt1 = tmp;
	}
	//mating
	for(int i = 0; i < rdpt1; ++i){
		geneson[sonnum1][i] = genemom[rdgene1][i];
		geneson[sonnum2][i] = genemom[rdgene2][i];
	}
	for(int i = rdpt1; i <= rdpt2; ++i){
		geneson[sonnum1][i] = genemom[rdgene2][i];
		geneson[sonnum2][i] = genemom[rdgene1][i];
	}
	for(int i = rdpt2+1; i < 10; ++i){
		geneson[sonnum1][i] = genemom[rdgene1][i];
		geneson[sonnum2][i] = genemom[rdgene2][i];
	}
	//print
	/*cout << rdgene1+1 <<" "<<rdgene2+1<<" "<<rdpt1+1<<" "<<rdpt2+1<<endl;
	for(int i = 0; i < 10; ++i){
		cout << "\tJob"<< i+1;
	}
	cout << endl;
	for(int i = 0 ; i < sonnum2+1; ++i){
		cout << "son" << i+1 << "\t";
		for(int j = 0; j < 10; ++j){
			cout << setiosflags(ios::fixed) << setprecision(5) << geneson[i][j] << " ";
		}
		cout << endl; 
	}*/
}

void motation(int num){ //motate gene and generate one son once
	//random select gene
	int rdgene = rand() % 50;
	//random select two point to motate
	int rdpt1 = rand() % 10; 
	int rdpt2 = rand() % 10;
	while(rdpt1 == rdpt2){
		rdpt2 = rand() % 10;
	}
	if(rdpt2 < rdpt1){
		int tmp = rdpt2;
		rdpt2 = rdpt1;
		rdpt1 = tmp;
	}
	//motate
	for(int i = 0; i < rdpt1; ++i){
		geneson[num][i] = genemom[rdgene][i];
	}
	for(int i = rdpt1; i <= rdpt2; ++i){
		geneson[num][i] = ((double) rand() / (RAND_MAX + 1.0));
	}
	for(int i = rdpt2+1; i < 10; ++i){
		geneson[num][i] = genemom[rdgene][i];
	}
	//print
	/*cout << rdgene+1<<" "<<rdpt1+1<<" "<<rdpt2+1<<endl;
	for(int i = 0; i < 10; ++i){
		cout << "\tJob"<< i+1;
	}
	cout << endl;
	for(int i = 0 ; i < num+1; ++i){
		cout << "son" << i+1 << "\t";
		for(int j = 0; j < 10; ++j){
			cout << setiosflags(ios::fixed) << setprecision(5) << geneson[i][j] << " ";
		}
		cout << endl; 
	}*/
}

void findMachine(){ // find correspond machine number of genemom and geneson's random number 
	//find genemom 
	for(int i = 0; i < 50; ++i){
		for(int j = 0; j < 10; ++j){
			double x = genemom[i][j];
			int num = j;
			int cando = 3, machinenum = 0;
			double min = 0.0, max = 1.0;
			for(int k = 0; k < 3; ++k){
				if(job[num][k] < 0){
					cando--;
				}
			}
			double range = max / cando;
			max = min + range;
			while(job[num][machinenum] < 0){
					machinenum++;
			}
			while((!((x>=min)&&(x<=max))) && (max <= 1) && (machinenum < 3)){
				machinenum++;
				while(job[num][machinenum] < 0){
					machinenum++;
				}
				min = max;
				max += range;
			}
			mommac[i][j]= machinenum;
		}
	}
	//find geneson
	for(int i = 0; i < 50; ++i){
		for(int j = 0; j < 10; ++j){
			double x = geneson[i][j];
			int num = j;
			int cando = 3, machinenum = 0;
			double min = 0.0, max = 1.0;
			for(int k = 0; k < 3; ++k){
				if(job[num][k] < 0){
					cando--;
				}
			}
			double range = max / cando;
			max = min + range;
			while(job[num][machinenum] < 0){
					machinenum++;
			}
			while((!((x>=min)&&(x<=max))) && (max <= 1) && (machinenum < 3)){
				machinenum++;
				while(job[num][machinenum] < 0){
					machinenum++;
				}
				min = max;
				max += range;
			}
			sonmac[i][j]= machinenum;
		}
	}
} 

void findTime(int num){ // find each gene total time
	int max = -1;  //each gene cost time
	int judge = 0; //if judge == 1, num >= 50
	int (*maptmp)[10]; //copy mommac or sonmac
	machine tmp[3][10]; //record each job in its corresponse machine data
	int countmp[3]; //count how many job in each machine
	//copy mommac or sonmac
	if(num < 50){
		maptmp = mommac;
	}
	else{
		maptmp = sonmac;
		num -= 50;
		judge = 1;
	}
	//initial
	for(int i = 0; i < 3; ++i){
		countmp[i] = 0;
		for(int j = 0; j < 10; ++j){
			tmp[i][j].start = 0;
			tmp[i][j].end = 0;
			tmp[i][j].assignjob = 0;
		}
	}
	//calculate time of each machine cost
	for(int i = 0; i < 10; ++i){
		tmp[maptmp[num][i]][countmp[maptmp[num][i]]].assignjob = i+1;
		if(countmp[maptmp[num][i]] == 0){
			tmp[maptmp[num][i]][countmp[maptmp[num][i]]].end += job[i][maptmp[num][i]];
		}
		else{
			tmp[maptmp[num][i]][countmp[maptmp[num][i]]].start = tmp[maptmp[num][i]][countmp[maptmp[num][i]]-1].end;
			tmp[maptmp[num][i]][countmp[maptmp[num][i]]].end = tmp[maptmp[num][i]][countmp[maptmp[num][i]]].start + job[i][maptmp[num][i]];
		}
		countmp[maptmp[num][i]]++;
	}
	//find max time which machine cost and it will be this gene total time
	for(int i = 0; i < 3; ++i){
		if(countmp[i] > 0){
			if(tmp[i][countmp[i]-1].end > max){
				max = tmp[i][countmp[i]-1].end;
			}
		}
	}
	//save the result
	if(judge == 1){
		num += 50;
	}
	data[num].time = max;
	data[num].genenum = num;
}

void sortGene(){ //copy data and sort data
	//copy data to sortdata
	for(int i = 0; i < 100; ++i){
		sortdata[i].time = data[i].time;
		sortdata[i].genenum = data[i].genenum;
	}
	//sort sortdata
	for(int i = 0; i < 99; ++i){
		for(int j = i+1; j < 100;++j){
			if(sortdata[i].time > sortdata[j].time){
				int tmp1 = sortdata[i].time;
				int tmp2 = sortdata[i].genenum;
				sortdata[i].time = sortdata[j].time;
				sortdata[i].genenum = sortdata[j].genenum;
				sortdata[j].time = tmp1;
				sortdata[j].genenum = tmp2;
			}
		}
	}
}

void answer(){  //find the min answer which correspond to gene
	int num = sortdata[0].genenum; //the min gene
	int (*maptmp)[10]; //copy mommac or sonmac
	int countmp[3]; //count how many job in each machine
	//copy mommac or sonmac
	if(num < 50){
		maptmp = mommac;
	}
	else{
		maptmp = sonmac;
		num -= 50;
	}
	//initial
	for(int i = 0; i < 3; ++i){
		anscount[i] = 0;
		for(int j = 0; j < 10; ++j){
			ansmachine[i][j].start = 0;
			ansmachine[i][j].end = 0;
			ansmachine[i][j].assignjob = 0;
		}
	}
	//calculate time of each machine cost and save to ansmachine and anscount
	for(int i = 0; i < 10; ++i){
		ansmachine[maptmp[num][i]][anscount[maptmp[num][i]]].assignjob = i+1;
		if(anscount[maptmp[num][i]] == 0){
			ansmachine[maptmp[num][i]][anscount[maptmp[num][i]]].end += job[i][maptmp[num][i]];
		}
		else{
			ansmachine[maptmp[num][i]][anscount[maptmp[num][i]]].start = ansmachine[maptmp[num][i]][anscount[maptmp[num][i]]-1].end;
			ansmachine[maptmp[num][i]][anscount[maptmp[num][i]]].end = ansmachine[maptmp[num][i]][anscount[maptmp[num][i]]].start + job[i][maptmp[num][i]];
		}
		anscount[maptmp[num][i]]++;
	}	
}

void select(){  //select the better 50 genes from 100 genes to replace mother
	float genemomtmp[50][10];  //save temp mom, and when it select completed, genemomtmp will be assign to genemom
	//select the better 10 gene and save to genemomtmp
	for(int i = 0; i < 10;++i){
		for(int j = 0; j < 10; ++j){
			if(sortdata[i].genenum < 50){
				genemomtmp[i][j] = genemom[sortdata[i].genenum][j];
			}
			else if(sortdata[i].genenum >= 50){
				genemomtmp[i][j] = geneson[sortdata[i].genenum-50][j];
			}
		}
	}
	int exist[100]; //check gene whether selected or not,selected:1,not selected:0
	//initial
	for(int i = 0; i < 10; ++i){
		exist[i] = 1;
	}
	for(int i = 10; i < 100; ++i){
		exist[i] = 0;
	}
	int sn = (1+90)*90/2; //sum of ���Ž��L�k(����) 
	//select remainder 40 genes
	for(int i = 0; i < 40; ++i){
		//���Ž��L�k 
		float rdnum = ((double) rand() / (RAND_MAX + 1.0)); // random generate select number 0~1 
		int rdcal = rdnum * sn; //�ҨD
		int levelsum = 0; //���l
		int randnum = 0; //�ĴX�� 
		for(int k = 90; k > 0; --k){
			levelsum += k;
			if(levelsum >= rdcal){
				randnum = 101 - k - 1;
				break;
			}
		} 
		//check whether selected or not
		while(exist[randnum] == 1){
			rdnum = ((double) rand() / (RAND_MAX + 1.0)); // random generate select number 0~1 
			rdcal = rdnum * sn; //�ҨD
			levelsum = 0; //���l
			randnum = 0; //�ĴX�� 
			for(int k = 90; k > 0; --k){
				levelsum += k;
				if(levelsum >= rdcal){
					randnum = 101 - k - 1;
					break;
				}
			}
		}
		exist[randnum] = 1;
		//copy selected data
		if(sortdata[randnum].genenum < 50){
			for(int j = 0; j < 10; ++j){
				genemomtmp[i+10][j] = genemom[sortdata[randnum].genenum][j];
			}
		}
		else if(sortdata[randnum].genenum >= 50){
			for(int j = 0; j < 10; ++j){
				genemomtmp[i+10][j] = geneson[sortdata[randnum].genenum-50][j];
			}			
		}
	}
	//copy completed genemomtmp to genemom
	for(int i = 0; i < 50; ++i){
		for(int j = 0; j < 10; ++j){ 
			genemom[i][j] = genemomtmp[i][j];
		}
	}
}

void print(int matenum){
	//mom
	cout << "\t";
	for(int i = 0; i < 10; ++i){
		cout << "\tJob"<< i+1;
	}
	cout << "\t Object"<< endl;
	for(int i = 0 ; i < 50; ++i){
		cout << "Chromosome" << i+1 << "\t";
		for(int j = 0; j < 10; ++j){
			cout << setiosflags(ios::fixed) << setprecision(5) << genemom[i][j] << " ";
		}
		cout << " " << data[i].time;
		cout << endl; 
	}
	//son
	for(int i = 0; i < 10; ++i){
		cout << "\tJob"<< i+1;
	}
	cout << "\t Object"<< endl;
	for(int i = 0 ; i < matenum*2; ++i){
		cout << "son" << i+1 << "\t";
		for(int j = 0; j < 10; ++j){
			cout << setiosflags(ios::fixed) << setprecision(5) << geneson[i][j] << " ";
		}
		cout << " " << data[i+50].time;
		cout << endl; 
	}
	for(int i = matenum*2 ; i < 50; ++i){
		cout << "son" << i+1 << "\t";
		for(int j = 0; j < 10; ++j){
			cout << setiosflags(ios::fixed) << setprecision(5) << geneson[i][j] << " ";
		}
		cout << " " << data[i+50].time;
		cout << endl; 
	}
	//mommac
	/*cout << "map" <<endl;
	for(int i = 0 ; i < 50; ++i){
		cout << "mommac" << i+1 << "\t";
		for(int j = 0; j < 10; ++j){
			cout << mommac[i][j]+1 << " ";
		}
		cout << endl; 
	}
	//sonmac
	for(int i = 0 ; i < 50; ++i){
		cout << "sonmac" << i+1 << "\t";
		for(int j = 0; j < 10; ++j){
			cout <<  sonmac[i][j]+1 << " ";
		}
		cout << endl; 
	} */
}

void printans(){ // print answer
	//answer
	/*cout << "answer"<<endl;
	for(int i = 0; i < 3; ++i){
		cout <<"machine"<<i+1<<endl;
		for(int j = 0; j < anscount[i]; ++j){
			cout << "job"<<ansmachine[i][j].assignjob<<"\tST="<< ansmachine[i][j].start << "\tCT="<<ansmachine[i][j].end<<endl;
		}
		cout<<endl;
	}*/
	plotans.push_back(sortdata[0].time);
	cout <<"ans="<<sortdata[0].time<<endl;
}

int geneAlgorithm(float mate, float motate, double start){ //completed gene algorithm and recursive
	double loopend;
	int judge = 0; //if == 1, break
	int matenum = 50 * mate / 2;
	int motatenum = 50 * motate;
	select();
	for(int i = 0; i < matenum; ++i){
		mating(i);
	}
	for(int i = 50 * mate; i < 50;++i){
		motation(i);
	}
	findMachine();
	for(int i = 0; i < 100; ++i){
		findTime(i);
	}
	sortGene();
	answer();
	//print(matenum);
	printans();
	/*loopend = clock();
	if(((loopend - start) / CLOCKS_PER_SEC) > 60.0)
		judge = 1;*/ 
	return judge;
}


int main(){	
	double START,END;
    START = clock();
	srand(time(NULL));
	float mate = 0.8, motate = 0.2; //mate rate and motate rate
	//first time gene algorithm
	initial();
	int judge;
	int runtime = 0;
	int matenum = 50 * mate / 2;
	int motatenum = 50 * motate;
	for(int i = 0; i < matenum; ++i){
		mating(i);
	}
	for(int i = 50 * mate; i < 50;++i){
		motation(i);
	}
	findMachine();
	for(int i = 0; i < 100; ++i){
		findTime(i);
	}
	sortGene();
	answer();
	//print(matenum);
	printans();
	runtime++;
	//recursive algoruthm
	for(int i = 0; i < 7; ++i){
		if(plotans.back() == 158)
			break;
		geneAlgorithm(mate, motate, START);
		runtime++;
		if(i % 3 == 0){
			mate -= 0.1;
			motate += 0.1;
		}
	}
	for(int i = 0; i < 100000; ++i){
		if(plotans.back() == 158)
			break;
		judge = geneAlgorithm(mate, motate,START);
		runtime++;
		mate = 0.2;
		motate = 0.8;
		if(judge == 1){
			break;
		}
	}/*
	while(plotans.back() != 158){
		mate = 0.5;
		motate = 0.5;
		geneAlgorithm(mate,motate, START);
		runtime++;
	}*/
	cout << "runtime = "<<runtime <<endl;
	
	END = clock();
	
    cout << endl << "it include cin cost�G" << (double)clock()/CLOCKS_PER_SEC << " sec" ;
    cout << endl << "it cost�G" << (END - START) / CLOCKS_PER_SEC << " S" << endl;
	/*
	//use file to call python to draw picture
	fstream linefile;     
	linefile.open("linefile.txt", ios::out | ios::trunc); 
	if(linefile.fail())
		cout << "file can't open!\n";
	else{
		for(int i = 0; i < plotans.size(); ++i){
			linefile << plotans[i] << endl;
		}
	}
	linefile.close();
*/
	
	//print final answer
	cout << "answer"<<endl;
	for(int i = 0; i < 3; ++i){
		cout <<"machine"<<i+1<<endl;
		for(int j = 0; j < anscount[i]; ++j){
			cout << "job"<<ansmachine[i][j].assignjob<<"\tST="<< ansmachine[i][j].start << "\tCT="<<ansmachine[i][j].end<<endl;
		}
		cout<<endl;
	}
	//cout <<"aaaaaaa"<<system("python plot.py");
	return 0;
}
	


import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import product
import os
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)


current_directory = os.getcwd()



# Parameters
noises=[0.05,0.5,1,2]
noise_str=["005","05","1","2"]
angles=[45,90,180,120]
detail=[]
with open(current_directory+f'/Angle_{angles[0]}/Noise_{noises[0]}/ccf-vcfparameters.txt', 'r') as file:
    for line in file:
        detail.append(line)
Length_of_box = float(detail[1])   # Size of the grid
numberoftrial=int(detail[10])
maxiter=int(detail[3])
Number_of_agents=int(detail[0])
Lx=int(detail[1])
Ly=float(detail[2])
v0=float(detail[4])
dt=float(detail[5])
density=float(detail[8])
rc=float(detail[9])
dr=float(detail[11])


numberofbins=int(Lx/(2*dr))
numberoftimesteps=0
for i in range( maxiter):
    if(i<10):tf=1
    if(i>10):tf=10
    if(i>100):tf=50
    if(i>1000):tf=100
    if(i%tf==0):numberoftimesteps+=1

numberofnoises=len(noises)
numberofangles=len(angles)



# Function to load data from files
def load_data(file_path):
    order = []
    time = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                t ,o = map(float, line.split())
                order.append(o)
                time.append(t)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

    return order,time

times=[]

for t in range(maxiter):
    if(t<10):tf=1
    if(t>10):tf=10
    if(t>100):tf=50
    if(t>1000):tf=100
    if(t%200==0 and t>5000):times.append(t)



for j in range(0,numberofangles): 
    for i in range(0,numberofnoises):
        vcf= np.zeros(numberofbins)
        ccf= np.zeros(numberofbins)
        r=np.zeros(numberofbins)    

        for t in times:
            for trial in range(0,numberoftrial):
                
                # Load order parameter vs time data
                vcf_temp,rrr = load_data(current_directory+f'/Angle_{angles[j]}/Noise_{noises[i]}/correlation_data/velocitycorrelation_vs_r_{trial}_{t}_.dat')
                vcf+=vcf_temp
                
                # Load order parameter vs time data
                ccf_temp,rr = load_data(current_directory+f'/Angle_{angles[j]}/Noise_{noises[i]}/correlation_data/connectedcorrelation_vs_r_{trial}_{t}_.dat')
                ccf+=ccf_temp
                r+=rr
                
        vcf/=numberoftrial*len(times)
        ccf/=numberoftrial*len(times)
        r/=numberoftrial*len(times)

        with open(current_directory+f'/Figure/correlation/ccf_vs_r_{int(angles[j])}_{noise_str[i]}.dat','w') as file:
            for tim in range(numberofbins):
                file.write(f"{r[tim]}"+f" {ccf[tim]}\n")    
        
        with open(current_directory+f'/Figure/correlation/vcf_vs_r_{int(angles[j])}_{noise_str[i]}.dat','w') as file:
            for tim in range(numberofbins):
                file.write(f"{r[tim]}"+f" {vcf[tim]}\n")



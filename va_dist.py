
import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import product
import os
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)


current_directory = os.getcwd()



# Parameters
noises=[0.05,0.5,1]
angles=[45,90,120,180]
detail=[]
with open(current_directory+f'/Angle_{angles[0]}/Noise_{noises[0]}/parameters.txt', 'r') as file:
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


numberoftimesteps=0
for i in range( maxiter):
    if(i<10):tf=1
    if(i>10):tf=10
    if(i>100):tf=50
    if(i>1000):tf=100
    if(i%tf==0):numberoftimesteps+=1

numberofnoises=len(noises)
numberofangles=len(angles)

plt.rcParams['axes.linewidth'] = 2.0
plt.rcParams["legend.labelspacing"]=0.1
#plt.rc_context({"xtick.major.pad": 8})
#plt.rc_context({"ytick.major.pad": 5})
plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)
#plt.rc('legend',fontsize=30)
plt.rcParams["font.family"] = "serif"
plt.rcParams['mathtext.fontset'] ="cm"
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.size'] = 10
#plt.rcParams['xtick.major.width'] = 2
plt.rcParams['xtick.minor.size'] = 5
#plt.rcParams['xtick.minor.width'] = 1.5
plt.rcParams['ytick.major.size'] = 10
#plt.rcParams['ytick.major.width'] = 2
plt.rcParams['ytick.minor.size'] = 5
#plt.rcParams['ytick.minor.width'] = 1.5
plt.rcParams["legend.handlelength"] = 1.0
plt.rcParams["legend.handletextpad"] = 0.2




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

colour=['darkgreen','royalblue','salmon']
markers=["o","s","^"]
label=["(a)","(b)","(c)","(d)"]
index=[[0,0],[0,1],[1,0],[1,1]]
angles_rad=[r"$\pi/4$",r"$\pi/2$",r"$2\pi/3$",r"$\pi$"]
noises_str=["0.05","0.5","1.0"]
# Loop through different trials to read data and create quiver plots
order=[]
for j in range(0,numberofangles): 
    for i in range(0,numberofnoises):
        for trial in range(0,numberoftrial):
            # Path templates
            path = current_directory+f'/Angle_{angles[j]}/Noise_{noises[i]}/orderdata/order_vs_time_{trial}_.txt'
            # Load order parameter vs time data
            o,t = load_data(path)
            order.append(o)


plt.hist(o)


plt.tight_layout()

plt.show()

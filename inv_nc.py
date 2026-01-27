
import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import product
import os
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib

current_directory = os.getcwd()

matplotlib.use('Qt5Agg')

# Parameters
noises=[0.05,0.5,2]
angles=[45, 180]
detail=[]
with open(current_directory+f'/Angle_{angles[0]}/Noise_{noises[0]}/parameters.txt', 'r') as file:
    for line in file:
        detail.append(line)
Length_of_box = float(detail[1])   # Size of the grid
numberoftrials=int(detail[10])
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

plt.rcParams["legend.frameon"]=False 
plt.rcParams["legend.loc"]="lower right"

fig, axes = plt.subplots(2, figsize=(7, 7))


# Function to load data from files
def load_data(file_path):
    order = []
    time = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                o = map(float, line.split())
                order.append(o)
                
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

    return order

colour=['darkgreen','royalblue','salmon']
markers=["o","s","^"]
label=["(a)","(b)","(c)","(d)"]

angles_rad=[r"$\pi/4$",r"$\pi$"]
noises_str=["0.05","0.5","2.0"]

times=[]
for t in range(maxiter):
    if(t<10):tf=1
    if(t>10):tf=10
    if(t>100):tf=50
    if(t>1000):tf=100
    if(t%tf==0):
        times.append(t)

# Loop through different trials to read data and create quiver plots
for j in range(0,numberofangles): 
    for i in range(0,numberofnoises):
        number=np.zeros(len(times))
        for trial in range(numberoftrials):
            for t,tim in enumerate(times):
                # Path templates
                path = current_directory+f'/Angle_{angles[j]}/Noise_{noises[i]}/cluster_index/mass_{trial}_{tim}_.txt'
                # Load data
                o = load_data(path)
                if(len(o)!=0):
                    number[t]+=1/float(len(o))
        number*=Number_of_agents/numberoftrials

        # Plot
        ax = axes[j] 

        if(j==0):
            ax.plot(times,number, c=colour[i], marker=markers[i],label=r"$\eta =$"+f"{noises_str[i]}", markeredgecolor=colour[i],markerfacecolor="None")
            ax.legend( prop={'size': 17},labelspacing = 0.2,frameon=False,bbox_to_anchor=(0.1, 0.2, 0.2, 0.6))
           
        else:
            ax.plot(times,number, c=colour[i], marker=markers[i], markeredgecolor=colour[i],markerfacecolor="None")
 
            
        ax.annotate( r"$\alpha$ = " + f'{angles_rad[j]}',size=25,xy=(0.15,0.7),xycoords="axes fraction")
        ax.annotate(label[j],size=15,xy=(0.05,0.85),xycoords="axes fraction")
    
        if(j==1):
            ax.set_xlabel(r'$t$',fontsize=25)
        if(i==0):
            ax.set_ylabel(r'$\langle N/n_c(t) \rangle$',fontsize=25,labelpad=1)
        
        ax.title.set_position((0.15, 0.9))
        #ax.set_ylim(0,1.05)
        #ax.set_xlim(7,9000)
        ax.set_xscale("log")
        #ax.set_yscale("log")
        ax.tick_params(axis='x', which='minor')
        ax.tick_params(left=True, top=True ,right=True)
        ax.tick_params(axis="x", direction="in")
        ax.tick_params(axis="y", direction="in")

ax=axes[0]
#props = dict(boxstyle='round', facecolor='None', alpha=0.2)
#string=f"$N=${Number_of_agents} \n"+"$L=$"+f"{Lx} "
#ax.text(0.2,0.9,string,transform=ax.transAxes,fontsize=13,verticalalignment='top',bbox=props)

#for ticks 
ax1=axes[0]
ax2=axes[1]


#ax1.xaxis.set_major_locator(MultipleLocator(2500))
#ax1.xaxis.set_minor_locator(MultipleLocator(1250))
#ax1.yaxis.set_major_locator(MultipleLocator(4))
#ax1.yaxis.set_minor_locator(MultipleLocator(2))
#ax1.set_ylim(0,22)
ax1.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True)

#ax2.xaxis.set_major_locator(MultipleLocator(2500))
#ax2.xaxis.set_minor_locator(MultipleLocator(1250))
#ax2.yaxis.set_major_locator(MultipleLocator(2))
#ax2.yaxis.set_minor_locator(MultipleLocator(1))
ax2.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True)


plt.tight_layout()
plt.show()

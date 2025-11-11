
import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import product
import os
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import seaborn as sns

current_directory = os.getcwd()



# Parameters
noises=[0.05,0.5,2]
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


sns.set_theme(style="white")
sns.set_context("paper")
plt.rcParams['axes.linewidth'] = 2.0
plt.rcParams["legend.labelspacing"]=0.1
#plt.rc_context({"xtick.major.pad": 8})
#plt.rc_context({"ytick.major.pad": 5})
plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)
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



fig, axes = plt.subplots(2,2, figsize=(8,8))


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
noises_str=["0.05","0.5","2.0"]
# Loop through different trials to read data and create quiver plots
for j in range(0,numberofangles): 
    for i in range(0,numberofnoises):
        order= np.zeros(numberoftimesteps)
        time=np.zeros(numberoftimesteps)
        for trial in range(0,numberoftrial):
            # Path templates
            path = current_directory+f'/Angle_{angles[j]}/Noise_{noises[i]}/orderdata/order_vs_time_{trial}_.txt'
            # Load order parameter vs time data
            o,t = load_data(path)
            order+=o
            time+=t
    
        order/=numberoftrial
        time/=numberoftrial
        # Plot
        n=index[j][0]
        m=index[j][1]
        ax = axes[n,m]
        #ax.set_xscale("log")
        
        if(n==0 and m==0):
            ax.plot(time,order, c=colour[i], marker=markers[i],label=r"$\eta =$"+f"{noises_str[i]}", markeredgecolor=colour[i],markerfacecolor="None")
        else:
            ax.plot(time,order, c=colour[i], marker=markers[i], markeredgecolor=colour[i],markerfacecolor="None")
        #ax.set_title( "α = " + f'{angles[j]}',fontsize=14,pad=-14)
        
        
        #for ticks 
        ax.xaxis.set_major_locator(MultipleLocator(2500))
        ax.xaxis.set_minor_locator(MultipleLocator(500))
        ax.yaxis.set_major_locator(MultipleLocator(0.5))
        ax.yaxis.set_minor_locator(MultipleLocator(0.1))
        
        ax.annotate( r"$\alpha$ = " + f'{angles_rad[j]}',size=25,xy=(0.2,0.05),xycoords="axes fraction")
        ax.annotate(label[j],size=25,xy=(0.8,0.05),xycoords="axes fraction")
        
        if(n==1):
            ax.set_xlabel(r'$t$',fontsize=30)
        if(m==0):
            ax.set_ylabel(r'$\langle v_{a}(t) \rangle$',fontsize=30,labelpad=1)
        
        ax.legend(loc="best", prop={'size': 18},labelspacing = 0.2,frameon=False,bbox_to_anchor=(0.5, 0.45, 0.5, 0.5))
        ax.title.set_position((0.15, 0.9))
        ax.set_ylim(0,1.05)
        ax.set_xlim(0.1,9900)
        ax.tick_params(axis="x",which="minor" ,bottom=True,left=True, top=True ,right=True,direction="in",length=4)
        ax.tick_params(axis="x",which="major" ,bottom=True,left=True, top=True ,right=True,direction="in",length=8)
        ax.tick_params(axis="y",which="minor" ,bottom=True,left=True, top=True ,right=True,direction="in",length=4)
        ax.tick_params(axis="y",which="major" ,bottom=True,left=True, top=True ,right=True,direction="in",length=8)

ax=axes[0,0]
props = dict(boxstyle='round', facecolor='white', alpha=0.2)
string=f"$N=${Number_of_agents} \n"+"$L=$"+f"{Lx} "
#ax.text(0.2,0.9,string,transform=ax.transAxes,fontsize=13,verticalalignment='top',bbox=props)

'''ax=axes[1,0]
string=r"\textcolor{#3756ec}{o} : "+f"{noises[0]}\n"+ r"\textcolor{#FF5733}{o} : "+f"{noises[1]}\n"+r"\textcolor{#e4b1f2}{o} : "+f"{noises[2]}\n"
ax.text(-0.5,1,string,transform=ax.transAxes,fontsize=10,verticalalignment='top',bbox=props)
'''



plt.legend()
plt.tight_layout()

#plt.savefig('fig3.pdf', format='pdf',bbox_inches='tight')
plt.show()

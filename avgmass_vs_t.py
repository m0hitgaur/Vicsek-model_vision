
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



fig, axes = plt.subplots(2,2, figsize=(7, 7))


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
for j in range(0,numberofangles): 
    for i in range(0,numberofnoises):
        # Path templates
        path = current_directory+f'/Angle_{angles[j]}/Noise_{noises[i]}/cluster_index/avgmass_vs_t_.txt'
        # Load data
        o,t = load_data(path)
        # Plot
        n=index[j][0]
        m=index[j][1]
        ax = axes[n,m]
        #ax.set_xscale("log")
        
        if(n==0 and m==0):
            ax.plot(t,o, c=colour[i], marker=markers[i],label=r"$\eta =$"+f"{noises_str[i]}", markeredgecolor=colour[i],markerfacecolor="None")
        else:
            ax.plot(t,o, c=colour[i], marker=markers[i], markeredgecolor=colour[i],markerfacecolor="None")
        #ax.set_title( "α = " + f'{angles[j]}',fontsize=14,pad=-14)
        
        
        if(n==0 and m==0):
            ax.annotate( r"$\alpha$ = " + f'{angles_rad[j]}',size=17,xy=(0.6,0.8),xycoords="axes fraction")
        else:
            ax.annotate( r"$\alpha$ = " + f'{angles_rad[j]}',size=17,xy=(0.5,0.1),xycoords="axes fraction")
        ax.annotate(label[j],size=15,xy=(0.05,0.85),xycoords="axes fraction")
        
        if(n==1):
            ax.set_xlabel(r'$t$',fontsize=25)
        if(m==0):
            ax.set_ylabel(r'$\langle m \rangle$',fontsize=25,labelpad=1)
        
        ax.legend(loc="best", prop={'size': 11},labelspacing = 0.2,frameon=False,bbox_to_anchor=(0.5, 0.3, 0.5, 0.5))
        ax.title.set_position((0.15, 0.9))
        #ax.set_ylim(0,1.05)
        ax.set_xlim(0,9900)
        ax.tick_params(axis='x', which='minor')
        ax.tick_params(left=True, top=True ,right=True)
        ax.tick_params(axis="x", direction="in")
        ax.tick_params(axis="y", direction="in")
        # ax.set_xscale("log")
        #  ax.set_yscale("log")
ax=axes[0,0]
props = dict(boxstyle='round', facecolor='white', alpha=0.2)
string=f"$N=${Number_of_agents} \n"+"$L=$"+f"{Lx} "
ax.text(0.2,0.9,string,transform=ax.transAxes,fontsize=13,verticalalignment='top',bbox=props)

'''ax=axes[1,0]
string=r"\textcolor{#3756ec}{o} : "+f"{noises[0]}\n"+ r"\textcolor{#FF5733}{o} : "+f"{noises[1]}\n"+r"\textcolor{#e4b1f2}{o} : "+f"{noises[2]}\n"
ax.text(-0.5,1,string,transform=ax.transAxes,fontsize=10,verticalalignment='top',bbox=props)
'''

#for ticks 
ax1=axes[0,0]
ax2=axes[0,1]
ax3=axes[1,0]
ax4=axes[1,1]

ax1.xaxis.set_major_locator(MultipleLocator(2500))
ax1.xaxis.set_minor_locator(MultipleLocator(1250))
ax1.yaxis.set_major_locator(MultipleLocator(2))
ax1.yaxis.set_minor_locator(MultipleLocator(1))
ax1.set_ylim(0,20)
ax1.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True)

ax2.xaxis.set_major_locator(MultipleLocator(2500))
ax2.xaxis.set_minor_locator(MultipleLocator(1250))
ax2.yaxis.set_major_locator(MultipleLocator(10))
ax2.yaxis.set_minor_locator(MultipleLocator(5))
ax2.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True)

ax3.xaxis.set_major_locator(MultipleLocator(2500))
ax3.xaxis.set_minor_locator(MultipleLocator(1250))
ax3.yaxis.set_major_locator(MultipleLocator(50))
ax3.yaxis.set_minor_locator(MultipleLocator(10))
ax3.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True)

ax4.xaxis.set_major_locator(MultipleLocator(2500))
ax4.xaxis.set_minor_locator(MultipleLocator(1250))
ax4.yaxis.set_major_locator(MultipleLocator(20))
ax4.yaxis.set_minor_locator(MultipleLocator(10))
ax4.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True)


plt.legend()
plt.tight_layout()

plt.savefig('fig3.pdf', format='pdf',bbox_inches='tight')
plt.show()

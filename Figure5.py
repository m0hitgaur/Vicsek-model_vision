
import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import product
import os
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import seaborn as sns

current_directory = os.getcwd()



# Parameters
noises=[0.5]
angles=[45,180]
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



fig, axes = plt.subplots(1, figsize=(4.5,4.5))


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

sns.set_theme(style="white") # 'whitegrid' provides a grid, 'deep' is a good default color palette
sns.set_context("paper")
sns.set_palette("colorblind")


colour=['steelblue','orangered','darkslategray',"mediumseagreen"]
markers_rad=["o","v"]
markers_corr=["^","s"]
label=["(a)","(b)","(c)","(d)"]
index=[[0,0],[0,1],[1,0],[1,1]]
angles_rad=[r"$\pi/4$",r"$\pi$"]#r"$\pi/2$",r"$2\pi/3$",
noises_str=["0.5"]
# Loop through different trials to read data and create quiver plots

ax=axes

path_radius_45 = current_directory+f'/Angle_{angles[0]}/Noise_{noises[0]}/cluster_index/radius.txt'
path_corr_45 = current_directory+f'/Angle_{angles[0]}/Noise_{noises[0]}/correlation_data/velocorrlength_vs_time_zerocrossing.dat'

path_radius_180 = current_directory+f'/Angle_{angles[1]}/Noise_{noises[0]}/cluster_index/radius.txt'
path_corr_180 = current_directory+f'/Angle_{angles[1]}/Noise_{noises[0]}/correlation_data/velocorrlength_vs_time_zerocrossing.dat'

# Load order parameter vs time data
corr_45,t_corr_45 = load_data(path_corr_45)
rad_45,t_rad_45 =load_data(path_radius_45)
corr_180,t_corr_180 = load_data(path_corr_180)
rad_180,t_rad_180 =load_data(path_radius_180)

# Plot
ax.plot(t_corr_45,corr_45, c=colour[0], marker="o",label=r"$ \xi_{v} \;(\alpha =$"+f"{angles_rad[0]})", markeredgecolor=colour[0],markerfacecolor="None")
ax.plot(t_rad_45,rad_45, c=colour[1], marker="o",label=r"$ R_g \;  (\alpha=$"+f"{angles_rad[0]})", markeredgecolor=colour[1],markerfacecolor="None")

ax.plot(t_corr_180,corr_180, c=colour[0], marker="^",label=r"$ \xi_{v} \; (\alpha =$"+f"{angles_rad[1]})", markeredgecolor=colour[0],markerfacecolor="None")
ax.plot(t_rad_180,rad_180, c=colour[1], marker="^",label=r"$ R_g \; (\alpha =$"+f"{angles_rad[1]})", markeredgecolor=colour[1],markerfacecolor="None")
x=np.linspace(20,400,10) 
ax.plot(x,2.7*x**0.2,color="black")    
ax.annotate( r"$t^{1/5}$",size=15,xy=(0.62,0.8),xycoords="axes fraction")    

x=np.linspace(100,800,10) 
ax.plot(x,0.42*x**0.25,color="black",linestyle="--")    
ax.annotate( r"$t^{1/4}$",size=15,xy=(0.62,0.35),xycoords="axes fraction")    

x=np.linspace(10,800,10) 
y1=np.zeros(10)
y2=np.full(10,14)
ax.fill_between(x,y1,y2,color="green",alpha=0.15)
ax.set_ylim(0.7,12)
x=np.linspace(820,5000,10) 
y1=np.zeros(10)
y2=np.full(10,14)
ax.fill_between(x,y1,y2,color="blue",alpha=0.15)
#for ticks 
ax.xaxis.set_major_locator(MultipleLocator(1000))
ax.xaxis.set_minor_locator(MultipleLocator(500))
ax.yaxis.set_major_locator(MultipleLocator(0.5))
ax.yaxis.set_minor_locator(MultipleLocator(0.1))
ax.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True)

#ax.annotate( r"$\alpha$ = " + f'{angles_rad[j]}',size=17,xy=(0.5,0.1),xycoords="axes fraction")
#ax.annotate(label[j],size=15,xy=(0.05,0.85),xycoords="axes fraction")

#ax.set_xlabel(r'$t$',fontsize=25)
#ax.set_ylabel(r'$\langle \xi_{v} \rangle \; , \langle R_g \rangle$',fontsize=25,labelpad=0.1)
ax.annotate( r'$\langle \xi_{v}(t) \rangle \; , \langle R_g(t) \rangle$',size=23,xy=(-0.14,0.3),xycoords="axes fraction",rotation=90)    
ax.annotate( r'$t$',size=23,xy=(0.4,-0.08),xycoords="axes fraction")    

ax.legend(loc="best", prop={'size': 12},labelspacing = 0.2,frameon=False,bbox_to_anchor=(0.1, 0.1, 0.5, 0.5))
ax.title.set_position((0.15, 0.9))

#ax.set_ylim(0,6)
ax.set_xlim(1,5000)
ax.tick_params(axis='x', which='minor')
ax.tick_params(left=True, top=True ,right=True)
ax.tick_params(axis="x", direction="in")
ax.tick_params(axis="y", direction="in")
ax.set_xscale("log")
ax.set_yscale("log")

ax=axes 
props = dict(boxstyle='round', facecolor='white', alpha=0.2)
string=f"$N=${Number_of_agents} \n"+"$L=$"+f"{Lx} "
ax.text(0.05,0.92,string,transform=ax.transAxes,fontsize=13,verticalalignment='top',bbox=props)

'''ax=axes[1,0]
string=r"\textcolor{#3756ec}{o} : "+f"{noises[0]}\n"+ r"\textcolor{#FF5733}{o} : "+f"{noises[1]}\n"+r"\textcolor{#e4b1f2}{o} : "+f"{noises[2]}\n"
ax.text(-0.5,1,string,transform=ax.transAxes,fontsize=10,verticalalignment='top',bbox=props)
'''



#plt.legend()
plt.tight_layout()

plt.savefig('fig5.pdf', format='pdf',bbox_inches='tight')
plt.show()

import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import product
import os
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import seaborn as sns
current_directory = os.getcwd()

plt.rcParams["font.family"] = "serif"
plt.rcParams['mathtext.fontset'] ="cm"
sns.set_theme(style="white")
sns.set_context("paper")

# Function to load data from files
def load_data_theta(file_path):
    order = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                o =  float(line.strip())
                order.append(o)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

    return order

def load_data_one(file_path):
    order = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                o =  line.strip()
                order.append(o)
   
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

    return order
# Parameters

noise=["0.05","0.5"]
angle=["45","180"]
angles_rad=["$\pi/4$","$\pi$"]
noises_str=["0.05","0.5"]
label=["(a)","(b)","(c)","(d)","(e)","(f)"]


plt.rcParams['axes.linewidth'] = 2.0
plt.rcParams["legend.labelspacing"]=0.1
#plt.rc_context({"xtick.major.pad": 8})
#plt.rc_context({"ytick.major.pad": 5})
plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)
plt.rc('legend',fontsize=25)
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



detail=load_data_one(current_directory+f'/Angle_{angle[0]}/Noise_{noise[0]}/parameters.txt')
N=detail[0]
L = detail[1]   # Size of the grid
numberoftrials=1#int(detail[10])

binnumber=100
start_bin=0
end_bin=1
bin_a=np.linspace(start_bin,end_bin,binnumber+1)
fig, axes=plt.subplots(3,2,figsize=(10,13),layout='constrained')


times=[5000,6000,7000,8000]
for n in range(len(noise)):
    for a in range(len(angle)):
        hist_dv=np.zeros(binnumber)
        hist_v=np.zeros(binnumber)
        for time in times:
            for trial in range(numberoftrials):   
                path_template_theta =current_directory+f'/Angle_{angle[a]}/Noise_{noise[n]}/flockingdata/theta_{trial}_{time}_.dat'   
                # Load position and angle data
                theta = np.array(load_data_theta(path_template_theta))
                vx=abs(np.cos(theta))
                avg_vx=np.sum(vx)/float(len(vx))         
                
                v_count,v_bin_edge=np.histogram(vx,bins=bin_a)   
                dv_count,dv_bin_edge=np.histogram(vx-avg_vx ,bins=bin_a)
                
                dv_bin_center=0.5* (dv_bin_edge[:-1]+dv_bin_edge[1:])
                v_bin_center=0.5* (v_bin_edge[:-1]+v_bin_edge[1:])
                #if(a==1 and n==0):
                #    plt.bar(v_bin_center,v_count,color="salmon",width=0.0125,label=f"{time} {trial}",alpha=0.5)
                #    plt.legend()
                #    plt.show()
                hist_v+=v_count
                hist_dv+=dv_count
                bin_dv=dv_bin_center
                bin_v=v_bin_center

        ax=axes[a+1][n]
        hist_dv/=numberoftrials

        hist_dv/=np.sum(hist_dv)
        hist_v/=np.sum(hist_v)

   
        ax.bar(bin_dv,hist_dv,color="darkblue",width=0.025,alpha=0.5,label=r"$z=\delta v_{x}$")
        ax.bar(bin_v,hist_v,color="red",width=0.025,label=r"$z=v_{x}$",alpha=0.2)
        if (a==0 ):             
            ax.legend( prop={'size': 25},labelspacing = 0.2,frameon=False,bbox_to_anchor=(0.4, 0.2, 0.7, 0.6))
        else:
            ax.legend( prop={'size': 25},labelspacing = 0.2,frameon=False,bbox_to_anchor=(0.5, 0.2, 0.5, 0.5))
    
           

label_colourbar=[[r"$-\pi$",r"$\pi/3$",r"0",r"$\pi/2$"],["-0.05","0","0.05"]]

tick=[[-3.14, -1 ,0,1.5],[-0.05,0,0.05]]

axes_dev=[axes[0,0],axes[0,1]]

cmap = plt.cm.twilight  # Cyclic colormap for directions
norm = plt.Normalize(vmin=-np.pi, vmax=np.pi)  # Normalize angles to [-π, π]
import matplotlib.ticker as mticker


for i,ax in enumerate(axes_dev):
    # Path templates
    trial_=10
    time_to_plot=7000
    path_template_x = current_directory + f'/Angle_{angle[i]}/Noise_{noise[0]}/flockingdata/positionx_{trial_}_{time_to_plot}_.dat'
    path_template_y = current_directory + f'/Angle_{angle[i]}/Noise_{noise[0]}/flockingdata/positiony_{trial_}_{time_to_plot}_.dat'
    path_template_theta = current_directory + f'/Angle_{angle[i]}/Noise_{noise[0]}/flockingdata/theta_{trial_}_{time_to_plot}_.dat'
    
    # Load position and angle data
    positionx = load_data_theta(path_template_x)
    positiony = load_data_theta(path_template_y)
    theta = load_data_theta(path_template_theta)
    
    if positionx is None or positiony is None or theta is None:
        print(f"Skipping Noise {noise[i]} | Angle {angle[j]} due to missing data.")
        continue

    # Extract data for the specific time step
    px = positionx
    py = positiony
    th = theta

    # Compute velocity components
    vx = np.cos(th)
    vy = np.sin(th)

    avg_vx=np.sum(vx)/float(len(vx))
    avg_vy=np.sum(vy)/float(len(vy))
    dvx=vx-avg_vx
    dvy=vy-avg_vy
    theta_avg=np.sum(theta)/float(len(theta))
    # Map the direction (angle) to colors using the colormap
    dtheta=theta-theta_avg 
    
    #periodic boundary condition

    colors = cmap(norm(dtheta))  # Map angles to RGBA colors
    norm = plt.Normalize(vmin=np.min(dtheta), vmax=np.max(dtheta))  # Normalize angles
    data=load_data_theta(current_directory+f"/Angle_{angle[0]}/Noise_{noise[0]}/flockingdata/details.txt")
    Lx=data[1]
    Ly=data[2]
    
    # Plot the quiver plot
    
    ax.quiver(px, py,np.cos(dtheta),np.sin(dtheta) ,color=colors, angles='xy', scale_units='xy', scale=1.7)
    
    ax.set_xlim([0, Lx])
    ax.set_ylim([0, Ly])
    ax.set_xticks([])
    ax.set_yticks([])
    
    cbar = fig.colorbar(plt.cm.ScalarMappable( cmap=cmap, norm=norm), ax=ax, location='bottom', shrink=0.8, pad=0.1,ticks=tick[i],format=mticker.FixedFormatter(label_colourbar[i]))
    
    cbar.set_label(r'$\delta \theta_{i}$ (in Radians)',fontsize=25)
    cbar.ax.tick_params(labelsize=20)


axes_1=[[1,0],[1,1],[2,0],[2,1]]
ax1=axes[1,0]
ax2=axes[2,0]
ax3=axes[2,1]
ax1.set_ylabel(r"$P~(|z|)$",fontsize=30)
ax2.set_ylabel(r"$P~(|z|)$",fontsize=30)
ax2.set_xlabel(r"$|z|(\times v_0)$",fontsize=30)
ax3.set_xlabel(r"$|z|(\times v_0)$",fontsize=30)

for i,ax in enumerate(axes_1):
    n=ax[0]
    m=ax[1]
    ax1=axes[n,m]
    ax1.annotate( r"$\eta=$"+f"${noises_str[m]}$",size=25,xy=(0.4,0.85),xycoords="axes fraction")    
    ax1.annotate( r"$\alpha=$"+f"{angles_rad[n-1]}",size=25,xy=(0.4,0.75),xycoords="axes fraction")  
    ax1.annotate(f"${label[i+2]}$",size=25,xycoords="axes fraction",xy=(0.8,0.85))
    
    ax1.xaxis.set_major_locator(MultipleLocator(0.2))
    ax1.xaxis.set_minor_locator(MultipleLocator(0.1 ))
    if (i==2):
        ax1.yaxis.set_major_locator(MultipleLocator(0.1))
        ax1.yaxis.set_minor_locator(MultipleLocator(0.05 ))
    else:
        ax1.yaxis.set_major_locator(MultipleLocator(0.02))
        ax1.yaxis.set_minor_locator(MultipleLocator(0.01 ))
    if(i==0):
        ax1.set_ylim(0,0.12)
    ax1.tick_params(which='minor', direction="in", length=3, color="black",right=True,top=True,bottom=True,left=True)
    ax1.tick_params(which='major', direction="in", length=6, color="black",right=True,top=True,bottom=True,left=True)
        

axes[0,0].annotate( r"$\eta=$"+f"${noises_str[0]}$",size=25,xy=(0.6,1.075),xycoords="axes fraction")    
axes[0,0].annotate( f"${label[0]}$",size=25,xy=(0.025,1.075),xycoords="axes fraction")
axes[0,0].annotate( r"$\alpha=$"+f"{angles_rad[0]}",size=25,xy=(0.2,1.075),xycoords="axes fraction")   


axes[0,1].annotate( r"$\eta=$"+f"${noises_str[0]}$",size=25,xy=(0.6,1.075),xycoords="axes fraction")    
axes[0,1].annotate( f"${label[1]}$",size=25,xy=(0.025,1.075),xycoords="axes fraction")
axes[0,1].annotate( r"$\alpha=$"+f"{angles_rad[1]}",size=25,xy=(0.2,1.075),xycoords="axes fraction")   
axes[1,1].annotate( f" ",size=5,xy=(0.9,1.1),xycoords="axes fraction")

#plt.subplots_adjust(left=0.057, right=0.912, top=0.933, bottom=0.052, wspace=0.167, hspace=0.1)
plt.show()

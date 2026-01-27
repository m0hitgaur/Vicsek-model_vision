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
fig, axes=plt.subplots(2,2,figsize=(10,13),layout='constrained')


label_colourbar=[[r"$-2.8$",r"0",r"$2.8$"],[r"$-2.1$","0",r"$1.04$"]]
   #-2.8,2.8   -2.1 2\pi/3   1.04 \pi/3  
tick=[[-2.8 ,0,2.8],[-2.1,0,1.04]]

axes_dev=[axes[1,0],axes[1,1]]

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

    px = positionx
    py = positiony
    th = theta

    vx = np.cos(th)
    vy = np.sin(th)

    avg_vx=np.sum(vx)/float(len(vx))
    avg_vy=np.sum(vy)/float(len(vy))

    dvx=vx-avg_vx
    dvy=vy-avg_vy
    dtheta=np.atan2(dvy,dvx)


    colors = cmap(norm(dtheta))  # Map angles to RGBA colors
    norm = plt.Normalize(vmin=np.min(dtheta), vmax=np.max(dtheta))  # Normalize angles
    data=load_data_theta(current_directory+f"/Angle_{angle[0]}/Noise_{noise[0]}/flockingdata/details.txt")
    Lx=data[1]
    Ly=data[2]
    
    # Plot the quiver plot
 
    ax.quiver(px, py, np.cos(dtheta),np.sin(dtheta),color=colors, angles='xy', scale_units='xy', scale=1.7)
    
    ax.set_xlim([0, Lx])
    ax.set_ylim([0, Ly])
    ax.set_xticks([])
    ax.set_yticks([])
    
    cbar = fig.colorbar(plt.cm.ScalarMappable( cmap=cmap, norm=norm), ax=ax, location='bottom', shrink=0.8, pad=0.1,ticks=tick[i],format=mticker.FixedFormatter(label_colourbar[i]))
    
    cbar.set_label(r'$\delta \theta_{i}$ (in Radians)',fontsize=20)
    cbar.ax.tick_params(labelsize=20)



label_colourbar=[[r"$-\pi$",r"0",r"$\pi$"],[r"$-\pi$",r"0",r"$\pi$"]]

tick=[[-3.14 ,0,3.14],[-3.14 ,0,3.14]]

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

    
    #periodic boundary condition

    colors = cmap(norm(theta))  # Map angles to RGBA colors
    #norm = plt.Normalize(vmin=np.min(theta), vmax=np.max(theta))  # Normalize angles
    data=load_data_theta(current_directory+f"/Angle_{angle[0]}/Noise_{noise[0]}/flockingdata/details.txt")
    Lx=data[1]
    Ly=data[2]
    
    # Plot the quiver plot
    
    ax.quiver(px, py,np.cos(theta),np.sin(theta) ,color=colors, angles='xy', scale_units='xy', scale=1.7)
    
    ax.set_xlim([0, Lx])
    ax.set_ylim([0, Ly])
    ax.set_xticks([])
    ax.set_yticks([])
    
    cbar = fig.colorbar(plt.cm.ScalarMappable( cmap=cmap, norm=norm), ax=ax, location='bottom', shrink=0.8, pad=0.1,ticks=tick[i],format=mticker.FixedFormatter(label_colourbar[i]))
    
    cbar.set_label(r'$ \theta_{i}$ (in Radians)',fontsize=20)
    cbar.ax.tick_params(labelsize=20)


#axes[0,0].annotate( r"$\eta=$"+f"${noises_str[0]}$",size=25,xy=(0.65,1.075),xycoords="axes fraction")    
axes[0,0].annotate( f"${label[0]}$",size=25,xy=(0.005,1.075),xycoords="axes fraction")
axes[0,0].annotate( r"$\alpha=$"+f"{angles_rad[0]}",size=25,xy=(0.4,1.075),xycoords="axes fraction")   
#axes[0,0].annotate( f" ",size=5,xy=(0.9,1.1),xycoords="axes fraction")

#axes[0,1].annotate( r"$\eta=$"+f"${noises_str[0]}$",size=25,xy=(0.6,1.075),xycoords="axes fraction")    
axes[0,1].annotate( f"${label[1]}$",size=25,xy=(0.005,1.075),xycoords="axes fraction")
axes[0,1].annotate( r"$\alpha=$"+f"{angles_rad[1]}",size=25,xy=(0.4,1.075),xycoords="axes fraction")   
#axes[0,1].annotate( f" ",size=5,xy=(0.9,1.1),xycoords="axes fraction")

#axes[1,0].annotate( r"$\eta=$"+f"${noises_str[0]}$",size=25,xy=(0.65,1.075),xycoords="axes fraction")    
axes[1,0].annotate( f"${label[2]}$",size=25,xy=(0.005,1.075),xycoords="axes fraction")
#axes[1,0].annotate( r"$\alpha=$"+f"{angles_rad[0]}",size=25,xy=(0.2,1.075),xycoords="axes fraction")   
#axes[1,0].annotate( f" ",size=5,xy=(0.9,1.1),xycoords="axes fraction")

#axes[1,1].annotate( r"$\eta=$"+f"${noises_str[0]}$",size=25,xy=(0.6,1.075),xycoords="axes fraction")    
axes[1,1].annotate( f"${label[3]}$",size=25,xy=(0.005,1.075),xycoords="axes fraction")
#axes[1,1].annotate( r"$\alpha=$"+f"{angles_rad[1]}",size=25,xy=(0.2,1.075),xycoords="axes fraction")   
axes[1,1].annotate( f" ",size=5,xy=(-0.1,1.1),xycoords="axes fraction")

#plt.subplots_adjust(left=0.057, right=0.912, top=0.933, bottom=0.052, wspace=0.167, hspace=0.1)
plt.show()

import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import product
import os
import matplotlib.ticker as mticker
import seaborn as sns

current_directory = os.getcwd()

# Parameters
time=[50,100,1000,5000]  
trial = 24
noises = [2]
angles = [45,180]
numberofnoises = len(noises)
numberofangles = len(angles)
colours=['black','red','blue','green']
mark=['.', '+', 'x', '1']

# Prepare the figure
fig, axes = plt.subplots(len(angles), len(time), figsize=(20,10))
plt.rcParams["font.family"] = "serif"
plt.rcParams['mathtext.fontset'] ="cm"
sns.set_theme(style="white")
sns.set_context("paper")

#fig.suptitle(f'Different Noises and Vision Angles for time: {time_to_plot}', y=1)
angles_rad=["$\pi/4$","$\pi$"]
noises_str=["0.5"]
# Function to load data from files
def load_data(path):
    data = []
    try:
        with open(path, 'r') as f:
            for line in f:
                data.append(float(line.strip()))
        return np.array(data)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
details=load_data(current_directory+f"/Angle_{angles[0]}/Noise_{noises[0]}/flockingdata/details.txt")
numberoftrials=int(details[8])



# Define a cyclic colormap and normalization for direction
cmap = plt.cm.twilight_shifted  # Cyclic colormap for directions
norm = plt.Normalize(vmin=-np.pi, vmax=np.pi)  # Normalize angles to [-π, π]

# Loop through different trials to read data and create quiver plots
for i,time_to_plot in enumerate(time): 
    for j in range(numberofangles):
        # Path templates
        path_template_x = current_directory + f'/Angle_{angles[j]}/Noise_{noises[0]}/flockingdata/positionx_{trial}_{time_to_plot}_.dat'
        path_template_y = current_directory + f'/Angle_{angles[j]}/Noise_{noises[0]}/flockingdata/positiony_{trial}_{time_to_plot}_.dat'
        path_template_theta = current_directory + f'/Angle_{angles[j]}/Noise_{noises[0]}/flockingdata/theta_{trial}_{time_to_plot}_.dat'
        
        # Load position and angle data
        positionx = load_data(path_template_x)
        positiony = load_data(path_template_y)
        theta = load_data(path_template_theta)
        
        if positionx is None or positiony is None or theta is None:
            print(f"Skipping Noise {noises[i]} | Angle {angles[j]} due to missing data.")
            continue

        # Extract data for the specific time step
        px = positionx
        py = positiony
        th = theta

        # Compute velocity components
        vx = np.cos(th)
        vy = np.sin(th)

        # Map the direction (angle) to colors using the colormap
        colors = cmap(norm(th))  # Map angles to RGBA colors
        
        data=load_data(current_directory+f"/Angle_{angles[0]}/Noise_{noises[0]}/flockingdata/details.txt")
        Lx=data[1]
        Ly=data[2]
        
        # Plot the quiver plot
        ax = axes[ j,i]
        ax.quiver(px, py, vx, vy, color=colors, angles='xy', scale_units='xy', scale=1.75)
        
        ax.set_xlim([0, Lx])
        ax.set_ylim([0, Ly])
        ax.set_xticks([])
        ax.set_yticks([])

cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=axes, anchor=(0.5,-0.5),orientation='horizontal', shrink=0.5,fraction=0.15,ticks=[-3.14, -1.57,0,1.57 ,3.14],format=mticker.FixedFormatter([r'$-\pi$',r'$-\pi/2$', '$0$', r'$\pi/2$',r'$\pi$']))
#cbar.set_label(r'$\theta_{i}$ (in Radians)',fontsize=20,loc="right")
ax.annotate( r'$\theta_{i}$ (in Radians)',size=45,xy=(-0.1,-0.25),xycoords="axes fraction") 
cbar.ax.tick_params(labelsize=30)


ax_time=[[0,0],[0,1],[0,2],[0,3]]#,[0,4]]
ax_angle=[[0,0],[1,0]]

for i,ax in enumerate(ax_time):
    n=ax[0]
    m=ax[1]
    ax1=axes[n,m]
    ax1.annotate( r"$t="+f"{time[m]}"+r"$",size=45,xy=(0.3,1.1),xycoords="axes fraction")    

for j,ax in enumerate(ax_angle):
    n=ax[0]
    m=ax[1]
    ax1=axes[n,m]
    ax1.annotate( r"$\alpha=$"+f"{angles_rad[n]}",size=45,xy=(-0.2,0.3),xycoords="axes fraction",rotation=90)    


#horizontal 1  (left=>right)
line = plt.Line2D([0.035, 0.98], [0.52, 0.52], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)


#vertical 5
line = plt.Line2D([0.98, 0.98], [0.13, 0.9], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)

#vertical 5
line = plt.Line2D([0.035, 0.035], [0.13, 0.9], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)


#horizontal 4 (top=>bottom)
line = plt.Line2D([0.035, 0.98], [0.13, 0.13], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)

#horizontal 1
line = plt.Line2D([0.035, 0.98], [0.9, 0.9], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)


plt.subplots_adjust(left=0.043, right=0.971, top=0.888, bottom=0.148, wspace=0.06, hspace=0.13)
plt.savefig('fig2.pdf', format='pdf')
plt.show()


'''#vertical 2
line = plt.Line2D([0.24, 0.24], [0.01, 0.94], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
#vertical 3
line = plt.Line2D([0.447, 0.447], [0.01, 0.94], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
#vertical 4
line = plt.Line2D([0.655, 0.655], [0.01, 0.94], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
'''
'''#horizontal 3
line = plt.Line2D([0.035, 0.86], [0.32, 0.32], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
#horizontal 2
line = plt.Line2D([0.035, 0.86], [0.634, 0.634], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
'''
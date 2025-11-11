import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import product
import os
import matplotlib.ticker as mticker
import seaborn as sns
current_directory = os.getcwd()

# Parameters
time_to_plot = 5000#input("timee to plot")  # 2500  # Adjust this for different time steps
trial = 24
noises = [ 0.5, 0.05]
angles = [45,  180]
numberofnoises = len(noises)
numberofangles = len(angles)
colours=['black','red','blue','green']
mark=['.', '+', 'x', '1']

# Prepare the figure
fig, axes = plt.subplots(2,2, figsize=(15,15))
plt.rcParams["font.family"] = "serif"
plt.rcParams['mathtext.fontset'] ="cm"
sns.set_theme(style="white")
sns.set_context("paper")

#fig.suptitle(f'Different Noises and Vision Angles for time: {time_to_plot}', y=1)
angles_rad=["$\pi/4$","$\pi$"]
noises_str=["0.5","0.05"]
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
for i in range(numberofnoises): 
    for j in range(numberofangles):
        # Path templates
        trial_=trial
        path_template_x = current_directory + f'/Angle_{angles[j]}/Noise_{noises[i]}/flockingdata/positionx_{trial_}_{time_to_plot}_.dat'
        path_template_y = current_directory + f'/Angle_{angles[j]}/Noise_{noises[i]}/flockingdata/positiony_{trial_}_{time_to_plot}_.dat'
        path_template_theta = current_directory + f'/Angle_{angles[j]}/Noise_{noises[i]}/flockingdata/theta_{trial_}_{time_to_plot}_.dat'
        
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

        avg_vx=np.sum(vx)/len(vx)
        avg_vy=np.sum(vy)/len(vy)

        # Map the direction (angle) to colors using the colormap
        colors = cmap(norm(th))  # Map angles to RGBA colors
        data=load_data(current_directory+f"/Angle_{angles[0]}/Noise_{noises[0]}/flockingdata/details.txt")
        Lx=data[1]
        Ly=data[2]
        
        # Plot the quiver plot
        ax = axes[i, j]
        ax.quiver(px, py, vx-avg_vx, vy-avg_vy, color=colors, angles='xy', scale_units='xy', scale=1.75)
        
        ax.set_xlim([0, Lx])
        ax.set_ylim([0, Ly])
        ax.set_xticks([])
        ax.set_yticks([])

cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=axes, orientation='vertical', fraction=0.02, pad=0.6,location="right",ticks=[-3.14, -1.57,0,1.57 ,3.14],format=mticker.FixedFormatter([r'$-\pi$',r'$-\pi/2$', '$0$', r'$\pi/2$',r'$\pi$']))
cbar.set_label(r'$\theta_{i}$ (in Radians)',fontsize=25)
cbar.ax.tick_params(labelsize=25)


ax_noise=[[0,0],[1,0]]
ax_angle=[[0,0],[0,1]]

for ax in ax_noise:
    n=ax[0]
    m=ax[1]
    ax1=axes[n,m]
    ax1.annotate( r"$\eta=$"+f"{noises_str[n]}",size=35,xy=(-0.1,0.2),xycoords="axes fraction",rotation=90)    

for ax in ax_angle:
    n=ax[0]
    m=ax[1]
    ax1=axes[n,m]
    ax1.annotate( r"$\alpha=$"+f"{angles_rad[m]}",size=35,xy=(0.35,1.05),xycoords="axes fraction")    


'''
#vertical 1  (left=>right)
line = plt.Line2D([0.035, 0.035], [0.01, 0.94], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
#vertical 2
line = plt.Line2D([0.24, 0.24], [0.01, 0.94], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
#vertical 3
line = plt.Line2D([0.447, 0.447], [0.01, 0.94], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
#vertical 4
line = plt.Line2D([0.655, 0.655], [0.01, 0.94], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
#vertical 5
line = plt.Line2D([0.86, 0.86], [0.01, 0.94], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)

#horizontal 4 (top=>bottom)
line = plt.Line2D([0.035, 0.86], [0.01, 0.01], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
#horizontal 3
line = plt.Line2D([0.035, 0.86], [0.32, 0.32], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
#horizontal 2
line = plt.Line2D([0.035, 0.86], [0.634, 0.634], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
#horizontal 1
line = plt.Line2D([0.035, 0.86], [0.94, 0.94], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
'''

plt.subplots_adjust(left=0.043, right=0.852, top=0.93, bottom=0.021, wspace=0.1, hspace=0.1)
plt.savefig('fig2.pdf', format='pdf')
plt.show()

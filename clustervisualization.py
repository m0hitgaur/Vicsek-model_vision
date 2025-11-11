import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import os

current_directory = os.getcwd()
plt.rcParams["font.family"] = "serif"
plt.rcParams['mathtext.fontset'] ="cm"
sns.set_theme(style="white")
sns.set_context("paper")

# Prepare the figure
fig, axes = plt.subplots(1,2, figsize=(20,10))
plt.rcParams["font.family"] = "serif"
plt.rcParams['mathtext.fontset'] ="cm"
sns.set_theme(style="white")
sns.set_context("paper")



# Function to load data from files
def load_data(path):
    """Loads numerical data from a file, one number per line."""
    data = []
    try:
        with open(path, 'r') as f:
            for line in f:
                data.append(float(line.strip()))
    except FileNotFoundError:
        return None
    except ValueError:
        return None
    return np.array(data)

Lx=32
Ly=32
N=2560
current_angle=45
current_angle_str=r"\pi/4"
current_noise=0.05
current_noise_str="0.05"
current_trial=24
current_time=500
label=["a)","b)"]
# --- Load Data ---
path_template_x = os.path.join(current_directory, f'Angle_{current_angle}', f'Noise_{current_noise}', 'flockingdata', f'positionx_{current_trial}_{current_time}_.dat')
path_template_y = os.path.join(current_directory, f'Angle_{current_angle}', f'Noise_{current_noise}', 'flockingdata', f'positiony_{current_trial}_{current_time}_.dat')
path_template_theta = os.path.join(current_directory, f'Angle_{current_angle}', f'Noise_{current_noise}', 'flockingdata', f'theta_{current_trial}_{current_time}_.dat')
path_template_clusterindex = os.path.join(current_directory, f'Angle_{current_angle}', f'Noise_{current_noise}', 'cluster_index', f'clusterindex_{current_trial}_{current_time}_.txt')
path_template_radius = os.path.join(current_directory, f'Angle_{current_angle}', f'Noise_{current_noise}', 'cluster_index', f'radius_{current_trial}_{current_time}_.txt')
path_template_mass = os.path.join(current_directory, f'Angle_{current_angle}', f'Noise_{current_noise}', 'cluster_index', f'mass_{current_trial}_{current_time}_.txt')

positionx = load_data(path_template_x)
positiony = load_data(path_template_y)
theta = load_data(path_template_theta)
ci = load_data(path_template_clusterindex)
radius=load_data(path_template_radius)
mass=load_data(path_template_mass)

distinct_ci = list(set(ci))
cluster=[]

for i,c in enumerate(distinct_ci):
    current_cluster=[]
    for j,b in enumerate(ci):
        if(b==c):  
            current_cluster.append(j)
    cluster.append(current_cluster)  

# Ensure enough colors for distinct clusters, max(..., 1) handles case with no clusters
colourlist = sns.color_palette("Paired", max(len(distinct_ci), 1))

colour = list(range(N))
cl=list(range(N))
for i,clus in enumerate(cluster)  :
    if(len(clus)>=10):
        for j in clus:
            colour[j]=colourlist[i]
            cl[j]=i+1
    else:
        for j in clus:
            colour[j]="black"
            cl[j]=0        



print("--- Cluster Analysis Results ---\n")
print("Size of clusters:\n")
# Sort cluster keys for consistent output
n=1
for k,i in enumerate(mass):
    for j,clus in enumerate(cluster):
        if(len(clus)==i):
            print(f"Cluster {n}: id:{j+1}  {i} agents   radius= {radius[k]}\n")
            n+=1
        
print("------------------------------\n")


# Compute velocity components
# Check if theta has the same length as position data before computing vx, vy
if len(positionx) == len(theta) and len(positiony) == len(theta):
    vx = np.cos(theta)
    vy = np.sin(theta)

    # Plot the quiver plot
    # Check if color list has the same length as position data
    if len(positionx) == len(colour):
           axes[1].scatter(positionx, positiony,marker="o",color=colour)
            
    else:
            print("Warning: Number of position/theta data points does not match number of color points. Plotting without colors.")
            axes[1].plot(positionx, positiony) # Plot without colors
    axes[0].scatter(positionx, positiony,marker="o",color="black")
else:
    print("Error: Mismatch in the number of position and angle data points. Cannot plot vectors.\n")
    axes[1].clear() # Clear the plot


# Set plot title and labels
axes[0].set_xlabel("") # Added axis labels
axes[0].set_ylabel("")
axes[0].set_xticks([])
axes[0].set_yticks([])
axes[0].set_xlim(0,Lx)
axes[0].set_ylim(0,Ly)


axes[1].set_xlabel("") # Added axis labels
axes[1].set_ylabel("")
axes[1].set_xticks([])
axes[1].set_yticks([])
axes[1].set_xlim(0,Lx)
axes[1].set_ylim(0,Ly)

axes[0].annotate(label[0],size=40,xy=(0.05,0.95),xycoords="axes fraction")
axes[1].annotate(label[1],size=40,xy=(0.05,0.95),xycoords="axes fraction")

axes[1].arrow(
    18,         # x coordinate of the base
    3,         # y coordinate of the base
    0.9,              # length of the arrow along x
    -1.3,              # length of the arrow along y
    width=0.8,       # Thickness of the arrow body
    head_width=2.5,  # Width of the arrowhead
    head_length=1.5, # Length of the arrowhead
    fc='red',       # Fill color
    ec='red'    # Edge color
)
axes[1].arrow(
    17,         # x coordinate of the base
    27,         # y coordinate of the base
    1,              # length of the arrow along x
    1,              # length of the arrow along y
    width=0.8,       # Thickness of the arrow body
    head_width=2.5,  # Width of the arrowhead
    head_length=1.5, # Length of the arrowhead
    fc='red',       # Fill color
    ec='red'    # Edge color
)
line = plt.Line2D([0.003, 0.003], [0.006, 0.991], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)

#vertical 5
line = plt.Line2D([0.997,0.997], [0.006, 0.991], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)

#horizontal 4 (top=>bottom)
line = plt.Line2D([0.003, 0.997], [0.991, 0.991], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)

#horizontal 1
line = plt.Line2D([0.003, 0.997], [0.006,0.006], transform=fig.transFigure, color="black", linewidth=2)
fig.add_artist(line)
plt.tight_layout()
plt.subplots_adjust(left=0.007,bottom=0.014,right=0.993,top=0.986,wspace=0.048,hspace=0.2)
plt.show()

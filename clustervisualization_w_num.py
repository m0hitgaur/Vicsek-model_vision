import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns
import os

current_directory = os.getcwd()

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
current_noise=2
current_trial=80
current_time=9300   

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
colourlist = sns.color_palette("husl", max(len(distinct_ci), 1))
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
visit=np.zeros(len(cluster))
for k,i in enumerate(mass):
    for j,clus in enumerate(cluster):
        if(len(clus)==i and visit[j]==0):
            print(f"Cluster {n}: id:{j+1}  {i} agents   radius= {radius[k]}\n")
            visit[j]=1
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
            plt.quiver(positionx, positiony, vx, vy, angles='xy', scale_units='xy', color=colour, scale=1)
            for h,cii in enumerate(cl):
                plt.text(positionx[h], positiony[h], s=cii,  fontsize=4)
  
    else:
            print("Warning: Number of position/theta data points does not match number of color points. Plotting without colors.")
            plt.quiver(positionx, positiony, vx, vy, angles='xy', scale_units='xy', scale=1) # Plot without colors
else:
    print("Error: Mismatch in the number of position and angle data points. Cannot plot vectors.\n")
    plt.clear() # Clear the plot

# Set plot title and labels
plt.title(f"") # More descriptive title
plt.xlabel("") # Added axis labels
plt.ylabel("")
plt.xlim(0, Lx)
plt.ylim(0, Ly)
plt.show()

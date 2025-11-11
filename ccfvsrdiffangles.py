import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import product
import os

current_directory = os.getcwd()



# Parameters
r_to_plot = 1400  # Adjust this for different r steps
trial=0
noises=[0.05,0.1,0.5,1]
angles=[45,90,120,180]
numberofnoises=len(noises)
numberofangles=len(angles)

# Prepare the figure
fig, axes = plt.subplots(2,4, figsize=(20,10))
#fig.suptitle(f'Different Noises and Vision Angles for r : {r_to_plot}',y=1)

# Function to load data from files
def load_data(file_path):
    ccf = []
    r = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                t ,o = map(float, line.split())
                ccf.append(o)
                r.append(t)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except IOError:
        print(f"Error: An IOError occurred while opening the file '{file_path}'.")
        return None
    return ccf,r

colour=['black','maroon','midnightblue','green']

detail=[]
with open(current_directory+f'/Angle_{angles[0]}/Noise_{noises[0]}/parameters.txt', 'r') as file:
    for line in file:
        detail.append(line)
Length_of_box = float(detail[1])   # Size of the grid


# Loop through different trials to read data and create quiver plots
for i in range(0,numberofangles): 
        for j in range(0,numberofnoises):
            # Path templates
            path = current_directory+f'/Angle_{angles[i]}/Noise_{noises[j]}/correlation_data/connectedcorrelation_vs_r_{r_to_plot}_.dat'
            # Load connected correlation function vs r data
            ccf,r = load_data(path)

        
            
            # Plot
            ax = axes[0,i]
            ax.plot(r,ccf, color=colour[j], marker='')
            ax.set_title(f' Angles {angles[i]}')
            ax.set_xlabel('r')
            ax.set_ylabel('Connected correlation function')
            ax.set_xlim([0, Length_of_box/2])
            ax.set_yscale("log")


for j in range(0,numberofangles):
    for i in range(0,numberofnoises):
            # Path templates
            path = current_directory+f'/Angle_{angles[j]}/Noise_{noises[i]}/correlation_data/connectedcorrlength_vs_time.dat'
            # Load connected correlation function vs r data
            vcl,t = load_data(path)

            
            numberoftimesteps=int(detail[3])
            # Plot
            ax = axes[1,j]
            ax.plot(t,vcl, color=colour[i], marker=' ')
            ax.set_title(f' Angle {angles[j]}')
            ax.set_xlabel('time')
            ax.set_ylabel('Connected correlation length')
            ax.set_xlim([0,numberoftimesteps])
            ax.set_ylim([0, Length_of_box/2])
  

plt.tight_layout()
plt.show()
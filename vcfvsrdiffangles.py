import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import product
import os

current_directory = os.getcwd()



# Parameters
time_to_plot = 900  # Adjust this for different r steps
noises=[0.05,0.1,0.5,1]
angles=[45,90,120,180]
numberofnoises=len(noises)
numberofangles=len(angles)

# Prepare the figure
fig, axes = plt.subplots(2,3, figsize=(10, 10))
#fig.suptitle(f'Different Noises and Vision Angles for r : {time_to_plot}',y=1)

# Function to load data from files
def load_data(file_path):
    vcf = []
    r = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                t ,o = map(float, line.split())
                vcf.append(o)
                r.append(t)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except IOError:
        print(f"Error: An IOError occurred while opening the file '{file_path}'.")
        return None
    return vcf,r

colour=['black','maroon','midnightblue','blue']

detail=[]
with open(current_directory+f'/Angle_{angles[0]}/Noise_{noises[0]}/parameters.txt', 'r') as file:
    for line in file:
        detail.append(line)
Length_of_box = float(detail[1])   # Size of the grid
# Loop through different trials to read data and create quiver plots

for i in range(0,numberofnoises): 
    for j in range(0,numberofangles):
            # Path templates
            path = current_directory+f'/Angle_{angles[j]}/Noise_{noises[i]}/correlation data/velocitycorrelation_vs_r_{time_to_plot}_.dat'
            # Load connected correlation function vs r data
            vcf,r = load_data(path)

            

            
            # Plot
            ax = axes[0,i]
            ax.plot(r,vcf, color=colour[j], marker='o')
            ax.set_title(f'Noise {noises[i]}')
            ax.set_xlabel('r')
            ax.set_ylabel('Velocity correlation function')
            ax.set_xlim([0, Length_of_box/2])
   

for i in range(0,numberofnoises):
    for j in range(0,numberofangles):
            # Path templates
            path = current_directory+f'/Angle_{angles[j]}/Noise_{noises[i]}/correlation data/velocitycorrelationcorrlength_vs_time.dat'
            # Load connected correlation function vs r data
            vcl,t = load_data(path)


            numberoftimesteps=int(detail[3])
            
            # Plot
            ax = axes[1,i]
            ax.plot(t,vcl, color=colour[j], marker='o')
            ax.set_title(f'Noise {noises[i]}')
            ax.set_xlabel('time')
            ax.set_ylabel('Velocity correlation length')
            ax.set_xlim([0, numberoftimesteps])
            ax.set_ylim([0, Length_of_box/2])
   




plt.tight_layout()
plt.show()
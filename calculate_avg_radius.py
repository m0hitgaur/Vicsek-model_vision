import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
angles=["45","90","120","180"]
angles_rad=[r"$\pi/4$",r"$\pi/2$",r"$2\pi/3$",r"$\pi$"]
noises=["1","0.5","0.05"]
number_of_trials=100
number_of_timesteps=10000

times=[]
for t in range(0,number_of_timesteps):
    if(t<10):tf=1
    if(t>10):tf=10
    if(t>100):tf=50
    if(t>1000):tf=100
    if(t%tf==0):times.append(t)


fig,axes= plt.subplots(4,3,figsize=(10,10))

for i,current_angle in enumerate(angles):
    for j,current_noise in enumerate(noises):
        avg=np.zeros(len(times))
        for current_trial in range(number_of_trials):
            avg_temp=np.zeros(len(times))
            for t,current_time in enumerate(times):
                # --- Load Data ---
                path_template_mass = os.path.join(current_directory, f'Angle_{current_angle}', f'Noise_{current_noise}', 'cluster_index', f'radius_{current_trial}_{current_time}_.txt')
                radius_array=load_data(path_template_mass)
                r=radius_array.sum()/len(radius_array)
                avg_temp[t]=r
            avg+=avg_temp
        avg/=number_of_trials
        with open(os.path.join(current_directory, f'Angle_{current_angle}', f'Noise_{current_noise}', 'cluster_index', f'radius_vs_t_.txt'),"w") as f:
            for r,rad in enumerate(avg):
                f.write(f"{times[r]} {rad} \n")


        






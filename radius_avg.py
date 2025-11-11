import os
import numpy as np
import time
import math

# --- Configuration ---
# Assuming the script is in the same directory as fluctuationparameters.txt
# and the flockingdata folder is also in the same directory.

def load_data(path):
    data = []
    try:
        with open(path, 'r') as f:
            for line in f:
                data.append(float(line.strip()))
    except FileNotFoundError:
        print(f"Warning: File not found: {path}. Generating dummy data for demonstration.")
    except ValueError:
        print(f"Error: Invalid data (non-numeric) in file: {path}. Skipping this file.")
        return None
    return np.array(data)

current_directory = os.getcwd()
parameter_file_path = "fluctuationparameters.txt"
data_folder_name = "flockingdata"

noises=["1","0.5","0.05"]
angles=["180","120","90","45"]

# Extract parameters for clarity
number_of_agents = 2560
Lx = 32
Ly = 32
number_of_timesteps = 10000
number_of_trials = 100

print(f"System size = {Lx} x {Ly}")
print(f"Number of time steps = {number_of_timesteps}")
print(f"Number of agents = {number_of_agents}")
print(f"Total number of trials = {number_of_trials}")

# --- Determine Timesteps to Process (Mimics C++ logic) ---
# Note: The C++ code snippet you provided *only* adds timestep 5000
# to timearray if number_of_timesteps >= 5001.
# If you intend to process a range or interval of timesteps,
# you should modify this logic here.
# For now, we'll strictly follow the provided C++ loop structure.
timearray = []
for t in range(number_of_timesteps):
    # The C++ code had conditional time_interval logic but only pushed 5000
    if(t<10): time_interval=1
    if(t>10): time_interval=10
    if(t>100): time_interval=50
    if(t>1000): time_interval=100
    if (t%time_interval==0): # This condition strictly matches the C++ snippet's push_back
        timearray.append(t)

print(f"Processing the following timesteps: {timearray}")
if not timearray:
    print("Warning: No timesteps selected based on the current logic.")


# --- Main Processing Loop ---
start_time_total = time.time()
for noise in noises:
    for angle in angles:
        output_filename = current_directory+f"/Angle_{angle}/Noise_{noise}/cluster_index/radius.txt"  
        with open(output_filename, 'w') as xyz_file:        
            for current_timestep in timearray:
                radius_data=[]
                for trial in range(number_of_trials):
                    radius_filename = current_directory+f"/Angle_{angle}/Noise_{noise}/cluster_index/radius_{trial}_{current_timestep}_.txt"
                    rad = load_data(radius_filename)
                    if len(rad)>0:
                        radius_data.append(rad)
                    else:
                        radius_data.append([0])
                
                if len(radius_data)>0:
                    r=np.concatenate(radius_data).flatten()
                    xyz_file.write(f"{current_timestep} {r.sum()/len(r)}\n")
                else:
                    xyz_file.write(f"{current_timestep} {0}\n")

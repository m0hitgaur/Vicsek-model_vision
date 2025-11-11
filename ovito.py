import os
import numpy as np
import time
import math

# --- Configuration ---
# Assuming the script is in the same directory as fluctuationparameters.txt
# and the flockingdata folder is also in the same directory.
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
number_of_trials = 5

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
                
        for trial in range(number_of_trials):
            print(f"\nProcessing Trial number {trial}")
            start_time_trial = time.time()

            
                        # Loop through the selected timesteps
            for current_timestep in timearray:
                output_xyz_filename = current_directory+f"/Angle_{angle}/Noise_{noise}/xyz/flocking_trial_{trial}_{current_timestep}.xyz"
                try:
                    # Open the output XYZ file for the current trial
                    with open(output_xyz_filename, 'w') as xyz_file:

                        #print(f"  Processing timestep {current_timestep}...")

                        # Construct input file paths for the current trial and timestep
                        theta_filename = os.path.join(current_directory,f"Angle_{angle}/Noise_{noise}",data_folder_name, f"theta_{trial}_{current_timestep}_.dat")
                        posix_filename = os.path.join(current_directory,f"Angle_{angle}/Noise_{noise}",data_folder_name, f"positionx_{trial}_{current_timestep}_.dat")
                        posiy_filename = os.path.join(current_directory,f"Angle_{angle}/Noise_{noise}",data_folder_name, f"positiony_{trial}_{current_timestep}_.dat")

                        # --- Read Data for the current timestep ---
                        try:
                            # Using numpy to read data is efficient for large files
                            position_x = np.loadtxt(posix_filename)
                            position_y = np.loadtxt(posiy_filename)
                            theta = np.loadtxt(theta_filename)

                            if not (len(position_x) == number_of_agents and
                                    len(position_y) == number_of_agents and
                                    len(theta) == number_of_agents):
                                print(f"    Warning: Data file sizes don't match expected number of agents at timestep {current_timestep}. Skipping frame.")
                                continue # Skip this timestep if data is incomplete

                        except FileNotFoundError as e:
                            print(f"    Error: Input file not found at timestep {current_timestep}: {e}. Skipping frame.")
                            continue # Skip this timestep if files are missing
                        except Exception as e:
                            print(f"    Error reading data files at timestep {current_timestep}: {e}. Skipping frame.")
                            continue # Skip on other reading errors


                        # --- Write data to .xyz format ---

                        # Line 1: Number of particles
                        xyz_file.write(f"{number_of_agents}\n")

                        # Line 2: Comment line (include box dimensions for OVITO)
                        # OVITO understands 'Lattice="ax bx cx ay by cy az bz cz"'
                        # For a 2D box Lx x Ly, we can use (Lx, 0, 0), (0, Ly, 0), (0, 0, 1)
                        comment_line = f'Timestep: {current_timestep} Lattice="{Lx} 0 0 0 {Ly} 0 0 0 1" Properties=type:S:1:pos:R:3:orientation:R:1\n'
                        # Properties=type:S:1:pos:R:3 adds columns: Type (String, 1 char), Position (Real, 3 components)
                        # We add :orientation:R:1 for the theta angle as a Real with 1 component
                        xyz_file.write(comment_line)

                        # Subsequent lines: Particle data
                        for i in range(number_of_agents):
                            # Particle type (e.g., "Agent" or "Pt"), x, y, z (set z=0 for 2D), and theta
                            # Use fixed precision for coordinates
                            xyz_file.write(f"Agent {position_x[i]:.6f} {position_y[i]:.6f} 0.0 {theta[i]:.6f}\n")

                # The 'with open(...) as f:' syntax automatically closes the file

                except IOError as e:
                    print(f"Error writing to output file {output_xyz_filename}: {e}")
                    # Continue to the next trial or exit, depending on desired behavior
                    continue # Continue to next trial if writing fails for one


            finish_time_trial = time.time()
            print(f"Time taken to process trial {trial}: {finish_time_trial - start_time_trial:.2f} seconds")

# --- Finish ---
finish_time_total = time.time()
print(f"\nTotal time elapsed: {finish_time_total - start_time_total:.2f} seconds")
print("Conversion complete.")

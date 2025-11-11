
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import os
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib import rcParams

current_directory = os.getcwd()


#rcParams['text.usetex'] = True
#rcParams['text.latex.preamble'] = [r'\usepackage{lmodern}'] 
plt.rcParams['axes.linewidth'] = 2.0
plt.rcParams["legend.labelspacing"]=0.1
#plt.rc_context({"xtick.major.pad": 8})
#plt.rc_context({"ytick.major.pad": 5})
plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)
#plt.rc('legend',fontsize=30)
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



# Function to load data from files
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

# Define simulation parameters and constants
angles=["45","90","120","180"]
angles_rad=[r"$\pi/4$",r"$\pi/2$",r"$2\pi/3$",r"$\pi$"] # LaTeX formatted angles for labels
noises=["1","0.5","0.05"]
number_of_trials=100
times=[4000,5000,6000,7000]
alpha_scaling = 1.5
length_factors = [1.82**(-alpha_scaling), 3.41**(-alpha_scaling), 9.33**(-alpha_scaling), 19.75**(-alpha_scaling)]


# Set a visually appealing style for Seaborn plots
sns.set_theme(style="dark", palette="deep") # 'whitegrid' provides a grid, 'deep' is a good default color palette
sns.set_context("paper")
sns.set_palette("colorblind")

# Create a figure and two subplots (axes) to display the plots side-by-side
# Increased figure size for better readability of two plots
fig, axes = plt.subplots(1, 2, figsize=(8, 3.5)) 

# --- Plot 1: Mass Distribution for Different Noises (Fixed Angle = 180) ---
# This loop iterates through different noise levels to plot their mass distributions.
for j, current_noise in enumerate(noises):
    avgmass = []
    for current_trial in range(number_of_trials):
        for t, current_time in enumerate(times):
            # Construct the file path for the mass data for the current trial, time, and noise
            path_template_mass = os.path.join(current_directory, f'Angle_180', f'Noise_{current_noise}', 'cluster_index', f'mass_{current_trial}_{current_time}_.txt')
            mass = load_data(path_template_mass)
            if mass is not None:
                avgmass.append(mass)

    if avgmass: 
        # Concatenate all mass arrays and flatten them into a single array
        avg = np.concatenate(avgmass).flatten()
        frequency, bin_edges = np.histogram(avg, bins=50)
        x_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:]) # Calculate the center of each bin
        frequency = frequency.astype(float)
        frequency /= frequency.sum() # Normalize the frequency so that the sum of all frequencies is 1
        sns.lineplot(x=x_centers, y=frequency, ax=axes[0], label=r"$\eta =$" + current_noise, linewidth=2)

# --- Plot 2: Mass Distribution for Different Angles (Fixed Noise = 0.5) ---

# This loop iterates through different angles to plot their mass distributions.
for j, current_angle in enumerate(angles):
    avgmass = []
    for current_trial in range(number_of_trials):
        for t, current_time in enumerate(times):
            # Construct the file path for the mass data for the current trial, time, and angle
            path_template_mass = os.path.join(current_directory, f'Angle_{current_angle}', f'Noise_0.5', 'cluster_index', f'mass_{current_trial}_{current_time}_.txt')
            mass = load_data(path_template_mass)
            if mass is not None:
                avgmass.append(mass)
    
    if avgmass:
        # Concatenate all mass arrays and flatten them
        avg = np.concatenate(avgmass).flatten()
        
        # Calculate the histogram manually
        frequency, bin_edges = np.histogram(avg, bins=50)
        x_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        
        frequency = frequency.astype(float)
        frequency /= frequency.sum() # Normalize frequency

        # Apply the specific scaling factor from `length_factors` as in the original code
        frequency_scaled = frequency * length_factors[j]
        
        # Write the unscaled frequency data to a file, as per the original script
        with open(f"hist_{current_angle}.txt","w") as file:
            for i, f_val in enumerate(frequency): # Note: original writes unscaled frequency
                file.write(f"{x_centers[i]} {f_val} \n")

        # Use Seaborn's `lineplot` to plot the scaled histogram data
        sns.lineplot(x=x_centers, y=frequency_scaled, ax=axes[1], label=r"$\alpha =$" + angles_rad[j], linewidth=1.5)


#********************************Customise*******************************************************

# First subplot

#axes[0].set_title(r'Avg. cluster mass Distribution for $\alpha = \pi$', fontsize=16)
axes[0].set_xlabel('Avg. Cluster Mass', fontsize=14)
axes[0].set_ylabel('Normalized Frequency (log)', fontsize=14)
axes[0].set_ylim(0.0005, 1) # Set Y-axis limits, adjusted for log scale visibility
#axes[0].set_xscale("log") # Set X-axis to logarithmic scale
axes[0].set_yscale("log") # Set Y-axis to logarithmic scale
axes[0].legend( fontsize=12, title_fontsize=13)
axes[0].tick_params(left=True, top=True ,right=True)
axes[0].tick_params(axis="x", direction="in")
axes[0].tick_params(axis="y", direction="in")
axes[0].xaxis.set_major_locator(MultipleLocator(500))
axes[0].xaxis.set_minor_locator(MultipleLocator(100))
#axes[0].yaxis.set_major_locator(MultipleLocator(0.00))
#axes[0].yaxis.set_minor_locator(MultipleLocator(0.1))
axes[0].tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True)
axes[0].tick_params(which='minor', direction="in", length=2, color="black",left=True,bottom=True,right=True,top=True)
axes[0].tick_params(which='major', direction="in", length=4, color="black",left=True,bottom=True,right=True,top=True)

# Add an annotation within the plot, similar to the original code
axes[0].annotate(r"$\alpha =\pi$", size=16, xy=(0.45, 0.9), xycoords="axes fraction")


# Second subplot

#axes[1].set_title(r'Mass Distribution for $\eta = 0.5$', fontsize=16)
axes[1].set_xlabel('Avg. Cluster Mass', fontsize=14)
#axes[1].set_ylabel('Scaled Normalized Frequency', fontsize=14)
#axes[1].set_xscale("log") # Set X-axis to logarithmic scale
axes[1].set_yscale("log") # Set Y-axis to logarithmic scale
#axes[1].legend(title=r'Angle ($\alpha$)', fontsize=12, title_fontsize=13)
axes[1].legend( fontsize=12, title_fontsize=13)
axes[1].annotate(r"$\eta = 0.5$", size=16, xy=(0.4, 0.9), xycoords="axes fraction")
axes[1].tick_params(left=True, top=True ,right=True)
axes[1].tick_params(axis="x", direction="in")
axes[1].tick_params(axis="y", direction="in")
axes[1].xaxis.set_major_locator(MultipleLocator(100))
axes[1].xaxis.set_minor_locator(MultipleLocator(50))
#axes[1].yaxis.set_major_locator(MultipleLocator(0.2))
#axes[1].yaxis.set_minor_locator(MultipleLocator(0.1))
axes[1].tick_params(which='minor', direction="in", length=2, color="black",left=True,bottom=True,right=True,top=True)
axes[1].tick_params(which='major', direction="in", length=4, color="black",left=True,bottom=True,right=True,top=True)


# Adjust the layout to prevent titles and labels from overlapping
plt.tight_layout()

# Display the plot
plt.show()


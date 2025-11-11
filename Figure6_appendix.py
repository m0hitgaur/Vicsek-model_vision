
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
#plt.rcParams['axes.linewidth'] = 2.0
#plt.rcParams["legend.labelspacing"]=0.1
plt.rcParams["font.weight"]=700
#plt.rc_context({"xtick.major.pad": 8})
#plt.rc_context({"ytick.major.pad": 5})
plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)
#plt.rc('legend',fontsize=30)
plt.rcParams["font.family"] = "serif"
plt.rcParams['mathtext.fontset'] ="cm"
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
#plt.rcParams['xtick.major.size'] = 10
#plt.rcParams['xtick.major.width'] = 2
#plt.rcParams['xtick.minor.size'] = 5
#plt.rcParams['xtick.minor.width'] = 1.5
#plt.rcParams['ytick.major.size'] = 10
#plt.rcParams['ytick.major.width'] = 2
#plt.rcParams['ytick.minor.size'] = 5
#plt.rcParams['ytick.minor.width'] = 1.5
#plt.rcParams["legend.handlelength"] = 1.0
#plt.rcParams["legend.handletextpad"] = 0.2
#plt.rcParams["legend.loc"]="lower left"

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

N=2560
number_of_bins=100
bins=np.linspace(20,2560,number_of_bins+1)
binsize=bins[1]-bins[0]
x_centers = 0.5 * (bins[:-1] + bins[1:]) # center of each bin

# Define simulation parameters 
angles=["45","90","120","180"]
angles_rad=[r"$\pi/4$",r"$\pi/2$",r"$2\pi/3$",r"$\pi$"]
noises=["2","0.5","0.05"]
noise_to_plot=noises[0]
number_of_trials=100
times=[6000,7000,8000,9000]
label=[r"$(a)$",r"$(b)$",r"$(c)$"]
alpha_scaling = 1.5
length_factors = [122.9**(-alpha_scaling), 101.4**(-alpha_scaling), 88.4**(-alpha_scaling), 79.3**(-alpha_scaling)]
markers=["<","o","^","s"]

sns.set_theme(style="white") # 'whitegrid' provides a grid, 'deep' is a good default color palette
sns.set_context("paper")
sns.set_palette("colorblind")

#fig, axd = plt.subplot_mosaic([[ 'right','upper left'],[ 'right','lower left']],figsize=(8, 4), layout="constrained") 
fig, axes = plt.subplots(1,2,figsize=(8,4))



# --- Plot 1---

for j, current_noise in enumerate(noises):
    avgmass = []
    for current_trial in range(number_of_trials):
        for t, current_time in enumerate(times):
            path_template_mass = os.path.join(current_directory, f'Angle_180', f'Noise_{current_noise}', 'cluster_index', f'mass_{current_trial}_{current_time}_.txt')
            mass,b =np.histogram(load_data(path_template_mass),bins=bins)
            if mass is not None:
                avgmass.append(mass)
    

    if avgmass: 
        frequency=np.zeros(number_of_bins)
        for m in avgmass:
            frequency+=m
        frequency/=len(avgmass)
        frequency = frequency.astype(float)
        frequency /= frequency.sum()*25 
        axes[1].plot(x_centers, frequency, label=r"$\eta ={}$ $" + current_noise+r"$", marker=markers[j],markerfacecolor="None")


# --- Plot 2---

for j, current_noise in enumerate(noises):
    avgmass = []
    for current_trial in range(number_of_trials):
        for t, current_time in enumerate(times):
            path_template_mass = os.path.join(current_directory, f'Angle_90', f'Noise_{current_noise}', 'cluster_index', f'mass_{current_trial}_{current_time}_.txt')
            mass,b =np.histogram(load_data(path_template_mass),bins=bins)
            if mass is not None:
                avgmass.append(mass)
    

    if avgmass: 
        frequency=np.zeros(number_of_bins)
        for m in avgmass:
            frequency+=m
        frequency/=len(avgmass)
        frequency = frequency.astype(float)
        frequency /= frequency.sum()*25 
        axes[0].plot(x_centers, frequency, label=r"$\eta ={}$ $" + current_noise+r"$", marker=markers[j],markerfacecolor="None")





#********************************Customise*******************************************************

# First subplot
n1=0
#axes[0].set_title(r'Avg. cluster mass Distribution for $\alpha = \pi$', fontsize=16)
#axes[0].set_xlabel(r'$m_{c}$', fontsize=25)
#axes[0].set_ylabel(r'$P(m_{c})$', fontsize=25)
axes[0].annotate(r"$m_c$", size=25, xy=(0.4, -0.06), xycoords="axes fraction")
axes[0].annotate(r"$P(m_c)$", size=25, xy=(-0.3, 0.5), xycoords="axes fraction")

#axes[0].set_ylim(0.000005, 1) # Set Y-axis limits, adjusted for log scale visibility
axes[0].set_xscale("log") # Set X-axis to logarithmic scale
axes[0].set_yscale("log") # Set Y-axis to logarithmic scale
axes[0].tick_params(axis="x", direction="in",labelsize=15)
axes[0].tick_params(axis="y", direction="in",labelsize=15)
#axes[0].xaxis.set_major_locator(MultipleLocator(500))
#axes[0].xaxis.set_minor_locator(MultipleLocator(100))
#axes[0].yaxis.set_major_locator(MultipleLocator(0.00))
#axes[0].yaxis.set_minor_locator(MultipleLocator(0.1))
axes[0].tick_params(which='minor', direction="in", length=4, color="black",left=True,bottom=True,right=True,top=True)
axes[0].tick_params(which='major', direction="in", length=8, color="black",left=True,bottom=True,right=True,top=True)

axes[0].annotate(r"$\alpha =\pi$", size=25, xy=(0.35, 0.9), xycoords="axes fraction")
axes[0].annotate(label[0],size=20,xy=(0.8,0.9),xycoords="axes fraction")

axes[0].legend(prop={'size': 18},labelspacing = 0.1,frameon=False,bbox_to_anchor=(0.4, 0.25, 0.3, 0.15))



# second subplot

#axes.set_title(r'Avg. cluster mass Distribution for $\alpha = \pi$', fontsize=16)
#axes[1].set_xlabel(r'$m_{c}$', fontsize=25)
axes[1].annotate(r"$m_c$", size=25, xy=(0.4, -0.06), xycoords="axes fraction")
#axes[1].set_ylabel(r'$P(m_{c})$', fontsize=25)
#axes.set_ylim(0.000005, 1) # Set Y-axis limits, adjusted for log scale visibility
axes[1].set_xscale("log") # Set X-axis to logarithmic scale
axes[1].set_yscale("log") # Set Y-axis to logarithmic scale
axes[1].tick_params(axis="x", direction="in",labelsize=15)
axes[1].tick_params(axis="y", direction="in",labelsize=15)
#axes[1].xaxis.set_major_locator(MultipleLocator(500))
#axes[1].xaxis.set_minor_locator(MultipleLocator(100))
#axes[1].yaxis.set_major_locator(MultipleLocator(0.00))
#axes[1].yaxis.set_minor_locator(MultipleLocator(0.1))

axes[1].tick_params(which='minor', direction="in", length=4, color="black",left=True,bottom=True,right=True,top=True)
axes[1].tick_params(which='major', direction="in", length=8, color="black",left=True,bottom=True,right=True,top=True)

axes[1].annotate(r"$\alpha =\pi/2$", size=25, xy=(0.3, 0.9), xycoords="axes fraction")
axes[1].annotate(label[1],size=20,xy=(0.8,0.9),xycoords="axes fraction")

#axes[1].legend(prop={'size': 18},labelspacing = 0.1,frameon=False,bbox_to_anchor=(0.4, 0.25, 0.3, 0.15))




plt.tight_layout()
# Display the plot
plt.show()


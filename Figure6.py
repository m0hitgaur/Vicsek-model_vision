
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import os
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib import rcParams
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
current_directory = os.getcwd()


#rcParams['text.usetex'] = True
#rcParams['text.latex.preamble'] = [r'\usepackage{lmodern}'] 
plt.rcParams['axes.linewidth'] = 2.0
#plt.rcParams["legend.labelspacing"]=0.1
#plt.rcParams["font.weight"]=700
#plt.rc_context({"xtick.major.pad": 8})
#plt.rc_context({"ytick.major.pad": 5})
plt.rc('xtick',labelsize=25)
plt.rc('ytick',labelsize=25)
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
noises_str=["2.0","0.5","0.05"]
noises=["2","0.5","0.05"]
noise_to_plot=noises[2]
number_of_trials=100
times=[6000,7000,8000,9000]
label=[r"$(a)$",r"$(b)$",r"$(c)$"]
markers=["<","o","^","s"]

sns.set_theme(style="white") # 'whitegrid' provides a grid, 'deep' is a good default color palette
sns.set_context("paper")
sns.set_palette("colorblind")

#fig, axd = plt.subplot_mosaic([[ 'right','upper left'],[ 'right','lower left']],figsize=(8, 4), layout="constrained") 
fig, axd = plt.subplots(1,3,figsize=(12,4))
axes=[]

for  ax in axd:
    axes.append(ax)

# --- Plot 1---

ax_in=inset_axes(axes[0], width="65%", height="65%", loc="lower left",bbox_to_anchor=(0.11, .05, .71, .5),bbox_transform=axes[0].transAxes)

for j, current_noise in enumerate(noises):
    avgmass = []
    for current_trial in range(number_of_trials):
        for t, current_time in enumerate(times):
            path_template_mass = os.path.join(current_directory, f'Angle_45', f'Noise_{current_noise}', 'cluster_index', f'mass_{current_trial}_{current_time}_.txt')
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
        axes[0].plot(x_centers, frequency, label=r"$\eta =$ $" + noises_str[j]+r"$", marker=markers[j],markerfacecolor="None")

#Inset
avgmass = []
for current_trial in range(number_of_trials):
    for t, current_time in enumerate(times):
        path_template_mass = os.path.join(current_directory, f'Angle_45', f'Noise_{noises[0]}', 'cluster_index', f'mass_{current_trial}_{current_time}_.txt')
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
    ax_in.plot(x_centers, frequency, marker=markers[0],markerfacecolor="None")
    #ax_in.tick_params(axis='x', labelbottom=False)
    #ax_in.tick_params(axis='y', labelleft=False)

ax_in.set_yscale("log")
ax_in.tick_params(which='minor', direction="in", length=1.5, color="black",left=True,bottom=True,right=True,top=True)
ax_in.tick_params(which='major', direction="in", length=3, color="black",left=True,bottom=True,right=True,top=True)
ax_in.set_xlim(25,850)
ax_in.annotate(r"$\eta=2.0$",xycoords="axes fraction",xy=(0.4,0.7),size=18)
ax_in.xaxis.set_major_locator(MultipleLocator(200))
ax_in.xaxis.set_minor_locator(MultipleLocator(50))
ax_in.tick_params(axis='y', which='major', pad=1)

# --- Plot 2 ---

alpha_scaling = 1.5
length_factors = [122.9**(-alpha_scaling), 101.4**(-alpha_scaling), 88.4**(-alpha_scaling), 79.3**(-alpha_scaling)]
for j, current_angle in enumerate(angles):
    avgmass = []
    for current_trial in range(number_of_trials):
        for t, current_time in enumerate(times):
            path_template_mass = os.path.join(current_directory, f'Angle_{current_angle}', f'Noise_{noises[2]}', 'cluster_index', f'mass_{current_trial}_{current_time}_.txt')
            mass,b =np.histogram(load_data(path_template_mass),bins=bins)
            if mass is not None:
                avgmass.append(mass)
    
    if avgmass:
        frequency=np.zeros(number_of_bins)
        for m in avgmass:
            frequency+=m
        frequency/=len(avgmass)
        frequency = frequency.astype(float)
        frequency /= frequency.sum() *25

        frequency_scaled = frequency * length_factors[j]
        
#        with open(f"hist_{current_angle}.txt","w") as file:
#            for i, f_val in enumerate(frequency): 
#                file.write(f"{x_centers[i]} {f_val} \n")    
        
        axes[1].plot(x_centers, frequency, label=r"$\alpha =$" + angles_rad[j],marker=markers[j],markerfacecolor="None")


# --- Plot 3 ---


alpha_scaling = 1.5
length_factors = [89.5**(-alpha_scaling), 83.9**(-alpha_scaling), 73.1**(-alpha_scaling), 75.8**(-alpha_scaling)]

for j, current_angle in enumerate(angles):
    avgmass = []
    for current_trial in range(number_of_trials):
        for t, current_time in enumerate(times):
            path_template_mass = os.path.join(current_directory, f'Angle_{current_angle}', f'Noise_{noises[1]}', 'cluster_index', f'mass_{current_trial}_{current_time}_.txt')
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

        frequency_scaled = frequency * length_factors[j]
        
        with open(f"hist_{current_angle}.txt","w") as file:
            for i, f_val in enumerate(frequency): 
                file.write(f"{x_centers[i]} {f_val} \n")    
        
        axes[2].plot(x_centers, frequency, label=r"$\alpha =$" + angles_rad[j],marker=markers[j],markerfacecolor="None")

#********************************Customise*******************************************************

# First subplot
n1=0
#axes[n1].set_title(r'Avg. cluster mass Distribution for $\alpha = \pi$', fontsize=16)
#axes[n1].set_xlabel(r'$m_{c}$', fontsize=25)
axes[n1].annotate(r"$m_c$", size=25, xy=(0.45, -0.1), xycoords="axes fraction")
axes[n1].annotate(r"$P(m_c)$", size=25, xy=(-0.32, 0.48), xycoords="axes fraction")

#axes[n1].set_ylabel(r'$P(m_{c})$', fontsize=25)
axes[n1].set_xlim(25, 2000) 
axes[n1].set_xscale("log")
axes[n1].set_yscale("log")
axes[n1].tick_params(axis="x", direction="in",labelsize=15)
axes[n1].tick_params(axis="y", direction="in",labelsize=15)
#axes[n1].xaxis.set_major_locator(MultipleLocator(500))
#axes[n1].xaxis.set_minor_locator(MultipleLocator(100))
#axes[n1].yaxis.set_major_locator(MultipleLocator(0.00))
#axes[n1].yaxis.set_minor_locator(MultipleLocator(0.1))
axes[n1].tick_params(which='minor', direction="in", length=4, color="black",left=True,bottom=True,right=True,top=True)
axes[n1].tick_params(which='major', direction="in", length=8, color="black",left=True,bottom=True,right=True,top=True)

axes[n1].annotate(r"$\alpha =\pi/4$", size=20, xy=(0.4, 0.9), xycoords="axes fraction")
axes[n1].annotate(label[0],size=23,xy=(0.83,0.9),xycoords="axes fraction")

axes[n1].legend(prop={'size': 13},labelspacing= 0,frameon=False,bbox_to_anchor=(0.5, 0.64))






# Third subplot
n2=1
#axes[n2].set_title(r'Mass Distribution for $\eta = 0.5$', fontsize=16)
#axes[n2].set_xlabel(r'$m_{c}$', fontsize=25)
#axes[n2].set_ylabel(r'$P(m_c)$', fontsize=14)
axes[n2].annotate(r"$m_c$", size=25, xy=(0.45, -0.1), xycoords="axes fraction")
axes[n2].set_xscale("log") # Set X-axis to logarithmic scale
axes[n2].set_yscale("log") # Set Y-axis to logarithmic scale
axes[n2].legend(prop={'size': 15},labelspacing = 0.1,frameon=False,bbox_to_anchor=(0.4, 0.3, 0.15, 0.2))
#axes[n2].set_ylim(0.0000001,0.003)
#axes[n2].set_xlim(0,2500)
axes[n2].annotate(r"$\eta = "+f"{noises_str[2]}$", size=20, xy=(0.4, 0.9), xycoords="axes fraction")
axes[n2].tick_params(axis="x", direction="in",labelsize=15)
axes[n2].tick_params(axis="y", direction="in",labelsize=15)
#axes[n2].xaxis.set_major_locator(MultipleLocator(25))
#axes[n2].xaxis.set_minor_locator(MultipleLocator(12.5))
#axes[n2].yaxis.set_major_locator(MultipleLocator(0.2))
#axes[n2].yaxis.set_minor_locator(MultipleLocator(0.1))
axes[n2].tick_params(which='minor', direction="in", length=4, color="black",left=True,bottom=True,right=True,top=True)
axes[n2].tick_params(which='major', direction="in", length=8, color="black",left=True,bottom=True,right=True,top=True)
axes[n2].annotate(label[n2],size=23,xy=(0.83,0.9),xycoords="axes fraction")



# Second subplot
n3=2
#axes[n3].set_title(r'Mass Distribution for $\eta = 0.5$', fontsize=16)
#axes[n3].set_xlabel(r'$m_{c}$', fontsize=25)
#axes[n3].set_ylabel(r'$P(m_c)$', fontsize=14)
axes[n3].annotate(r"$m_c$", size=25, xy=(0.45, -0.1), xycoords="axes fraction")
axes[n3].set_xscale("log") # Set X-axis to logarithmic scale
axes[n3].set_yscale("log") # Set Y-axis to logarithmic scale
axes[n3].legend(prop={'size': 15},labelspacing = 0.1,frameon=False,bbox_to_anchor=(0.4, 0.3, 0.15, 0.2))
#axes[n3].set_ylim(0.0000001,0.003)
#axes[n3].set_xlim(0,2500)
axes[n3].annotate(r"$\eta = "+f"{noises[1]}$", size=20, xy=(0.4, 0.9), xycoords="axes fraction")
axes[n3].tick_params(axis="x", direction="in",labelsize=15)
axes[n3].tick_params(axis="y", direction="in",labelsize=15)
#axes[n3].xaxis.set_major_locator(MultipleLocator(25))
#axes[n3].xaxis.set_minor_locator(MultipleLocator(12.5))
#axes[n3].yaxis.set_major_locator(MultipleLocator(0.2))
#axes[n3].yaxis.set_minor_locator(MultipleLocator(0.1))
axes[n3].tick_params(which='minor', direction="in", length=4, color="black",left=True,bottom=True,right=True,top=True)
axes[n3].tick_params(which='major', direction="in", length=8, color="black",left=True,bottom=True,right=True,top=True)
axes[n3].annotate(label[n3],size=23,xy=(0.83,0.9),xycoords="axes fraction")


x_=np.linspace(40,200,1000)
#axes[n2].plot(x_,(0.01*x_**(-alpha_scaling)),linestyle="--",color="black")
#axes[n2].annotate(r"$ m_{c}^{-3/2} $",size=15,xy=(0.4,0.8),xycoords="axes fraction")

#axes[n3].plot(x_,(0.01*x_**(-alpha_scaling)),linestyle="--",color="black")
#axes[n3].annotate(r"$ m_{c}^{-3/2} $",size=15,xy=(0.4,0.8),xycoords="axes fraction")


x__=np.linspace(100,300,100)
axes[n1].plot(x__,(20*x__**(-1.8)),linestyle="--",color="black")
axes[n1].annotate(r"$ m_{c}^{-9/5} $",size=15,xy=(0.33,0.78),xycoords="axes fraction")


plt.subplots_adjust(left=0.085,bottom=0.133,right=0.971,top=0.964,wspace=0.205,hspace=0.2)


plt.savefig('fig6.pdf', format='pdf',bbox_inches='tight')
# Display the plot
plt.show()


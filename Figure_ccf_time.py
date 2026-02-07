
import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import product
import os
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib import rcParams
import seaborn as sns
current_directory = os.getcwd()



# Parameters
markers=["o","s","^"]
label=["(a)","(b)","(c)","(d)","(e)","(f)"]
noises=[0.05,2]
noise_str=["005","2"]
angles=[45,180]
time=[10,100,1000,5000]
label_size=25
angles_rad=[r"$\pi/4$",r"$\pi$"]
numberofnoises=len(noises)
numberofangles=len(angles)
noises_str=[r"$0.05$",r"$2.0$"]
numberofnoises=len(noises)
numberofangles=len(angles)
sns.set_theme(style="white") # 'whitegrid' provides a grid, 'deep' is a good default color palette
sns.set_context("paper")

#rcParams['text.usetex'] = True
#rcParams['text.latex.preamble'] = [r'\usepackage{lmodern}'] 
plt.rcParams['axes.linewidth'] = 2.0
plt.rcParams["legend.labelspacing"]=0.1
#plt.rc_context({"xtick.major.pad": 8})
#plt.rc_context({"ytick.major.pad": 5})
plt.rc('xtick',labelsize=25)
plt.rc('ytick',labelsize=25)
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



fig, axes = plt.subplots(2,2, figsize=(10,10))


# Function to load data from files
def load_data(file_path):
    ccf = []
    r = []
    
    with open(file_path, 'r') as file:
        for line in file:
            t ,o = map(float, line.split())
            ccf.append(o)
            r.append(t)

    return ccf,r

colour_time=['black','darkgreen','royalblue','salmon']
colour_angle=['black','darkgreen','royalblue','salmon']
markers=["o","s","^","v"]

detail=[]
with open(current_directory+f'/Angle_{angles[0]}/Noise_{noises[0]}/parameters.txt', 'r') as file:
    for line in file:
        detail.append(line)
Length_of_box = float(detail[1])   # Size of the grid


timetoplot=3
n=1 #noise 

for i in range(len(time)):
    path = current_directory+f'/Angle_{angles[0]}/Noise_{noises[0]}/correlation_data/connectedcorrelation_vs_r_{time[i]}_.dat'
    if(i==3):
        path = current_directory+f'/Figure/correlation/ccf_vs_r_{int(angles[0])}_{noise_str[0]}.dat'
    # Load connected correlation function vs r data
    ccf,r = load_data(path)
    ax=axes[0,0]
    ax.plot(r,ccf,c=colour_time[i], marker=markers[i],markerfacecolor="none", markeredgecolor=colour_time[i],label="$t=$"+f"{time[i]}")
    #ax.legend(loc="best", prop={'size': 11},labelspacing = 0.2,frameon=False,bbox_to_anchor=(0.5, 0.35, 0.5, 0.5))
    ax.set_xlim(0,Length_of_box/2)
    #ax.set_xlabel('$r$',fontsize=25)
    ax.plot(r,ccf,c=colour_time[i], marker=markers[i],markerfacecolor="none")
    ax.annotate(r"$\eta =$"+noises_str[0],size=25,xy=(0.55,0.85),xycoords="axes fraction")
    ax.annotate(r"$\alpha =$"+angles_rad[0],size=25,xy=(0.55,0.775),xycoords="axes fraction")    
    ax.annotate(label[0],size=label_size,xy=(0.06,0.07),xycoords="axes fraction")
    ax.annotate(r'$C_{\delta v}(r)$',size=30,xy=(-0.3,0.4),xycoords="axes fraction",rotation=90)
    
    #ax.set_ylabel(r'$C_{\delta v}(r)$',fontsize=30)
    ax.tick_params(left=True, top=True ,right=True)
    ax.tick_params(axis="x", direction="in")
    ax.tick_params(axis="y", direction="in")
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True,left=True,bottom=True)
    ax.tick_params(which='major', direction="in", length=6, color="black",right=True,top=True,left=True,bottom=True)



for i in range(len(time)):
    path = current_directory+f'/Angle_{angles[0]}/Noise_{noises[1]}/correlation_data/connectedcorrelation_vs_r_{time[i]}_.dat'
    if(i==3):
        path = current_directory+f'/Figure/correlation/ccf_vs_r_{int(angles[0])}_{noise_str[1]}.dat'
    # Load connected correlation function vs r data
    ccf,r = load_data(path)
    ax=axes[1,0]
    #ax.set_xlabel('$r$',fontsize=25)
    ax.plot(r,ccf,c=colour_time[i], marker=markers[i],markerfacecolor="none", markeredgecolor=colour_time[i],label="$t=$"+f"{time[i]}")
    ax.annotate("$\eta =$"+noises_str[1],size=25,xy=(0.6,0.85),xycoords="axes fraction")
    ax.annotate(label[2],size=label_size,xy=(0.02,0.07),xycoords="axes fraction")
    ax.annotate(r"$\alpha =$"+angles_rad[0],size=25,xy=(0.6,0.775),xycoords="axes fraction")    
    ax.legend( prop={'size': 24},labelspacing = 0.2,frameon=False,bbox_to_anchor=(0.55, 0.25, 0.5, 0.5))
    ax.set_xlabel('$r$',fontsize=30)
    #ax.set_ylabel(r'$C_{\delta v}(r)$',fontsize=30)    
    ax.annotate(r'$C_{\delta v}(r)$',size=30,xy=(-0.3,0.4),xycoords="axes fraction",rotation=90)
    ax.set_xlim(0,Length_of_box/2)
    ax.tick_params(left=True, top=True ,right=True,bottom=True)
    ax.tick_params(axis="x", direction="in")
    ax.tick_params(axis="y", direction="in")
    #for ticks 
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True,left=True,bottom=True)
    ax.tick_params(which='major', direction="in", length=6, color="black",right=True,top=True,left=True,bottom=True)


for i in range(len(time)):
    path = current_directory+f'/Angle_{angles[1]}/Noise_{noises[0]}/correlation_data/connectedcorrelation_vs_r_{time[i]}_.dat'
    #if(i==3):
    #    path = current_directory+f'/Figure/correlation/vcf_vs_r_{int(angles[1])}_{noise_str[0]}.dat'
    # Load connected correlation function vs r data
    ccf,r = load_data(path)
    ax=axes[0,1]
    #ax.set_xlabel('$r$',fontsize=30)
    ax.plot(r,ccf,c=colour_time[i], marker=markers[i],markerfacecolor="none", markeredgecolor=colour_time[i],label="$t=$"+f"{time[i]}")
    ax.annotate(r"$\eta =$"+noises_str[0],size=25,xy=(0.6,0.85),xycoords="axes fraction")
    ax.annotate(label[1],size=label_size,xy=(0.06,0.07),xycoords="axes fraction")
    ax.annotate(r"$\alpha =$"+angles_rad[1],size=25,xy=(0.6,0.775),xycoords="axes fraction")    
    ax.set_xlim(0,Length_of_box/2)
    ax.set_ylim(-0.2,1.05)
    ax.tick_params(left=True, top=True ,right=True)
    ax.tick_params(axis="x", direction="in")
    ax.tick_params(axis="y", direction="in")
    #for ticks 
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True,left=True,bottom=True)
    ax.tick_params(which='major', direction="in", length=6, color="black",right=True,top=True,left=True,bottom=True)

for i in range(len(time)):
    path = current_directory+f'/Angle_{angles[1]}/Noise_{noises[1]}/correlation_data/connectedcorrelation_vs_r_{time[i]}_.dat'
    #if(i==3):
    #    path = current_directory+f'/Figure/correlation/vcf_vs_r_{int(angles[1])}_{noise_str[1]}.dat'
    # Load connected correlation function vs r data
    ccf,r = load_data(path)
    ax=axes[1,1]
    ax.set_xlabel('$r$',fontsize=30)
    ax.plot(r,ccf,c=colour_time[i], marker=markers[i],markerfacecolor="none", markeredgecolor=colour_time[i],label="$t=$"+f"{time[i]}")
    ax.annotate("$\eta =$"+noises_str[1],size=25,xy=(0.6,0.85),xycoords="axes fraction")
    ax.annotate(label[3],size=label_size,xy=(0.06,0.07),xycoords="axes fraction")
    ax.annotate(r"$\alpha =$"+angles_rad[1],size=25,xy=(0.6,0.775),xycoords="axes fraction")    
    #ax.set_xlabel('$r$',fontsize=20)
    ax.set_xlim(0,Length_of_box/2)
    ax.tick_params(left=True, top=True ,right=True)
    ax.tick_params(axis="x", direction="in")
    ax.tick_params(axis="y", direction="in")
    #for ticks 
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True,left=True,bottom=True)
    ax.tick_params(which='major', direction="in", length=6, color="black",right=True,top=True,left=True,bottom=True)
plt.tight_layout()
plt.savefig('fig4_appendix.pdf', format='pdf',bbox_inches='tight')

#plt.legend()

plt.show()



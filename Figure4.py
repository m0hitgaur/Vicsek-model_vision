
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
noises=[0.05,0.5,2]
angles=[45,90,120,180]
label_size=25
x_label_size=30
y_label_size=30
Fit=False
time=[10,100,500,5000]
angles_rad=[r"$\pi/4$",r"$\pi/2$",r"$2\pi/3$",r"$\pi$"]
numberofnoises=len(noises)
numberofangles=len(angles)
noises_str=[r"$0.05$",r"$0.5$",r"$2.0$"]
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
plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)
plt.rc('legend',fontsize=20)
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



fig, axes = plt.subplots(2,2, figsize=(8,8))


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


# Loop through different trials to read data and create quiver plots
for i in range(0,numberofnoises): 
        
    # Path templates
    path = current_directory+f'/Angle_180/Noise_{noises[i]}/correlation_data/velocitycorrelation_vs_r_5000_.dat'

    
    # Load connected correlation function vs r data
    ccf,r = load_data(path)     
    
    # Plot
    ax = axes[0,0]
    ax.plot(r,ccf,  c=colour_angle[i], marker=markers[i],markerfacecolor="none",label=r"$\eta =$"+noises_str[i])
    ax.legend(loc="best", prop={'size': 20},labelspacing = 0.05,frameon=False,bbox_to_anchor=(0.45, 0.3, 0.5, 0.5))
    #ax.set_xlabel('$r$',fontsize=x_label_size)
    ax.set_ylabel('$C_{v}(r)$',size=y_label_size)
    ax.annotate(label[0],size=label_size,xy=(0.1,0.1),xycoords="axes fraction")
    ax.annotate(r"$\alpha =$"+angles_rad[3],size=25,xy=(0.55,0.85),xycoords="axes fraction")
    ax.set_xlim([0, Length_of_box/2])
    ax.set_ylim(-0.4,1.05)
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True,bottom=True,left=True)
    ax.tick_params(which='major', direction="in", length=8, color="black",right=True,top=True,bottom=True,left=True)






# Loop through different trials to read data and create quiver plots
for i in range(0,numberofangles): 
        
    # Path templates
    path = current_directory+f'/Angle_{angles[i]}/Noise_{noises[0]}/correlation_data/velocitycorrelation_vs_r_{time[timetoplot]}_.dat'

    if(i==0):
        path = current_directory+f"/Figure/correlation/vcf_vs_r_45_005.dat"
    
    # Load connected correlation function vs r data
    ccf,r = load_data(path)     
    
    # Plot
    ax = axes[0,1]
    ax.plot(r,ccf,  c=colour_angle[i], marker=markers[i],markerfacecolor="none",label=r"$\alpha =$"+angles_rad[i])
    #ax.legend(loc="best", prop={'size': 15},labelspacing = 0.05,frameon=False,bbox_to_anchor=(0.5, 0.5, 0.5, 0.5))
    #ax.set_xlabel('$r$',fontsize=x_label_size)
    #ax.set_ylabel('$C_{v}(r)$',size=y_label_size)
    ax.annotate(label[1],size=label_size,xy=(0.1,0.1),xycoords="axes fraction")
    ax.annotate("$\eta =$"+noises_str[0],size=25,xy=(0.55,0.85),xycoords="axes fraction")
    ax.set_xlim([0, Length_of_box/2])
    ax.set_ylim(-0.4,1.05)
    #ax.set_yscale("log")
    if(Fit):
        r=np.array(r)
        for i in range(len(ccf)-1):
            if(ccf[i]*ccf[i+1]<0):
                slope=(ccf[i+1]-ccf[i])/(r[i+1]-r[i])
                xi=r[i]-(ccf[i]/slope)
        fit=0.5*np.arcsin(np.exp(-(r)**2/xi**2))
        ax.plot(r,fit,label="fit")
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True,bottom=True,left=True)
    ax.tick_params(which='major', direction="in", length=8, color="black",right=True,top=True,bottom=True,left=True)



for i in range(0,numberofangles): 
        
    # Path templates
    path = current_directory+f'/Angle_{angles[i]}/Noise_{noises[1]}/correlation_data/velocitycorrelation_vs_r_{time[timetoplot]}_.dat'
    # Load connected correlation function vs r data
    ccf,r = load_data(path)

    
    # Plot
    ax = axes[1,0]
    ax.plot(r,ccf,c=colour_time[i], marker=markers[i],markerfacecolor="none", markeredgecolor=colour_time[i],label=r"$\alpha=$"+f"{angles_rad[i]}")
    ax.annotate("$\eta =$"+noises_str[1],size=25,xy=(0.6,0.85),xycoords="axes fraction")
    ax.set_xlabel('$r$',fontsize=x_label_size)
    ax.set_ylabel('$C_{v}(r)$',size=y_label_size)
    ax.annotate(label[2],size=label_size,xy=(0.1,0.1),xycoords="axes fraction")
    ax.set_xlim([0, Length_of_box/2])
    ax.set_ylim(-0.4,1.05)
    ax.tick_params(left=True, top=True ,right=True)
    ax.tick_params(axis="x", direction="in")
    ax.tick_params(axis="y", direction="in")
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True,bottom=True,left=True)
    ax.tick_params(which='major', direction="in", length=8, color="black",right=True,top=True,bottom=True,left=True)


for i in range(0,numberofangles): 
        
    # Path templates
    path = current_directory+f'/Angle_{angles[i]}/Noise_{noises[2]}/correlation_data/velocitycorrelation_vs_r_{time[timetoplot]}_.dat'
    # Load connected correlation function vs r data
    ccf,r = load_data(path)
    # Plot
    ax = axes[1,1]
    ax.plot(r,ccf,  c=colour_angle[i], marker=markers[i],markerfacecolor="none",label=r"$\alpha =$"+angles_rad[i])
    ax.annotate("$\eta =$"+noises_str[2],size=25,xy=(0.6,0.85),xycoords="axes fraction")
    ax.set_xlabel('$r$',fontsize=x_label_size)
    #ax.set_ylabel(r'$C^{c}(r)$',fontsize=y_label_size)
    xi=0
    if(Fit):
        r=np.array(r)
        for i in range(len(ccf)-1):
            if(ccf[i]*ccf[i+1]<0):
                slope=(ccf[i+1]-ccf[i])/(r[i+1]-r[i])
                xi=r[i]-(ccf[i]/slope)
        print(xi)
        fit=np.arcsin(np.exp(-(r)**2/4**2))
        fit/=fit[0]
        ax.plot(r,fit,label="fit")
    
    ax.legend(loc="right", prop={'size': 18},labelspacing = 0.2,frameon=False,bbox_to_anchor=(0.55, 0.35,0.5,0.5))
    ax.annotate(label[3],size=label_size,xy=(0.1,0.1),xycoords="axes fraction")
    ax.set_xlim([0, Length_of_box/2])
    ax.set_ylim(-0.4,1.05)
    ax.tick_params(left=True, top=True ,right=True)
    ax.tick_params(axis="x", direction="in")
    ax.tick_params(axis="y", direction="in")
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    ax.tick_params(which='minor', direction="in", length=4, color="black",right=True,top=True,bottom=True,left=True)
    ax.tick_params(which='major', direction="in", length=8, color="black",right=True,top=True,bottom=True,left=True)
   # ax.set_yscale("log")
   # ax.set_xscale("log")

#plt.legend()
plt.tight_layout()
plt.show()




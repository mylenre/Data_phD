# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 21:53:58 2020

@author: s1995204
"""

import os
import math
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
plt.rcParams['savefig.facecolor'] = "0.8"
plt.style.use('seaborn')
colormap = np.array(['teal', 'forestgreen', 'navy', 'royalblue', 'palevioletred', 'tan', 'magenta', 'green', 'black'])


#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\POROSITY_SEAMS')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\PUMPING_RATE')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\GEOMETRY\6_VOLUME-MINED-ROCK')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\CONDUCTIVITY_HOST_ROCK')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\GEOMETRY')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\PUMPING_DEPTH')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\HYDRAULIC_CONDUCTIVITY_HOST_ROCK')

#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\NEW\Recovery')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\NEW\Geothermal_gradient')
#os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\aaaaallllll\GEOMETRY')
#os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\aaaaallllll\GEOMETRY\6_VOLUME_MINED')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\NEW\Boundaries\analysis')
os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\NEW\hydraulic_conductivity')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\NEW\Pumping_rate')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\NEW\seam_porosity')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\NEW\seam_productivity')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\NEW\Heat_conductivity')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\NEW\permeability_contrasts')
#os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\aaaaallllll\GEOMETRY\6_VOLUME_MINED_v3')
#os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\aaaaallllll\Host rock density')
#os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\aaaaallllll\Host rock heat capacity')
#®os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\NEW\Head_gradient')
d = '.'
subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
subdirs = [x.replace('.\\','') for x in subdirs]
filelist=glob.glob('*\*MATERIALGROUP.txt')
N = len(filelist)

# initialize variables
scenario = {}
energy_start={}
energy_final={}

Nmg = input("Enter number of material groups: ")  #number of material group = 5
print(Nmg +' materials in the model.')
Nmg = eval(Nmg)
j = 0

for i in range(N): #If geometry
    data={}
    with open(filelist[i]) as file:
       name = filelist[i]
       print('processing ' + name)
       for line in file:
           if("Time") in line:
               this_line = line.split(' ')
               time = this_line[1].rstrip()
               mg = []
               energy = []
               continue
           if('Material_Group Energy_J_(Using Kelvin)') in line:
               j = 1
               continue
           if (j > 0) and (j < (Nmg + 1)):  # Need to verify this
               this_line = line.split(' ')
               mg.append(this_line[0].rstrip())
               energy.append(float(this_line[1].rstrip()))
               j += 1
           if line == '\n':
               continue
           data[float(time)] = [mg, energy]
    folder = name.split('\\')[0].split('_')[1]
    #scenario[subdirs[i]] = [data]       
    scenario[folder] = [data]   
    
ts = input("Enter final time step: ")  
ts = eval(ts)

#%% plot initial energy and energy change
title = 'Host rock  hydraulic conductivity (m/s)' #'Volume mined ($m^3$)'
tr = 0
fts = 12
s = 3 # considered start of time series to avoid offsets

#label= ['1e-3 (1e-7, 1e-4)',
#        '1e-4 (1e-7, 1e-3)',
#        '1e-5 (1e-7, 1e-2)',
#        '1e-6 (1e-7, 1e-1)',
#        '1e-6 (1e-8, 1e-2)',
#        '1e-4 (1e-6, 1e-2)',
#        '1e-3 (1e-5, 1e-2)']
i=0
fig = plt.figure(figsize=(5,7))
gs1 = gridspec.GridSpec(1, 1)
ax1 = fig.add_subplot(gs1[0])
gs1.tight_layout(fig, rect=[0.15, 0.5, 1,0.98])
for key1 in scenario:
    print(str(key1))
    energy_tot = {}
    for key2 in scenario[key1][0]:
        if int(key2) <= (ts*86400):
            energy_tot[key2] = int(sum(scenario[key1][0][key2][1]))
    energy_tot_df = pd.DataFrame(list(energy_tot.items()),columns = ['Time','J'])
    
    energy_start[key1]=int((energy_tot_df['J'].head(s))[s-1])
    energy_start_df = pd.DataFrame(list(energy_start.items()),columns = ['Scenario','Jtot'])
    energy_final[key1]=int(energy_tot_df['J'].tail(1))
    energy_final_df = pd.DataFrame(list(energy_final.items()),columns = ['Scenario','Jtot'])
    categories = np.array(range(len(energy_final_df)))
      
    ax1.scatter(energy_tot_df['Time'][s-1::]/86400, energy_tot_df['J'][s-1::], marker= 'x', s=10, color=colormap[i], label = key1) #.split('_')[1]
    ax1.set_title(title,fontsize = fts)
    ax1.set_xlabel('Time (day)')
    ax1.ticklabel_format(axis='y', useOffset=False)
    ax1.set_ylabel('Energy (J)', fontsize = fts)
    ax1.legend(bbox_to_anchor=(0.01, 0.68), loc = 'center left', prop={'size': fts}, ncol = 2) #
    i += 1
    
a=[float(x) for x in energy_final_df['Scenario']]
b= energy_final_df['Jtot']-energy_start_df['Jtot']  
gs2 = gridspec.GridSpec(2, 1)
ax2 = fig.add_subplot(gs2[0])
ax3 = fig.add_subplot(gs2[1])
gs2.tight_layout(fig, rect=[0.25, 0.01 ,1, 0.5], h_pad=0.9)

ax2.scatter(a,energy_start_df['Jtot'], marker= 'x', s=20, c=colormap[categories])
#ax2.scatter(energy_start_df['Scenario'],energy_start_df['Jtot'], marker= 'x', s=10, c=colormap[categories])
ax2.tick_params(top=False, bottom=False, left=True, right=False,labelleft=True, labelbottom=False)
ax2.ticklabel_format(axis='y', useOffset=False)
ax2.set_ylabel('Initial Energy (J)', fontsize = fts)

ax3.scatter(a,b, marker= 'x', s=20, c=colormap[categories])
#ax3.scatter(energy_final_df['Scenario'],b, marker= 'x', s=20, c=colormap[categories])
ax3.set_xlabel('Value', fontsize = fts)
ax3.set_ylabel('Energy Change (J)', fontsize = fts)
ax3.ticklabel_format(axis='y', useOffset=False)
plt.xlim(1e-8,1e-5) #plt.xlim(1e-5, 1e-2) #
#plt.xscale("log")
plt.xticks(fontsize = fts, rotation = tr)
plt.yticks(fontsize = fts)

plt.savefig('Energy_t0_'+str(ts)+'_v2.png', facecolor='w',transparent=False,frameon=None, metadata=None)


# %% Plot time-series of energy and energy change
i = 0
fig = plt.figure(figsize=(5,7))
gs = gridspec.GridSpec(5, 1)

ax = fig.add_subplot(gs[:3,:])
for key1 in scenario:
    print(str(key1))
    energy_tot = {}
    for key2 in scenario[key1][0]:
        if int(key2) <= (ts*86400):
            energy_tot[key2] = int(sum(scenario[key1][0][key2][1]))
    energy_tot_df = pd.DataFrame(list(energy_tot.items()),columns = ['Time','J'])
    
    energy_start[key1]=int((energy_tot_df['J'].head(s))[s-1])
    energy_start_df = pd.DataFrame(list(energy_start.items()),columns = ['Scenario','Jtot'])
    energy_final[key1]=int(energy_tot_df['J'].tail(1))
    energy_final_df = pd.DataFrame(list(energy_final.items()),columns = ['Scenario','Jtot'])
    categories = np.array(range(len(energy_final_df)))
     
    if (key1 == '180 - 200 m (FLUX)') or (key1 == '50 - 70 m (FLUX)'):
        energy_tot_df['J'] = energy_tot_df['J'] - 158423769712
    ax.scatter(energy_tot_df['Time'][s-1::]/86400, energy_tot_df['J'][s-1::], marker= 'x', s=8, color=colormap[i], label = key1) #.split('_')[1]
    #ax.scatter(energy_tot_df['Time'][s-1::]/86400, energy_tot_df['J'][s-1::], marker= 'x', s=8, color=colormap[i], label = label[i]) #.split('_')[1]
    i += 1
    ax.set_title(title,fontsize = fts)
    ax.set_xlabel('Time (days)',fontsize = fts)
    ax.set_ylabel('Energy (J)',fontsize =fts)
    plt.ticklabel_format(axis='y', useOffset=False)
    plt.xticks(fontsize = fts)
    plt.yticks(fontsize = fts)
    ax.legend(bbox_to_anchor=(0.05, 0.55), loc = 'center left', prop={'size': fts}, ncol = 1) #

ax1 = fig.add_subplot(gs[3:,:])#ax1.scatter(a,b, marker= 'x', s=40, c=colormap[categories])
#ax1.scatter(energy_final_df['Scenario'],b, marker= 'x', s=40, c=colormap[categories])
ax1.scatter(a,b, marker= 'x', s=40, c=colormap[categories])
ax1.set_xlabel('Value', fontsize = fts)
ax1.set_ylabel('Energy Change (J)', fontsize = fts)
plt.ticklabel_format(axis='y', useOffset=False)
plt.xlim(1e-8,1e-5) # plt.xlim(1e-5,1e-2) 
plt.xscale("log")
plt.xticks(fontsize = fts, rotation = tr)
plt.yticks(fontsize = fts)

gs.tight_layout(fig, rect=[0, 0 ,1, 1], h_pad=1) #plt.tight_layout() #pad=0.2, w_pad=0.2, h_pad=0.2

plt.savefig('Energy_'+str(ts)+'_v2.png', facecolor='w',transparent=False,frameon=None, metadata=None)

# %% plot on separate plots
i = 0
n = math.ceil(len(scenario)/2)
plt.figure(figsize=(10,10))
for key1 in scenario:
    print(str(key1))
    energy_tot = {}
    for key2 in scenario[key1][0]:
        if int(key2) < (ts*86400):
            energy_tot[key2] = int(sum(scenario[key1][0][key2][1]))
    energy_tot_df = pd.DataFrame(list(energy_tot.items()),columns = ['Time','J'])

    plt.subplot(n,2,i+1)
    plt.scatter(energy_tot_df['Time'][s-1::]/86400, energy_tot_df['J'][s-1::], marker= 'x', s=5) #, label = key1
    plt.title(key1, size=fts)
    plt.xlabel('Time (day)',fontsize = fts)
    plt.ylabel('Energy (Joules)',fontsize = fts)
    plt.ticklabel_format(useOffset=False)
    plt.ticklabel_format(axis='y', useOffset=False)
    plt.xticks(fontsize = fts)
    plt.yticks(fontsize = fts)
    plt.legend()
    i += 1
plt.suptitle('Total energy change over time for each scenario', size= 11, y =1)
plt.tight_layout()
plt.savefig('Energy_ts_'+str(ts)+'.png', facecolor='w',transparent=False,frameon=None, metadata=None)
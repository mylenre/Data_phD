# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 21:53:58 2020

@author: s1995204
"""

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
plt.rcParams['savefig.facecolor'] = "0.8"
plt.style.use('seaborn')
colormap = np.array(['teal', 'forestgreen', 'royalblue', 'palevioletred', 'tan', 'magenta', 'green', 'black'])

poro = 0.1
rho = 2500 * (1-poro) + 1000 * poro
c = 950 * (1-poro) + 4680 * poro

#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\POROSITY_SEAMS')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\PUMPING_RATE')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\GEOMETRY\6_VOLUME-MINED-ROCK')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\CONDUCTIVITY_HOST_ROCK')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\GEOMETRY')
#os.chdir(r'R:\Modeling\2D_Models\Energy_analysis\2.3_SENSITITIVTYANALYSIS\ALL\PUMPING_DEPTH')
#os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\Heat_extraction_paper\2MG')

os.chdir(r'S:\Modeling\1D_Models\3_Heat_extraction_new_areas\100m_BHE_30m²\2_Production_30Y\0_1D-SI')


#os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\Heat_extraction_model_water\3_30Y')

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
    
ts = input("Enter final time step (days): ")  
ts = eval(ts)

i=0
fig = plt.figure(figsize=(4,7))
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
    
    energy_start[key1]=int(energy_tot_df['J'].head(1))
    energy_start_df = pd.DataFrame(list(energy_start.items()),columns = ['Scenario','Jtot'])
    energy_final[key1]=int(energy_tot_df['J'].tail(1))
    energy_final_df = pd.DataFrame(list(energy_final.items()),columns = ['Scenario','Jtot'])
    categories = np.array(range(len(energy_final_df)))
      
    ax1.scatter(energy_tot_df['Time']/86400, energy_tot_df['J'], marker= 'x', s=1, color=colormap[i], label = key1) #.split('_')[1]
    i += 1
    ax1.set_title('Pumping depth (m)',fontsize = 12)
    ax1.set_xlabel('Time (day)')
    ax1.ticklabel_format(axis='y', useOffset=False)
    ax1.set_ylabel('Energy (Joules)', fontsize = 12)
    ax1.legend()

#a=[float(x) for x in energy_final_df['Scenario']]
b= energy_final_df['Jtot']-energy_start_df['Jtot']  

gs2 = gridspec.GridSpec(2, 1)
ax2 = fig.add_subplot(gs2[0])
ax3 = fig.add_subplot(gs2[1])
gs2.tight_layout(fig, rect=[0.25, 0.01 ,1, 0.5], h_pad=0.9)

#ax2.scatter(a,energy_start_df['Jtot'], marker= 'x', s=20, c=colormap[categories])
ax2.scatter(energy_start_df['Scenario'],energy_start_df['Jtot'], marker= 'x', s=20, c=colormap[categories])
ax2.set_ylabel('Initial Energy (J)', fontsize = 12)
ax2.ticklabel_format(axis='y', useOffset=False)

#ax3.scatter(a,b, marker= 'x', s=20, c=colormap[categories])
ax3.scatter(energy_final_df['Scenario'],b, marker= 'x', s=20, c=colormap[categories])
ax3.set_xlabel('Value', fontsize = 12)
ax3.set_ylabel('Energy Change (J)', fontsize = 12)
ax3.ticklabel_format(axis='y', useOffset=False)
    
#%% solar: os.chdir(r'R:\Modeling\1D_Models\2_Heat_extraction_model_water\Analysis\Solar')

flux = {}
for key1 in scenario:
    print(key1)
    energy_tot = []
    for key2 in scenario[key1][0]: 
        energy_tot.append(int(sum(scenario[key1][0][key2][1])))
    for i in mg:
        i = eval(i)
        m1 = []
        m1.append([scenario[key1][0][key2][1][i] for key2 in scenario[key1][0]])
        m1 = np.subtract(m1[0],775527074728)
        flux[key1]=m1

plt.figure()
plt.subplot(1,2,1) 
plt.plot(energy_tot_df['Time']/(86400*366),  flux['reference'])
plt.plot(energy_tot_df['Time']/(86400*366),  flux['solar'])

plt.subplot(1,2,2) 
diff = flux['solar']-flux['reference']
plt.plot(energy_tot_df['Time']/(86400*366),diff)


m1=[]
m2=[]
time = list(scenario['1D-SI-CST-T'][0].keys())
m1.append([scenario['1D-SI-CST-T'][0][key2][1][0] for key2 in scenario['1D-SI-CST-T'][0]])
m2.append([scenario['1D-SI-FLUX'][0][key2][1][0] for key2 in scenario['1D-SI-FLUX'][0]])
a= np.array(m1[0]).T
b = np.array(m2[0]).T
diff = np.subtract(a,b)

time_yr = np.array(time)/(86400*366)
fig = plt.figure(figsize=(7,5))
plt.plot(time_yr, diff)
plt.xlabel('Time (year)', fontsize = 12)
plt.ylabel('Energy difference (J)', fontsize = 12)
plt.title('Energy difference using constant surface temperature or surface heat flux')
plt.tight_layout()
# %% PLOT ON SAME PLOT 
tr = 0 #tick rotation
i = 0
plt.figure(figsize=(5,8))
plt.subplot(2,1,1)
for key1 in scenario:
    print(str(key1))
    energy_tot = {}
    for key2 in scenario[key1][0]:
        if int(key2) <= (ts*86400):
            energy_tot[key2] = int(sum(scenario[key1][0][key2][1]))
    energy_tot_df = pd.DataFrame(list(energy_tot.items()),columns = ['Time','J'])
    
    energy_start[key1]=int(energy_tot_df['J'].head(1))
    energy_start_df = pd.DataFrame(list(energy_start.items()),columns = ['Scenario','Jtot'])
    energy_final[key1]=int(energy_tot_df['J'].tail(1))
    energy_final_df = pd.DataFrame(list(energy_final.items()),columns = ['Scenario','Jtot'])
    categories = np.array(range(len(energy_final_df)))
      
    plt.scatter(energy_tot_df['Time'][2::]/86400, energy_tot_df['J'][2::], marker= 'x', s=10, color=colormap[i], label = key1) #.split('_')[1]
    i += 1
    plt.title('Hydraulic conductivity of the seams (m/s)',fontsize = 12)
    plt.xlabel('Time (days)',fontsize = 12)
    plt.ylabel('Energy (Joules)',fontsize = 12)
    plt.ticklabel_format(axis='y', useOffset=False)
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.ticklabel_format(useOffset=False)
    plt.legend()
plt.tight_layout()

plt.subplot(4,1,3)
plt.scatter(energy_start_df['Scenario'],energy_start_df['Jtot'], marker= 'x', s=20, c=colormap[categories])
#plt.scatter(energy_final_df['Scenario'],energy_final_df['Jtot'], marker= 'o', s=50, c=colormap[categories])
plt.ylabel('Initial Energy (J)', fontsize = 12)
plt.ticklabel_format(axis='y', useOffset=False)
plt.xticks(fontsize = 12, rotation = tr)
plt.yticks(fontsize = 12)

plt.subplot(4,1,4)
#a=[float(x) for x in energy_final_df['Scenario']]
b= energy_final_df['Jtot']-energy_start_df['Jtot']  # energy_final_df['Jtot']
#plt.scatter(a,b, marker= 'o', s=50, c=colormap[categories])
plt.scatter(energy_final_df['Scenario'],b, marker= 'x', s=20, c=colormap[categories])
plt.xlabel('Value', fontsize = 12)
plt.ylabel('Energy Change (J)', fontsize = 12)
plt.ticklabel_format(axis='y', useOffset=False)
plt.xticks(fontsize = 12, rotation = tr)
plt.yticks(fontsize = 12)

plt.tight_layout() #pad=0.2, w_pad=0.2, h_pad=0.2
#locs, labels=plt.xticks()
#new_xticks=[key for key in scenario] #new_xticks=[key.split('_')[1] for key in scenario]
#plt.xticks(locs,new_xticks, rotation=20)
#plt.legend()

#%% FOR GEOMETRY / POROSITY
i = 0
plt.figure(figsize=(10,10))
# plt.subplot(1,2,1)
for key1 in scenario:
    print(str(key1))
    energy_tot = {}
    for key2 in scenario[key1][0]:
        if int(key2) < (ts*86400):
            energy_tot[key2] = int(sum(scenario[key1][0][key2][1]))
    energy_tot_df = pd.DataFrame(list(energy_tot.items()),columns = ['Time','J'])
    energy_start[key1]=int(energy_tot_df['J'].head(1))
    energy_start_df = pd.DataFrame(list(energy_start.items()),columns = ['Scenario','Jtot'])
    energy_final[key1]=int(energy_tot_df['J'].tail(1))
    energy_final_df = pd.DataFrame(list(energy_final.items()),columns = ['Scenario','Jtot'])
    categories = np.array(range(len(energy_final_df)))
        
    plt.subplot(4,2,i+1)
    plt.scatter(energy_tot_df['Time'][2:(ts+1)]/86400, energy_tot_df['J'][2::], marker= 'x', s=5, color=colormap[i]) #, label = key1
    #plt.title(key1.split('_')[1], size=8)
    plt.title(key1, size=14)
    plt.xlabel('Time (day)',fontsize = 14)
    plt.ylabel('Energy (Joules)',fontsize = 14)
    plt.ticklabel_format(useOffset=False)
    plt.ticklabel_format(axis='y', useOffset=False)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.legend()
    i += 1
plt.suptitle('Total energy change over time for each scenario', size= 11, y =1)
plt.tight_layout()

plt.figure(figsize=(8,8))
#a=[float(x) for x in energy_final_df['Scenario']]
b=energy_final_df['Jtot']-energy_start_df['Jtot']
#plt.scatter(a,b, marker= 'o', s=50, c=colormap[categories]) #plt.scatter(energy_final_df['Scenario'][0:-1],energy_final_df['Jtot'][0:-1], marker= 'o', s=50, c=colormap[categories][0:-1]) #REMOVE LAST ELEMENT
#plt.scatter(energy_final_df['Scenario'],energy_final_df['Jtot'], marker= 'o', s=50, c=colormap[categories])
plt.scatter(energy_final_df['Scenario'],b, marker= 'x', s=50, c=colormap[categories])

plt.title('Final change in energy content after ' + str(ts) +' days for each scenario', fontsize=14)
plt.xlabel('Porosity', fontsize = 14) #Hydraulic conductivity (x 1e-7 m/s)
plt.ylabel('Energy change (Joules)', fontsize = 14)
plt.xticks(rotation = 20, fontsize = 14)
plt.ticklabel_format(axis='y', useOffset=False)
plt.yticks(fontsize = 14)
#locs, labels=plt.xticks()
#new_xticks=[key for key in scenario]
#plt.xticks(locs,new_xticks, rotation=25)

#%% plot per material group 3D models - 3-4MGs
#%Geometry : finite model: 150*150*40; SI model: 150*150*15 

fts = 8
ts = 366*86400
h = input("Enter borehole length: ")  
a_bhe_1y = input("Enter borehole radius (1 year): ") 
a_bhe_30y = input("Enter borehole radius (30 years): ") 
h = eval(h)
a_bhe_1y = eval(a_bhe_1y)
a_bhe_30y = eval(a_bhe_30y)

surfaceBHE = 2*np.pi*a_bhe_1y*h
surfaceOUT = 2*np.pi*a_bhe_30y*h

flux = {}

ax = input("calculate axial fluxes ? (y/n) ") 
if ax == 'y': 
    if Nmg == 4:
       volume=['r < '+str(a_bhe_1y)+'m','r < '+str(a_bhe_30y)+' m','r > '+str(a_bhe_30y)+' m', 'over/underlying']
    if Nmg == 3:
       volume = ['r < 8 m','r > 8 m','over/underlying'] 
if ax == 'n': 
    if Nmg == 3:
       volume=['r < '+str(a_bhe_1y)+'m','r < '+str(a_bhe_30y)+' m','r > '+str(a_bhe_30y)+' m']
    if Nmg == 2:
       volume = ['r < 8 m','r > 8 m']      

    
for key1 in scenario:
    print(key1)
    energy_tot = []
    for key2 in scenario[key1][0]: 
        energy_tot.append(int(sum(scenario[key1][0][key2][1])))
    plt.figure(figsize=(8,6))
    for i in mg:
        i = eval(i)
        m1 = []
        m1.append([scenario[key1][0][key2][1][i] for key2 in scenario[key1][0]])
        plt.subplot(2,2,i+1)
        plt.scatter(scenario[key1][0].keys(), m1, s=1)
        plt.title('material n°' + str(i),fontsize = fts)

        plt.subplot(2,2,4)
        plt.scatter(scenario[key1][0].keys(), energy_tot, s=1)
        plt.title('Total energy',fontsize = fts)
        plt.ticklabel_format(axis='y', useOffset=False)
        plt.xticks(fontsize = fts)
        plt.yticks(fontsize = fts)
        plt.tight_layout()
        
        m1 = m1[0]
        dm1 = np.subtract(m1[1::],m1[:-1])/(ts)
        leg = volume[i]
        flux[leg]=dm1

x= np.linspace(0,30,30)
plt.figure()
for i in flux.keys():
    plt.plot(x,flux[i], label= i)
plt.legend()
plt.xlabel('Time (Years)')
plt.ylabel('Energy change (W)')
plt.title('Total energy change in each volume')

# calculate radial fluxes 
plt.figure()
if (Nmg == 3) or (Nmg == 4):
        flux_in = (flux[volume[0]]-(flux[volume[1]]+flux[volume[2]]))/surfaceBHE
        plt.plot(x,flux_in, label='Flux at '+str(a_bhe_1y)+' m')
        flux_out = ((flux[volume[0]]+flux[volume[1]])-flux[volume[2]])/surfaceOUT
        plt.plot(x,flux_out, label='Flux at '+str(a_bhe_30y)+' m')
        plt.legend()
        plt.xlabel('Time (Years)')
        plt.ylabel('Heat flux (W/m²)')
#if Nmg == 2:
#        surfaceBHE = 2*np.pi*8*h
#        flux_in = (flux['r < 8m']-(flux['r > 8m']))/surfaceBHE
#        plt.plot(x,flux_in, label='Flux at 8 m')
#        plt.legend()
#        plt.xlabel('Time (Years)')
#        plt.ylabel('Heat flux (W/m²)')       
       

print('Contribution from BHE volume within the first year: '+ str
      (((scenario['energy'][0][0.0][1][0])-(scenario['energy'][0][31622400.0][1][0]))/
       (sum(scenario['energy'][0][0.0][1])-sum(scenario['energy'][0][31622400.0][1]))))
print('Contribution from BHE + outside volume within the first year: '+ str
      (((scenario['energy'][0][0.0][1][0]+scenario['energy'][0][0.0][1][1])-(scenario['energy'][0][31622400.0][1][0]+scenario['energy'][0][31622400.0][1][1]))/
       (sum(scenario['energy'][0][0.0][1])-sum(scenario['energy'][0][31622400.0][1]))))
print('Contribution from BHE volume after 30 years: '+ str
      (((scenario['energy'][0][0.0][1][0])-(scenario['energy'][0][948672000.0][1][0]))/
       (sum(scenario['energy'][0][0.0][1])-sum(scenario['energy'][0][948672000.0][1]))))
print('Contribution from BHE + outside volume after 30 years: '+ str
      (((scenario['energy'][0][0.0][1][0]+scenario['energy'][0][0.0][1][1])-(scenario['energy'][0][948672000.0][1][0]+scenario['energy'][0][948672000.0][1][1]))/
       (sum(scenario['energy'][0][0.0][1])-sum(scenario['energy'][0][948672000.0][1]))))


#calculate axial recharge
if ax == 'y': 
    if Nmg == 4:
        print('Contribution from axial recharge within the first year: '+ str
              (((scenario['energy'][0][0.0][1][3])-(scenario['energy'][0][31622400.0][1][3]))/
               (sum(scenario['energy'][0][0.0][1])-sum(scenario['energy'][0][31622400.0][1]))))
        print('Contribution from axial recharge afetr 30 years: '+ str
              (((scenario['energy'][0][0.0][1][3])-(scenario['energy'][0][948672000.0][1][3]))/
               (sum(scenario['energy'][0][0.0][1])-sum(scenario['energy'][0][948672000.0][1]))))
    if Nmg == 3:
        print('Contribution from axial recharge within the first year: '+ str
              (((scenario['energy'][0][0.0][1][2])-(scenario['energy'][0][31622400.0][1][2]))/
               (sum(scenario['energy'][0][0.0][1])-sum(scenario['energy'][0][31622400.0][1]))))
        print('Contribution from axial recharge afetr 30 years: '+ str
              (((scenario['energy'][0][0.0][1][2])-(scenario['energy'][0][948672000.0][1][2]))/
               (sum(scenario['energy'][0][0.0][1])-sum(scenario['energy'][0][948672000.0][1]))))



 #%% plot per material group 1D models - 2MGs
fts = 8
ts = 366
yr = input("Enter number of years: ")  
h = input("Enter borehole length: ")  
r = input("Enter borehole radius: ") 
h = eval(h)
yr = eval(yr)
r = eval(r)

#axial recharge  
surfaceBHE = np.pi*(r**2)

flux = {}
volume=['OUT','BHE']
for key1 in scenario:
    print(key1)
    energy_tot = []
    for key2 in scenario[key1][0]: 
        energy_tot.append(int(sum(scenario[key1][0][key2][1])))
    plt.figure(figsize=(8,2))
    for i in mg:
        i = eval(i)
        m1 = []
        m1.append([scenario[key1][0][key2][1][i] for key2 in scenario[key1][0]])
        plt.subplot(1,3,i+1)
        plt.scatter(scenario[key1][0].keys(), m1, s=1)
        plt.title('material n°' + str(i),fontsize = fts)

        plt.subplot(1,3,3)
        plt.scatter(scenario[key1][0].keys(), energy_tot, s=1)
        plt.title('Total energy',fontsize = fts)
        plt.ticklabel_format(axis='y', useOffset=False)
        plt.xticks(fontsize = fts)
        plt.yticks(fontsize = fts)
        plt.tight_layout()
        m1 = m1[0]
        #a = np.array(m1[:-1]).reshape(yr,366)
        #m1 = np.sum(a, axis=1)
        dm1 = np.subtract(m1[1::],m1[:-1])*surfaceBHE/(86400)
        #a = np.array(dm1).reshape(yr,366)
        #dm1 = np.sum(a, axis=1)
        leg = volume[i]
        flux[leg]=dm1

x= np.linspace(0,yr*366,yr*366)
plt.figure()
for i in flux.keys():
    plt.plot(x,flux[i], label= i)
plt.legend()
plt.xlabel('Time (Years)')
plt.ylabel('Energy change (W)')
plt.xticks(np.arange(0, yr*366, step=366), [str(i) for i in np.arange(0,yr,step=1)])  # Set text labels.
plt.title('Total energy change in each volume')


plt.figure()
flux_in = (flux['OUT']-flux['BHE'])/(2*surfaceBHE)# FLUX INDUCED BY HEAT EXTRACTION

plt.plot(x,flux_in, label='Axial fluxes')
plt.legend()
plt.xlabel('Time (Years)')
plt.ylabel('Heat flux (W/m²)')
plt.xticks(np.arange(0, yr*366, step=366), [str(i) for i in np.arange(0,yr,step=1)])  # Set text labels.
plt.title('Heat flux at volume interfaces')

# tf = list(scenario['energy'][0].keys())[-1]
# print('Contribution from axial recharge after '+str(yr) +' year(s): '+ str
#               (((scenario['energy'][0][0.0][1][0])-(scenario['energy'][0][tf][1][0]))/
#                (sum(scenario['energy'][0][0.0][1])-sum(scenario['energy'][0][tf][1]))))


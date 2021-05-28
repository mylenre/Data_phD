# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:23:13 2019

@author: s1995204
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import glob
plt.style.use('seaborn')

#os.chdir(r'S:\Modeling\1D_Models\3_Heat_extraction_new_areas\Solar\4_ALTERNATIVE\6_BACK\0_EI')
os.chdir(r'S:\Modeling\2D_Models\5_Energy_analysis\2_SENSITITIVTYANALYSIS\NEW\9_Seam_productivity')


filename='A5_ply_WELL_1_t1'
#filelist=glob.glob(filename+'.tec')
filelist=glob.glob('*\*'+filename+'.tec')
N = np.size(filelist)

# Initialize variables
time_all = []
scenario = {}

for i in range(N): #If geometry
    data={}
    with open(filelist[i]) as file:
       name = filelist[i]
       print('processing ' + name)
       for line in file:
           if("TITLE" in line):
               continue
           if("VARIABLES" in line):
               continue
           if(' ZONE T' in line):
               this_line = line.replace('"','').replace('e+','e').split("=")
               time = this_line[2].rstrip()
               time_all.append(time)
               x = []
               Tx= []
               continue
           else:
               this_line=line.replace('e+','e').split(' ')
               x.append(float(this_line[0].rstrip()))
               Tx.append(float(this_line[1].rstrip()))
           data[float(time)] = [x,Tx]
    subdir = filelist[i].split('\\')[0].split('_')[1]
    scenario[subdir] = [data]  


#%% [596,597,598,599,600,601] solar variations fro 100 years
colormap = np.array([ 'palevioletred',  'royalblue', 'tan', 'teal', 'forestgreen', 'magenta', 'green', 'black'])
fts=11
j=0
# find unique values of time
res=list(set.intersection(*map(set,[scenario[i][0].keys() for i in scenario])))
res = pd.DataFrame(np.array(res)/86400)
#print('Number of time steps: ' + str(int(np.size(time_all)/N)))
print('Available time to plots: ', res)

timeplot=input("Enter index of time steps to plot (i.e. [30, 52]) : ") 
timeplot=eval(timeplot)
#label = ['< 1e-2 m/s (HEAD)','>= 1e-2 m/s (HEAD)','1e-2 m/s (FLUX)']
plt.figure(figsize=(5,5.5))
for i in timeplot:
    for key in scenario:
        print(str(key))
        #n=list(scenario[key][0].keys())[i-1]
        n = int(res.iloc[30]) * 86400
        tf= scenario[key][0][n]
        #plt.plot(tf[1],tf[0],lw=1.5, label= key, color = colormap[j]) #, marker= 'x', s=10, color=colormap[i], label = str(int(n/86400))
        plt.plot(tf[1],tf[0],lw=1.5, label = str(key)) #, color = colormap[j]) #, marker= 'x', s=10, color=colormap[i], label = str(int(n/86400))

        #plt.plot(tf[1],tf[0],lw=1.5, label= str(key), color = colormap[j]) #, marker= 'x', s=10, color=colormap[i], label = key
        #plt.plot(tf[1],tf[0],lw=1.2, label= label[j], color = colormap[j]) #, marker= 'x', s=10, color=colormap[i], label = key
        #plt.title('a) Temperature recovery profiles for different \n  seams hydraulic conductivity (m/s)', fontsize = fts)        
        plt.xlabel('Temperature (°C)', fontsize = fts)
        plt.ylabel('Depth (m)', fontsize = fts)
        plt.xticks(fontsize = fts)
        plt.yticks(fontsize = fts)
        plt.xlim(4,20)
        plt.ylim(max(tf[0]), min(tf[0]))
        plt.legend(loc = 'best')
        #plt.legend(['61 days', '122 days','183 days', '244 days', '305 days','366 days'], prop={'size': fts}, loc = 'lower left')
        j += 1 
plt.tight_layout() #pad=0.2, w_pad=0.2, h_pad=0.2
#plt.text(16,10,'Time: '+ str(int(n/86400)) +' days', fontsize=fts)
#plt.axhline(y=100,xmin=0,xmax=1, linewidth=1, color='k', ls='--')
#plt.axhline(y=130,xmin=0,xmax=1, linewidth=1, color='k', ls='--')
#plt.axhline(y=160,xmin=0,xmax=1, linewidth=1, color='k', ls='--')

# geothermal gradients
#plt.plot([12.1,15.1],[0,300], '--', c='r')  
#plt.plot([10.8,16.8],[0,300], '--', c='b')  
#plt.plot([9,15],[0,300], '--', c='y')             
#plt.plot([9.5,18.5],[0,300], '--', c='g')   
plt.plot([9,21.8],[0,500], '--', c='k') 

#plt.savefig('Temperature_profile.png', facecolor='w',frameon=None, metadata=None)
#%%   
j=0
plt.figure(figsize=(5,4))
plt.rcParams['font.size'] = 12
for key in scenario:
        n=list(scenario[key][0].keys())[-1]
        n=list(scenario[key][0].keys())[i-1]
        tf= scenario[key][0][n]
        Taverage= np.mean(tf[1][50:100])
        plt.scatter(key, Taverage, lw=2, marker= 'x',color=colormap[j]) #, marker= 'x', s=10, color=colormap[i], label = key
        plt.title('Average temperature in mined area after '+ str(int(n/86400)) +' days')
        plt.xlabel('Porosity')
        plt.xticks(fontsize = 11, rotation = 25)
        plt.ylabel('Average temperature( °C)')
        j += 1
#plt.savefig('Average_Temperature.png', facecolor='w',frameon=None, metadata=None)

#%% 
#Tsurface = [12.1,10.8,9.5]
#Taverage = {}
#plt.rcParams['font.size'] = 12
#for key in scenario:
#        n=list(scenario[key][0].keys())[-1]
#        n=list(scenario[key][0].keys())[i-1]
#        tf= scenario[key][0][n]
#        Taverage[key]= round(np.mean(tf[1][50:100]),2)
#        
#plt.figure(figsize=(4,6))
#plt.subplot(2,1,1)
#Taverage= np.array(list(Taverage.items()))
#plt.scatter(Taverage[:,0], Taverage[:,1], lw=2, marker= 'x') #, marker= 'x', s=10, color=colormap[i], label = key
#plt.title('Average temperature in mined area after '+ str(int(n/86400)) +' days')
#plt.xlabel('Geothermal gradient (°C/km)')
#plt.xticks(fontsize = 11, rotation = 0)
#plt.ylabel('Average temperature (°C)')
#
#plt.subplot(2,1,2)
#plt.scatter(Tsurface, Taverage[:,1], lw=2, marker= 'x') #, marker= 'x', s=10, color=colormap[i], label = key
#plt.title('Average temperature in mined area after '+ str(int(n/86400)) +' days')
#plt.xlabel('Surface temperature (°C)')
#plt.xticks(fontsize = 11, rotation = 0)
#plt.ylabel('Average temperature (°C)')
#
#plt.tight_layout() #plt.tight_layout() #pad=0.2, w_pad=0.2, h_pad=0.2
#
##plt.savefig('Average_Temperature.png', facecolor='w',frameon=None, metadata=None)

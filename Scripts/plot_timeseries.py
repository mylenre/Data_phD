# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 13:22:40 2021

@author: s1995204
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import glob
plt.style.use('seaborn')
colormap = np.array([ 'palevioletred',  'royalblue', 'tan', 'teal', 'forestgreen', 'magenta', 'green', 'black'])

os.chdir(r'S:\Modeling\2D_Models\5_Energy_analysis\2_SENSITITIVTYANALYSIS\NEW\9_Seam_productivity')

filename='A5_time_POINTOUT2'
filelist=glob.glob('*\*'+filename+'.tec')
N = np.size(filelist)

# Initialize variables
scenario = {}

for i in range(N): #If geometry
    data={}
    with open(filelist[i]) as file:
        next(file)
        next(file)
        next(file)
        name = filelist[i]
        print('processing ' + name)
        t = []
        temp= []
        head= []
        for line in file:
               this_line=line.replace('e+','e').split(' ')
               t.append(float(this_line[0].rstrip()))
               temp.append(float(this_line[1].rstrip()))
               head.append(float(this_line[2].rstrip()))
    subdir = filelist[i].split('\\')[0].split('_')[1]
    scenario[subdir] = [t, temp, head]

j = 0
fts=11
plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
for key in scenario:
        print(str(key))
        tf= scenario[key]
        plt.plot(tf[0],tf[1],lw=1.5, label= key, color = colormap[j]) #, marker= 'x', s=10, color=colormap[i], label = key
        plt.title('a) Temperature time series', fontsize = fts)        
        plt.ylabel('Temperature (°C)', fontsize = fts)
        plt.xlabel('Time (s)', fontsize = fts)
        plt.xticks(fontsize = fts)
        plt.yticks(fontsize = fts)
        plt.xlim(0,45792000)
        #plt.ylim(max(tf[0]), min(tf[0]))
        plt.legend(prop={'size': fts}, loc = 'best')
        j += 1 
        
j = 0
plt.subplot(1,2,2)
for key in scenario:
        print(str(key))
        tf= scenario[key]
        plt.plot(tf[0],tf[2],lw=1.5, label= key, color = colormap[j]) #, marker= 'x', s=10, color=colormap[i], label = key
        plt.title('b) Head time series', fontsize = fts)        
        plt.xlabel('Time (s)', fontsize = fts)
        plt.ylabel('Head (m)', fontsize = fts)
        plt.xticks(fontsize = fts)
        plt.yticks(fontsize = fts)
        plt.xlim(0,45792000)
        #plt.ylim(max(tf[0]), min(tf[0]))
        plt.legend(prop={'size': fts}, loc = 'best')
        j += 1 
#plt.savefig('Average_Temperature.png', facecolor='w',frameon=None, metadata=None)
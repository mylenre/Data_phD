# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 23:25:20 2021

@author: s1995204
"""


import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

plt.style.use('seaborn')
colormap = np.array(['teal', 'darkslategray', 'royalblue', 'navy', 'goldenrod', 'palevioletred', 'green', 'black','rosybrown','steelblue'])
os.chdir(r'S:\Data\LOGS\CA_LOGS\corrected')


filelist=glob.glob('*.txt')
N = len(filelist)
name = [i.split('_')[0] for i in filelist]
date = [i.split('.')[0].split('_')[1] for i in filelist]

filelist_i=insets=glob.glob('.\Insets\*')
N_i = len(filelist_i)
name_i = [i.split('_')[1].split('.')[0] for i in filelist_i]

insets = {}
for i in range(N_i): 
   df=pd.read_csv(filelist_i[i], delimiter=',',index_col=0)
   insets[name_i[i]] = df


log = {}
for i in range(N): 
   df=pd.read_csv(filelist[i], delimiter=',')
   log[filelist[i]] = df
   if name[i] == name[i-1]:
       plt.plot(log[filelist[i]]['Temp'],log[filelist[i]]['Depth(mAOD)'], label = 'date: ' + date[i][-2:] + '/' + date[i][:4])
       plt.xlabel('Temperature (°C)')
       plt.ylabel('Depth (mAOD)')
       plt.title(name[i], fontsize=14)
       plt.legend()

   else:
       plt.figure(figsize=(6,8))
       plt.plot(log[filelist[i]]['Temp'],log[filelist[i]]['Depth(mAOD)'], label = 'date: ' + date[i][-2:] + '/' + date[i][:4])
       plt.xlabel('Temperature (°C)')
       plt.ylabel('Depth (mAOD)')
       plt.title(name[i], fontsize=14)
       plt.legend()
       if name[i] in name_i:
           [plt.text(min(log[filelist[i]]['Temp']), insets[name[i]]['Level (mAOD)'][k], insets[name[i]].index[:][k]) for k in  range(len(insets[name[i]].index[:]))]

   mean_T =  np.mean(log[filelist[i]]['Temp'])
   mean_d =  np.mean(log[filelist[i]]['Depth(mAOD)']) 
   min_T =  np.min(log[filelist[i]]['Temp'])
   max_T =  np.max(log[filelist[i]]['Temp'])
   min_d = np.min(log[filelist[i]]['Depth(mAOD)']) 
   max_d = np.max(log[filelist[i]]['Depth(mAOD)']) 
   gradient = round((max_T-min_T)/(max_d-min_d),3)
   
   print(name[i], ': average gradient:', gradient, 'mean temperature:', round(mean_T,2), 'at', round(mean_d,0), 'm')
   
   if name[i] in name_i:
       [plt.axhline(y=insets[name[i]]['Level (mAOD)'][j], xmin=0, xmax=1, c = 'k', lw= '1') for j in range(len(insets[name[i]]['Level (mAOD)']))]
       
  # plt.savefig(name[i] +'_' + date[i] + '.png')  
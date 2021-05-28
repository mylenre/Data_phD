# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 23:23:20 2021

@author: s1995204
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import chain
import seaborn as sns

#%% temperature farr et al., 2020
os.chdir(r'S:\Data\Data_GIS\Temperature\FarrEtAl_2020')
dfi = pd.read_csv('Temperature_FarrEtAl_2020_plot.txt', delimiter=',')
df = dfi[dfi['Value']=='Mean']
mwb = list(df['MWB'].unique())
previous_coalfield = 'initialisation'
for i in mwb:
    select = df[df['MWB']==i]
    coalfield = select.iloc[0]['Coalfield']
    if coalfield != previous_coalfield:
        plt.figure(figsize=(15,8))
        j = 1
    plt.subplot(6,5,j)
    g =sns.scatterplot(x="Depth",y="Temperature (°C)",
              hue="Type",
              data=select, 
              legend=False)
    g.set(xlabel=None)
    g.set(ylabel=None)
    plt.gca().invert_yaxis()
    plt.title(i, fontsize =8)
    plt.tight_layout(pad=0.5, h_pad=None, w_pad=None, rect=None)
    g.set_xlim(left=0, right=1000)
    g.set_ylim(bottom=0, top=40);

    previous_coalfield = select.iloc[0]['Coalfield']
    j += 1
    gradient = (select[select['Type']=='Equilibrium'].iloc[-1]['Temperature (°C)']-select[select['Type']=='Equilibrium'].iloc[0]['Temperature (°C)'])/(select[select['Type']=='Equilibrium'].iloc[-1]['Depth']-select[select['Type']=='Equilibrium'].iloc[0]['Depth'])
    print(i+' :'+ str(round(gradient*1000,2))+ ' °C/km')
#%% temperature farr et al., 2020 version 2
os.chdir(r'R:\Data\Data_GIS\Temperature\FarrEtAl_2020')
dfi = pd.read_csv('Temperature_FarrEtAl_2020_plot2.txt', delimiter=',')
df = dfi[dfi['Value']=='Mean']
mwb = df['MWB'].unique().tolist()
j=1
plt.figure(figsize=(15,8))
for i in mwb:
    select = df[df['MWB']==i]
    plt.subplot(2,5,j)
    g =sns.lineplot(x="Temperature (°C)",y="Depth",
              hue="Type",
              data=select, 
              legend="brief")
    g =sns.scatterplot(x="Temperature (°C)",y="Depth",
              hue="Type",
              data=select, 
              legend=False)    
    g.set(xlabel=None)
    g.set(ylabel=None)
    plt.title(i, fontsize = 10)
    plt.ylabel("Depth", fontsize = 10) # label for x-axis
    plt.xlabel("Temperature", fontsize = 10) # label for y-axis
    plt.tight_layout(pad=0.5, h_pad=None, w_pad=None, rect=None)
    g.set_xlim(left=0, right=40)
    g.set_ylim(bottom=900, top=0);
    j += 1
   
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 08:31:39 2020

@author: s1995204
"""
import numpy as np
import os
import glob
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
os.chdir(r'R:\Data\Data_GIS\CoalAuthority_Data\Water_Data\Water_Data\Water_Level')
filelist=glob.glob('*_WL.txt')
l = np.size(filelist)

fig, ax = plt.subplots(figsize=(8,8))
#plt.figure(figsize=(8,8))    
for i in filelist:
    print(i)
    name= i.split('.')[0]
    id=filelist.index(i)
    data = pd.read_csv(i, parse_dates=['Date'],index_col=['Date']) 
    #data = pd.read_csv(i, delimiter=',', header=0)
    #data.dropna(subset=["Date"], inplace=True)
    #date = data.iloc[:,0]
    #val= data.iloc[:,1]
    data.columns = ['val']
    #plt.subplot(l,1,id+1)
    #plt.plot(date, val, label=name)
    ax.plot(data.index.values,
        data['val'],
       label = name)
# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="Water level",
       title="Water level in shafts")
plt.legend(loc='best')
#plt.savefig('Water_Level.png')  

os.chdir(r'R:\Data\Data_GIS\CoalAuthority_Data\Water_Data\Water_Data\Flow_Rate')
filelist=glob.glob('*.txt')
l = np.size(filelist)
fig, ax = plt.subplots(figsize=(8,8))
for i in filelist:
    print(i)
    name= i.split('.')[0]
    id=filelist.index(i)
    data = pd.read_csv(i, parse_dates=['Date'],index_col=['Date']) 
    data.columns = ['val']
    ax.plot(data.index.values,
        data['val'],
       label = name)
ax.set(xlabel="Date",
       ylabel="Flow rate (L/s)",
       title="Discharge or abstraction rate from shafts")
plt.legend(loc='best')
#plt.savefig('Flow_Rate.png') 
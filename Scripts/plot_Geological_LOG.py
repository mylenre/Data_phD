# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 22:43:14 2021

@author: s1995204
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import glob

os.chdir(r'C:\Users\s1995204\Documents_LOCAL\LOGS\GEOINDEX\files\Litterature')
data = {}
temp = {}
cond = {}

tlist=glob.glob('*_T.txt')
for i in tlist:
    name = i.split('.')[0].split('_')[0]
    value = i.split('.')[0].split('_')[1]
    df = pd.read_csv(i, delimiter=',')
    temp[name] = df
    
klist=glob.glob('*_K.txt')
for i in klist:
    name = i.split('.')[0].split('_')[0]
    value = i.split('.')[0].split('_')[1]
    df = pd.read_csv(i, delimiter=',')
    cond[name] = df

#for key in data.keys():
#    print(key)
#    plt.figure(figsize=(8,4))
#    plt.subplot(1,2,1)
#    plt.scatter(data[key]['K']['Thermal Conductivity'],data[key]['K']['Depth'])
#    plt.gca().invert_yaxis()
#    plt.subplot(1,2,2)
#    plt.plot(data[key]['T']['Temp'],data[key]['T']['Depth'])
#    plt.gca().invert_yaxis()

plt.figure(figsize=(8,4))
plt.subplot(1,2,1)
for key in cond.keys():
    plt.scatter(cond[key]['Thermal Conductivity'],cond[key]['Depth'],marker='|', s=20)
    plt.gca().invert_yaxis()
    plt.xlabel('Heat conductivity')
    plt.ylabel('Depth')
plt.subplot(1,2,2)
for key in temp.keys():
    plt.plot(temp[key]['Temp'],temp[key]['Depth'], label=key)
    plt.gca().invert_yaxis()
    plt.xlabel('Temperature gradient')
    plt.ylabel('Depth')
    plt.legend()
    
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 23:19:57 2020

@author: s1995204
"""

import pandas as pd
import numpy as np
from numpy import log as ln
import matplotlib.pyplot as plt
import os


os.chdir(r'R:\GitHub\Data_phD\Data\Rainfall')
name ={}
Rain= {}
ListavDaily=[]
Listkey=[]
rate=[]

with open('filelist.txt', 'r') as filehandle:
    for line in filehandle:
        line = line[:-1]
        line=line.split(',')
        data = pd.read_csv(line[0], delimiter=',', header=0)
        year=data['Timestamp']
        rf=data['Value']
        date=np.array(year)
        rainfall=np.array(rf)
        name[line[1]]=rainfall

for key,val in name.items():
   # print("key:", key,"val",val)
   if(np.size(val))==120:
       val=val.reshape(12,10)
       avRainfall= np.mean(val, axis=1)
       #plt.figure(figsize=(16,5))
       #plt.plot(avRainfall,label=key)  
       #plt.ylabel('mm')
       #plt.legend(loc="best")
       Rain[key]=avRainfall
       avDaily=np.sum(avRainfall)/365.25
       ListavDaily.append(avDaily)
       Listkey.append(key)
       m3persec=np.sum(avRainfall)/(365.25*24*3600)*1e-3
       rate.append(m3persec)
       

plt.figure(figsize=(16,5))
plt.bar(Listkey[:],ListavDaily[:])
plt.xticks(rotation=90)
plt.title('average daily precipitation (mm)') #L/m2 (*10e-3 m3/m2)

Precipitation=np.stack((Listkey,rate), axis=-1)
np.savetxt('RainfallRate_m3persec.txt', Precipitation)

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:34:26 2019

@author: s1995204
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\2D_Mine_Models\Benchmark\TH\Layers\LM4\V2')
filelist=glob.glob('*\LM4_time_POINTOUT*.tec')

#file_name = input("Enter name : ") 
plt.figure(figsize=(8,6))

for i in filelist:
    print(i)
    id=filelist.index(i)
    this_line = i.split("\\")
    case= this_line[0]
    pt = this_line[1].replace('.','_').split("_")
    name= case + ' : '+ pt[2]
    with open(i, 'r') as file: 
      for line in file:
        if("TITLE" in line):
           continue
        if("VARIABLES" in line):
           continue
        if(' ZONE T' in line):
           #this_line = line.replace('"','').replace(' ','').split("=")
           #name=this_line[2]
           #name=name.rstrip()
           break
    t = np.loadtxt(i, skiprows=3, usecols=0)  
    T = np.loadtxt(i, skiprows=3, usecols=1)
    #ts=t[:]/(3600*24*365.25) #for years
    ts=t[:]/(3600) #for hours
    nbplot=np.size(filelist)
    #plt.subplot(nbplot,1,id+1)
    plt.plot(ts[:],T[:],label=name)
    plt.legend(loc='best')
    #plt.xlabel('Time (yrs)')
    #plt.ylabel('Temperature')
    #plt.title('Tempeature change at '+ name)
    #plt.tight_layout()

plt.xlabel('Time (hours)')
plt.ylabel('Temperature')
plt.title('Tempeature change at selected points')

#plt.legend(fontsize=12)  
plt.savefig('TchangeVSTime.png') 
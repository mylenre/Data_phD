# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:34:26 2019

@author: s1995204
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\Modeling_results\Solar_1D_models\Updates\Model_2')
filelist=glob.glob('TDiff-Wall_time_POINT*.tec')

#file_name = input("Enter name : ") 
plt.figure(figsize=(10,20))

for i in filelist:
    print(i)
    id=filelist.index(i)
    with open(i, 'r') as file: 
      for line in file:
        if("TITLE" in line):
           continue
        if("VARIABLES" in line):
           continue
        if(' ZONE T' in line):
           this_line = line.replace('"','').replace(' ','').split("=")
           name=this_line[2]
           name=name.rstrip()
           break
    t = np.loadtxt(i, skiprows=3, usecols=0)  
    T = np.loadtxt(i, skiprows=3, usecols=1)
    ts=t[:]/(3600*24*365.25)
    nbplot=np.size(filelist)
    plt.subplot(nbplot,1,id+1)
    plt.plot(ts[:],T[:])
    plt.xlabel('Time (yrs)')
    plt.ylabel('Temperature')
    plt.title('Tempeature change at '+ name)
    plt.tight_layout()

#plt.legend(loc='best')
#plt.legend(fontsize=12)  
plt.savefig('TchangeVSTime.png') 
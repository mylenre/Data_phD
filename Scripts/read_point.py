# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:34:26 2019

@author: s1995204
"""
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\Modeling_results\Solar_1D_models\Rock\Flux\Test\1_year')


file_name = input("Enter name : ") 
print(file_name)
with open(file_name+'.tec', 'r') as file: 
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
       

plt.figure(figsize=(18,10))
t = np.loadtxt(file_name+'.tec', skiprows=3, usecols=0)  
T = np.loadtxt(file_name+'.tec', skiprows=3, usecols=1)
t=t[:]/(3600*24*365.25)
plt.plot(t[:],T[:])
plt.xlabel('Time (yrs)')
plt.ylabel('Temperature')
plt.legend(loc='best')
plt.legend(fontsize=12)  
plt.title('Tempeature change at '+ name)
plt.savefig('Tchange_'+name+'.png') 
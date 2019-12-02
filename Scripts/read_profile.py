# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:23:13 2019

@author: s1995204
"""
import matplotlib.pyplot as plt
import numpy as np

time = []
z = []
T= []
#file_name = input("Enter name : ") 

#print(file_name)
#with open(file_name+'.tec', 'r') as file: 
with open('M2_ply_PROD_WELL_t2.tec', 'r') as file:
  next(file)
  for line in file:
    if("TITLE" in line):
       continue
    if("VARIABLES" in line):
       continue
    if(' ZONE T' in line):
       this_line = line.replace('"','').replace('e+','e').split("=")
       time.append(float(this_line[2]))
    else:
       this_line=line.replace('e+','e').split(' ')
       #this_line = list(filter(None, this_line))
       z.append(float(this_line[0].rstrip()))
       T.append(float(this_line[1].rstrip()))
       data = [z,T]
#IDmaxz= z.index(np.max(z)
IDmaxz = []
for i in range(0, len(z)) : 
    if z[i] == np.max(z): 
        IDmaxz.append(i)       
IDsurf = []
for i in range(0, len(z)) : 
    if z[i] == 0: 
        IDsurf.append(i) 
IDsurf=IDsurf[0::2];

#nbplot=len(z)/(id+1)
z= np.array(z) 
T= np.array(T)
time=np.array(time)
time_yrs=time/(3600*24*365)

plt.figure(figsize=(10,10))
plt.rcParams['font.size'] = 12
for i in range(0, np.size(time),10):
    plt.plot(T[IDsurf[i]:IDmaxz[i]],-z[IDsurf[i]:IDmaxz[i]], label=time[i])     
plt.xlabel('Temperature')
plt.ylabel('Depth borehole')
plt.legend(loc='best')
plt.legend(fontsize=12)  
plt.title('Change in sub-surface temperature with time (sec) for a top BC: T=10 C')
plt.savefig("Tprofiles.png") 

plt.figure(figsize=(10,5))
plt.plot(time_yrs,T[IDmaxz])
plt.xlabel('Time (years)')
plt.ylabel('Temperature at ~100m depth')
plt.legend(loc='best')
plt.legend(fontsize=12)  
plt.title('Change in BTH with time')
plt.savefig("BTH.png") 

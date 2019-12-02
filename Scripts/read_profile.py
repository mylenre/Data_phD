# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:23:13 2019

@author: s1995204
"""
import matplotlib.pyplot as plt
import numpy as np

def moving_average(y, K=5):
    """
    2K+1 point moving average of array y
    """
    N = np.size(y)      # find the size of y
    s = np.zeros(N)     # make an array of zeros with the same size
    for n in range(N):  # loop for the moving average
        kmin = max(n-K, 0)    # limit to indices within the array
        kmax = min(n+K+1, N)  # i.e. range 0 to N-1
        s[n] = np.mean(y[kmin:kmax])
    return s            # return the smoothed array

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
IDmaxz = []
for i in range(0, len(z)) : 
    if z[i] == np.max(z): 
        IDmaxz.append(i) 
ID98 = []			#define depth for plotting T change over time
for i in range(0, len(z)) : 
    if z[i] == 98.5: 
        ID98.append(i)       
IDsurf = []
for i in range(0, len(z)) :  
    if z[i] == 0: 
        IDsurf.append(i)         #identify new time step
IDsurf=IDsurf[0::2];             # remove doublons

#nbplot=len(z)/(id+1)
z= np.array(z) 
T= np.array(T)
time=np.array(time)
time_yrs=time/(3600*24*365)

plt.figure(figsize=(20,10))
plt.subplot(1,2,1)
plt.rcParams['font.size'] = 12
for i in range(0, np.size(time),30): # change increment not to plot all time-step profiles
    plt.plot(T[IDsurf[i]:IDmaxz[i]],-z[IDsurf[i]:IDmaxz[i]], label=time[i])     
plt.xlabel('Temperature')
plt.ylabel('Depth borehole')
plt.legend(loc='best')
plt.legend(fontsize=12)  
plt.title('Change in sub-surface temperature with time (s) for a top BC: T=10 C')

plt.subplot(1,2,2)
for i in range(0, np.size(time),30): # change increment not to plot all time-step profiles
    T_smooth = moving_average(T[IDsurf[i]:IDmaxz[i]], K=5)
    plt.plot(T_smooth, -z[IDsurf[i]:IDmaxz[i]], lw=1,label=time[i])   
plt.xlabel('Temperature')
plt.ylabel('Depth borehole')
plt.legend(loc='best')
plt.legend(fontsize=12)  
plt.title('Average change in temperature by 5 nodes intervals')

plt.savefig("Tprofiles.png") 

plt.figure(figsize=(10,10))
plt.subplot(2,1,1)
plt.plot(time_yrs,T[ID98])
plt.xlabel('Time (years)')
plt.ylabel('Temperature at ~98m depth')
plt.legend(loc='best')
plt.legend(fontsize=12)  
plt.title('Change in temperature with time')
#plt.savefig("T98m.png")

plt.subplot(2,1,2)
plt.plot(time_yrs,T[IDmaxz])
plt.xlabel('Time (years)')
plt.ylabel('Bottom Hole temperature')
plt.legend(loc='best')
plt.legend(fontsize=12)  
plt.title('Change in BTH with time')
#plt.savefig("BTH.png") 
plt.savefig("Tchange.png") 
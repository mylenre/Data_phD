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
zi = input("Enter node depth to plot : ") 
print(zi + ' m')
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
IDsurf = []
for i in range(0, len(z)) :  
    if z[i] == 0: 
        IDsurf.append(i)         #identify new time step
IDsurf=IDsurf[0::2];             # remove doublons
IDmaxz = []
for i in range(0, len(z)) : 
    if z[i] == np.max(z): 
        IDmaxz.append(i) 
IDz = []			             #define depth for plotting T change over time
for i in range(0, len(z)) : 
    if z[i] == eval(zi): 
        IDz.append(i)       

z= np.array(z) 
T= np.array(T)
time=np.array(time)
time_day=time/(3600*24)
time_month=time/(3600*24*30.4375)
time_yrs=time/(3600*24*365.25)

timeplot=input("Enter time steps to plot (i.e. [0, 5, 120]) : ") 
timeplot=eval(timeplot)
timeplotval=np.take(time, timeplot)
timeplotval=list(map(str, timeplotval))
print("The time steps are {} s.".format(', '.join(timeplotval)))

plt.figure(figsize=(20,10))
plt.subplot(1,2,1)
plt.rcParams['font.size'] = 12
#for i in range(0, np.size(time),30): # change increment not to plot all time-step profiles
for i in timeplot:
    plt.plot(T[IDsurf[i]:IDmaxz[i]],-z[IDsurf[i]:IDmaxz[i]], label=time_yrs[i])     
plt.xlabel('Temperature')
plt.ylabel('Depth borehole')
plt.legend(loc='best')
plt.legend(fontsize=12)  
plt.title('Sub-surface temperature for different time steps (yrs), with Tsurf=10°C')

YN = input("Plot smooth temperature profile (Y/N)?") 
if YN == 'Y':
    N_av=input("Number of successive nodes to average: ")
    plt.subplot(1,2,2)
    #for i in range(0, np.size(time),30): # change increment not to plot all time-step profiles
    for i in timeplot:
        T_smooth = moving_average(T[IDsurf[i]:IDmaxz[i]], K=eval(N_av))
        plt.plot(T_smooth, -z[IDsurf[i]:IDmaxz[i]], lw=1,label=time[i])   
    plt.xlabel('Temperature')
    plt.ylabel('Depth borehole')
    plt.legend(loc='best')
    plt.legend(fontsize=12)  
    plt.title('Average sub-surface temperature for '+ eval(N_av) + 'nodes')
    plt.savefig("Tprofiles.png") 
else:
    plt.savefig("Tprofiles.png")    

plt.figure(figsize=(10,10))
plt.subplot(2,1,1)
plt.plot(time_yrs,T[IDz])
plt.xlabel('Time (years)')
plt.ylabel('Temperature at '+ zi + ' m depth', )
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
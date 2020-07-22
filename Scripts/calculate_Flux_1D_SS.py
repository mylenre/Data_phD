# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:44:57 2020

@author: s1995204
"""

import matplotlib.pyplot as plt
import numpy as np
import os
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\30_years\1_Sensitivity_Analysis\Conductivity\2_PROD')
time = []
node = {}
N= 10001  #need update
i=0
xflux = []
flux = {}

#define rock properties
kth = 1.2
#poro = 0.1
#K = (kth* poro)+(1-poro)*0.63 #Need to create a list of kth & porosity 
#                           #for each cell in put in loop
                           
####### profile #######


file_name='TDiff-Wall_ply_OUT_t1'
#file_name='BHE3_ply_profile_vert_2_t5'

print(file_name)
with open(file_name+'.tec', 'r') as file: 
  next(file)
  for line in file:
    if("TITLE" in line):
       continue
    if("VARIABLES" in line):
       continue
    if(' ZONE T' in line):
       this_line = line.replace('"','').replace('e+','e').split("=")
       time.append(float(this_line[2]))
       j=0
       x = []
       T = []
       i=i+1
       print("time step : " + str(i-1))
       continue   
    if j < N:
          this_line=line.replace('e+','e').split(' ')
          x.append(float(this_line[0].rstrip()))
          T.append(float(this_line[1].rstrip()))
          j=j+1
    node[time[i-1]] = [x,T]
    

####### Plot profile #######
print('Number of time steps: ' + str(np.size(time)))
print("Available time steps: %s", node.keys())          

timeplot=input("Enter time steps to plot (i.e. [0, 5, 120]) : ") 
#t = input("Enter time step (sec) : ") #1000
timeplot=eval(timeplot)

time=np.array(time)
time_hour = time/60
time_day=time/(3600*24)
time_month=time/(3600*24*30.4375)
time_yrs=time/(3600*24*366)

time_scale= time_yrs[:]

plt.figure(figsize=(16,8))
plt.subplot(1,2,1)

plt.rcParams['font.size'] = 12
for i in timeplot:
    ts = list(node.keys())[i]
    val_time = node[ts]
    plt.plot(val_time[0][0:2000], val_time[1][0:2000], lw=2, label=str(int(time_scale[i])))     
plt.xlabel('Distance Z (m)')
plt.ylabel('Temperature')
plt.legend(loc='best')
plt.axhline(y=0, xmin=0, xmax=1, linewidth=1, color='r', ls='--')
plt.axvline(x=50, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
plt.axvline(x=90, ymin=0, ymax=1, linewidth=1, color='k', ls='--')

plt.title('Temperature along the line' )

#thermal conductivity
k=[]
#for i in range(len(T)):
#    if val_time[0][i]<50:
#        k.append(1.2)
#    if (val_time[0][i]>=50) and (val_time[0][i]<250):
#        k.append(1.8)
#    if val_time[0][i]>=250:
#        k.append(2.3)
for i in range(len(T)):
        k.append(kth)                     

#define size of each element --> to verify
xsize = [0]
for i in range(len(val_time[0])):
     if i == 0:
         continue
     else:
         sx = val_time[0][i] - val_time[0][i-1] 
         xsize.append(sx)
xsize[0] = xsize[1]

#calculate flux - Finite difference approach
#f = open('flux.txt', 'a')  
plt.subplot(1,2,2)
for i in timeplot:
    ts = list(node.keys())[i]
    ts_name = str(ts)
    val_time = node[ts]
    xi = val_time[0]
    Ti = val_time[1]
    xflux=[]

    for ii in range(len(xi)):
           if ii == 0 :
              Tn = Ti[ii]
              Txn = Ti[ii+1]
              q = k[ii] * (Txn - Tn)/(xsize[ii])
           if ii == N-1 :
              Tn = Ti[ii]
              Txp = Ti[ii-1]
              q = k[ii] * (Tn - Txp)/(xsize[ii])
           else :
              Txp = Ti[ii-1]
              Txn = Ti[ii+1]
              q = k[ii] * ((Txn - Txp)/(2 * xsize[ii])) 
           xflux.append(q)
    tab = np.vstack((xi, xflux)).T#[xi,xflux]
    np.savetxt('Flux_ts_' + ts_name +'.txt', tab, fmt='%f')
    #f.write('time step: %s\n' % ts_name )     
    flux[ts_name] = tab
    z = plt.plot(xi[1:2000],xflux[1:2000])
#f.close()
plt.axhline(y=0, xmin=0, xmax=1, linewidth=1, color='r', ls='--')
plt.axhline(y=0, xmin=0.27, xmax=0.45, linewidth=2, color='k', ls='-') #50-90m deep BH
plt.axvline(x=50, ymin=0.1, ymax=0.8, linewidth=2, color='k', ls='--')
plt.axvline(x=90, ymin=0.1, ymax=0.8, linewidth=2, color='k', ls='--')

#plt.axhline(y=0, xmin=0.09, xmax=0.45, linewidth=2, color='k', ls='-') #5-45m deep BH
#plt.axvline(x=50, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
#plt.axvline(x=5, ymin=0.1, ymax=0.8, linewidth=2, color='k', ls='--')
#plt.axvline(x=45, ymin=0.1, ymax=0.8, linewidth=2, color='k', ls='--')


#plt.axvline(x=250, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
#plt.axvline(x=450, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
#plt.axvline(x=650, ymin=0, ymax=1, linewidth=1, color='k', ls='--')

plt.xlabel('Distance Z (m)')
plt.ylabel('Flux (W/m2)')
plt.title('Vertical flux' )
#plt.suptitle('Change in the temperature profile and flux due to surface warming for 1000 years')
#plt.suptitle('Steady state profile with constant flux (Production in 2200 m2) - shallow well ')
#plt.suptitle('Steady state profile - CUT well ')
#plt.suptitle('Steady state profile with solar flux - 1000 W extraction ')

plt.savefig('Flux_prod.png')  





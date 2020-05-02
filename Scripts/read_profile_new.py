# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:23:13 2019

@author: s1995204
"""
import matplotlib.pyplot as plt
import numpy as np
import os
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\2D_Mine_Models\Benchmark\TH\Layers\LM4\V2\COMPLEX_v2')

time = []
x = []
x2 = []
y = []
Tx= []
Tx2= []
Ty= []

####### profile X1 #######


file_name='LM4_ply_XLINE_t1'
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
    else:
       this_line=line.replace('e+','e').split(' ')
       #this_line = list(filter(None, this_line))
       x.append(float(this_line[0].rstrip()))
       Tx.append(float(this_line[1].rstrip()))
       data = [x,Tx]

IDminx = []
for i in range(0, len(x)) :  
    if x[i] == 0: 
        IDminx.append(i)         #identify new time step
IDmaxx = []
for i in range(0, len(x)) : 
    if x[i] == np.max(x): 
        IDmaxx.append(i) 
    
x= np.array(x) 
Tx= np.array(Tx)


####### profile X2 #######


file_name='LM4_ply_XLINE2_t3'
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
       #time.append(float(this_line[2]))
    else:
       this_line=line.replace('e+','e').split(' ')
       #this_line = list(filter(None, this_line))
       x2.append(float(this_line[0].rstrip()))
       Tx2.append(float(this_line[1].rstrip()))
       data = [x2,Tx2]
    
x2= np.array(x2) 
Tx2= np.array(Tx2)

####### profile Y #######

file_name='LM4_ply_YLINE_t2'
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
       #time.append(float(this_line[2]))
    else:
       this_line=line.replace('e+','e').split(' ')
       #this_line = list(filter(None, this_line))
       y.append(float(this_line[0].rstrip()))
       Ty.append(float(this_line[1].rstrip()))
       data = [y,Ty]
IDminy = []
for i in range(0, len(y)) :  
    if y[i] == 0: 
        IDminy.append(i)         #identify new time step
IDmaxy = []
for i in range(0, len(y)) : 
    if y[i] == np.max(y): 
        IDmaxy.append(i) 
    
y= np.array(y) 
Ty= np.array(Ty)

####### time #######
print('Number of time steps: ' + str(np.size(time)))

timeplot=input("Enter time steps to plot (i.e. [0, 5, 120]) : ") 
timeplot=eval(timeplot)

time=np.array(time)
time_hour = time/60
time_day=time/(3600*24)
time_month=time/(3600*24*30.4375)
time_yrs=time/(3600*24*365.25)

time_scale = time_hour[:]
time_name = '(min)'

plt.figure(figsize=(20,8))

####### Plot profile X #######
plt.subplot(1,3,1)
plt.rcParams['font.size'] = 12
for i in timeplot:
    plt.plot(x[IDminx[i]:IDmaxx[i]], Tx[IDminx[i]:IDmaxx[i]], lw=2, label=str(int(time_scale[i])))     
plt.xlabel('Distance X')
plt.ylabel('Temperature')
plt.legend(loc='best')
plt.legend(fontsize=12)  
plt.title('Temperature along X in permeable layer' )

####### Plot profile X2 #######
plt.subplot(1,3,2)
plt.rcParams['font.size'] = 12
for i in timeplot:
    plt.plot(x2[IDminx[i]:IDmaxx[i]], Tx2[IDminx[i]:IDmaxx[i]], lw=2, label=str(int(time_scale[i])))     
plt.xlabel('Distance X')
plt.ylabel('Temperature')
plt.legend(loc='best')
plt.legend(fontsize=12)  
plt.title('Temperature along X in impermeable layer ')

####### profile Y #######
plt.subplot(1,3,3)
plt.rcParams['font.size'] = 12
for i in timeplot:
    plt.plot(Ty[IDminy[i]:IDmaxy[i]],-y[IDminy[i]:IDmaxy[i]], lw=2, label=str(int(time_scale[i])))     
plt.xlabel('Temperature')
plt.ylabel('Depth Y')
plt.legend(loc='best')
plt.legend(fontsize=12)  
plt.title('Temperature along Y ')
plt.suptitle('Temperature profile along X and Y directions for different time steps '+ time_name)
plt.savefig("Tprofiles.png")  
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 20:47:35 2020

@author: s1995204
"""

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import os
import numpy as np
import pandas as pd
import glob

plt.style.use('seaborn')
model_name=input('enter model name:')
filename=model_name+'_domain_tri.tec'


#%% MODEL 1
#%% read nodes/elements from mesh file
os.chdir(r'S:\Modeling\2D_Models\Geobattery\NEW\2_100_m\0_No_mine\XY')

file = open(model_name+'.msh','r')
N = int(file.readlines()[4].rstrip())
file = open(model_name+'.msh','r')
lines=file.readlines()[5:N+5]
lines = np.array([lines.split(' ') for lines in lines])
nodes=pd.DataFrame(lines, columns = ['id','x','y','z'])


file = open(model_name+'.msh','r')
lines=file.readlines()[N+7:-1]
lines = np.array([lines.split(' ') for lines in lines])[:,3::]
elements=pd.DataFrame(lines, columns = ['n1','n2','n3'])


#%
time = []
x = []
y = []
z = []
T = []
node1 = {}
i=0

print(filename)
with open(filename, 'r') as file: 
  next(file)
  for line in file:
    if("TITLE" in line):
       continue
    if('STRANDID' in line):
       continue
    if("VARIABLES" in line):
       this_line = line.replace('"','').replace('=',',').split(",")
       variables = this_line[1:np.size(this_line)]
       continue
    if('ZONE T' in line):
       this_line = line.replace('"','').replace('e+','e').replace('s','').replace('=',',').split(",")
       time.append(float(this_line[1]))
       j=0
       x = []
       y = []
       z = []
       T = []
       i=i+1
       print("time step : " + str(i-1))
       continue   
    if j < N:
          this_line=line.replace('e+','e').split(' ')
          x.append(float(this_line[0].rstrip()))
          y.append(float(this_line[1].rstrip()))
          z.append(float(this_line[2].rstrip()))
          T.append(float(this_line[3].rstrip())) #change here
          j=j+1
    node1[time[i-1]] = [x,y,z,T]
    
#% calculate differences between two time steps
final_ts = int((pd.DataFrame(node1.keys()))[0][len(node1)-1])
first_ts = int((pd.DataFrame(node1.keys()))[0][0]) #0
final_val = node1[final_ts]
first_val = node1[first_ts]

#extract values from a specific slice
x = np.array(final_val[0]).transpose()
y = np.array(final_val[1]).transpose() #change here

#% create unstructured grid
nodes_x = nodes['x'].tolist()
nodes_y = nodes['y'].tolist()
triangles = elements.loc[:,['n1','n2','n3']].values.tolist()  
#a=np.around(np.array(np.linspace(-3,3,num=40)),1).tolist()
triangulation = tri.Triangulation(nodes_x,nodes_y,triangles) 


#%

plt.figure(figsize=(12,4))
plt.subplot(121)
scalars = np.array(final_val[3])
a=np.around(np.array(np.linspace(0,30,num=31)),1).tolist()

plt.tricontourf(triangulation,scalars,cmap='seismic', levels=a)

plt.colorbar()
plt.xlabel('Distance along profile (m)')
plt.ylabel('Depth (m)')
plt.title('Temperature distribution after 20 years (°C)')

plt.axvline(x=0, ymin=0, ymax=1, linewidth=2, color='k')
plt.axvline(x=np.max(final_val[0]), ymin=0, ymax=1, linewidth=2, color='k')
plt.axhline(y=0, xmin=0, xmax=1, linewidth=2, color='k')
plt.axhline(y=np.min(final_val[2]), xmin=0, xmax=1, linewidth=2, color='k')

a = 0.475 #0.55
b = 0.975 #0.75
plt.axvline(x=110, ymin=a, ymax=b, linewidth=2, color='k')
plt.axvline(x=140, ymin=a, ymax=b, linewidth=2, color='k')
plt.axvline(x=170, ymin=a, ymax=b, linewidth=2, color='k')
plt.axvline(x=200, ymin=a, ymax=b, linewidth=2, color='k')
#
#plt.axvline(x=180, ymin=0.38, ymax=0.4, linewidth=2, color='k')
#plt.axvline(x=280, ymin=0.38, ymax=0.4, linewidth=2, color='k')
#plt.axhline(y=-120, xmin=0.6, xmax=0.93, linewidth=2, color='k')
#plt.axhline(y=-124, xmin=0.6, xmax=0.93, linewidth=2, color='k')



plt.subplot(122)

Tval = (np.array(final_val[3]) - np.array(first_val[3])).T
Tval = Tval.tolist()
scalars = Tval
a=np.around(np.array(np.linspace(-20,20,num=41)),1).tolist()

plt.tricontourf(triangulation,scalars,cmap='seismic', levels=a)

plt.colorbar()
plt.xlabel('Distance along profile (m)')
plt.ylabel('Depth (m)')
plt.title('Thermal footprint of heat extraction after 20 years (°C)')

plt.axvline(x=0, ymin=0, ymax=1, linewidth=2, color='k')
plt.axvline(x=np.max(final_val[0]), ymin=0, ymax=1, linewidth=2, color='k')
plt.axhline(y=0, xmin=0, xmax=1, linewidth=2, color='k')
plt.axhline(y=np.min(final_val[2]), xmin=0, xmax=1, linewidth=2, color='k')

a = 0.475 #0.55
b = 0.975 #0.75
plt.axvline(x=110, ymin=a, ymax=b, linewidth=2, color='k')
plt.axvline(x=140, ymin=a, ymax=b, linewidth=2, color='k')
plt.axvline(x=170, ymin=a, ymax=b, linewidth=2, color='k')
plt.axvline(x=200, ymin=a, ymax=b, linewidth=2, color='k')
#
#plt.axvline(x=180, ymin=0.38, ymax=0.4, linewidth=2, color='k')
#plt.axvline(x=280, ymin=0.38, ymax=0.4, linewidth=2, color='k')
#plt.axhline(y=-120, xmin=0.6, xmax=0.93, linewidth=2, color='k')
#plt.axhline(y=-124, xmin=0.6, xmax=0.93, linewidth=2, color='k')

plt.tight_layout()
plt.savefig('Residual_Temp_t20.png')  

    
#%% MODEL 2
#%%
os.chdir(r'S:\Modeling\2D_Models\Geobattery\NEW\2_100_m\1_Mine\XY')
time = []
x = []
y = []
z = []
T = []
node2 = {}
i=0

print(filename)
with open(filename, 'r') as file: 
  next(file)
  for line in file:
    if("TITLE" in line):
       continue
    if('STRANDID' in line):
       continue
    if("VARIABLES" in line):
       this_line = line.replace('"','').replace('=',',').split(",")
       variables = this_line[1:np.size(this_line)]
       continue
    if('ZONE T' in line):
       this_line = line.replace('"','').replace('e+','e').replace('s','').replace('=',',').split(",")
       time.append(float(this_line[1]))
       j=0
       x = []
       y = []
       z = []
       T = []
       i=i+1
       print("time step : " + str(i-1))
       continue   
    if j < N:
          this_line=line.replace('e+','e').split(' ')
          x.append(float(this_line[0].rstrip()))
          y.append(float(this_line[1].rstrip()))
          z.append(float(this_line[2].rstrip()))
          T.append(float(this_line[3].rstrip())) #change here
          j=j+1
    node2[time[i-1]] = [x,y,z,T]  
    
#% calculate differences between two time steps
final_ts = int((pd.DataFrame(node2.keys()))[0][len(node2)-1])
first_ts = int((pd.DataFrame(node2.keys()))[0][0]) #0
final_val = node2[final_ts]
first_val = node2[first_ts]

#extract values from a specific slice
x = np.array(final_val[0]).transpose()
y = np.array(final_val[1]).transpose() #change here

#% create unstructured grid
nodes_x = nodes['x'].tolist()
nodes_y = nodes['y'].tolist()
triangles = elements.loc[:,['n1','n2','n3']].values.tolist()  
#a=np.around(np.array(np.linspace(-3,3,num=40)),1).tolist()
triangulation = tri.Triangulation(nodes_x,nodes_y,triangles) 


plt.figure(figsize=(12,4))
plt.subplot(121)
scalars = np.array(final_val[3])
a=np.around(np.array(np.linspace(0,30,num=31)),1).tolist()

plt.tricontourf(triangulation,scalars,cmap='seismic', levels=a)

plt.colorbar()
plt.xlabel('Distance along profile (m)')
plt.ylabel('Depth (m)')
plt.title('Temperature distribution after 20 years (°C)')

plt.axvline(x=0, ymin=0, ymax=1, linewidth=2, color='k')
plt.axvline(x=np.max(final_val[0]), ymin=0, ymax=1, linewidth=2, color='k')
plt.axhline(y=0, xmin=0, xmax=1, linewidth=2, color='k')
plt.axhline(y=np.min(final_val[2]), xmin=0, xmax=1, linewidth=2, color='k')

plt.axvline(x=110, ymin=0.55, ymax=0.75, linewidth=2, color='k')
plt.axvline(x=140, ymin=0.55, ymax=0.75, linewidth=2, color='k')
plt.axvline(x=170, ymin=0.55, ymax=0.75, linewidth=2, color='k')
plt.axvline(x=200, ymin=0.55, ymax=0.75, linewidth=2, color='k')

plt.axvline(x=180, ymin=0.38, ymax=0.4, linewidth=2, color='k')
plt.axvline(x=280, ymin=0.38, ymax=0.4, linewidth=2, color='k')
plt.axhline(y=-120, xmin=0.6, xmax=0.93, linewidth=2, color='k')
plt.axhline(y=-124, xmin=0.6, xmax=0.93, linewidth=2, color='k')



plt.subplot(122)

Tval = (np.array(final_val[3]) - np.array(first_val[3])).T
Tval = Tval.tolist()
scalars = Tval
a=np.around(np.array(np.linspace(-20,20,num=41)),1).tolist()

plt.tricontourf(triangulation,scalars,cmap='seismic', levels=a)

plt.colorbar()
plt.xlabel('Distance along profile (m)')
plt.ylabel('Depth (m)')
plt.title('Thermal footprint of heat extraction after 20 years (°C)')

plt.axvline(x=0, ymin=0, ymax=1, linewidth=2, color='k')
plt.axvline(x=np.max(final_val[0]), ymin=0, ymax=1, linewidth=2, color='k')
plt.axhline(y=0, xmin=0, xmax=1, linewidth=2, color='k')
plt.axhline(y=np.min(final_val[2]), xmin=0, xmax=1, linewidth=2, color='k')

plt.axvline(x=110, ymin=0.55, ymax=0.75, linewidth=2, color='k')
plt.axvline(x=140, ymin=0.55, ymax=0.75, linewidth=2, color='k')
plt.axvline(x=170, ymin=0.55, ymax=0.75, linewidth=2, color='k')
plt.axvline(x=200, ymin=0.55, ymax=0.75, linewidth=2, color='k')

plt.axvline(x=180, ymin=0.38, ymax=0.4, linewidth=2, color='k')
plt.axvline(x=280, ymin=0.38, ymax=0.4, linewidth=2, color='k')
plt.axhline(y=-120, xmin=0.6, xmax=0.93, linewidth=2, color='k')
plt.axhline(y=-124, xmin=0.6, xmax=0.93, linewidth=2, color='k')
plt.tight_layout()

plt.savefig('Residual_Temp_t30_m2.png')  

# %% calculate differences between two models
m1 = int((pd.DataFrame(node1.keys()))[0][len(node1)-1])
m2 = int((pd.DataFrame(node2.keys()))[0][len(node2)-1])
final_val = node1[m1]
first_val = node2[m2]

#extract values from a specific slice
x = np.array(final_val[0]).transpose()
y = np.array(final_val[1]).transpose() #change here
Tval = (np.array(first_val[3]) - np.array(final_val[3])).T
Tval = Tval.tolist()

#% create unstructured grid
nodes_x = nodes['x'].tolist()
nodes_y = nodes['y'].tolist() #change here
triangles = elements.loc[:,['n1','n2','n3']].values.tolist()  
a=np.around(np.array(np.linspace(-30,30,num=61)),1).tolist()
#a=np.around(np.array(np.linspace(-3,3,num=40)),1).tolist()

scalars = Tval
plt.figure(figsize=(10,5))
triangulation = tri.Triangulation(nodes_x,nodes_y,triangles) 
#plt.tricontourf(triangulation,scalars,cmap='OrRd', levels=a)
plt.tricontourf(triangulation,scalars,cmap='seismic', levels=a)

plt.colorbar()
plt.xlabel('Distance along profile (m)')
plt.ylabel('Depth (m)')
plt.title('Thermal footprint of the heat from mines after 20 years of production (°C)')

plt.axvline(x=0, ymin=0, ymax=1, linewidth=2, color='k')
plt.axvline(x=np.max(final_val[0]), ymin=0, ymax=1, linewidth=2, color='k')
plt.axhline(y=0, xmin=0, xmax=1, linewidth=2, color='k')
plt.axhline(y=np.min(final_val[2]), xmin=0, xmax=1, linewidth=2, color='k')

plt.axvline(x=110, ymin=0.55, ymax=0.75, linewidth=2, color='k')
plt.axvline(x=140, ymin=0.55, ymax=0.75, linewidth=2, color='k')
plt.axvline(x=170, ymin=0.55, ymax=0.75, linewidth=2, color='k')
plt.axvline(x=200, ymin=0.55, ymax=0.75, linewidth=2, color='k')

plt.axvline(x=180, ymin=0.38, ymax=0.4, linewidth=2, color='k')
plt.axvline(x=280, ymin=0.38, ymax=0.4, linewidth=2, color='k')
plt.axhline(y=-120, xmin=0.6, xmax=0.93, linewidth=2, color='k')
plt.axhline(y=-124, xmin=0.6, xmax=0.93, linewidth=2, color='k')
#plt.savefig('T_Diff_Mine-NoMine.png')  
plt.savefig('T_Diff_NoMine-Mine.png')  

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
plt.style.use('seaborn')


os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\Geobattery\2_Version_2\1_Geothermal_Flux_No_Mine')
model_name=input('enter model name:')
filename=model_name+'_domain_tri.tec'

#%% read nodes from mesh file
#node_file = 'NODES.txt'
#nodes=pd.read_csv(node_file, delimiter=',')
#N = len(nodes)
file = open(model_name+'.msh','r')
N = int(file.readlines()[4].rstrip())
file = open(model_name+'.msh','r')
lines=file.readlines()[5:N+5]
lines = np.array([lines.split(' ') for lines in lines])
nodes=pd.DataFrame(lines, columns = ['id','x','y','z'])

#%% read elements from mesh file
#element_file = 'ELEMENTS.txt'
#elements=pd.read_csv(element_file, delimiter=',')
file = open(model_name+'.msh','r')
lines=file.readlines()[N+7:-1]
lines = np.array([lines.split(' ') for lines in lines])[:,3::]
elements=pd.DataFrame(lines, columns = ['n1','n2','n3'])


#%%
time = []
x = []
y = []
z = []
T = []
node = {}
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
          T.append(float(this_line[4].rstrip())) #change here
          j=j+1
    node[time[i-1]] = [x,y,z,T]
    
    
   
# %% calculate differences between two time steps
final_ts = int((pd.DataFrame(node.keys()))[0][len(node)-1])
first_ts = int((pd.DataFrame(node.keys()))[0][0]) #0
final_val = node[final_ts]
first_val = node[first_ts]

#extract values from a specific slice
x = np.array(final_val[0]).transpose()
y = np.array(final_val[2]).transpose() #change here
Tval = (np.array(final_val[3]) - np.array(first_val[3])).T
Tval = Tval.tolist()

#% create unstructured grid
nodes_x = nodes['x'].tolist()
nodes_y = nodes['z'].tolist()
triangles = elements.loc[:,['n1','n2','n3']].values.tolist()  
a=np.around(np.array(np.linspace(-2.6,2.6,num=40)),1).tolist()
#a=np.around(np.array(np.linspace(-3,3,num=40)),1).tolist()

scalars = Tval
plt.figure(figsize=(8,4))
triangulation = tri.Triangulation(nodes_x,nodes_y,triangles) 
plt.tricontourf(triangulation,scalars,cmap='hot', levels=a[0:20])
#plt.tricontourf(triangulation,scalars,cmap='seismic', levels=a)

plt.colorbar()
plt.xlabel('Distance along profile (m)')
plt.ylabel('Depth (m)')
plt.title('Residual temperature (°C)')

plt.axvline(x=0, ymin=0, ymax=1, linewidth=2, color='k')
plt.axvline(x=np.max(final_val[0]), ymin=0, ymax=1, linewidth=2, color='k')
plt.axhline(y=0, xmin=0, xmax=1, linewidth=2, color='k')
plt.axhline(y=np.min(final_val[2]), xmin=0, xmax=1, linewidth=2, color='k')

plt.axvline(x=100, ymin=0.55, ymax=0.75, linewidth=2, color='k')
plt.axvline(x=200, ymin=0.55, ymax=0.75, linewidth=2, color='k')

plt.axvline(x=180, ymin=0.38, ymax=0.4, linewidth=2, color='k')
plt.axvline(x=280, ymin=0.38, ymax=0.4, linewidth=2, color='k')
plt.axhline(y=-120, xmin=0.6, xmax=0.93, linewidth=2, color='k')
plt.axhline(y=-124, xmin=0.6, xmax=0.93, linewidth=2, color='k')

#plt.axvline(x=0, ymin=0, ymax=300, linewidth=2, color='k')
#plt.axvline(x=800, ymin=0, ymax=300, linewidth=2, color='k')
#plt.axhline(y=0, xmin=0, xmax=1, linewidth=2, color='k')
#plt.axhline(y=-300, xmin=0, xmax=1, linewidth=2, color='k')
#
#
#plt.axvline(x=375, ymin=0, ymax=300, linewidth=2, color='k')
#plt.axvline(x=425, ymin=0, ymax=300, linewidth=2, color='k')
#plt.axhline(y=-99, xmin=0, xmax=1, linewidth=2, color='k')
#plt.axhline(y=-129, xmin=0, xmax=1, linewidth=2, color='k')
#plt.axhline(y=-159, xmin=0, xmax=1, linewidth=2, color='k')

#plt.axhline(y=-114, xmin=0, xmax=1, linewidth=2, color='k')
#plt.axhline(y=-144, xmin=0, xmax=1, linewidth=2, color='k')
#plt.axhline(y=-174, xmin=0, xmax=1, linewidth=2, color='k')

plt.savefig('Residual_Temp_t100.png')  

test=np.array(final_val).T


# -*- coding: utf-8 -*-
"""
Created on Sun May  3 00:41:21 2020

@author: s1995204
"""
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd

os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\2_3D-SI_100')
filename='SI_BHE_sfc_surface_output_t0.tec'

time = []
x = []
y = []
z = []
T = []
node = {}
N= 10857
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
       time.append(float(this_line[2]))
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
          T.append(float(this_line[3].rstrip()))
          j=j+1
    node[time[i-1]] = [x,y,z,T]
    
    
    
    
#%% v1
# extract values for time step t  
print(pd.DataFrame(node.keys(), columns=['Available time steps:']))          
t=pd.DataFrame(node.keys())[0][eval(input("Enter index of time step : "))]
val = node[t]

#extract values from a specific slice
print("x = 0, y = 1, z = 2")   
hslice = val[eval(input("Slice: "))]  # the coordinate along which is drawn the profile
s0 = [i for i,x in enumerate(hslice) if x == 0]
x = np.array(val[eval(input("Horizontal direction: "))]).transpose()
y = np.array(val[eval(input("Vertical direction: "))]).transpose()
Tval=np.array(val[3]).T
data = np.array([x,y, Tval]).T

# find unique values of x and y
xu = np.unique(x)
yu = -np.sort(-np.unique(y))

#define size of each element: nsize = size n -1 
# the first element is the distance btween x and x-1
xsize = []
ysize = []

for i in range(1,np.size(xu),1):
         sx = abs(xu[i] - xu[i-1])
         xsize.append(sx)
for i in range(1,np.size(yu),1):
         sy = abs(yu[i] - yu[i-1])
         ysize.append(sy)
         
# calculate flux
Kth=2.22
xasc=[]
yasc=[]
Tasc=[]
xflux = []
yflux = []
Q = []

for ii in range(0,len(xu)-1,1):
    print('node x n°' + str(ii))
    for jj in range(0,len(yu)-1,1):
          print('node y n°' + str(jj))
          Ti = float(data[np.logical_and(data[:,0]==xu[ii], data[:,1]==yu[jj] ),2])
          Tasc.append(Ti) 
          Txn = float(data[np.logical_and(data[:,0]==xu[ii+1], data[:,1]==yu[jj] ),2])
          if ii == 0:
              qx = ((Ti - Txn)/(xsize[ii])) * Kth
          if ii != 0:            
              Txp = float(data[np.logical_and(data[:,0]==xu[ii-1], data[:,1]==yu[jj] ),2])
              qx = ((Txp - Txn)/(xsize[ii-1]+xsize[ii])) * Kth
              #qy = ((Ti - Txn)/xsize[ii]) * Kth

          Tyn = float(data[np.logical_and(data[:,0]==xu[ii], data[:,1]==yu[jj+1] ),2])
          if jj == 0:
              qy = ((Ti - Tyn)/(ysize[jj])) * Kth
          if jj != 0:            
              Typ = float(data[np.logical_and(data[:,0]==xu[ii], data[:,1]==yu[jj-1] ),2])
              qy = ((Typ - Tyn)/(ysize[jj-1]+ysize[jj])) * Kth
              #qy = ((Ti - Tyn)/ysize[jj]) * Kth
              
          xasc.append(xu[ii])  
          yasc.append(yu[jj])
          q  = np.sqrt(qx**2+qy**2)
          xflux.append(qx)
          yflux.append(qy)
          Q.append(q)    
        
# save results in text file
tab = np.vstack((xasc, yasc, Tasc, xflux, yflux, Q)).T
np.savetxt('Flux_Results_t' + str(time) +'_v1.txt', tab, fmt='%f')

# plot results
a=list(np.around(np.array(np.linspace(0,15,16)),1))
b=list(np.around(np.array(np.linspace(-5.2,0.8,10)),1))
c=list(np.around(np.array(np.linspace(-4,4,9)),1))
 
T2D = np.reshape(Tasc,(len(yu)-1,len(xu)-1), order = 'F')        
xflux2D = np.reshape(xflux,(len(yu)-1,len(xu)-1), order = 'F')
yflux2D = np.reshape(yflux,(len(yu)-1,len(xu)-1), order = 'F')

plt.figure(figsize=(15,4))
#Temperature
plt.subplot(1,3,1)
z1 = plt.contourf(xu[0:20],yu[0:-1],T2D[:,0:20], cmap='coolwarm', levels=a)
plt.colorbar(z1, shrink=0.9)
plt.xlabel('Distance X')
plt.ylabel('Depth')
plt.title('Temperature' )

#Horizontal flux
plt.subplot(1,3,2)
z2 = plt.contourf(xu[0:20],yu[0:-1],xflux2D[:,0:20],cmap='Spectral_r', levels=b)
plt.colorbar(z2, shrink=0.9)
#plt.clim(-1000, 1000)
plt.xlabel('Distance X')
plt.title('Horizontal flux' )

#vertical flux
plt.subplot(1,3,3)
z3 = plt.contourf(xu[0:20],yu[0:-1],yflux2D[:,0:20],cmap='Spectral_r', levels=c)
plt.colorbar(z3, shrink=0.9)
plt.xlabel('Distance X')
plt.title('Vertical flux' )
plt.tight_layout()

plt.savefig('Flux' + str(t) + '_v1.png')  


#%% v2

# extract values for time step t  
print(pd.DataFrame(node.keys(), columns=['Available time steps:']))          
t=pd.DataFrame(node.keys())[0][eval(input("Enter index of time step : "))]
val = node[t]


#extract values from a specific slice
print("x = 0, y = 1, z = 2")   
hslice = val[eval(input("Slice: "))]  # the coordinate along which is drawn the profile
s0 = [i for i,x in enumerate(hslice) if x == 0]
x = np.array(val[eval(input("Horizontal direction: "))]).transpose()
y = np.array(val[eval(input("Vertical direction: "))]).transpose()
Tval=np.array(val[3]).T
data = np.array([x,y, Tval]).T

# find unique values of x and y
xu = np.unique(x)
yu = -np.sort(-np.unique(y))

#define size of each element: nsize = size n -1 
# the first element is the distance btween x and x-1
xsize = []
ysize = []

for i in range(1,np.size(xu),1):
         sx = abs(xu[i] - xu[i-1])
         xsize.append(sx)
for i in range(1,np.size(yu),1):
         sy = abs(yu[i] - yu[i-1])
         ysize.append(sy)
         
# calculate flux
Kth=2.22
xasc=[]
yasc=[]
Tasc=[]
xflux = []
yflux = []
Q = []
         
for ii in range(1,len(xu)-1,1):
    print('node x n°' + str(ii))
    for jj in range(1,len(yu)-1,1):
          print('node y n°' + str(jj))
          Ti = float(data[np.logical_and(data[:,0]==xu[ii], data[:,1]==yu[jj] ),2])
          Tasc.append(Ti) 
          Txp = float(data[np.logical_and(data[:,0]==xu[ii-1], data[:,1]==yu[jj] ),2])
          if ii == len(xu):
              qx = -((Ti - Txp)/xsize[ii-1]) * Kth
          if ii != len(xu):            
              Txn = float(data[np.logical_and(data[:,0]==xu[ii+1], data[:,1]==yu[jj] ),2])
              #qx = - ((Txn - Txp)/(xsize[ii-1]+xsize[ii-2])) * Kth
              qx =- ((Ti - Txp)/xsize[ii-1]) * Kth   
              
          Typ = float(data[np.logical_and(data[:,0]==xu[ii], data[:,1]==yu[jj-1] ),2])
          if jj == len(yu):
              qy = -((Ti - Typ)/ysize[jj-1]) * Kth
          if jj != len(yu):
              #Tyn = float(data[np.logical_and(data[:,0]==xu[ii], data[:,1]==yu[jj+1] ),2])
              #qy = - ((Tyn - Typ)/(ysize[jj-1]+ysize[jj-2])) * Kth
              qy = -((Ti - Typ)/ysize[jj-1]) * Kth
                               
          xasc.append(xu[ii])  
          yasc.append(yu[jj])
          q  = np.sqrt(qx**2+qy**2)
          xflux.append(qx)
          yflux.append(qy)
          Q.append(q)    
# save results in text file
tab = np.vstack((xasc, yasc, Tasc, xflux, yflux, Q)).T
np.savetxt('Flux_Results_t' + str(time) +'_v2.txt', tab, fmt='%f')

# plot results
a=list(np.around(np.array(np.linspace(0,15,16)),1))
b=list(np.around(np.array(np.linspace(-5.6,0.8,10)),1))
c=list(np.around(np.array(np.linspace(-4,4,9)),1))

xu = np.sort(np.unique(xasc))
yu = -np.sort(-np.unique(yasc))


T2D = np.reshape(Tasc,(len(yu),len(xu)), order = 'F')        
xflux2D = np.reshape(xflux,(len(yu),len(xu)), order = 'F')
yflux2D = np.reshape(yflux,(len(yu),len(xu)), order = 'F')

plt.figure(figsize=(15,4))
#Temperature
plt.subplot(1,3,1)
z1 = plt.contourf(xu[0:20],yu[::],T2D[:,0:20], cmap='coolwarm', levels=a)
plt.colorbar(z1, shrink=0.9)
plt.xlabel('Distance X')
plt.ylabel('Depth')
plt.title('Temperature' )

#Horizontal flux
plt.subplot(1,3,2)
z2 = plt.contourf(xu[0:20],yu[::],xflux2D[:,0:20],cmap='Spectral_r', levels=b)
plt.colorbar(z2, shrink=0.9)
#plt.clim(-1000, 1000)
plt.xlabel('Distance X')
plt.title('Horizontal flux' )

#vertical flux
plt.subplot(1,3,3)
z3 = plt.contourf(xu[0:20],yu[::],yflux2D[:,0:20],cmap='Spectral_r', levels=c)
plt.colorbar(z3, shrink=0.9)
plt.xlabel('Distance X')
plt.title('Vertical flux' )
plt.tight_layout()

plt.savefig('Flux' + str(t) + '_v2.png')  
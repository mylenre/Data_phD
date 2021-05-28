# -*- coding: utf-8 -*-
"""
Created on Sun May  3 00:41:21 2020

@author: s1995204
"""
import matplotlib.pyplot as plt
import os
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\Heat_extraction_model_water\2_1Y\2_3D-SI_VO\366day')
Kth=2.2
              
# extract values for time step t  
print("Available time steps: %s", node.keys())          
t = input("Enter time step (sec) : ")
t=eval(t)
val = node[t]

#extract values from a specific slice
print("x = val[0], y = val[1], z = val[2]")   
hslice = eval(input("Slice: "))  # the coordinate along which is drawn the profile
s0 = [i for i,x in enumerate(hslice) if x == 0]
x = np.array(eval(input("Horizontal direction: "))).transpose()
y = np.array(eval(input("Vertical direction: "))).transpose()
Tval=np.array(val[3]).T
data = np.array([x,y, Tval]).T

# find unique values of x and y
xu = np.unique(x)
yu = np.unique(y)

#define size of each element
xsize = [0]
ysize = [0]

for i in range(np.size(xu)):
     if i == 0:
         continue
     else:
         sx = xu[i] - xu[i-1] 
         xsize.append(sx)
for i in range(np.size(yu)):
     if i == 0:
         continue
     else:
         sy = yu[i] - yu[i-1] 
         ysize.append(sy)
xsize[0] = xsize[1]
ysize[0] = ysize[1] 

# %% calculate flux
xasc=[]
yasc=[]
Tasc=[]
xflux = []
yflux = []
Q = []

for ii in range(len(xu)):
    print('node x n°' + str(ii))
    for jj in range(len(yu)):
          print('node y n°' + str(jj))
          Ti = float(data[np.logical_and(data[:,0]==xu[ii], data[:,1]==yu[jj] ),2])
          if ii != 0:            
              Txp = float(data[np.logical_and(data[:,0]==xu[ii-1], data[:,1]==yu[jj] ),2])
          if ii != len(xu)-1:
              Txn = float(data[np.logical_and(data[:,0]==xu[ii+1], data[:,1]==yu[jj] ),2])
          if ii == len(xu)-1:
              Txn = Ti
          if ii == ii==0:
              Txp = Ti
              
          if jj != 0:            
              Typ = float(data[np.logical_and(data[:,0]==xu[ii], data[:,1]==yu[jj-1] ),2])
          if jj != len(yu)-1:
              Tyn = float(data[np.logical_and(data[:,0]==xu[ii], data[:,1]==yu[jj+1] ),2])
          if jj == len(yu)-1:
              Tyn = Ti
          if jj == jj==0:
              Typ = Ti              
          xasc.append(xu[ii])  
          yasc.append(yu[jj])
          Tasc.append(Ti)                       
          qx = ((Txn - Txp)/(2 * xsize[ii])) * Kth
          qy = ((Tyn - Typ)/(2 * ysize[jj])) * Kth
          q  = np.sqrt(qx**2+qy**2)
          xflux.append(qx)
          yflux.append(qy)
          Q.append(q)    
        
# save results in text file
tab = np.vstack((xasc, yasc, Tasc, xflux, yflux, Q)).T
np.savetxt('Flux_Results_t' + str(time) +'_v1.txt', tab, fmt='%f')

#%% plot results 
T2D = np.reshape(Tasc,(len(yu),len(xu)), order = 'F')        
xflux2D = np.reshape(xflux,(len(yu),len(xu)), order = 'F')
yflux2D = np.reshape(yflux,(len(yu),len(xu)), order = 'F')

plt.figure(figsize=(20,4))
x = xu
y = yu
xx, yy = np.meshgrid(x, y, sparse=True)

#Temperature
plt.subplot(1,3,1)
z1 = plt.contourf(x,y,T2D, cmap='coolwarm', levels=[3,4,5,6,7,8,9,10,11,12,13,14,15])
plt.colorbar(z1, shrink=0.9)
plt.xlabel('Distance X')
plt.ylabel('Depth')
plt.title('Temperature' )

#Horizontal flux
plt.subplot(1,3,2)
z2 = plt.contourf(x[1:18],y[1:-2],xflux2D[1:-2,1:18],cmap='Spectral')
plt.colorbar(z2, shrink=0.9)
#plt.clim(-1000, 1000)
plt.xlabel('Distance X')
plt.title('Horizontal flux' )

#vertical flux
plt.subplot(1,3,3)
z3 = plt.contourf(x[1:18],y[1:-2],yflux2D[1:-2,1:18],cmap='Spectral')
plt.colorbar(z3, shrink=0.9)
plt.xlabel('Distance X')
plt.title('Vertical flux' )
plt.tight_layout()

plt.savefig('Flux_2D_t' + str(t) + '_v1.png')  

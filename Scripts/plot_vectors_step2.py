# -*- coding: utf-8 -*-
"""
Created on Sun May  3 00:41:21 2020

@author: s1995204
"""
import matplotlib.pyplot as plt
import os
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\Heat_Models\3D_2_structures')

#define rock properties
kth = 2.0
poro = 0.1
K = (kth* poro)+(1-poro)*0.63 #Need to create a list of kth & porosity 
                           #for each cell in put in loop                           
# extract values for time step t  
print("Available time steps: %s", node.keys())          
t = eval(input("Enter time step (sec) : ")) #1000
val = node[t]
xval= val[0]
yval=val[1]
Tval=val[3]

uxval= set()
uyval= set()
for x in xval:
    x=round(x,0)
    uxval.add(x)
for y in yval:
    y=round(y,0)
    uyval.add(y)
uxval = sorted(list(uxval))
uyval = sorted(list(uyval))

#define size of each element
xsize = [0]
ysize = [0]

for i in range(np.size(uxval)):
     if i == 0:
         continue
     else:
         sx = uxval[i] - uxval[i-1] 
         xsize.append(sx)
for i in range(np.size(uyval)):
     if i == 0:
         continue
     else:
         sy = uyval[i] - uyval[i-1] 
         ysize.append(sy)
xsize[0] = xsize[1]
ysize[0] = ysize[1]  

#calculate flux
xflux = []
yflux = []
xasc = []
yasc = []
Tasc = []
Q = []
          
for ii in range(len(uxval)):
    print("look at val node ii " + str(ii))
    for jj in range(len(uyval)):
        print("look at val node jj " + str(jj))
        for k in range(len(xval)):
            if uxval[ii] == round(xval[k],0) and uyval[jj] == round(yval[k],0) :
                Tx = Tval[k]
                print("Selected node: n " + str(k))
            if ii!=0 :
                if uxval[ii-1] == round(xval[k],0) and uyval[jj] == round(yval[k],0)  :
                    Txp = Tval[k]
                    print("Previous node in x direction: " + str(k))
                if ii!=(len(uxval)-1) and uxval[ii+1] == round(xval[k],0) and uyval[jj] == round(yval[k],0)  :
                    Txn = Tval[k]
                    print("Next node in x direction: " + str(k))
                if ii==(len(uxval)-1) :
                    Txn = 10.86
                    print("Node at x_right boundary, Tn = 10.86 ")
            if ii==0 :
                Txp = 10.86
                print("Node at x_left boundary, Tp = 10.86")
                if uxval[ii+1] == round(xval[k],0) and uyval[jj] == round(yval[k],0)  :
                    Txn = Tval[k]
                    print("Next node in x direction: " + str(k))
            if jj!=0 :
                if uxval[ii] == round(xval[k],0) and uyval[jj-1] == round(yval[k],0)  :
                    Typ = Tval[k]
                    print("Previous node in y direction: " + str(k))
                if jj!=(len(uyval)-1) and uxval[ii] == round(xval[k],0) and uyval[jj+1] == round(yval[k],0)  :
                    Tyn = Tval[k]
                    print("Next node in y direction: " + str(k))
                if jj==(len(uyval)-1) :
                    Tyn = 10.86
                    print("Node at y_top boundary, Tn = 10.86 ")
            if jj==0 :
                Typ = 10.86
                print("Node at y_bottom boundary, Tp = 10.86")
                if uxval[ii] == round(xval[k],0) and uyval[jj+1] == round(yval[k],0)  :
                    Tyn = Tval[k]
                    print("Next node in y direction: " + str(k))               
            else:
                print("nope")
        xasc.append(uxval[ii])
        yasc.append(uyval[jj])
        Tasc.append(Tx)
        qx = ((Txn - Txp)/(2 * xsize[ii])) * K
        qy = ((Tyn - Typ)/(2 * ysize[jj])) * K
        q  = np.sqrt(qx**2+qy**2)
        xflux.append(qx)
        yflux.append(qy)
        Q.append(q)

#save results in text file
tab = np.vstack((xasc, yasc, Tasc, xflux, yflux, Q)).T
np.savetxt('Flux_Results_t' + str(t) +'.txt', tab, fmt='%f')

# plot results 
T2D = np.reshape(Tasc,(len(uyval),len(uxval)), order = 'F')        
xflux2D = np.reshape(xflux,(len(uyval),len(uxval)), order = 'F')
yflux2D = np.reshape(yflux,(len(uyval),len(uxval)), order = 'F')

plt.figure(figsize=(20,4))
x = uxval
y = uyval
xx, yy = np.meshgrid(x, y, sparse=True)

#Temperature
plt.subplot(1,3,1)
z1 = plt.contourf(x,y,T2D, cmap='coolwarm')
plt.colorbar(z1, shrink=0.9)
plt.xlabel('Distance X')
plt.ylabel('Depth')
plt.title('Temperature' )

#Horizontal flux
plt.subplot(1,3,2)
z2 = plt.contourf(x,y,xflux2D,cmap='Spectral')
plt.colorbar(z2, shrink=0.9)
#plt.clim(-1000, 1000)
plt.xlabel('Distance X')
plt.title('Horizontal flux' )

#vertical flux
plt.subplot(1,3,3)
z3 = plt.contourf(x,y,yflux2D,cmap='Spectral')
plt.colorbar(z3, shrink=0.9)
plt.xlabel('Distance X')
plt.title('Vertical flux' )

plt.savefig('Flux_2D_t' + str(t) + '.png')  




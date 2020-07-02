# -*- coding: utf-8 -*-
"""
Created on Sun May  3 00:41:21 2020

@author: s1995204
"""
import matplotlib.pyplot as plt
import os
os.chdir(r'R:\Modeling\Heat_Extraction_Paper\Unsteady_State\Profile_3D_30yr_Unsteady\26.5m')

xval=[]
yval=[]
                        
# extract values for time step t  
print("Available time steps: %s", node.keys())          
t = input("Enter time step (sec) : ") #1000
t=eval(t)
val = node[t]

#extract values from a specific slice
print("x = val[0], y = val[1], z = val[2]")   
hslice = eval(input("Slice: ")) #val[1]
s0 = [i for i,x in enumerate(hslice) if x == 0]
x = eval(input("Horizontal direction: ")) #val[0]
y = eval(input("Vertical direction: ")) #val[2]
Tval=val[3]

for i in s0:
    xval.append(x[i])
    yval.append(y[i])

uxval= set()
uyval= set()
for x in xval:
    uxval.add(x)
for y in yval:
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
            if uxval[ii] == xval[k] and uyval[jj] == yval[k] :
                Tx = Tval[k]
                print("Selected node: n " + str(k))
            if ii!=0 :
                if uxval[ii-1] == xval[k] and uyval[jj] == yval[k] :
                    Txp = Tval[k]
                    print("Previous node in x direction: " + str(k))
                if ii!=(len(uxval)-1) and uxval[ii+1] == xval[k] and uyval[jj] == yval[k] :
                    Txn = Tval[k]
                    print("Next node in x direction: " + str(k))
                if ii==(len(uxval)-1) :
                    Txn = 0
                    print("Node at x_right boundary, Tn = 0 ")
            if ii==0 :
                Txp = 100
                print("Node at x_left boundary, Tp = 100")
                if uxval[ii+1] == xval[k] and uyval[jj] == yval[k] :
                    Txn = Tval[k]
                    print("Next node in x direction: " + str(k))
            if jj!=0 :
                if uxval[ii] == xval[k] and uyval[jj-1] == yval[k] :
                    Typ = Tval[k]
                    print("Previous node in y direction: " + str(k))
                if jj!=(len(uyval)-1) and uxval[ii] == xval[k] and uyval[jj+1] == yval[k] :
                    Tyn = Tval[k]
                    print("Next node in y direction: " + str(k))
                if jj==(len(uyval)-1) :
                    Tyn = 0
                    print("Node at y_top boundary, Tn = 0 ")
            if jj==0 :
                Typ = 0
                print("Node at y_bottom boundary, Tp = 0")
                if uxval[ii] == xval[k] and uyval[jj+1] == yval[k] :
                    Tyn = Tval[k]
                    print("Next node in y direction: " + str(k))               
            else:
                print("nope")
        xasc.append(uxval[ii])
        yasc.append(uyval[jj])
        Tasc.append(Tx)
        
        #define rock properties
        if jj > 58:
            Kth = 1.2
        else:
            Kth = 1.8
        #poro = 0.1
        #K = (Kth* poro)+(1-poro)*0.63                            
        qx = ((Txn - Txp)/(2 * xsize[ii])) * Kth
        qy = ((Tyn - Typ)/(2 * ysize[jj])) * Kth
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

plt.savefig('Flux_2D_t' + str(t) + '.png')  




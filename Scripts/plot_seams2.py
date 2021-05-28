# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 09:52:55 2020

@author: s1995204
"""
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl  # noqa
from scipy import interpolate
from scipy.interpolate import griddata

mpl.style.use('seaborn')

os.chdir(r'R:\GitHub\Data_phD\GIS\Export')

filelist=glob.glob('*.csv')
l = np.size(filelist)

#fig, ax = plt.subplots(figsize=(8,5))
fig = plt.figure(figsize=(30,20))
#ax = plt.axes(projection="3d")
ax1 = fig.add_subplot(111,projection='3d')

for i in filelist:
    print(i)
    name= i.split('.')[0]
    id=filelist.index(i)
    data = pd.read_csv(i, delimiter=',', header=0) 
    #ax.scatter3D(data.X, data.Y, data.z, cmap="hsv");
    ax1.scatter(data.X, data.Y, data.z, marker='o', s=5, label = name)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_zticks([-400,-300,-200, -100,0, 100])
ax1.set_zlim3d(-400,0)
ax1.legend(loc='best')
plt.show()


 


fig = plt.figure(figsize=(30,20))
ax2 = fig.add_subplot(111,projection='3d')
#ax2 = fig.gca(projection='3d')

for i in filelist:
    print(i)
    name= i.split('.')[0]
    id=filelist.index(i)
    data = pd.read_csv(i, delimiter=',', header=0)    
    points = np.array([data.X, data.Y])
    points = points.T
    values = np.array(data.z)
    grid_x, grid_y = np.mgrid[429998:447500:100j, 534983:555023:100j]
    grid_z = griddata(points, values, (grid_x, grid_y), method='linear')
    ax2.plot_surface(grid_x, grid_y, grid_z)

    #grid_x1 = grid_x[:,0]
    #grid_y1 = grid_y[0,:]
    #ax1.contourf(grid_x1, grid_y1, grid_z,cmap='Spectral') 
    
#    grid_x1 = grid_x.reshape(1,np.size(grid_x))
#    grid_x1=grid_x1.T
#    grid_y1 = grid_y.reshape(1,np.size(grid_y)) 
#    grid_y1=grid_y1.T
#    grid_z1 = grid_z.reshape(1, np.size(grid_z))
#    grid_z1=grid_z1.T
#    idx=np.argwhere(~np.isnan(grid_z1))
#    x=grid_x1[idx[:,0]]
#    y=grid_y1[idx[:,0]]
#    z=grid_z1[idx[:,0]]
#    
#    ax2.plot_surface(x,y,z, cmap=plt.cm.viridis, linewidth=0.2)

ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_zticks([-400,-300,-200, -100,0, 100])
ax2.set_zlim3d(-400,0)
#ax2.view_init(30, 45)

#elev = -60
#azim = 30
#ax2.view_init(elev, azim)
plt.show()
#print('ax1.azim {}'.format(ax2.azim))
#print('ax2.elev {}'.format(ax2.elev))


#plt.subplot(122)
#plt.imshow(grid_z.T, extent=(429998.0, 447500.0, 534983.0, 555023.0), origin='lower')


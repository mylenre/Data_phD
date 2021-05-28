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
ax1 = fig.add_subplot(121,projection='3d')
ax2 = fig.add_subplot(122,projection='3d')

for i in filelist:
    print(i)
    name= i.split('.')[0]
    id=filelist.index(i)
    data = pd.read_csv(i, delimiter=',', header=0) 
    #ax.scatter3D(data.X, data.Y, data.z, cmap="hsv");
    ax1.scatter(data.X, data.Y, data.z, marker='o', s=5, label = name)
    
    points = np.array([data.X, data.Y])
    points = points.T
    values = np.array(data.z)
    grid_x, grid_y = np.mgrid[429998:447500:500j, 534983:555023:500j]
    grid_z = griddata(points, values, (grid_x, grid_y), method='linear')
    #grid_x1 = grid_x[:,0]
    #grid_y1 = grid_y[0,:]
    #ax1.contourf(grid_x1, grid_y1, grid_z,cmap='Spectral') 
    ax2.scatter(grid_x, grid_y, grid_z,cmap='Spectral')

ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_zticks([-400,-300,-200, -100,0, 100])
ax1.set_zlim3d(-400,0)
ax1.legend(loc='best')

ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_zticks([-400,-300,-200, -100,0, 100])
ax2.set_zlim3d(-400,0)

#elev = -60
#azim = 30
#ax2.view_init(elev, azim)
plt.show()
#print('ax1.azim {}'.format(ax2.azim))
#print('ax2.elev {}'.format(ax2.elev))


#plt.subplot(122)
#plt.imshow(grid_z.T, extent=(429998.0, 447500.0, 534983.0, 555023.0), origin='lower')


# -*- coding: utf-8 -*-
"""
Created on Tuesday 28 Jan 2019

@author: mylene
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.interpolate import interp1d # interpolation package
import statsmodels.api as sm
from scipy import stats
import itertools

os.chdir(r'R:\GitHub\Data_phD\Data')

data = pd.read_csv('T_Burley.csv', delimiter=',', header=0)
print(type(data))
BH= data['Borehole_name']
region=data['Region']
depth=-data['Depth']
temperature = data['Temp']
gradient=data['T_grad']
datatype=data['Type']
print(temperature)

df=pd.DataFrame(dict(depth=depth, t=temperature, label=datatype))
groups=df.groupby('label')


fig, axs = plt.subplots(1,2,figsize=(16,8), sharey=True)
#fig, axs = plt.subplots(1,5,figsize=(20,8), sharey=True)
fig.suptitle('Temperature profiles for different measurement types')
fig.subplots_adjust(wspace=0.15)

i=0
x0=0
y0= 0
for name, group in groups:
    if(group.iat[i,2]=='BHT') or (group.iat[i,2]=='MWT'):
        axs[i].plot(group.t, group.depth, marker='o', markersize='6', linestyle='', ms=12, label=name)
        axs[i].set_title(name)
            
        # correlation and rms error 
        m, c, r, p, se = stats.linregress(group.t, group.depth) # slope, intercept, correlation coefficient,p-value, sterror of estimate
        tfit = np.arange(max(group.t)+2)
        dfit = c + m*tfit
        axs[i].plot(tfit, dfit,color='black',linestyle='--')
        # label the line
        # eqn = 'T = ' + str(round(c,2)) + '+' + str(round(m,2)) + ' x' 
        # axs[i].text(x0,y0,eqn,rotation=0)
        i +=1
        
fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom =False, left=False, right=False)
plt.xlabel('Temperature (°C) ')
plt.ylabel('Depth (m)')

plt.savefig('T_Burley_1984_v2.png', dpi=400)


#x0=400
#y0= 60
#for name, group in groups:
#    axs[i].plot(group.depth, group.t, marker='o', markersize='6', linestyle='', ms=12, label=name)
#    axs[i].set_title(name)
#        
#    # correlation and rms error 
#    m, c, r, p, se = stats.linregress(group.depth, group.t) # slope, intercept, correlation coefficient,p-value, sterror of estimate
#    dfit = np.arange(max(group.depth)+2)
#    tfit = c + m*dfit
#    axs[i].plot(dfit, tfit,color='black',linestyle='--')
#    # label the line
#    eqn = 'T = ' + str(round(c,2)) + '+' + str(round(m,2)) + ' x' 
#    axs[i].text(x0,y0,eqn,rotation=0)
#    i +=1
#    
#fig.add_subplot(111, frameon=False)
#plt.tick_params(labelcolor='none', top=False, bottom =False, left=False, right=False)
#plt.xlabel('Depth (m)')
#plt.ylabel('Temperature (°C)')

#plt.savefig('T_Burley_1984.png', dpi=400)


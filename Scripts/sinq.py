# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 01:12:49 2019

@author: mylen
"""

import os
import numpy as np
import matplotlib.pyplot as plt
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\30_years\7.3_SOLAR_NO_PROD0')
#qmax=input("Enter qmax : ")
#qmin=input("Enter qmin : ")
#amp=(abs(eval(qmax))+abs(eval(qmin)))/2

qmax=8.4
qmin=-qmax
amp=abs(qmax-qmin)/2

dt_t=1
dt_s=dt_t*3600*24

#t_y=input("Enter nb year : ")
#t_y=eval(t_y)
t_y=30 # define in accordance to time scale
t_d=dt_d*366*t_y
t_s=dt_s*366*t_y
p=366
time = np.arange(0, t_d, dt_d)
time_s= np.arange(0, t_s, dt_s)
time_yr = time/p

plt.figure(figsize=(14,6))

##surface flux
plt.subplot(1,2,1)
amplitude = amp*np.sin(2*np.pi*(time/p)) #-0.0682  #0.0372 #0.01207 
data=np.stack((time_s, amplitude), axis=-1)
np.savetxt('surface_flux.txt', data)
plt.plot(time_yr, amplitude, "k-", label="Surface flux", linewidth=2)
plt.title('Surface flux and temperature')
plt.xlabel('Time (years)')
plt.ylabel('Amplitude surface flux (W/m²) ')
plt.ylim(-10,10)
plt.grid(True, which='both')
plt.axhline(y=0, color='k')

##temperature y=0 --> scale to appropriate time length
plt.twinx()
t = np.loadtxt('POINT0.txt', skiprows=0, usecols=0)  # first column 
tyr= t/(3600*24*366)
T = np.loadtxt('POINT0.txt', skiprows=0, usecols=1)  # 2nd column 
plt.plot(tyr[0:730], T[0:730], "r-.", label="Temperature", linewidth=1)
plt.ylim(-2,20)
plt.ylabel('Temperature (degC)',color='r')
plt.savefig('surface_flux_zoom.png') 


##extraction
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\30_years\8_PROD_3D_Cyclical_v3')
dt_s=2635200
t_s=948672000+dt_s
p=12
time_s= np.arange(0, t_s, dt_s)
time = np.arange(0, 361, 1)
time_yr = time/p
plt.figure(figsize=(14,6))
#plt.figure(figsize=(14,6))
plt.subplot(1,2,2)
amplitude = -294*np.sin(2*np.pi*(time/p))-1000
data=np.stack((time_s, amplitude), axis=-1)
np.savetxt('extraction_rate.txt', data)
plt.plot(time_yr, amplitude, "k-", label="Extraction rate", linewidth=2)
plt.title('Extraction rate along borehole')
plt.xlabel('Time (years)')
plt.ylabel('Extraction rate (W)')
plt.ylim(-1500,-600)
plt.grid(True, which='both')
plt.tight_layout()
plt.savefig('extraction.png') 

#plt.savefig('q_input_'+ qmin +'_'+qmax+'.png')
#plt.savefig('surface_flux_extraction.png') 

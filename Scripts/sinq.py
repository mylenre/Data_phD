# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 01:12:49 2019

@author: mylen
"""

import os
import numpy as np
import matplotlib.pyplot as plt
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\Heat_Models\RHP\Ref\Step_2_Flux_unsteady_state\Flux_solar_prod')

#qmax=input("Enter qmax : ")
#qmin=input("Enter qmin : ")
#amp=(abs(eval(qmax))+abs(eval(qmin)))/2

qmax=6
qmin=-qmax
amp=abs(qmax-qmin)/2

dt_d=1
dt_s=3600*24

#t_y=input("Enter nb year : ")
#t_y=eval(t_y)
t_y=50
t_d=dt_d*366*t_y
t_s=dt_s*366*t_y
time = np.arange(0, t_d, dt_d)
time_s= np.arange(0, t_s, dt_s)
time_yr = time/366

plt.figure(figsize=(14,6))

##surface flux
plt.subplot(1,2,1)
amplitude = amp*np.sin(2*np.pi*(time/t_d*t_y))+0.01207 #-0.066495 #0.06
data=np.stack((time_s, amplitude), axis=-1)
np.savetxt('surface_flux.txt', data)
plt.plot(time_yr, amplitude, "k-", label="Surface flux", linewidth=2)
plt.title('Surface flux and temperature')
plt.xlabel('Time (years)')
plt.ylabel('Amplitude surface flux (W/m²) ')
plt.ylim(-10,10)
plt.grid(True, which='both')
plt.axhline(y=0, color='k')

##temperature y=0
plt.twinx()
t = np.loadtxt('POINT0.txt', skiprows=0, usecols=0)  # first column 
tyr= t/(3600*24*366)
T = np.loadtxt('POINT0.txt', skiprows=0, usecols=1)  # 2nd column 
plt.plot(tyr[:], T[:], "r-.", label="Temperature", linewidth=1)
plt.ylim(-2,20)
plt.ylabel('Temperature (degC)',color='r')


##extraction
plt.subplot(1,2,2)
amplitude = -294*np.sin(2*np.pi*(time/t_d*t_y))-1000
data=np.stack((time_s, amplitude), axis=-1)
np.savetxt('extraction_rate.txt', data)
plt.plot(time_yr, amplitude, "k-", label="Extraction rate", linewidth=2)
plt.title('Extraction rate along borehole')
plt.xlabel('Time (years)')
plt.ylabel('Extraction rate (W)')
plt.ylim(-1500,-600)
plt.grid(True, which='both')
plt.tight_layout()

#plt.savefig('q_input_'+ qmin +'_'+qmax+'.png') 
plt.savefig('surface_flux_extraction_rate.png') 

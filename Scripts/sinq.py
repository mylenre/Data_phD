# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 01:12:49 2019

@author: mylen
"""

import os
import numpy as np
import matplotlib.pyplot as plt
#os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\30_years\7_SOLAR\Amplitude_8\ISOTHERMAL')
os.chdir(r'C:\Workspace\recover\Users\s1995204\Documents_LOCAL\Modeling\6_BACK_COND_AMP\0_EI')
#qmax=input("Enter qmax : ")
#qmin=input("Enter qmin : ")
#amp=(abs(eval(qmax))+abs(eval(qmin)))/2

qmax=7 # 8.4
qmin=-qmax
amp=abs(qmax-qmin)/2

dt_t=1
dt_s=dt_t*3600*24

#t_y=input("Enter nb year : ")
#t_y=eval(t_y)
t_y=101 # define in accordance to time scale
t_d=dt_t*366*t_y
t_s=dt_s*366*t_y
p=366
time = np.arange(0, t_d, dt_t)
time_s= np.arange(0, t_s, dt_s)
time_yr = time/p

plt.figure(figsize=(14,6))

##surface flux
plt.subplot(1,2,1)
amplitude = amp*np.sin(2*np.pi*(time/p))-0.0457728 # -0.06324 #-0.0682  #0.0372 #0.01207 
data=np.stack((time_s, amplitude), axis=-1)
np.savetxt('surface_flux.txt', data)

plt.plot(time_yr, amplitude, "k-", label="Surface flux", linewidth=2)
plt.title('Surface flux and temperature')
plt.xlabel('Time (years)')
plt.ylabel('Amplitude surface flux (W/m²) ')
plt.ylim(-10,10)
plt.grid(True, which='both')
plt.axhline(y=0, color='k')

#%%
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\7_SOLAR\2_NO_PROD')
qmax=6
qmin=-qmax
amp=abs(qmax-qmin)/2

yr =10
dt_s = 2635200 # =30.5 days = 1 month
t_s= yr * 31622400 + dt_s
p = 12 # months
tt = yr * p + 1
time_s= np.arange(0, t_s, dt_s)
time = np.arange(0, tt, 1)
time_yr = time/p

amplitude = -amp*np.sin(2*np.pi*(time/p))-0.056832
data=np.stack((time_s, amplitude), axis=-1)
np.savetxt('surface_flux.txt', data)

plt.figure(figsize=(14,6))
plt.subplot(1,2,1)
plt.plot(time_yr, amplitude, "k-", label="Surface flux", linewidth=2)
plt.title('Surface flux and temperature')
plt.xlabel('Time (years)')
plt.ylabel('Amplitude surface flux (W/m²) ')
plt.ylim(-10,10)
plt.grid(True, which='both')
plt.axhline(y=0, color='k')
plt.tight_layout()

# %% temperature y=0 --> scale to appropriate time length
plt.twinx()
t = np.loadtxt('POINT0.txt', skiprows=0, usecols=0)  # first column 
tyr= t/(3600*24*366)
T = np.loadtxt('POINT0.txt', skiprows=0, usecols=1)  # 2nd column 
plt.plot(tyr[0:730], T[0:730], "r-.", label="Temperature", linewidth=1)
plt.ylim(-2,20)
plt.ylabel('Temperature (degC)',color='r')

# %% save fgure
plt.savefig('surface_flux.png') 

#%%
os.chdir(r'C:\Workspace\recover\Users\s1995204\Documents_LOCAL\Modeling\Solar\v3')
qmax=16
qmin=2
amp=abs(qmax-qmin)/2

dt_t=1
dt_s=dt_t*3600*24

t_y=31 # define in accordance to time scale
t_d=dt_t*366*t_y
t_s=dt_s*366*t_y
p=366
time = np.arange(0, t_d, dt_t)
time_s= np.arange(0, t_s, dt_s)
time_yr = time/p

plt.figure(figsize=(14,6))

##surface flux
plt.subplot(1,2,1)
amplitude = -amp*np.sin(2*np.pi*(time/p))+9 
data=np.stack((time_s, amplitude), axis=-1)
np.savetxt('surface_T.txt', data)

plt.plot(time_yr, amplitude, "k-", label="Surface flux", linewidth=2)
plt.title('Surface flux and temperature')
plt.xlabel('Time (years)')
plt.ylabel('Amplitude surface flux (W/m²) ')
plt.ylim(2,16)
plt.grid(True, which='both')
plt.axhline(y=0, color='k')

# %% extraction
os.chdir(r'C:\Workspace\recover\Users\s1995204\Documents_LOCAL\Modeling\Geobattery\Cyclical')
yr = 20
dt_s = 2635200 # =30.5 days = 1 month
t_s= yr * 31622400 + dt_s
p = 12 # months
tt = yr * p + 1
time_s= np.arange(0, t_s, dt_s)
time = np.arange(0, tt, 1)
time_yr = time/p

amplitude = -500*np.sin(2*np.pi*(time/p))-1500
data=np.stack((time_s, amplitude), axis=-1)
np.savetxt('extraction_rate.txt', data)

plt.figure(figsize=(14,6))
plt.subplot(1,2,2)
plt.plot(time_yr, amplitude, "k-", label="Extraction rate", linewidth=2)
plt.title('Extraction rate along borehole')
plt.xlabel('Time (years)')
plt.ylabel('Extraction rate (W)')
plt.ylim(-2100,-900)
plt.grid(True, which='both')
plt.tight_layout()
plt.savefig('extraction.png') 

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 13:26:30 2020

@author: mylen
"""

import math
import numpy as np
from scipy import special
import matplotlib.pyplot as plt
import pandas as pd

lambda_r = 2.78
lambda_w = 0.63
c_r = 1280
c_w = 4068
d_r = 2500
d_w = 1000
phi = 0.1

lambda_m = (lambda_r *(1-phi)) + (lambda_w * phi)
d_m = (d_r *(1-phi)) + (d_w * phi)
c_m = (c_r *(1-phi)) + (c_w * phi)
rho_c = d_m* c_m
D = lambda_m / rho_c # Thermal diffusion coefficient

x=0.96
DP=2e4
DP_DL=DP/x
k=2.184e-13
u= 1.8e-5

ux= (DP_DL * k) / u # Darcy velocity
vx = ux / phi # advective velocity
vT= ux *((d_w*c_w)/(d_m*c_m))

dispersivity = 0
DD = D + ux * dispersivity

t_tot = 1000
dt=1
Ti = 0
T0= 100
Q = T0 * rho_c

# Continuous / moving infinite point source (1D)

#solution time
n=1
st=[]
for t in range(10000):
    t1 = Q /(rho_c * (4*np.pi * DD)**((1+n)/2)) #○ if n=1, rho_c * DD = lambda --> q/(4*pi*lamda)
    t2 = - (x-vT*(t+dt))/np.sqrt(4*DD*(t+dt))
    T = t1*math.exp(t2)
    st.append(T) 
plt.figure(figsize=(16,5))    
plt.plot(range(10000),st,color='black')
plt.xlabel('time')
plt.ylabel('temperature')

#solution distance: continuous
sd=[]
list = np.arange(0.0001,1,0.0001)
for x in list:
    t1 = (x-ux*t_tot)/np.sqrt(4*DD*t_tot)
    t2 = math.exp((x*ux)/(DD))
    t3 = (x+ux*t_tot)/np.sqrt(4*DD*t_tot)
    T = (special.erfc(t1)+t2*special.erfc(t3))*T0/2
    sd.append(T) 
    
plt.figure(figsize=(16,5))    
plt.plot(list,sd,color='black')

#import data
data = pd.read_csv('1D_Cont.csv', delimiter=',', header=0)
xp = data['xp']
Tp = data['Tp']
plt.plot(xp,Tp, color='blue')
plt.xlabel('distance')
plt.ylabel('temperature')



#solution distance: pulse
sd=[]
n=1
list = np.arange(0.0001,1,0.0001)
for x in list:
    t1 = (x-vT*t_tot)/np.sqrt(4*DD*t_tot)
    #t2 = (x*vT)/(DD)
    t3 = (x+vT*t_tot)/np.sqrt(4*DD*t_tot)
    #T = (T0/(rho_c*(4*np.pi*DD)**((1+n)/2)))*(math.exp(-t2)*special.erfc(-t1)+math.exp(t2)*special.erfc(t3))
    t2 = (x*vT)/(2*DD)
    #T = (T0/(rho_c*(4*np.pi*DD)**((1+n)/2)))*(math.exp(t2))*((1/(4*x))*(math.exp(-t2)*special.erfc(-t1)+math.exp(t2)*special.erfc(t3)))
    T = (100/(rho_c*(8*np.pi*DD)**((1+n)/2)))*(math.exp(-t1))*(special.erfc(-t1)-special.erfc(t3))
    sd.append(T) 
plt.figure(figsize=(16,5))    
plt.plot(list,sd,color='black')

#import data
data = pd.read_csv('1D_Pulse.csv', delimiter=',', header=0)
xc = data['xc']
Tc = data['Tc']
plt.plot(xc,Tc, color='blue')
plt.xlabel('distance')
plt.ylabel('temperature')


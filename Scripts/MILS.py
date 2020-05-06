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
phi = 0.5

lambda_m = (lambda_r *(1-phi)) + (lambda_w * phi)
d_m = (d_r *(1-phi)) + (d_w * phi)
c_m = (c_r *(1-phi)) + (c_w * phi)
rho_c = (d_r*c_r)*(1-phi)+(d_w*c_w)*phi

D = lambda_m / rho_c # Thermal diffusion coefficient

x=0.96
DP=2e4
DP_DL=DP/x
k=2.184e-13
u= 1.8e-5

ux= (DP_DL * k) / u # Darcy velocity
vx = ux / phi # advective velocity
vT=(ux*d_w*c_w)/(rho_c) #effective thermal velocity of convective heat transport (Molina-Giraldo, 2011)

dispersivity = 0
DD = D + ux * dispersivity #longitudinal diffusion-dispersion coefficient

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
plt.subplot(1,3,1)    
plt.plot(range(10000),st,color='black', lw=2,label="analytical")
plt.xlabel('time')
plt.ylabel('temperature')
plt.legend(loc='best')

#solution distance: continuous
sd=[]
list = np.arange(0.0001,1,0.0001)
for x in list:
    t1 = (x-vT*t_tot)/np.sqrt(4*DD*t_tot)
    t2 = math.exp((x*vT)/(DD))
    t3 = (x+vT*t_tot)/np.sqrt(4*DD*t_tot)
    T = (special.erfc(t1)+t2*special.erfc(t3))*T0/2
    sd.append(T) 
    
plt.subplot(1,3,2)   
plt.plot(list,sd,color='black',lw=2,label="analytical")

#import data
data = pd.read_csv('1D_Cont.csv', delimiter=',', header=0) #mesh = 1 mm poro=0.5
xp = data['xp']
Tp = data['Tp']
plt.plot(xp,Tp,'--', color='red',label="numerical")
plt.xlabel('distance')
plt.ylabel('temperature')
plt.legend(loc='best')



#solution distance: pulse
sd=[]
n=1
list = np.arange(0.0001,1,0.0001)
for x in list:
    t1 = -(x-vT*t_tot)/np.sqrt(4*DD*t_tot)
    t2 = math.exp((x*vT)/(2*DD))  
    t3 = (x+vT*t_tot)/np.sqrt(4*DD*t_tot)
    T = (1/(rho_c*(16*np.pi*DD)**((1+n)/2)))*(math.exp(t1))*(special.erfc(t1)+t2*special.erfc(t3))*T0/2 #(1/(rho_c*(4*np.pi*DD)**((1+n)/2)))
      
    #t4 = math.exp(-(x*vT)/(2*DD))
    #t5 = math.exp((x*vT)/(2*DD)) 
    #t6 = (x-vT*t_tot)/np.sqrt(4*DD*t_tot)
    #t7 = (x+vT*t_tot)/np.sqrt(4*DD*t_tot)
    #f=1/(4*x)*(t4*special.erfc(t6)+t5*special.erfc(t7))
    #T = (1/(2*lambda_m*np.pi))*t5*f*T0/2 #(1/(rho_c*(4*np.pi*DD)**((1+n)/2)))
   
    sd.append(T) 
plt.subplot(1,3,3)   
plt.plot(list,sd,color='black',label="analytical")


#import data
data = pd.read_csv('1D_Pulse.csv', delimiter=',', header=0) #poro = 0.5, mesh=1 mm
xc = data['xc']
Tc = data['Tc']
plt.plot(xc,Tc, color='blue',label="numerical")
plt.xlabel('distance')
plt.ylabel('temperature')
plt.legend(loc='best')
plt.savefig("analytical_vs_numerical_1D.png")  

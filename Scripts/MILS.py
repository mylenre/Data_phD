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
Dr= lambda_r/(d_r * c_r)

phi = 0.5
lambda_m = (lambda_r *(1-phi)) + (lambda_w * phi)
d_m = (d_r *(1-phi)) + (d_w * phi)
c_m = (c_r *(1-phi)) + (c_w * phi)
rho_c = (d_r*c_r)*(1-phi)+(d_w*c_w)*phi #volumetric heat capacity of the medium
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
lambda_x = lambda_m + dispersivity * d_w * c_w * ux #effective longitudinale thermal conductivity
DD = D + ux * dispersivity #longitudinal diffusion-dispersion coefficient

t_tot = 1000
dt=1
Ti = 0
T0= 100
Q = T0 * rho_c

n=1
###################Advection + Diffusion##################"
##### solution time continuous 
x=0.1 #MIDDLE point
st=[]
for t in range(1, 1001, 1):
    
    t1 = (x-vT*t)/np.sqrt(4*DD*t)
    t2 = math.exp((x*vT)/(DD))
    t3 = (x+vT*t)/np.sqrt(4*DD*t)
    T = (special.erfc(t1)+t2*special.erfc(t3))*T0/2
    st.append(T) 
plt.figure(figsize=(8,8))   
plt.subplot(2,2,1)    
plt.plot(range(1000),st,color='black', lw=2,label="analytical HT")
    
#import data 
data = pd.read_csv('1D_Cont_time.csv', delimiter=',', header=0) #mesh = 1 mm poro=0.5
T = data['T']
t = data['t']
plt.plot(t,T,'--', color='red',label="numerical HT")
plt.xlabel('time')
plt.ylabel('temperature')
plt.legend(loc='best')

###### solution distance: continuous
sd=[]
list = np.arange(0.0001,1,0.0001)
for x in list:
    t1 = (x-vT*t_tot)/np.sqrt(4*DD*t_tot)
    t2 = math.exp((x*vT)/(DD))
    t3 = (x+vT*t_tot)/np.sqrt(4*DD*t_tot)
    T = (special.erfc(t1)+t2*special.erfc(t3))*T0/2
    sd.append(T) 
    
plt.subplot(2,2,2) 
plt.plot(list,sd,color='black',lw=2,label="analytical HT")

#import data
data = pd.read_csv('1D_Cont.csv', delimiter=',', header=0) #mesh = 1 mm poro=0.5
xp = data['xp']
Tp = data['Tp']
plt.plot(xp,Tp,'--', color='red',label="numerical HT")
plt.xlabel('distance')
plt.ylabel('temperature')
plt.legend(loc='best')


###### #solution time pulse --> why does it work for lambda rock but not lamba wet matrix ??
x=0.1 #MIDDLE point
st=[]
for t in range(1,1001,1):
    t1 = (x-vT*t)**2/(4*DD*t)
    t2 = math.exp((x*vT)/(2*DD))  
    t3 = (x+vT*t)/np.sqrt(4*DD*t)
    #T = (1/(rho_c*(16*np.pi*DD)**((1+n)/2)))*(math.exp(t1))*(special.erfc(t1)+t2*special.erfc(t3))*T0/2 --> if n=1, rho_c*DD = lambda
    #T = (1/(16*lambda_x*np.pi))*(math.exp(-t1))*T0/2 #*(special.erfc(t1)+t2*special.erfc(t3))
    #T = (1/(16*lambda_x*np.pi))*(math.exp(-t1)-t2*special.erfc(t3))*T0/2
    T = (T0/np.sqrt(8*lambda_r*np.pi*t))*math.exp(-t1)-(T0**2/(2*8*lambda_r))*t2*special.erfc(t3)
    st.append(T) 
plt.subplot(2,2,3)   
plt.plot(range(1000),st,color='blue', lw=2,label="analytical HT")
plt.xlabel('time')
plt.ylabel('temperature')
plt.legend(loc='best')

#import data 
data = pd.read_csv('1D_Pulse_time.csv', delimiter=',', header=0) #mesh = 1 mm poro=0.5
T = data['T']
t = data['t']
plt.plot(t,T,'--', color='red',label="numerical HT")
plt.xlabel('time')
plt.ylabel('temperature')
plt.legend(loc='best')


###### #solution distance: pulse
sd=[]
list = np.arange(0.0001,1,0.0001)
for x in list:
    t1 = (x-vT*t_tot)**2/(4*DD*t_tot)
    t2 = math.exp((x*vT)/(2*DD))  
    t3 = (x+vT*t_tot)**2/(4*DD*t_tot)
    #T = (1/(rho_c*(16*np.pi*DD)**((1+n)/2)))*(math.exp(t1))*(special.erfc(t1)+t2*special.erfc(t3))*T0/2
    #T = (1/(16*lambda_r*np.pi))*(math.exp(-t1))*T0/2#*(special.erfc(t1)+t2*special.erfc(t3))  
    T = (T0/(np.sqrt(8*lambda_r*np.pi*t_tot)))*(math.exp(-t1))-(T0**2/(2*8*lambda_r))*t2*special.erfc(t3)
    sd.append(T) 
plt.subplot(2,2,4)   
plt.plot(list,sd,color='blue',label="analytical HT")


#import data
data = pd.read_csv('1D_Pulse.csv', delimiter=',', header=0) #poro = 0.5, mesh=1 mm
xc = data['xc']
Tc = data['Tc']
plt.plot(xc,Tc, '--', color='red',label="numerical HT")
plt.xlabel('distance')
plt.ylabel('temperature')
plt.legend(loc='best')
#plt.savefig("analytical_vs_numerical_1D.png")  


###########################Diffusion only#############################
tau = 1
dx = 1e-3
#Q = T0 * rho_c * dx / tau  (W)
Q = T0 * lambda_r # (W/m)

##### solution time continuous 
plt.figure(figsize=(8,8))   
plt.subplot(2,2,1)   
x=0.1 #MIDDLE point
st=[]
for t in range(1, 10001, 1):
    t1 = x/np.sqrt(4*Dr*t)
    T = T0*special.erfc(t1)
    st.append(T)  
plt.plot(range(10000),st,color='black', lw=2,label="analytical T")
    

#import data 
data = pd.read_csv('1D_Cont_time_Diff.csv', delimiter=',', header=0) #mesh = 1 mm poro=0.5
T = data['T']
t = data['t']
plt.plot(t,T,'--', color='red',label="numerical T")
plt.xlabel('time')
plt.ylabel('temperature')
plt.legend(loc='best')


###### solution distance: continuous
plt.subplot(2,2,2) 
sd=[]
n=2
list = np.arange(0.0001,1,0.0001)
for x in list:
    t0 = 1/(4*np.pi*Dr*t_tot)**((n+1)/2)
    t1 = x/np.sqrt(4*Dr*t_tot)
    t2 = math.exp(-x**2/(4*Dr*t_tot))
    t3 = ((Dr * t_tot)/np.pi)**((n+1)/2)
    T= T0*special.erfc(t1) #Heat conduction (Dirichlet)
    #T= 0.1*T0/(dx*lambda_m) * (t3 * t2 - x/2 * special.erfc(t1)) #Heatconduction (Neumann)
    sd.append(T) 
plt.plot(list,sd,color='black',lw=2,label="analytical T")

#import data
data = pd.read_csv('1D_Cont_Diff.csv', delimiter=',', header=0) #mesh = 1 mm poro=0.5
xp = data['x']
Tp = data['T']
plt.plot(xp,Tp,'--', color='red',label="numerical T")
plt.xlabel('distance')
plt.ylabel('temperature')
plt.legend(loc='best')


####### #solution time pulse 
plt.subplot(2,2,3)    
x=0.1 #MIDDLE point
n=2
st=[]
for t in range(1, 10001, 1):
    t0 = 1/(4*np.pi*Dr*t)**((n+1)/2)
    t1 = x/np.sqrt(4*Dr*t)
    t2 = math.exp(-x**2/(4*Dr*t))
    T =  Q/(d_r*c_r) * t0 * t2 #- (T0^2)/(16*lambda_r) * math.exp(-x/(2*Dr)) * special.erfc(t1) 
    st.append(T) 
plt.plot(range(10000),st,color='blue', lw=2,label="analytical T")
    

#import data 
data = pd.read_csv('1D_Pulse_time_Diff.csv', delimiter=',', header=0) #mesh = 1 mm poro=0.5
T = data['T']
t = data['t']
plt.plot(t,T,'--', color='red',label="numerical T")
plt.xlabel('time')
plt.ylabel('temperature')
plt.legend(loc='best')



###### #solution distance: pulse
plt.subplot(2,2,4)   
sd=[]
list = np.arange(0.0001,1,0.0001)
for x in list:
    t0 = 1/(4*np.pi*Dr*t_tot)**((n+1)/2)
    t1 = x/np.sqrt(4*Dr*t_tot)
    t2 = math.exp(-x**2/(4*Dr*t_tot))
    T =  Q/(d_r*c_r) * t0 * t2 #- (T0^2)/(16*lambda_r) * math.exp(-x/(2*Dr)) * special.erfc(t1) 
    sd.append(T) 
plt.plot(list,sd,color='blue',label="analytical T")

sd=[]
list = np.arange(0.0001,1,0.0001)
for x in list:
    t1 = x**2/(4*DD*t_tot)
    t2 = math.exp((-x)/(2*DD))  
    t3 = x**2/(4*DD*t_tot)
    T = (T0/(np.sqrt(8*lambda_r*np.pi*t_tot)))*(math.exp(-t1))-(T0**2/(2*8*lambda_r))*t2*special.erfc(t3)
    sd.append(T) 
plt.plot(list,sd,color='black',label="analytical HT")


#import data
data = pd.read_csv('1D_Pulse_Diff.csv', delimiter=',', header=0) #poro = 0.5, mesh=1 mm
xc = data['x']
Tc = data['T']
plt.plot(xc,Tc, '--', color='red',label="numerical T")
plt.xlabel('distance')
plt.ylabel('temperature')
plt.legend(loc='best')
#plt.savefig("analytical_vs_numerical_1D.png")  


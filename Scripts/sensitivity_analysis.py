# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 13:38:44 2020

@author: mylen
"""

p=input("Porosity:  ")
p=eval(p)
f=input("Flow rate (m3/s): ")
f=eval(f)
a=input("cross-section : ")
a=eval(a)

q = f/a
v = q/p
print('The darcy velocity is ' + str(q) + 'm/s')
print('The apparent velocity is ' + str(v) + 'm/s')

dt=input("Time step (s): ")
dt=eval(dt)
dx=input("element size: ")
dx=eval(dx)
k=input("Thermal conductivity: ") # 0.31
k=eval(k)
c=input("Heat capacity: ") # 1380
c=eval(c)
rho=input("density: ") #1500
rho=eval(rho)


D=k/(c*rho) #Diffusivity

disp = input('Dispersivity (1/2 element size): ') #0.5
disp = eval(disp)
DD = D + disp * v
print(' The diffusion-dispersion coefficient is: ' + str(DD))

Co = v*dt/dx# <1 / <1/2Pe
Ne = DD * dt / (dx**2) # [0.001 - 0.5]
Pe = v * dx/DD # <1 = diffusion / >1 = dispersion

print('Co = ' + str(round(Co,3)))
if Co>1:
    print('Too high!')
print('Ne = ' + str(round(Ne,3)))
if Ne < 0.001:
    print('Too low')
elif Ne > 0.5: 
    print('Too high')
print('Pe = ' + str(round(Pe,3)))
if Pe < 1:
    print('Dominant diffusive')
elif Pe > 1:
    print('Dominant dispersive')
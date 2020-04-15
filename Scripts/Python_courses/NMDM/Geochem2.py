# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 16:21:44 2019

@author: s1995204
"""
# different way to import packages
import numpy as np 
x = np.arange(11)

# from numpy import arange 
# x = arange(11)

np.arange(11) # print numbers from 0 to 10
np.arange(1,11,1)
np.arange(0.1,1.1,0.1)

# import the required packages to plot with matplotlib
import matplotlib.pyplot as plt 

t = np.arange(0,1e4,100) # time 0 to 9900 years in steps of 100 
thalf = 5730             # half-life in years 
L = np.log(2) / thalf    # decay constant in 1/years 
C14 = np.exp(-L*t)       # fraction of 14C remaining after time t 

plt.figure(figsize=(6,4)) 
plt.rcParams['font.size'] = 10 
plt.plot(t, C14, 'k--',linewidth=2)         # plot fraction against time 
plt.xlim(0,10000)
plt.ylim(0,1)
plt.xlabel('time')
plt.ylabel('remaining $^{14}$C')
plt.title('$^{14}$C') 
# plt.xticks(xlocs)
# plt.yticks(ylocs)

plt.savefig('fig.png')

###########################


import matplotlib.pyplot as plt
from scipy import stats

data = np.loadtxt('ocean.txt', skiprows=2)
d = data[:,0]
T = data[:,1]
N = data[:,2]
P = data[:,3]
Si = data[:,4]
print(d)

# make a scatter plot and label the axes
plt.figure(figsize=(6,4)) 
plt.rcParams['font.size'] = 10 
plt.plot(P,N, 'kx')
plt.xlim(0,4)
plt.ylim(0,50)
plt.xlabel('depth')
plt.xlabel('Phosphate ($\mu$mol kg$^{-1}$)')
plt.ylabel('Nitrate ($\mu$mol kg$^{-1}$)')

# fit a line by linear regression
m, c, r, p, se = stats.linregress(P,N) # slope, intercept, correlation coefficient,p-value, sterror of estimate
Pfit = np.arange(max(P)+2)
Nfit = c + m*Pfit
plt.plot(Pfit, Nfit,color='black')
plt.xticks([0,1,2,3,4])

# label the line
eqn = 'N = ' + str(round(c,2)) + '+' + str(round(m,2)) + 'P' 
x0=1
y0=20
plt.text(x0,y0,eqn,rotation=37)

# print and check the intercept and slope
print('intercept', c, np.mean(N) - m*np.mean(P))
print('slope', m, r*np.std(N)/np.std(P))


# correlation coefficients
r0,p0 = stats.pearsonr(P, N) # print correlation coefficient and p-value
r1,p1=stats.spearmanr(P,N)
print([r0,p0],
      [r1,p1])


#######################

name1 = 'Julie'
name2 = 'Jamie'
age1 = 20
age2 = 25
students = [[name1, name2],[age1, age2]]
print(students[0][1])

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 15:29:55 2019

@author: s1995204

Ice Core Plotting Demo
"""
#import modules
import numpy as np
import matplotlib.pyplot as plt

# file names
deu_file = 'deu.txt'
O18_file = 'O18.txt'
CO2_file = 'CO2.txt'
    
# read in the deuterium data
ice_age_deu = np.loadtxt(deu_file,skiprows=1,usecols=1)    
deu = np.loadtxt(deu_file,skiprows=1,usecols=2)
deltaTS = np.loadtxt(deu_file,skiprows=1,usecols=3)
    
# read in the o18 data
ice_age_O18 = np.loadtxt(O18_file,skiprows=1,usecols=0)    
O18 = np.loadtxt(O18_file,skiprows=1,usecols=1)
   
# read in the CO2 data
ice_age_CO2 = np.loadtxt(CO2_file,skiprows=1,usecols=0)    
CO2 = np.loadtxt(CO2_file,skiprows=1,usecols=1)

plt.figure(figsize=(8,10))

plt.subplot(411)
plt.plot(ice_age_deu/1000,deltaTS)
plt.xlim(0,420)
plt.xlabel('Age (ka)')
plt.tight_layout()
plt.ylabel('$\Delta TS$ ($^o$C)')

plt.title('420 ka climate record from the Vostok Ice Core (Petit et al., 1999)',fontsize=14)

plt.subplot(412)
plt.plot(ice_age_deu/1000,deu) 
plt.xlim(0,420)
plt.xlabel('Age (ka)')
plt.tight_layout()
plt.ylabel('$\delta D$ (\u2030)')
       
plt.subplot(413)
plt.plot(ice_age_CO2/1000,CO2) 
plt.xlim(0,420)
plt.xlabel('Age (ka)')
plt.tight_layout()
plt.ylabel('CO$_2$ (ppmv)')
   
plt.subplot(414)
plt.plot(ice_age_O18/1000,O18)
plt.xlim(0,420)
#plt.ylim(umin,ymax)
plt.xlabel('Age (ka)')
plt.tight_layout()
plt.ylabel('$\delta^{18}O_{atm}$ (\u2030)') # u2030 is perthrousand

plt.savefig('Vostok.png') # Other options are .pdf and .svg or .jpg

##### other example of subplots from geochem 4 #################

import matplotlib.pyplot as plt
import numpy as np

# read the data and split into variables
data = np.loadtxt('ocean.txt',skiprows=2)
z = data[:,0]  # depth
T = data[:,1]  # temperature (C)
N = data[:,2]  # nitrate concentration (micro mol / kg)
P = data[:,3]  # phosphate concentration (micro mol / kg)
Si = data[:,4] # silicate concentration (micro mol / kg)

# larger figure size for multiple plots
plt.figure(figsize=(12,8))

# temperature against depth
plt.subplot(221)
plt.plot(T,z,'o-',color='black')
plt.xlabel('Temperature ($^\circ$C)')
plt.ylabel('Depth (m)')
plt.xlim(0,30)
plt.ylim(3000,0)  # reverse y-axis running from 0 at the top to 3000 at the bottom

# nitrate against depth
plt.subplot(222)
plt.plot(N,z,'o-',color='black')
plt.xlabel('Nitrate ($\mu$mol kg$^{-1}$)')
plt.ylabel('Depth (m)')
plt.xlim(0,50)
plt.ylim(3000,0)

# phosphate against depth
plt.subplot(223)
plt.plot(P,z,'o-',color='black')
plt.xlabel('Phosphate ($\mu$mol kg$^{-1}$)')
plt.ylabel('Depth (m)')
plt.xlim(0,4)
plt.ylim(3000,0)

# silicate against depth
plt.subplot(224)
plt.plot(Si,z,'o-',color='black')
plt.ylabel('Depth (m)')
plt.xlabel('Silicate ($\mu$mol kg$^{-1}$)')
plt.xlim(0,200)
plt.ylim(3000,0)

plt.tight_layout()

####################to plot 2 datasets in same plot with legend #################

plt.figure(figsize=(6,5))
# nitrate against phosphate
plt.plot(P,N,'o',color='black',label='nitrate')
plt.xlabel('Phosphate ($\mu$mol kg$^{-1}$)')
# silicate against phosphate
plt.plot(P,Si,'x',color='black',label='silicate')
plt.xlim(0,3.5)
plt.ylim(0,160)
plt.xlabel('Phosphate ($\mu$mol kg$^{-1}$)')
plt.ylabel('Nitrate and silicate ($\mu$mol kg$^{-1}$)')

plt.legend(loc='best')

################# plotting on secondary axes #########################
# temperature against depth
plt.plot(T,z,'o-',color='black')
plt.xlabel('Temperature ($^\circ$C)')
plt.ylabel('Depth (m)')
plt.xlim(0,30)
plt.ylim(3000,0)

# nitrate against depth
plt.twiny()
plt.plot(N,z,'o-',color='blue')
plt.xlim(0,50)
plt.xlabel('Nitrate ($\mu$mol kg$^{-1}$)',color='blue')

#### OR ####
# temperature against depth
ax1 = plt.axes()
ax1.plot(T,z,'o-',color='black',label='temperature')
plt.xlabel('Temperature ($^\circ$C)')
plt.ylabel('Depth (m)')
plt.xlim(0,30)
plt.ylim(3000,0)
plt.legend(loc='lower center')

# nitrate against depth
ax2 = plt.twiny()
ax2.plot(N,z,'o--',color='black',label='nitrate')
plt.xlabel('Nitrate ($\mu$mol kg$^{-1}$)')
plt.xlim(0,50)
plt.legend(loc='center')


#### OR replace the 2 plt.legend lines by: #############
handle1, label1 = ax1.get_legend_handles_labels()
handle2, label2 = ax2.get_legend_handles_labels()
plt.legend(handle1+handle2, label1+label2,loc='lower center')

################# Error bars##################

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# read the data and split into variables
data =  np.loadtxt('meteorites.txt',skiprows=2)
d29Si = data[:,0]
d29err = data[:,1]
d30Si = data[:,2]
d30err = data[:,3]

# scatter plot with error bars
plt.figure(figsize=(6,6))
plt.errorbar(d29Si,d30Si,color='black',fmt='o',xerr=d29err,yerr=d30err)

# fit a line by linear regression
m, c, r, _, _ = stats.linregress(d29Si,d30Si)
fit29 = np.arange(-0.4,0,0.1)
fit30 = c + m*fit29
eqn = str(round(c,2)) + '+' + str(round(m,2)) + '$\delta^{29}$Si' 
plt.plot(fit29, fit30, color='black', label=eqn)
plt.plot(fit29, 2*fit29, '--', color='black', label='2$\delta^{29}$Si')

# label axes
plt.xlabel(u'$\delta^{29}$Si (\u2030)')
plt.ylabel(u'$\delta^{30}$Si (\u2030)')
plt.xlim(-0.4,-0.1)
plt.ylim(-0.8,-0.2)

plt.legend(loc='best')



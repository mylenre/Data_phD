# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

N = 50
av_mole = np.random.rand(N)
print(av_mole)

HIG = 1 + 2*np.exp(av_mole) + av_mole*av_mole + np.random.rand(N)
area = np.pi*(15*np.random.rand(N))**2
mole_error = 0.1 + 0.1*np.sqrt(av_mole)
hig_error = 0.1 + 0.2*np.sqrt(HIG)/10

# scatter plot
plt.scatter(av_mole, HIG, s=70, c=area, marker='o',cmap=plt.cm.jet)
cb = plt.colorbar()
cb.set_label('Field Area (m$^2$)',fontsize=20)

# scatter plot with errorbars
plt.figure(figsize=(6,6))
plt.errorbar(av_mole, HIG, xerr=mole_error, yerr=hig_error, fmt='o',color='black')
plt.xlabel('Average number of moles per sq. meter', fontsize=16)
plt.ylabel('Health Index for Gardeners (HIG)', fontsize=16)
plt.title('Mole population against gardeners health', fontsize=16)

slope, intercept, r_value, p_value, std_err = stats.linregress(av_mole, HIG)
print('slope = ', slope)
print('intercept = ', intercept)
print('r value = ', r_value)
print('p value = ', p_value)
print('standard error = ', std_err)

line = slope*av_mole+intercept
plt.plot(av_mole,line,'r-')
plt.title('Linear fit y(x)='+str('%.1f'%slope)+'x+'+str('%.1f'%intercept), fontsize=16)

# create boxplot 
import matplotlib.pyplot as plt
import numpy as np
basalt = np.loadtxt('basalt.txt')
andesite = np.loadtxt('andesite.txt')
rhyolite = np.loadtxt('rhyolite.txt')
data = [basalt, andesite, rhyolite]

fig = plt.figure()
fig.suptitle('Silica content in Basalt, Andesite and Rhyolite', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.boxplot(data)
ax.set_title('Figure 1')
ax.set_xlabel('Rock type')
ax.set_ylabel('% Si')
plt.xticks([1,2,3],['Basalt','Andesite','Rhyolite'])
plt.show()
plt.savefig(

#bp = plt.boxplot(data)
#plt.setp(bp['medians'], color='black')
#plt.xticks([1,2,3],['Basalt','Andesite','Rhyolite'])
#plt.title('Silica content in Basalt, Andesite and Rhyolite',fontsize=14)

# create histograms

n, bins, patches = plt.hist(av_mole, bins=15, facecolor='blue', edgecolor='k', alpha=0.5)
print(n)
print(bins)
print(patches)

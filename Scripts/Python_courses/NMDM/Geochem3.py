from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import math

############## load data ##############

x = np.loadtxt('data.txt', skiprows=3, usecols=0)  # first column 
y = np.loadtxt('data.txt', skiprows=3, usecols=1)  # second column
# or
data = np.loadtxt('data.txt', skiprows=3)  # all data
x = data[:,0]  # first column
y = data[:,1]  # second column

################ stats #################

Si = np.loadtxt('basalt.txt')
print(len(Si))
#print(Si)
dim = print(np.size(Si))
extent = print([np.amin(Si), np.amax(Si)])
average = print(round(np.mean(Si),2))
med = print(np.median(Si))
stdev = print(round(np.std(Si,ddof=1))) # (ddof stands for “delta degrees of freedom”; 
                 # ddof=0 is the default and returns the population standard deviation, 
                 # ddof=1 returns the sample standard deviation).
        
stats.skew(Si)

############ histograms ###############

ndata = len(Si)
print('nb data= ', ndata)
maxi = np.amax(Si)
mini = np.amin(Si)
extent = maxi - mini
print('extent = ', extent)
binsize = round(extent / math.sqrt(ndata))
print('bin size = ', binsize)
nbin= int(round(extent/binsize,0))
print('nb bin = ', nbin)

plt.hist(Si, bins = nbin, range=(mini,maxi),color='k',histtype='step')

################# subplot #################

x = np.arange(10)
plt.subplot(2,2,1)
plt.plot(x)
plt.subplot(2,2,2)
plt.plot(x**2)
plt.subplot(2,1,2)
plt.plot(x, x**2)

plt.savefig('subplots', dpi=400)

plt.figure()
plt.subplot(2,1,1)
plt.hist(Si, bins = 6, range=(mini,maxi),color='k',histtype='step')
plt.subplot(2,1,2)
plt.hist(Si, bins = 50, range=(mini,maxi),color='r',histtype='step')
plt.figure(figsize=(10,10))
plt.tight_layout()

plt.savefig('subplots_hist', dpi=400)

############## scatter plot ########################
plt.plot(x,y,'o') 
('$\mu$mol kg$^{-1}$')


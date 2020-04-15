################ interpolation package function in scipy : i.e. inter1d()####################
%matplotlib inline
"""
Demonstration of nearest-neighbour, linear and cubic spline interpolation
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

x = [0,0.5,1.6,3.8,5.2,6]    # irregularly spaced x points
y = np.sin(x)                # a function of x
xnew = np.linspace(np.min(x),np.max(x),100)  # regularly spaced x points with the same range

# interpolate between points and plot
for kind in ('nearest', 'linear', 'cubic'):
    func = interp1d(x, y, kind=kind)
    ynew = func(xnew)
    plt.plot(xnew, ynew, label=kind)

# plot points, label axes and lines
plt.plot(x,y,'o',color='black')
plt.xlabel('x',fontsize=16)
plt.ylabel('y',fontsize=16)
plt.legend(fontsize=12)  # note a different way of controlling font sizes

####################### Irregularly spaced sequential data############################
"""
Temperature reconstructions from the EPICA ice core
"""
import matplotlib.pyplot as plt
import numpy as np

# read age and temperature data
ages =  np.loadtxt('EPICA.txt',skiprows=2,usecols=1)
temp =  np.loadtxt('EPICA.txt',skiprows=2,usecols=2)

# plot the data with a stretched and reversed x-axis
plt.figure(figsize=(16,4))
plt.rcParams['font.size'] = 16
plt.plot(ages, temp, ',', color='black')
plt.xlim(800,0)
plt.ylim(-12,6)
plt.xlabel('Time (thousands of years before present)')
plt.ylabel('Temperature difference ($^\circ$C)')

# interpolate temperature to regular 100 years increments and plot again
from scipy.interpolate import interp1d
ages_reg = np.arange(1,800,0.1)
f = interp1d(ages, temp)
temp_reg = f(ages_reg)
plt.figure(figsize=(16,4))
plt.rcParams['font.size'] = 16
plt.plot(ages_reg, temp_reg, ',', color='black')
plt.xlim(800,0)
plt.ylim(-12,6)
plt.xlabel('Time (thousands of years before present)')
plt.ylabel('Temperature difference ($^\circ$C)')

######################### trend detection #################################################
"""
Temperature trends from the EPICA ice core
"""
from scipy import stats

# plot last 20 thousand years
plt.figure(figsize=(16,4))
plt.rcParams['font.size'] = 16
plt.plot(ages, temp, color='black')
plt.xlim(20,0)

# extract Holocene dates, plot temperature and fit a trend line
hol = ages<11.5
print(hol)
ages_hol = ages[hol]
temp_hol = temp[hol]
m, c, _, _, _ = stats.linregress(ages_hol, temp_hol)
Tfit = c + m*ages_hol
trend = str(round(-m,2))
plt.plot(ages_hol, Tfit, color='blue', lw=3, label='Holocene trend '+trend+'$^\circ$C/ka')
print('Holocene temperature trend',trend,'C per thousand years')

# extract LGM-Holocene dates, plot temperature and fit a trend line
lgm = np.logical_and(ages>11.5,ages<20)
ages_lgm = ages[lgm]
temp_lgm = temp[lgm]
m, c, _, _, _ = stats.linregress(ages_lgm, temp_lgm)
Tfit = c + m*ages_lgm
trend = str(round(-m,2))
plt.plot(ages_lgm, Tfit, color='red', lw=3, label='Deglaciation trend '+trend+'$^\circ$C/ka')
print('LGM to Holocene temperature trend',trend,'C per thousand years')

# extract Antarctic Cold Reversal dates, plot temperature and fit a trend line
acr = np.logical_and(ages>12.5,ages<14.5)
ages_acr = ages[acr]
temp_acr = temp[acr]
m, c, _, _, _ = stats.linregress(ages_acr, temp_acr)
Tfit = c + m*ages_acr
trend = str(round(-m,2))
plt.plot(ages_acr, Tfit, color='black', lw=3, label='ACR trend '+trend+'$^\circ$C/ka')
print('Antarctic Cold Reversal temperature trend',trend,'C per thousand years')

# label axes and lines
plt.ylim(-12,6)
plt.xlabel('Time (thousands of years before present)')
plt.ylabel('Temperature difference ($^\circ$C)')
plt.legend(loc='lower right')


####################################### functions 1 ##########################################
"""
Smoothed temperature reconstructions from the EPICA ice core
"""

def moving_average(y, K=5):
    """
    2K+1 point moving average of array y
    """
    N = np.size(y)      # find the size of y
    s = np.zeros(N)     # make an array of zeros with the same size
    for n in range(N):  # loop for the moving average
        kmin = max(n-K, 0)    # limit to indices within the array
        kmax = min(n+K+1, N)  # i.e. range 0 to N-1
        s[n] = np.mean(y[kmin:kmax])
    return s            # return the smoothed array

# plot interpolated temperatures
plt.figure(figsize=(16,4))
plt.rcParams['font.size'] = 16
plt.plot(ages_reg, temp_reg, ',')

# plot smoothed temperatures
temp_smooth = moving_average(temp_reg, K=50)
plt.plot(ages_reg, temp_smooth, color='black', lw=2)

# label the axes
plt.xlim(800,0)
plt.ylim(-12,6)
plt.xlabel('Time (thousands of years before present)')
plt.ylabel('Temperature difference ($^\circ$C)')

####################################### functions 2 ##########################################

def trend(x, y):
    """
    Plot a sequence, fit a trend line and return the slope of the line
    """
    plt.plot(x, y)
    m, c, _, _, _ = stats.linregress(x, y)
    y = c + m*x
    plt.plot(x, y, color='black', linewidth=2)
    return m
 
plt.figure(figsize=(16,4))
plt.rcParams['font.size'] = 16

# extract Holocene dates and call the user-defined trend() function   
ages_hol = ages[ages<11.5]
temp_hol = temp[ages<11.5]
m = trend(ages_hol, temp_hol)
print('Holocene temperature trend',round(-m,2),'C per thousand years')

# extract LGM-Holocene dates and call the user-defined trend() function  
ages_lgm = ages[np.logical_and(ages>11.5,ages<20)]
temp_lgm = temp[np.logical_and(ages>11.5,ages<20)]
m = trend(ages_lgm, temp_lgm)
print('LGM to Holocene temperature trend',round(-m,2),'C per thousand years')

# extract Antarctic Cold Reversal dates and call the user-defined trend() function  
ages_acr = ages[np.logical_and(ages>12.5,ages<14.5)]
temp_acr = temp[np.logical_and(ages>12.5,ages<14.5)]
m = trend(ages_acr, temp_acr)
print('Antarctic Cold Reversal temperature trend',round(-m,2),'C per thousand years')

# label axes
plt.xlim(20,0)
plt.ylim(-12,6)
plt.xlabel('Time (thousands of years before present)')
plt.ylabel('Temperature difference ($^\circ$C)')


######################### fourier synthesis #############################

"""
Fourier synthesis of a square wave
"""
import numpy as np
import matplotlib.pyplot as plt

# fundamental
x = np.linspace(0,2*np.pi,129)
y = np.sin(x)
plt.plot(x, y, label='N=0')

# first harmonic
y = y + np.sin(3.*x)/3.
plt.plot(x, y, label='N=1')

# higher harmonics
for N in range(2,31):
    k = 2*N + 1
    y = y + np.sin(float(k)*x)/float(k)
plt.plot(x, y, label='N=31')

# label axes
plt.xlabel('x')
plt.xlim(0,2*np.pi)
plt.xticks([0,np.pi,2*np.pi],['0','$\pi$','$2\pi$'])
plt.ylabel('y')

plt.legend()


###################### power spectra ###############################
"""
Code to add to the EPICA program to plot the temperature spectrum
"""

# subtract mean and find size of interpolated temperature series
y = temp_reg - np.mean(temp_reg)
N = np.size(y)

# calculate spectrum and frequencies
p = np.abs(np.fft.rfft(y))
f = np.arange(N/2+1)/(0.1*N)

# plot the spectrum with a logarithmic frequency scale
plt.rcParams['font.size'] = 16
plt.plot(f, p, color='black')
plt.xscale('log')

# place lines at the Milankovitch frequencies
plt.plot([1/100.,1/100.],[0,1e4],'--',color='black')
plt.plot([1/40.,1/40.],[0,1e4],'--',color='black')
plt.plot([1/23.,1/23.],[0,1e4],'--',color='black')

# label the axes
plt.ylim(0,1e4)
plt.xlabel('Frequency (ky$^{-1}$)')
plt.ylabel('Power')





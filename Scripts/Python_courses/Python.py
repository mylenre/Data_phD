########### import the required libraries and modules###########
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import csv
import math
import numpy as np
from scipy import stats
from scipy.interpolate import interp1d # interpolation package

####################### numpy functions #################
from numpy import arange 
x = np.arange(11) # print numbers from 0 to 10
#np.arange(1,11,1)
#np.arange(0.1,1.1,0.1)
print(x)
print(x[:2])
print(x[-2])
print(x[-2:])
var = 'Python'
print(var[::-1])

#np.cos(x), np.sin(x), np.tan(x) with angles as arguments (in radians)
#np.arccos(x) ...
#np.deg2rad(x), np.rad2deg(x)
#np.exp(x), np.log(x) 
#np.sqrt(x), np.log10(x)

x_mean = np.mean(x)
x_standard_dev = np.std(x)
x_rad=np.deg2rad(x)
x_sin = np.sin(x_rad)
np.arccos(np.deg2rad(1/np.sqrt(2)))
dim = print(np.size(x))
extent = print([np.amin(x), np.amax(x)])
average = print(round(np.mean(x),2))
med = print(np.median(x))
stdev = print(round(np.std(Si,ddof=1))) # (ddof stands for â€œdelta degrees of freedomâ; 
                 # ddof=0 is the default and returns the population standard deviation, 
                 # ddof=1 returns the sample standard deviation).
        
stats.skew(Si)

#################### attributes and methods #########################
print('O3 minimum',y.min())
print('O3 minimum',min(y))
print('O3 maximum',y.max())
print('O3 mean',y.mean().round(2))
print('O3 mean',round(np.mean(y),2))
print('O3 standard deviation',y.std().round(2))

# with functions
#  For a 2D array, operations are applied to columns of the arrays if axis=0 and rows if axis=1.
print('array minimum',np.min(X,axis=0))
print('array maximum',np.max(X,axis=0))
print('array mean',np.round(np.mean(X,axis=0),2))
print('array standard deviation',np.round(np.std(X,axis=0),2))
print()

# with methods
print('array minimum',X.min(axis=0))
print('array maximum',X.max(axis=0))
print('array mean',X.mean(axis=0).round(2))
print('array standard deviation',X.std(axis=0).round(2))

###################### create arrays ##############################
# 3d array with dimensions (time, latitude, longitude)
a = np.zeros((3, 3, 3))
# 4d array with dimensions (time, height, latitude, longitude)
b = np.zeros((3, 3, 3, 3))

# add 1 to the first columns
for i in [a, b]:
    i[..., 0] += 1.
 
# get diagonal values in the 5x5 array using fancy indexing
b = np.arange(25).reshape(5, 5)
print(b[[0, 1, 2, 3, 4],[0, 1, 2, 3, 4]])

#mask NaN values
a = np.array([[np.nan, 3., 1.], [2., 8., 5.]])
print(np.sum(np.ma.masked_invalid(a), axis=1))

#specific data
magnitude = np.array([2., 5., 6., 1.])
damage = np.array([1000., 100000., 110000, 10.])
print(np.sum(np.ma.masked_where(magnitude<5.0, damage)))

c = np.arange(3.)  # array containing [0., 1., 2.]
# ndarray.copy()

###################### functions ######################
def my_mean(x):
  total=0
  for i in range(len(x)):
      total = total + x[i]
  mean_value = total / len(x)
  return mean_value

################### input ########################

string = input('Type some text and hit return:') 
#  input() function reads text typed by the user (you in this case), with a string argument that will be printed on the screen to ask for inputprint(string)
print(string)
print(len(string))

number = eval(input('Enter a number:')) # for numeric inputs
print(number+number) # addition

##################### if loop ############################

today='Thursday'
if today=='Friday':
  print("Why not go home early?")
else:
  print("Hard work is a virtue! You can do it! I believe in you!")
  
############################ open files ##########################
pressure_data = [] # Create an empty list as before to store values

with open("StormEleanor_2_3_Jan.csv", "r") as weatherfile:
  next(weatherfile) # to skip the head line
  for line in weatherfile:
    #print(line)
    #print(type(line))
    data_row = line.split(',')
    #print(line.split(','))
    pressure = data_row[6] # each value of pressure of line(i) is overwritten by the line(i+1) one 
    #print(pressure) # those are strings
    pressure_data.append(float(pressure)) # to store all pressure values in numerical format

print(pressure_data[0])
print(type(pressure_data[0]))

              ############ with pandas #############
# When to use pandas:
  # Table-like columnar data
  # Interfacing with databases (MySQL etc.)
  # Multiple data-types in a single data file.
# When not to use pandas:
  # For really simple data files (a single column of values in a text file, for example, might be overkill).
  # If you are dealing with large gridded datasets of a single data type --> numpy.
  # If you are doing lots of matrix calculations, or other heavily mathematical operations on gridded data --> numpy

data = pd.read_csv('StormEleanor_2_3_Jan.csv', delimiter=',', header=0)
data = pd.read_csv('your_csv_file').values
print(type(data))
pressure_data = data['Pair_Avg']
print(pressure_data)

             ############ with csvfile ##################

with open('StormEleanor_2_3_Jan.csv', 'r') as csvfile:
  next(csvfile)
  for row in csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC): #quoting=csv.QUOTE_NONNUMERIC tells the csv module to read all the non-quoted values in the csv file as strings, and the rest as numeric values (e.g. floats)
     pressure_data.append(row[6])

# Check our variables look okay and they are the correct type:
print(pressure_data)
print(type(pressure_data[1]))


           ################### with numpy #################

x = np.loadtxt('data.txt', skiprows=3, usecols=0)  # first column 
y = np.loadtxt('data.txt', skiprows=3, usecols=1)  # second column
data = np.loadtxt('data.txt', skiprows=3)  # all data
x = data[:,0]  # first column
y = data[:,1]  # second column


####################### Timeseries values ######################
date_time_series = []
date_time = datetime.datetime(2018, 1, 2)
date_at_end = datetime.datetime(2018, 1, 3, 23, 59)
step = datetime.timedelta(minutes=1)

while date_time <= date_at_end:
  date_time_series.append(date_time)
  date_time += step

print(date_time_series)

####################################################################
################### plot data #####################################
####################################################################

plt.figure(figsize=(6,4))
 
plt.rcParams['font.size'] = 10 

plt.plot(date_time_series, pressure_data, 'kx-')
plt.plot(P,N,'o',color='black',label='nitrate')
plt.plot(x,y,'o',color='black')

plt.xlim(0,10000)
plt.ylim(0,1)
plt.ylabel("Pressure (hPa)")
plt.xlabel("Time")
#plt.xlabel('x',fontsize=16)
#plt.ylabel('y',fontsize=16)
plt.title("Average Pressure, JCMB Weather Station, 2-3rd Jan 2018", fontsize=14)
plt.xticks(rotation=-60)
# plt.xticks(xlocs)
# plt.yticks(ylocs)

plt.tight_layout()

# plot the data with a stretched and reversed x-axis
plt.figure(figsize=(16,4))
plt.rcParams['font.size'] = 16
plt.plot(ages, temp, ',', color='black')
plt.xlim(800,0)
plt.ylim(-12,6)
plt.xlabel('Time (thousands of years before present)')
plt.ylabel('Temperature difference ($^\circ$C)')

plt.legend(loc='lower right')
plt.legend(loc='best')
plt.legend(fontsize=12)  # note a different way of controlling font sizes

plt.savefig("pressure_final.png") # Other options are .pdf and .svg or .jpg

plt.title('$^{14}$C')
plt.title('Nitrate ($\mu$mol kg$^{-1}$)')
plt.xlabel(u'$\delta^{29}$Si (\u2030)')
plt.ylabel('$\delta D$ (\u2030)')
plt.ylabel('CO$_2$ (ppmv)')
plt.ylabel('$\delta^{18}O_{atm}$ (\u2030)') # u2030 is perthrousand
plt.xlabel('Temperature ($^\circ$C)')

           #########to plot 2 datasets in same plot with legend ########

plt.figure(figsize=(6,5))
# nitrate against phosphate
plt.plot(P,N,'o',color='black',label='nitrate')
plt.xlabel('Phosphate ($\mu$mol kg$^{-1}$)')
# silicate against phosphate
plt.plot(P,Si,'x',color='black',label='silicate')
plt.xlabel('Phosphate ($\mu$mol kg$^{-1}$)')
plt.ylabel('Nitrate and silicate ($\mu$mol kg$^{-1}$)')

plt.legend(loc='best')

           ############## plotting on secondary axes ################# 
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



            ############ subplot #################
plt.figure()

plt.subplot(2,1,1)
plt.plot(T,z,'o-',color='black')
plt.xlabel('Age (ka)')
plt.tight_layout()
plt.ylabel('Thickness')
plt.xlim(0,420)
plt.ylim(3000,0)  # reverse y-axis running from 0 at the top to 3000 at the bottom

plt.subplot(2,1,2)
plt.hist(Si, bins = 50, range=(mini,maxi),color='r',histtype='step')
plt.figure(figsize=(10,10))

plt.tight_layout()

plt.savefig('subplots_hist', dpi=400)

           ########## linear regression ##########
# correlation and rms error 
m, c, r, p, se = stats.linregress(P,N) # slope, intercept, correlation coefficient,p-value, sterror of estimate
Pfit = np.arange(max(P)+2)
Nfit = c + m*Pfit
plt.plot(Pfit, Nfit,color='black')
plt.xticks([0,1,2,3,4])

O3 = data[:,0]
Ta = data[:,2]
m, c, _, _, _ = linregress(Ta, O3)
O3fit = c + m*Ta
resid = O3fit - O3
print('rms error',np.sqrt(np.mean((resid)**2)))
print('correlation',pearsonr(O3fit,O3))

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

            ############# multiple regressions ############
import numpy as np
import statsmodels.api as sm

# read the independent and dependent variables
X = np.loadtxt('NYair.txt',skiprows=2,usecols=(1,2,3))
y = np.loadtxt('NYair.txt',skiprows=2,usecols=0)
# add a column of ones to include a constant term in the regression
X = sm.add_constant(X)
# fit a model by 'Ordinary Least Squares' and print the results
model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

# Comparison sigle / Multiple regression
# Instead of printing the coefficients, a = results.params will copy them to an array a. 
# An easy way to get a fit line is to use the matrix equation yfit = np.dot(X,a). 

plt.figure(figsize=(6,6))
plt.rcParams['font.size'] = 16
plt.plot(O3, O3fit, 'o', color='red', label='single regresion')

a = results.params 
yfit = np.dot(X,a) 
resid = yfit - y
print('rms error',np.sqrt(np.mean((resid)**2)))
print('correlation',pearsonr(yfit,y))
plt.plot(O3, yfit, 'o', color='black', label='multiple regresion')
plt.plot([0,200], [0,200], color='black')
plt.xlim(0,200)
plt.xlabel('Measured O$_3$ concentration (ppb)')
plt.ylim(0,200)
plt.ylabel('Predicted O$_3$ concentration (ppb)')
plt.legend(loc='upper left')


            ############ histograms ##################

ndata = len(x)
print('nb data= ', ndata)
maxi = np.amax(x)
mini = np.amin(x)
extent = maxi - mini
print('extent = ', extent)
binsize = round(extent / math.sqrt(ndata))
print('bin size = ', binsize)
nbin= int(round(extent/binsize,0))
print('nb bin = ', nbin)

plt.hist(x, bins = nbin, range=(mini,maxi),color='k',histtype='step')


         ################# Error bars##################
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

                  ############ complex plots ##############
vars = ['O$_3$ concentration (ppb)','Solar radiation (MJ m$^{-2}$)','Temperature ($^\circ$C)','Wind speed (m $^{-1}$)']
N, nvars = data.shape
print('Data file has',N,'rows and',nvars,'columns')

# 4x4 array of all possible scatterplot and correlations
plt.figure(figsize=(12,12))
plotnum = 1
for rownum in range(nvars):
    for colnum in range(nvars):
        plt.subplot(4,4,plotnum)
        plt.plot(data[:,colnum], data[:,rownum], 'o', color='black')
        r, p = pearsonr(data[:,colnum], data[:,rownum])
        print(vars[colnum],'and',vars[rownum],'correlation',round(r,2),'p =',round(p,3))
        plt.xlabel(vars[colnum])
        plt.ylabel(vars[rownum])
        plotnum += 1
        
print('correlation matrix')
print(np.corrcoef(data,rowvar=0).round(2))
plt.tight_layout()

# make scatterplots and add regression lines
plt.figure(figsize=(12,12))
plotnum = 1
for rownum in range(nvars):
    for colnum in range(nvars):
        if colnum < rownum:
            plt.subplot(4,4,plotnum)
            plt.plot(data[:,colnum], data[:,rownum], 'o', color='black')
            if rownum==3:
                plt.xlabel(vars[colnum],fontsize=12)
            else:
                plt.xticks([])
            if colnum==0:
                plt.ylabel(vars[rownum],fontsize=12)
            else:
                plt.yticks([])
            m, c, _, _, _ = linregress(data[:,colnum], data[:,rownum])
            xfit = data[:,colnum]
            yfit = c + m*xfit
            plt.plot(xfit, yfit, color='black')
        plotnum += 1

            ############## spatia tripots / contour plots ###########
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

# read the data file
x = np.loadtxt('survey.txt', usecols=0)
y = np.loadtxt('survey.txt', usecols=1)
z = np.loadtxt('survey.txt', usecols=2)

# make the plot square and select a font size
plt.figure(figsize=(6,6))
plt.rcParams['font.size'] = 14

# generate and plot the triangular network
plt.triplot(x, y, '--', color='grey')  # dashed grey lines to be less obtrusive
plt.triplot(x, y, 'o', color='black')

# angular contours from triangulation
# 10 m intervals, red dotted lines
levels = np.arange(200,300,10)
plt.tricontour(x, y, z, colors='red', levels=levels, linestyles='dotted') 

# refine the contours
triang = tri.Triangulation(x, y)
refiner = tri.UniformTriRefiner(triang)
tri_refi, z_refi = refiner.refine_field(z, subdiv=3)
c = plt.tricontour(tri_refi, z_refi, colors='black', levels=levels)
plt.clabel(c, fmt='%d')  # contour labels

# label axes
plt.xlim(0,100)
plt.ylim(0,100)
plt.xlabel('West-East (m)')
plt.ylabel('South-North (m)')

      ################# draw map image ########################
import matplotlib.pyplot as plt
import numpy as np
map = np.loadtxt('vegetation.txt')

vegclasses = ['ocean', 'ice','rock/lichen', 'prostrate tundra', 'dwarf shrub', 'low shrub', 'boreal evergreen needleleaf','boreal broadleaf deciduous','temperate evergreen needleaf', 'temperate broadleaf deciduous', 'xeric shrubland', 'xeric woodland','grass','lakes','deciduous needleleaf']

# print(plt.colormaps())
cmap = plt.get_cmap('jet', 15) 
plt.figure(figsize=(8,4))
plt.imshow(map,extent=[0,8000,0,1000],origin='lower', cmap=cmap, aspect='auto') # 'auto' used to let dimensions of figure being non proportional
# cmap = cmap for discrete features ( input data on pixel by pixel basis)
plt.xlim(0,8000)
plt.ylim(0,1000)
plt.xlabel('m')
plt.ylabel('m')
cbar = plt.colorbar(shrink=0.9, ticks=range(15)) # to discretise coorbar
# cbar.set_label('vegetation index')
cbar.set_ticklabels(vegclasses)


 

     ####################### plot elevation data ##################

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 14

# load the elevation data and plot an imag
z = np.loadtxt('ArthursSeat.txt')
plt.imshow(z, cmap='gray', extent=[0,1600,0,1600], origin='lower')

# axes
plt.xlim(0,1600)
plt.ylim(0,1600)
plt.yticks([0,500,1000,1500])
plt.xlabel('m')
plt.ylabel('m')

# colour bar
cbar = plt.colorbar()
cbar.set_label('Elevation (m)') 
cbar.set_ticks([50,100,150,200])

# image maps of gradient components and slope angle
plt.figure(figsize=(18,6))
dzdy, dzdx = np.gradient(z, 2)
slope = np.sqrt(dzdx**2 + dzdy**2)
angle = np.rad2deg(np.arctan(slope))

plt.subplot(131)
plt.imshow(dzdx, cmap='bwr', vmin=-7, vmax=7)  # blue-white-red colour map
cbar = plt.colorbar(orientation='horizontal', shrink=0.8)
cbar.set_label('west-east slope component')
cbar.set_ticks([-6,-4,-2,0,2,4,6])
plt.xticks([])
plt.yticks([])

plt.subplot(132)
plt.imshow(dzdy, cmap='bwr', vmin=-7, vmax=7)
cbar = plt.colorbar(orientation='horizontal', shrink=0.8)
cbar.set_label('south-north slope component')
cbar.set_ticks([-6,-4,-2,0,2,4,6])
plt.xticks([])
plt.yticks([])

plt.subplot(133)
plt.imshow(angle, cmap='gray')
cbar = plt.colorbar(orientation='horizontal', shrink=0.8)
cbar.set_label('Slope angle (degrees)')
plt.xticks([])
plt.yticks([])
print('Maximum angle',angle.max().round(0),'degrees')

# shaded contour map 
from matplotlib.colors import LightSource
print('Minimum elevation',z.min(),'m')
print('Maximum elevation',z.max(),'m')
plt.figure(figsize=(12,6))

plt.subplot(121)
ls = LightSource(azdeg=315, altdeg=45)
shadsurf = ls.shade(z, cmap=plt.cm.gray)
plt.imshow(shadsurf, alpha=0.8, origin='lower')   # apha = transparence
levels = np.arange(0, z.max(), 20)
c = plt.contour(z, levels , colors='black')
plt.clabel(c, fmt='%d') 
plt.xticks([])
plt.yticks([])

# shaded image
plt.subplot(122)
plt.imshow(z, cmap='terrain', origin='lower')   # plot color map as a function of z 
    #plt.imshow(z, cmap=plt.cm.gist_earth, alpha=0.5, origin='lower')
plt.imshow(shadsurf, alpha=0.5, origin='lower')  # plot relief with transparence
plt.xticks([])
plt.yticks([])
cbar = plt.colorbar(shrink=0.8)
cbar.set_label('Elevation (m)') 

##################### plot vectors ###########################

import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(8,8))

# read data and calculate wind speed
P = np.loadtxt('Psurf.txt')
U = np.loadtxt('Uwind.txt')
V = np.loadtxt('Vwind.txt')
W = np.sqrt(U**2 + V**2)

# wind speed as an image with a colour bar
# adding _r reverses a colour map - blue-white in this case
plt.imshow(W,cmap='Blues_r',origin='lower')    # _r for reversed color gradient
cbar = plt.colorbar(shrink=0.65)
cbar.set_label('wind speed (m s$^{-1}$)')

# surface pressure as a contour plot with 4 hPa spacing
levels = 960 + 4*np.arange(20)
levels = np.arange(P.min(), P.max(), 4)
cs = plt.contour(P, colors='black', levels=levels)
plt.clabel(cs, fmt='%d')

# wind vectors
plt.quiver(U,V)

plt.xticks([])
plt.yticks([])

###################  saving a file ################################
np.savetxt('save_file.csv', your_data, delimeter=',', comments='')
# save one data to npy file
np.save('save_file1.npy' ,data)
# save collection of data to single npz file
dataset = {'temperature': data1,
		   'humidity': data2}
np.savez('save_file2.npz', **dataset)

            ######## reopen files #############
open_data = np.load('save_file1.npy')
open_dataset = np.load('save_file2.npz')

         ######### access data in dataset###########
temperature = open_dataset['temperature']

name1 = 'Julie'
name2 = 'Jamie'
age1 = 20
age2 = 25
students = [[name1, name2],[age1, age2]]
print(students[0][1])

#################################################################################
##################################### interpolation #############################
#################################################################################

x = [0,0.5,1.6,3.8,5.2,6]                     # irregularly spaced x points
y = np.sin(x)                                 # a function of x
xnew = np.linspace(np.min(x),np.max(x),100)  # regularly spaced x points with the same range

# interpolate between points
for kind in ('nearest', 'linear', 'cubic'):
    func = interp1d(x, y, kind=kind)
    ynew = func(xnew)
    plt.plot(xnew, ynew, label=kind)

####################### Irregularly spaced sequential data####################
ages =  np.loadtxt('EPICA.txt',skiprows=2,usecols=1)
temp =  np.loadtxt('EPICA.txt',skiprows=2,usecols=2)

# interpolate temperature to regular 100 years increments and plot again
ages_reg = np.arange(1,800,0.1)
f = interp1d(ages, temp)
temp_reg = f(ages_reg)

######################### trend detection #################################################
# extract Holocene dates, plot temperature and fit a trend line
hol = ages<11.5
# LGM-Holocene dates: lgm = np.logical_and(ages>11.5,ages<20)
# Antarctic Cold Reversal dates :  acr = np.logical_and(ages>12.5,ages<14.5) 
print(hol)
ages_hol = ages[hol]
temp_hol = temp[hol]
m, c, _, _, _ = stats.linregress(ages_hol, temp_hol)
Tfit = c + m*ages_hol
trend = str(round(-m,2))
plt.plot(ages_hol, Tfit, color='blue', lw=3, label='Holocene trend '+trend+'$^\circ$C/ka')
print('Holocene temperature trend',trend,'C per thousand years')


############################ function 1 : moving average ##################################
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

################################ functions 2 : trend #######################################
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


######################### fourier synthesis of a square wave #############################
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

############## power spectra : plot temperature spectrum ###############################

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


###########################################################################################
years_dict = dict()
with open('list.txt', 'r') as list: 
    for line in list:
        if line[0] in years_dict:
            # append the new number to the existing array at this slot
            years_dict[line[0]].append(line[1])
        else:
            # create a new array in this slot
            years_dict[line[0]] = [line[1]]
            
#########################################################################
# Import cars data
import pandas as pd
cars = pd.read_csv('cars.csv', index_col = 0)

# Create car_maniac: observations that have a cars_per_cap over 500
cpc = cars['cars_per_cap']
many_cars = cpc > 500
car_maniac=cars[many_cars]

# Print car_maniac
print(car_maniac)


-----------------------------------------------------------------

# Import cars data
import pandas as pd
cars = pd.read_csv('cars.csv', index_col = 0)

# Import numpy, you'll need this
import numpy as np

# Create medium: observations with cars_per_cap between 100 and 500
cpc = cars['cars_per_cap']
between = np.logical_and(cpc > 100, cpc < 500)
medium = cars[between]

# Print medium
print(medium)

------------------------------------------------------------------

# areas list
areas = [11.25, 18.0, 20.0, 10.75, 9.50]

# Change for loop to use enumerate() and update print()
for a,b in enumerate(areas) :
    print("room "+ str(a)+ ": "+str(b))
    
-------------------------------------------------------------------
# Import numpy as np
import numpy as np

# For loop over np_height (1D numpy array)
for x in np_height:
    print(str(x) + ' inches')

# For loop over np_baseball (2D numpy array)
for x in np.nditer(np_baseball):
    print(str(x))

# iterate through pd DataFrame
import pandas as pd
cars = pd.read_csv('cars.csv', index_col = 0)

for lab, row in cars.iterrows() :
    print(lab + ": "+ str(row['cars_per_cap']))
    
# Code for loop that adds COUNTRY column
for lab, row in cars.iterrows():
    cars.loc[lab, "COUNTRY"]= row['country'].upper()

# using apply()
- brics["name_length"] = brics["country"].apply(len)
- cars["COUNTRY"] = cars["country"].apply(str.upper) for a method

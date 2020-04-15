########### for ###########################

"""
Scatter plots and correlation matrix for O3 data
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

# read data, find number of rows and columns
data = np.loadtxt('NYair.txt',skiprows=2)
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


#################### if #############################
"""
Scatterplots and regression lines for O3 data
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress, pearsonr

# read data
data = np.loadtxt('NYair.txt',skiprows=2)
vars = ['O$_3$ concentration (ppb)','Solar radiation (MJ m$^{-2}$)','Temperature ($^\circ$C)','Wind speed (m $^{-1}$)']

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

######################## correlation and rms error ###############
O3 = data[:,0]
Ta = data[:,2]
m, c, _, _, _ = linregress(Ta, O3)
O3fit = c + m*Ta
resid = O3fit - O3
print('rms error',np.sqrt(np.mean((resid)**2)))
print('correlation',pearsonr(O3fit,O3))

############## multiple regression results ###################
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

## attributes and methods
import numpy as np
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


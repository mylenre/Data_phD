# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:45:14 2019

@author: s1995204
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.interpolate import interp1d # interpolation package


os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\Modeling_results\Solar_1D_models\input_files')

yr = np.loadtxt('paisleydata.txt', skiprows=7, usecols=0)  # first column 
month = np.loadtxt('paisleydata.txt', skiprows=7, usecols=1)
Tmax = np.loadtxt('paisleydata.txt', skiprows=7, usecols=2)
Tmin = np.loadtxt('paisleydata.txt', skiprows=7, usecols=3)
T = np.array([Tmin, Tmax])
Tavg=np.average(T, axis=0)

day = [1]*np.size(yr)
df = pd.DataFrame({'year': yr,
                   'month': month,
                   'day': day})
date = pd.to_datetime(df[["year", "month", "day"]])

plt.figure(figsize=(18,10))
plt.plot(date, Tavg)

# discretise 729 months in 22188 days
dt=np.arange(0, np.size(yr),1)
#dt_s=np.arange(0, 22188*24*3600,24*3600)

# discretise 729 months (1/01/1959-31/10/2019) in 22218 days
dt_s=np.arange(0, 22219*24*3600,24*3600)
points = np.array([dt,
                   Tavg]).T  

# Linear length along the line:
distance = np.cumsum(np.sqrt(np.sum( np.diff(points, axis=0)**2, axis=1 )))
distance = np.insert(distance, 0, 0)/distance[-1]

# Interpolation/day
#alpha = np.linspace(0, 1, 22188) 
alpha = np.linspace(0, 1, 22219) 

interpolated_points = {}
interpolator =  interp1d(distance, points, kind='cubic', axis=0)
interpolated_points['cubic'] = interpolator(alpha)

# Graph:
plt.figure(figsize=(18,10))
for method_name, curve in interpolated_points.items():
    plt.plot(*curve.T, '-', label=method_name);

plt.plot(*points.T, label='original points');
plt.legend(); plt.xlabel('time (s)'); plt.ylabel('temperature');

#save
data=np.array([dt_s,curve[:,1]])
data=data.T
#np.savetxt('curveT_corr.txt', data, fmt=['%i','%f'])
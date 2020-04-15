# -*- coding: utf-8 -*-
# https://ourcodingclub.github.io/2018/11/30/numpy.html

"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
# functions
def my_mean(x):
  total=0
  for i in range(len(x)):
      total = total + x[i]
  mean_value = total / len(x)
  return mean_value

#if loop
today='Thursday'
if today=='Friday':
  print("Why not go home early?")
else:
  print("Hard work is a virtue! You can do it! I believe in you!")
  
# packages: numpy, scipy, matplotlib
import numpy as np
x = [1,3,6,2,8,4,1]
# use "mean" and "standard deviation" functions of numpy (np)
x_mean = np.mean(x)
x_standard_dev = np.std(x)
#print the result
print(x_mean)
print(x_standard_dev)

# import data 
import pandas as pd
import matplotlib.pyplot as plt
import datetime

data = pd.read_csv('StormEleanor_2_3_Jan.csv', delimiter=',', header=0)
data = pd.read_csv('your_csv_file').values

pressure_data = data['Pair_Avg']

# timeseries
# Code to create the timeseries values
date_time_series = []
date_time = datetime.datetime(2018, 1, 2)
date_at_end = datetime.datetime(2018, 1, 3, 23, 59)
step = datetime.timedelta(minutes=1)

while date_time <= date_at_end:
  date_time_series.append(date_time)
  date_time += step

print(date_time_series)

# plot data
plt.plot(date_time_series, pressure_data)
plt.ylabel("Pressure (hPa)")
plt.xlabel("Time")
plt.title("Average Pressure, JCMB Weather Station, 2-3rd Jan 2018")
plt.xticks(rotation=-60)
plt.tight_layout()
plt.savefig("pressure_final.png")

#saving a file
np.savetxt('save_file.csv', your_data, delimeter=',', comments='')
# save one data to npy file
np.save('save_file1.npy' ,data)
# save collection of data to single npz file
dataset = {'temperature': data1,
		   'humidity': data2}
np.savez('save_file2.npz', **dataset)

# reopen files
open_data = np.load('save_file1.npy')
open_dataset = np.load('save_file2.npz')
# access data in dataset
temperature = open_dataset['temperature']

# create 3d array with dimensions (time, latitude, longitude)
a = np.zeros((3, 3, 3))
# create 4d array with dimensions (time, height, latitude, longitude)
b = np.zeros((3, 3, 3, 3))

# add 1 to the first columns
for i in [a, b]:
    dimensions = len(i.shape)
    if dimensions == 3:
        i[:, :, 0] += 1.
    elif dimensions == 4:
        i[:, :, :, 0] += 1.
        
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
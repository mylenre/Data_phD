# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 08:24:11 2020

@author: mylen
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os


os.chdir(r'D:\mylen\Documents\phD\Data_phD\Data\Paisley')


data = np.loadtxt('Tcomp.txt', skiprows=1,usecols=(2,3))  # all data
#date = data[:,0]  
Tair = data[:,0]  
Tsoil = data[:,1]

date_time_series = []
date_time = datetime.datetime(2000, 1, 1)
date_at_end = datetime.datetime(2000, 12, 31)
step = datetime.timedelta(days=1)

while date_time <= date_at_end:
  date_time_series.append(date_time)
  date_time += step


plt.figure(figsize=(15,10))
plt.rcParams['font.size'] = 10 
plt.plot(date_time_series, Tair, label="Air Temperature", linewidth=2)
plt.plot(date_time_series, Tsoil, label="Soil Temperature at 30 cm depth", linewidth=2)
plt.ylabel("Temperature (°C)")
plt.xlabel("Time")
plt.title('2000 daily air and soil temperature at the Paisley station')
plt.legend(loc='lower right')
plt.legend(fontsize=12) 

plt.savefig("Tcomp_Paisley.png") 
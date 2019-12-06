# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:12:50 2019

@author: s1995204
"""
import numpy as np
import matplotlib.pyplot as plt
import os


os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling\Modeling_results\Solar_1D_models\input_files')

time1 = np.loadtxt('curveT_corr.txt', usecols=0)  # first column 
T = np.loadtxt('curveT_corr.txt', usecols=1)

plt.figure(figsize=(18,10))
plt.plot(time1, T)


time2 = np.loadtxt('sinq_-8_8.txt', usecols=0)
q = np.loadtxt('sinq_-8_8.txt',  usecols=1)
plt.plot(time2, q)

q2=3.0 * (T-10)/3
q2_min = min(q2)
#q2 = q2 + abs(q2_min)
plt.plot(time1,q2)

data=np.stack((time1, q2), axis=-1)
np.savetxt('curveq_corr.txt', data)

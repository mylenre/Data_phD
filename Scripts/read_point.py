# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:34:26 2019

@author: s1995204
"""

import numpy as np
import matplotlib.pyplot as plt
plt.figure(figsize=(18,10))
t = np.loadtxt('M2_time_PROD.tec', skiprows=3, usecols=0)  
T = np.loadtxt('M2_time_PROD.tec', skiprows=3, usecols=1)
t=t[:]/(3600*24)
plt.plot(t,T)
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:57:11 2019

@author: s1995204
"""

import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

list = np.arange(0, 730,1)
# Define some points:
points = np.array([listdate,
                   Tavg]).T  # a (nbre_points x nbre_dim) array

# Linear length along the line:
distance = np.cumsum( np.sqrt(np.sum( np.diff(points, axis=0)**2, axis=1 )) )
distance = np.insert(distance, 0, 0)/distance[-1]

# Interpolation for different methods:
alpha = np.linspace(0, 1, 22188)

interpolated_points = {}
interpolator =  interp1d(distance, points, kind='cubic', axis=0)
interpolated_points['cubic'] = interpolator(alpha)

# Graph:
plt.figure(figsize=(20,10))
for method_name, curve in interpolated_points.items():
    plt.plot(*curve.T, '-', label=method_name);

plt.plot(*points.T, label='original points');
plt.axis('equal'); plt.legend(); plt.xlabel('x'); plt.ylabel('y');
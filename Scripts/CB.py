# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 21:04:54 2020

@author: s1995204
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
os.chdir(r'\\students.geos.ed.ac.uk\s1995204\Documents')
store= {}

filename='Canterbury_Basin.csv'
print(filename)
data = pd.read_csv(filename, delimiter=',', header=0)

liste = np.arange(0.125,max(data.x),0.25)
for t in liste:
    tmin = t - 0.125
    tmax = t + 0.215
    i=data[(data['x'] < tmax) & (data['x'] > tmin)]
    val = i.y 
    pal = i.x
    operation = val.sum(skipna = True)/pal.sum(skipna = True) # remplacer par calcul que tu veux faire
    store[t] = operation


lists = sorted(store.items()) # sorted by key, return a list of tuples
x, y = zip(*lists) # unpack a list of pairs into two tuples
plt.figure(figsize=(8,4))
plt.plot(x, y, 'o--')
plt.title('wah cest trop beau')
plt.xlabel('truc 1')
plt.ylabel('truc 2')
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 16:37:11 2020

@author: s1995204
"""
import os
import pandas as pd
import numpy as np
os.chdir(r'R:\Data\Data_GIS')
data = pd.read_csv('Underground_coal_workings.csv', delimiter=',', header=0)
seam = {}
code= data['SE_CODE']
n= set()
for i in code:
    n.add(i)
for i in n:
    print(i)
    select =  data.loc[data['SE_CODE'] == i]
    seam[i]= select
    select.to_csv(i+'.txt', index=None)
   # np.savetxt(i+'.txt', select.values, fmt='%d %s %d %s %s %s %d %d %d', delimiter='\t'')
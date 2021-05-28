# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 14:57:55 2020

@author: s1995204
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from itertools import chain

plt.style.use('seaborn')
colormap = np.array(['teal', 'darkslategray', 'royalblue', 'navy', 'goldenrod', 'palevioletred', 'green', 'black','rosybrown','steelblue'])

os.chdir(r'R:\Data\Data_GIS\CoalAuthority_Data\Mine_Data')
df=pd.read_csv('pannels_bilston_glen.txt', delimiter=',', index_col=0)
df['vol_pannel'] = np.array(df['area']) * np.array(df['SE_THKNS'])
df['true_vol_pannel'] = np.array(df['area'])/abs(np.cos(np.array(df['DIP_RATE']))) * np.array(df['SE_THKNS'])
mine = pd.DataFrame()
mine['area'] = df['area'].groupby(df['COLLIERY']).sum()
mine['volume'] = df['vol_pannel'].groupby(df['COLLIERY']).sum()
mine['true_volume'] = df['true_vol_pannel'].groupby(df['COLLIERY']).sum()
mine['scaled_true_volume'] = mine['true_volume'] * 0.25

seam = pd.DataFrame()
seam['area'] = df['area'].groupby(df['SE_CODE']).sum()
seam['volume'] = df['vol_pannel'].groupby(df['SE_CODE']).sum()
seam['true_volume'] = df['true_vol_pannel'].groupby(df['SE_CODE']).sum()
seam['scaled_true_volume'] = seam['true_volume'] * 0.25


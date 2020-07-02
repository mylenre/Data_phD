# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 07:45:39 2020

@author: s1995204
"""

import numpy as np
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d # interpolation package
import seaborn as sns
sns.set()
col = ["k","y","g","b","c","m","r"]


os.chdir(r'R:\Modeling\Heat_Extraction_Paper\Steady_state\Analysis\1_year')

#variables
BHEt=50
BHEb=90

filelist=glob.glob('*.txt')
l = np.size(filelist)
d=[]
rows = np.arange(0,1000.1,0.1)
rows = [round(num, 1) for num in rows]
df = pd.DataFrame(rows)
df = df.rename(columns={0: 'ZONE'})
#df = df.set_index('ZONE')


fig, ax = plt.subplots(figsize=(8,5))
for i in filelist:
    print(i)
    name= i.split('.')[0]
    id=filelist.index(i)
    data = pd.read_csv(i, delimiter=',', header=0) 
    time = data.columns[1]
    data = data.rename(columns={time: 'T'})
    data['ZONE'].round(decimals=1)

    # Interpolate
    if name == '3D':
        interval = np.arange(0,150,0.1)
        interval = [round(num, 1) for num in interval]
        f = interp1d(data['ZONE'],data['T'])
        T_3D = f(interval)
        data_new = pd.DataFrame(list(zip(interval, T_3D)), columns =['ZONE', 'T']) 
        data_new['ZONE'].round(decimals=1)
    elif name == '3D_BHE':
        interval2 = np.arange(BHEt,BHEb,0.1)
        interval2 = [round(num, 1) for num in interval2]
        f2 = interp1d(data['ZONE'],data['T'])
        T_3D2 = f2(interval2)
        data_new = pd.DataFrame(list(zip(interval2, T_3D2)), columns =['ZONE', 'T']) 
        data_new['ZONE'].round(decimals=1)
    else:
        data_new = data
    ax.plot(data_new['ZONE'], data_new['T'],label = name, color=col[id], lw=3)
    d = pd.merge(df, data_new, on='ZONE', how='left')
    df[name] = d['T']
plt.axvline(x=15, ymin=0, ymax=0.3, linewidth=1, color='k', ls='--')
plt.axvline(x=BHEt, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
plt.axvline(x=BHEb, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
ax.set(xlabel="Distance along profile",
       ylabel="Temperature",
       title="Temperature along profile after 1 year production")
plt.axis((0,200,2,18))
plt.legend(loc='best')
plt.savefig('Temp_profile.png')

v0 = df['Steady_state']
v1 = df['1D_CF']
v2 = df['1D_CT']
v3 = df['1D_CF_BHE'] #.fillna(0)
v4 = df['3D']
v5 = df['3D_BHE']
solar_recharge = v2 - v1
axial = v1 - v3
lateral = v5 - v3
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(d['ZONE'], solar_recharge, 'g',lw=3, label = 'solar effects')
ax.plot(d['ZONE'], axial, 'y', lw=3,label = 'axial effects')
ax.plot(d['ZONE'], lateral, 'c', lw=3, label = 'lateral effects')
plt.axvline(x=BHEt, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
plt.axvline(x=BHEb, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
plt.axvline(x=32.7, ymin=0, ymax=0.08, linewidth=1, color='k', ls='--')
ax.set(xlabel="Distance along profile",
       ylabel="Temperature differences",
       title="Temperature differences along profile after 30 years production. \n  \n Solar effects is the difference in temperature along the vertical profile if constant temperature vs constant flux  boundary conditions are used. \n Axial effects represents the temperature difference along the 22000 m2 BHE if a rock column is available above/below and if not (BHE height = 2200m). \n Lateral effects represents the temperature difference between a profile situated at 26.5m from the BHE (3D model) and along the 2200m2 BHE (1D model).")
plt.axis((0,200,-0.2,7))
plt.legend(loc='best')
plt.savefig('Temp_diff.png')

BHEtx=BHEt * 10
BHEbx=BHEb * 10

#integrated temperature change
T1D_BHE = round(np.sum((v0-v3)),3)
T1D = round(np.sum((v0-v1)),3)
T1D_zoom = round(np.sum((v0[BHEtx:BHEbx]-v1[BHEtx:BHEbx])),3)
axial_recharge_1D = T1D_BHE-T1D_zoom
percentage_axial_recharge_1D = round(axial_recharge_1D/T1D_BHE*100,1)
T3D_BHE = round(np.sum((v0-v5)),3)
lateral_recharge = T1D_BHE-T3D_BHE
percentage_lateral_recharge = round(lateral_recharge/T1D_BHE*100,1)
T3D = round(np.sum((v0-v4)),3)
T3D_zoom = round(np.sum((v0[BHEtx:BHEbx]-v4[BHEtx:BHEbx])),3)
axial_recharge_3D = T3D_BHE-T3D_zoom
percentage_axial_recharge_3D = round(axial_recharge_3D/T3D_BHE*100,1)

#print('Integrated temperature difference along profile after 1 years of production, for: \n a 1D rock column (70 m2) with infinite vertical recharge (no lateral recharge): ' + str(T1D) + ', \n a 1D rock column (70 m2) of BHE height ('+str(BHEb-BHEt) + ' m): ' + str(T1D_BHE) + ', \n at 4.5m from the BHE for an infinite 3D rock volume (lateral and vertical recharge): ' + str(T3D)+ '\n and at 4.5m from the BHE for a volume with lateral recharge only: ' + str(T3D_BHE))
#print('In those models, only the geothermal flux contribute to recharge, as steady state gradient and heat comes from below (explain the cooling at the surface).')
print('Integrated temperature difference along profile after 30 years of production, for: \n a 1D rock column (2200 m2) with infinite vertical recharge (no lateral recharge): ' + str(T1D) + ', \n a 1D rock column (2200 m2) of BHE height ('+str(BHEb-BHEt) + ' m): ' + str(T1D_BHE) + ', \n at 26.5m from the BHE for an infinite 3D rock volume (lateral and vertical recharge): ' + str(T3D)+ '\n and at 26.5m from the BHE for a volume with lateral recharge only: ' + str(T3D_BHE))
print('In those models, only the geothermal flux contribute to recharge, as steady state gradient and heat comes from below (explain the cooling at the surface).')
print('Percentage axial recharge (1D) : ' + str(percentage_axial_recharge_1D) + '%')
print('Percentage lateral recharge : ' + str(percentage_lateral_recharge) + '%')
print('Percentage axial recharge (3D) : ' + str(percentage_axial_recharge_3D) + '%')

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
#col = ["c","b","y","r","g","k","m","b"]


os.chdir(r'S:\Modeling\1D_Models\3_Heat_extraction_new_areas\100m_BHE_30m2_deep\3_results')

#variables
BHEt=input("enter BHE top depth : ") 
BHEb=input("enter BHE bottom depth : ") 
BHEt = eval(BHEt)
BHEb=eval(BHEb)
BHEtx=BHEt * 10
BHEbx=BHEb * 10

filelist=glob.glob('*.txt')
l = np.size(filelist)
d=[]
rows = np.arange(0,1000.1,0.1)
rows = [round(num, 1) for num in rows]
df = pd.DataFrame(rows)
df = df.rename(columns={0: 'ZONE'})
#df = df.set_index('ZONE')


for i in filelist:
    print(i)
    name= i.split('.')[0]
    id=filelist.index(i)
    data = pd.read_csv(i, delimiter=',', header=0) 
    time = data.columns[1]
    data = data.rename(columns={time: 'T'})
    data['ZONE'].round(decimals=1)
  
    # take mean value if several value per depth
    if 'x=0' in name:
        data = data.groupby('ZONE',as_index=False).mean()
        
    # Interpolate
    if '3D_SI' in name:
        interval = np.arange(0,160.1,0.1)
        interval = [round(num, 1) for num in interval]
        f = interp1d(data['ZONE'],data['T'],bounds_error=False)
        Tf = f(interval)  
        data_new = pd.DataFrame(list(zip(interval, Tf)), columns =['ZONE', 'T'])
        data_new['ZONE'].round(decimals=1)
    if '3D_F' in name:
        data['ZONE']=data['ZONE']
        interval = np.arange(BHEt,BHEb,0.1)
        interval = [round(num, 1) for num in interval]
        f = interp1d(data['ZONE'],data['T'],bounds_error=False,fill_value = 'nan')
        Tf = f(interval)  
        data_new = pd.DataFrame(list(zip(interval, Tf)), columns =['ZONE', 'T'])
        data_new['ZONE'].round(decimals=1)
    if '1D' in name: 
        data_new = data
    d = pd.merge(df, data_new, on='ZONE', how='left')
    df[name] = d['T']


#%% profiles
r=2000
plt.figure(figsize=(8,8))

e1 = input("enter x1 value : ") 
e2 = input("enter x2 value : ") 
xmin = np.nanmin(df['3D_F_t30_x=0'])

plt.subplot(2,2,1)
plt.plot(df['1D_SI_t0'][0:r], -df['ZONE'][0:r], label = 'Steady State', color='k', lw=1)
plt.plot(df['1D_SI_t1'][0:r], -df['ZONE'][0:r], label = 'Axial recharge', color='c', lw=1)
plt.plot(df['1D_F_t1'][0:r], -df['ZONE'][0:r], label = 'BHE', color='darkblue', lw=1)
plt.axis([xmin, 14, -200 , 0])
plt.title('a) 1-year profiles (1D)')
#plt.xlabel("Distance along profile")
plt.ylabel("Temperature (°C)")
plt.axhline(y=-BHEt, linewidth=1, color='k', ls='--')
plt.axhline(y=-BHEb, linewidth=1, color='k', ls='--')
plt.legend(loc='best')

plt.subplot(2,2,2)
plt.plot(df['3D_SI_t0'],  -df['ZONE'], label = 'Steady State', color='k')
plt.plot(df['3D_SI_t1_x=0'], -df['ZONE'], label = 'Axial recharge, x = 0 m', color='indianred')
plt.plot(df['3D_SI_t1_x='+e1], -df['ZONE'], label = 'Axial recharge, x = 3 m', color='c')
plt.plot(df['3D_F_t1_x=0'], -df['ZONE'], label = 'BHE, x = 0 m', color='brown')
plt.plot(df['3D_F_t1_x='+e1], -df['ZONE'], label = 'BHE, x = 3 m', color='darkblue')
plt.axis([xmin, 14, -200 , 0])
plt.title('b) 1-year profiles (3D)')
#plt.xlabel("Distance along profile")
#plt.ylabel("Temperature")
plt.axhline(y=-BHEt, linewidth=1, color='k', ls='--')
plt.axhline(y=-BHEb, linewidth=1, color='k', ls='--')
plt.legend(loc='best')

plt.subplot(2,2,3)
plt.plot(df['1D_SI_t0'][0:r], -df['ZONE'][0:r], label = 'Steady State', color='k', lw=1)
plt.plot(df['1D_SI_t30'][0:r], -df['ZONE'][0:r], label = 'Axial recharge', color='c', lw=1)
plt.plot(df['1D_F_t30'][0:r], -df['ZONE'][0:r], label = 'BHE', color='darkblue', lw=1)
plt.axis([xmin, 14, -200 , 0])
plt.title('c) 30-year profiles (3D)')
plt.xlabel("Distance along profile (m)")
plt.ylabel("Temperature (°C)")
plt.axhline(y=-BHEt, linewidth=1, color='k', ls='--')
plt.axhline(y=-BHEb, linewidth=1, color='k', ls='--')
plt.legend(loc='best')

plt.subplot(2,2,4)
plt.plot(df['3D_SI_t0'], -df['ZONE'], label = 'Steady State', color='k')
plt.plot(df['3D_SI_t30_x=0'], -df['ZONE'], label = 'Axial recharge, x = 0 m', color='indianred')
plt.plot(df['3D_SI_t30_x='+e2], -df['ZONE'], label = 'Axial recharge, x = 17 m', color='c')
plt.plot(df['3D_F_t30_x=0'], -df['ZONE'], label = 'BHE, x = 0 m', color='brown')
plt.plot(df['3D_F_t30_x='+e2], -df['ZONE'], label = 'BHE, x = 17 m', color='darkblue')
plt.axis([xmin, 14, -200 , 0])
plt.title('d) 30-year profiles (3D)')
plt.xlabel("Distance along profile (m)")
#plt.ylabel("Temperature")
plt.axhline(y=-BHEt, linewidth=1, color='k', ls='--')
plt.axhline(y=-BHEb, linewidth=1, color='k', ls='--')
plt.legend(loc='best')

plt.tight_layout()
plt.savefig('profiles_v2.png')

#%% profiles
r=2000
plt.subplot(2,2,1)
plt.plot(df['1D_SI_t0'][0:r], df['ZONE'][0:r],label = 'Steady State', color='k', lw=1)
plt.plot(df['1D_SI_t1'][0:r], df['ZONE'][0:r],label = 'Axial recharge', color='c', lw=1)
plt.plot(df['1D_F_t1'][0:r], df['ZONE'][0:r],label = 'BHE', color='darkblue', lw=1)
plt.title('Temperature profile after 1 year (1D)')
plt.xlabel("Distance along profile")
plt.ylabel("Temperature")
plt.axvline(x=BHEt, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
plt.axvline(x=BHEb, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
plt.legend(loc='best')

plt.subplot(2,2,2)
plt.plot(df['3D_SI_t0'], df['ZONE'], label = 'Steady State', color='k')
plt.plot(df['3D_SI_t1_x=0'], df['ZONE'], label = 'Axial recharge, x = 0 m', color='indianred')
plt.plot(df['3D_SI_t1_x=8'], df['ZONE'], label = 'Axial recharge, x = 8 m', color='c')
plt.plot(df['3D_F_t1_x=0'], df['ZONE'], label = 'BHE, x = 0 m', color='brown')
plt.plot(df['3D_F_t1_x=8'], df['ZONE'], label = 'BHE, x = 8 m', color='darkblue')
plt.title('Temperature profile after 1 year (3D)')
plt.xlabel("Distance along profile")
plt.ylabel("Temperature")
plt.axvline(x=BHEt, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
plt.axvline(x=BHEb, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
plt.legend(loc='best')

plt.subplot(2,2,3)
plt.plot(df['1D_SI_t0'][0:r], df['ZONE'][0:r],label = 'Steady State', color='k', lw=1)
plt.plot(df['1D_SI_t30'][0:r], df['ZONE'][0:r],label = 'Axial recharge', color='c', lw=1)
plt.plot( df['1D_F_t30'][0:r], df['ZONE'][0:r],label = 'BHE', color='darkblue', lw=1)
plt.title('Temperature profile after 30 years (1D)')
plt.xlabel("Distance along profile")
plt.ylabel("Temperature")
plt.axvline(x=BHEt, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
plt.axvline(x=BHEb, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
plt.legend(loc='best')

plt.subplot(2,2,4)
plt.plot(df['3D_SI_t0'], df['ZONE'],label = 'Steady State', color='k')
plt.plot(df['3D_SI_t30_x=0'], df['ZONE'],label = 'Axial recharge, x = 0 m', color='indianred')
plt.plot(df['3D_SI_t30_x=8'], df['ZONE'],label = 'Axial recharge, x = 8 m', color='c')
plt.plot(df['3D_F_t30_x=0'], df['ZONE'],label = 'BHE, x = 0 m', color='brown')
plt.plot(df['3D_F_t30_x=8'], df['ZONE'],label = 'BHE, x = 8 m', color='darkblue')
plt.title('Temperature profile after 30 years (3D)')
plt.xlabel("Distance along profile")
plt.ylabel("Temperature")
plt.axvline(x=BHEt, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
plt.axvline(x=BHEb, ymin=0, ymax=1, linewidth=1, color='k', ls='--')
plt.legend(loc='best')

plt.tight_layout()
plt.savefig('profiles.png')
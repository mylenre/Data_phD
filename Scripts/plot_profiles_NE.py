# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 10:45:22 2020

@author: s1995204
"""
well = {}
welltime = {}
time={}
temp={}

import numpy as np
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d # interpolation package
import seaborn as sns
sns.set()


os.chdir(r'R:\GitHub\Data_phD\Scripts\Dawdon')
filelist=glob.glob('*.txt')
l = np.size(filelist)

# import insets
inset = pd.read_csv('Inset.csv', delimiter=',', header=0, index_col=0)

############################## IMPORT DATA############################333  
for i in filelist:
    print(i)
    name= i.split('_')[0]
    year=i.replace(".","_").split('_')[1]
    id=filelist.index(i)
    data = pd.read_csv(i, delimiter=',', header=0)
    data['D'].round(decimals=1)
    f = interp1d(data['D'],data['T'],bounds_error=False,fill_value = 'nan')
    interval = np.arange(-500,0,0.1)
    Tbis = f(interval)
    data_new = pd.DataFrame(list(zip(interval, Tbis)), columns =['D', 'T']) 
        
# Here: fill the dictionary with name of wells where profile is available that year
    if year not in time:
        time[year]= [name]
    else:
        time[year].append(name)
# Here, add Dataframe itself
    if year not in temp:
        temp[year] = [data_new]
    else:
        temp[year].append(data_new) 
# SAME FOR PROFILES PER WELL   
    if name not in welltime:
        welltime[name] = [year]
    else:
        welltime[name].append(year)
   
    if name not in well:
        well[name] = [data_new]
    else:
        well[name].append(data_new)
           
colors = {'Dawdon': 'b', 'Easington': 'r', 'Hawthorn':'g', 'Horden':'k'}
date=['2000','2003','2005','2008']
wells = ['Dawdon', 'Easington', 'Hawthorn', 'Horden']
# %% ####################### PLOT PROFILE PER DATES################################

plt.figure(figsize=(30,8))
for i in range(4):
    plt.subplot(1,4,i+1)
    for j in range(len(temp[date[i]])):
        print(time[date[i]][j])
        plt.plot(temp[date[i]][j]['T'],temp[date[i]][j]['D'], c = colors[time[date[i]][j]],  label=time[date[i]][j])
    plt.xlabel('Temperature')
    plt.ylabel('Depth')
    plt.title('Temperature profile '+str(date[i]) )    
    plt.legend()


# %%  ######################## PLOT PROFILES PER WELLS###########################

plt.figure(figsize=(30,8))
for i in range(4):
    plt.subplot(1,4,i+1)
    for j in range(len(well[wells[i]])):
        print(welltime[wells[i]][j])
        plt.plot(well[wells[i]][j]['T'],well[wells[i]][j]['D'],  label=welltime[wells[i]][j])
    for k in range(len(inset)):
        plt.axhline(y=inset[wells[i]][k], xmin=0, xmax=1,linewidth=1, color='k', ls='--')#,label=inset.index[k])
        plt.text(12, inset[wells[i]][k], inset.index[k])
    plt.xlabel('Temperature')
    plt.ylabel('Depth')
    plt.title('Temperature profile '+wells[i])    
    plt.legend()

#In case I want to plot temperature profiles per well:   
#         for k in range(len(inset)):
#            plt.axhline(y=inset[time[date[i]][j]][k], xmin=0.6, xmax=1,linewidth=1, color='k', ls='--') #label=inset.index[k]
#            print(inset[time[date[i]][j]][k])


# %%  ######################   #CALCULATE DIFFERENCES ############################
        
D2000 = temp['2000'][0]
D2003 = temp['2003'][0]
D2004 = temp['2004'][0]
D2005 = temp['2005'][0]
D2006 = temp['2006'][0]
D2008 = temp['2008'][0]

E2000 = temp['2000'][1]
E2005 = temp['2005'][1]
E2006 = temp['2006'][1]
E2008 = temp['2008'][1]

HA2000 = temp['2000'][2]
HA2003 = temp['2003'][1]
HA2005 = temp['2005'][2]
HA2006 = temp['2006'][2]
HA2008 = temp['2008'][2]

HO2003 = temp['2003'][2]
HO2004 = temp['2004'][1]
HO2005 = temp['2005'][3]
HO2006 = temp['2006'][3]
HO2008 = temp['2008'][3]

D1 = D2008 - D2006
D2 = D2006 - D2005
D3 = D2005 - D2004
D4 = D2004 - D2003
D5 = D2003 - D2000

E1 = D2008 - D2006
E2 = D2006 - D2005
E3 = D2005 - D2000

HA1 = HA2008 - HA2006
HA2 = HA2006 - HA2005
HA3 = HA2005 - HA2003
HA4 = HA2003 - HA2000

HO1 = HO2008 - HO2006
HO2 = HO2006 - HO2005
HO3 = HO2005 - HO2004
HO4 = HO2004 - HO2003

plt.figure(figsize=(30,8))
plt.subplot(1,4,1)
plt.plot(D1['T'], temp[date[0]][0]['D'], c = 'Navy',  label='2008-2006')
plt.plot(D2['T'], temp[date[0]][0]['D'], c = 'RoyalBlue',  label='2006-2005')
plt.plot(D3['T'], temp[date[0]][0]['D'], c = 'MediumSlateBlue',  label='2005-2004')
plt.plot(D4['T'], temp[date[0]][0]['D'], c = 'PaleTurquoise',  label='2004-2003')
plt.plot(D5['T'], temp[date[0]][0]['D'], c = 'Cyan',  label='2003-2000')
for k in range(len(inset)):
    plt.axhline(y=inset['Dawdon'][k], xmin=0, xmax=1,linewidth=1, color='k', ls='--')#,label=inset.index[k])
    plt.text(1, inset['Dawdon'][k], inset.index[k])
plt.xlabel('Temperature')
plt.ylabel('Depth')
plt.title('Temperature profile Dawdon ' )    
plt.legend()

plt.subplot(1,4,2)
plt.plot(E1['T'],temp[date[0]][0]['D'], c = 'DarkRed',  label='2008-2006')
plt.plot(E2['T'],temp[date[0]][0]['D'], c = 'Red',  label='2006-2005')
plt.plot(E3['T'],temp[date[0]][0]['D'], c = 'LightCoral',  label='2005-2000')
for k in range(len(inset)):
    plt.axhline(y=inset['Easington'][k], xmin=0, xmax=1,linewidth=1, color='k', ls='--')#,label=inset.index[k])
    plt.text(1, inset['Easington'][k], inset.index[k])
plt.xlabel('Temperature')
plt.ylabel('Depth')
plt.title('Temperature profile Easington ' )    
plt.legend()
    

plt.subplot(1,4,3)
plt.plot(HA1['T'], temp[date[0]][0]['D'],c = 'DarkGreen',  label='2008-2006')
plt.plot(HA2['T'],temp[date[0]][0]['D'], c = 'DarkSeaGreen',  label='2006-2005')
plt.plot(HA3['T'],temp[date[0]][0]['D'], c = 'MediumAquamarine',  label='2005-2003')
plt.plot(HA4['T'],temp[date[0]][0]['D'], c = 'GreenYellow',  label='2003-2000')
for k in range(len(inset)):
    plt.axhline(y=inset['Hawthorn'][k], xmin=0, xmax=1,linewidth=1, color='k', ls='--')#,label=inset.index[k])
    plt.text(1, inset['Hawthorn'][k], inset.index[k])
plt.xlabel('Temperature')
plt.ylabel('Depth')
plt.title('Temperature profile Hawthorn ' )    
plt.legend()
    

plt.subplot(1,4,4)
plt.plot(HO1['T'],temp[date[0]][0]['D'], c = 'k',  label='2008-2006')
plt.plot(HO2['T'],temp[date[0]][0]['D'], c = 'Grey',  label='2006-2005')
plt.plot(HO3['T'],temp[date[0]][0]['D'], c = 'LightGrey',  label='2005-2004')
plt.plot(HO4['T'],temp[date[0]][0]['D'], c = 'White',  label='2004-2003')
for k in range(len(inset)):
    plt.axhline(y=inset['Horden'][k], xmin=0, xmax=1,linewidth=1, color='k', ls='--')#,label=inset.index[k])
    plt.text(1, inset['Horden'][k], inset.index[k])
plt.xlabel('Temperature')
plt.ylabel('Depth')
plt.title('Temperature profile Horden ' )    
plt.legend()
    
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 23:27:01 2021

@author: s1995204
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
plt.style.use('seaborn')

# collect LOG data
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\LOGS\GEOINDEX\files')
filelist=glob.glob('*.txt')
log = []
total = {}


structure = {'MONKTONHOUSEBORE37':{'cms':[0,330],'pgp':[330,521], 'ulcs':[521,790], 'lcs':[790,10000]},
             'SPILMERSFORD': {'llcs':[0,22],'wlo':[22,128], 'gul':[128,287], 'art':[287,660],'inv':[660,10000]},
             'SALSBURGH':{'ulcs':[0,322], 'lcs':[322,526],'llcs':[526,632], 'wlo':[632,1113], 'art':[1113,1215]},
             'PUMPHERSTON': {'wlo':[0,65], 'gul':[65,903],'inv':[903,10000]},
             'MACKIES_MILL':{'cms':[0,330],'pgp':[330,521], 'ulcs':[521,790], 'lcs':[790,1000]}, 
             'LADY_VICT':{'lcs':[0,10000]},
             'BATES':{'cms':[0,10000]},
             'CHATERSHAUGH':{'cms':[0,10000]},
             'EASINGTON':{'cms':[0,10000]},
             'HAWTHORN':{'cms':[0,10000]},
             'ELDON':{'cms':[0,10000]},
             'HOUGHTON':{'cms':[0,10000]},
             'LADYSMITH':{'cms':[0,10000]},
             'LUMLEY6':{'cms':[0,10000]},
             'WESTOE':{'cms':[0,10000]}}
 
for i in filelist:
    name = i.split('.')[0]
    #print(name)
    df = pd.read_csv(i, delimiter=',',usecols=[0,1,2,3])
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].str.lower()
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("arkose","conglomerate")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("calcite","limestone")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("cannel","coal")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("ribs ","coal")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("ribs","coal")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("rib","coal")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("bbi","coal")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("cementstone","limestone")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("chert","sandstone")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("fakes","shale")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("blaes","shale") #!!! I have converted some of the blaes in sandstone in my ealy times of file processing!!!
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("haematite","ironstone")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("lava","basalt")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("marl","mudstone")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("mudatone","mudstone")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("breccia","conglomerate")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("seatearth","seatclay")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("seatrock","seatclay")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("clayrock","clay")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("soil","sand")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("tuff","basalt")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("agglomerate","basalt")
    
    thick = df['Thickness'].sum()
    tot = df['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/thick
    total[name] = tot

    if name in structure :
        print(i) 
        for j in structure[name]:
            print(j)
            formation = []
            borehole = []
            thick = df[(df['Depth'] > structure[name][j][0]) & (df['Depth'] < structure[name][j][1])]['Thickness'].sum()
            select = df[(df['Depth'] > structure[name][j][0]) & (df['Depth'] < structure[name][j][1])]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/thick
            select = pd.DataFrame(select)
            select.reset_index(inplace=True)
            for k in range(len(select)):
                formation.append(j)
                borehole.append(name)
            formation = pd.DataFrame(formation, columns=['fm'])
            borehole = pd.DataFrame(borehole, columns=['bh'])
            select["formation"]=formation
            select["borehole"]=borehole
            log.append(select)
            log_stacked = pd.concat([r for r in log], ignore_index=True)


#%% rock properties
rock = np.unique(log_stacked['NATURE OF STRATA'])

#add conductivities, density, heat capacity, diffusivity, rhp (W/m3)
properties =  {'agglomerate':[1.8,840,3000,7.14286E-07,8.96E-07],
'basalt':[1.8,840,3000,7.14286E-07,5.40E-07],
'clay':[1.11,860,1900,6.79315E-07,1.90E-06],
'clayrock':[1.11,920,2450,4.92458E-07,1.90E-06],
'coal':[0.4,1300,1350,2.2792E-07,5.00E-07],
'conglomerate':[2.74,930,2460,1.19766E-06,8.96E-07],
'dolerite':[1.81,858,2870,7.35037E-07,5.40E-07],
'dolomite':[3.94,920,2850,1.50267E-06,7.80E-07],
'fireclay':[0.59,920,2450,2.61757E-07,1.90E-06],
'ironstone':[2.85,880,2760,1.17342E-06,7.00E-07],
'limestone':[2.85,880,2760,1.17342E-06,2.07E-06],
'mudstone':[1.41,770,2600,7.04296E-07,1.39E-06],
'no core':[0.59,4185,1000,1.4098E-07,0.00E+00],
'ribs':[0.4,1300,1350,2.2792E-07,5.00E-07],
'sand':[0.77,860,1900,4.71236E-07,1.70E-06],
'sandstone':[4.54,930,2460,1.98444E-06,8.96E-07],
'seatclay':[2.42,860,2380,1.18233E-06,1.90E-06],
'shale':[1.3,390,2600,1.28205E-06,2.90E-06],
'siltstone':[1.84,910,2680,7.54469E-07,1.39E-06],
'soil':[0.77,860,1900,4.71236E-07,0.0000017],
'trachyte':[5.21,840,2440,2.54196E-06,0.0000032],
'tuff':[2.15,200,1500,7.16667E-06,0.0000032]}

properties = pd.DataFrame(properties).T
properties.columns=['cond','hc','rho','a','rhp']
#%%
colormap = {'limestone':'mediumturquoise', 'mudstone':'rosybrown',
                'no core':'green', 'sand':'gold', 'sandstone':'sandybrown',
                'seatclay':'gray', 'siltstone':'saddlebrown','coal':'black', 
                'ironstone':'darkmagenta', 'basalt': 'darkslategray', 
                'conglomerate':'goldenrod', 'fireclay':'firebrick', 
                'clay':'darkcyan', 'dolerite':'palevioletred', 
                'shale':'purple', 'trachyte':'indigo', 'dolomite':'cyan'}

#for k in structure.keys():
#    well = log_stacked[log_stacked['borehole']==k]
#    col = list(well['NATURE OF STRATA'].apply(lambda x: colormap[x]))
#    sns.catplot(x='formation', y='Thickness', hue='NATURE OF STRATA', data=well, kind='bar', palette = 'tab20') #palette=col )

averages_fm = {}
for name in structure.keys():
    well = log_stacked[log_stacked['borehole']== name]
    well1 = well.pivot(index='formation', columns='NATURE OF STRATA', values='Thickness')
    well1.plot(kind='bar', stacked=True, color = [colormap[i] for i in well1.columns] )
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.title('Percentage rock type for each formation at ' + str(name))
    plt.ylabel('Percentage')
    plt.tight_layout ()
    
    well2 = well.pivot(index='NATURE OF STRATA', columns='formation', values='Thickness')
    cond = well2.mul(properties['cond'], axis='index').sum(axis = 0)/100
    rhp = well2.mul(properties['rhp'], axis='index').sum(axis = 0)/100
    merged = pd.merge(pd.DataFrame(cond), pd.DataFrame(rhp), how ='outer', left_index=True, right_index=True) 
    merged.columns=['cond','rhp']
    averages_fm[name] = merged

averages_tot = []
for name2 in total.keys():
    cond = total[name2].mul(properties['cond'], axis='index').sum(axis = 0)/100
    rhp = total[name2].mul(properties['rhp'], axis='index').sum(axis = 0)/100
    averages_tot.append([name2, cond, rhp])
averages_tot = pd.DataFrame(averages_tot, columns=['borehole','cond','rhp'])
averages_tot = averages_tot.set_index(['borehole'])
#%% temperatures
temperatures={'AUCHENNIDY':[459,18,19.6],
              'BILSTON_GLEN':[670,15,8.7],
              'EASTHOUSES':[670,15,8.7], #Bilston Glen
              'FRANCES':[841,29.0,23.8],
              'HALLSIDE':[350,11.8,6],
              'LADY_VICT':[768,18,10.8],
              'LOCHHEAD':[1167,30.4,17.7],
              'RANDOLPH':[1167,30.4,17.7], #Lochhead
              'MACKIES_MILL':[960,33.3,24.6],
              'MONKTONHALLBORE37':[866,25.5,18.2],
              'SHERIFFALL':[866,25.5,18.2], #Moncktonhall
              'SALSBURGH':[874,29,24.1],
              'SPILMERSFORD':[877,27.8,20.9],
              'THORNTON_BRIDGE':[665,28.0,27.5],
              'THORNTON_FARM':[1055,38,26.8],
              'PUMPHERSTON':[1175,36.7,23.3],
              'QUEENSLIE':[691,36,38.4],
              'SEAFIELD':[789,29,25.3],
              'WELLSGREEN':[1485,42.3,22.0],
              'CAMERON':[1485,42.3,22.0], #Wellsgreen
              'BATES':[197,16.1,34.6], #North Seaton 
              'DAWDON':[529, 25, 29.7], #South Hetton
              'EASINGTON':[529, 25, 29.7],#South Hetton
              'HORDEN':[529, 25, 29.7],#South Hetton
              'HAWTHORN':[529, 25, 29.7],#South Hetton
              'ELDON':[100,10.6,31],
              'LADYSMITH':[100,10.6,31],
              'THRISLINGSTON':[100,10.6,31],
              'LUMLEY6':[100,15.4,14],
              'CHATERSHAUGH':[100,15.4,14], #Lumley
              'HOUGHTON':[100,15.4,14], #Lumley
              'WESTOE':[100,15.6,40.75],
              'WHITBURN':[100,15.6,40.75], #Westoe             
              'GLENROTH':[279,14.4,28.1],
              'BORELAND':[1007,29.8,20.1],
              'CLACHIE-BRIDGE':[600,13.2,16],  #23°C/km
              'HURLET':[295,15.6,22.86],
              'MARYHILL':[303,20,34] #36 °C/km
              }

temperatures = pd.DataFrame(temperatures).T
temperatures.columns=['depth','temperature','gradient']

data = averages_tot.merge(temperatures, how = 'inner', left_index = True, right_index = True)

plt.figure(figsize=(8,6))
plt.subplot(2,1,1)
plt.scatter(data['cond'], data['gradient'], c='b', label=list(data.index))
for label,x,y in zip(list(data.index), data['cond'], data['gradient']):
    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center
plt.xlabel('rock conductivity')
plt.ylabel('temperature gradient')

plt.subplot(2,1,2)
plt.scatter(data['rhp'], data['gradient'], c='r', label=list(data.index))
for label,x,y in zip(list(data.index), data['rhp'], data['gradient']):
    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center
plt.xlabel('radiogenic heat production')
plt.ylabel('temperature gradient')
plt.xlim(min(data['rhp']-1e-7), max(data['rhp']+1e-7))
plt.suptitle('relationship between temperature gradient, average rock conductivity, and radiogenic heat production')

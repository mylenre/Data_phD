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
from itertools import chain
import seaborn as sns

plt.style.use('seaborn')
colormap = np.array(['teal', 'darkslategray', 'royalblue', 'navy', 'goldenrod', 'palevioletred', 'green', 'black','rosybrown','steelblue'])

#%% collect LOG data
os.chdir(r'C:\Users\s1995204\Documents_LOCAL\LOGS\GEOINDEX\files')
filelist=glob.glob('*.txt')
log = {}
a = {}
rock = []

eldon = {}
houghton = {}
lumley ={}
moncktonhouse = {}
spilmersford = {}
salsburgh1a = {}
pumpherston  = {}
mackiesMill = {}

mcms = {}
lcms = {}
cms = {}
pgp = {}
ulcs = {}
lcs = {}
llcs = {}
wlo = {}
art = {}
gul = {}
inv = {}
devi = {}

for i in filelist:
    name = i.split('.')[0]
    df = pd.read_csv(i, delimiter=',',usecols=[0,1,2,3])
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].str.lower()
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("arkose","conglomerate")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("bbi","coal")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("calcite","limestone")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("cannel","coal")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("cementstone","limestone")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("chert","sandstone")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("fakes","shale")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("blaes","shale") #!!! I have converted some of the blaes in sandstone in my ealy times of file processing!!!
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("haematite","ironstone")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("lava","basalt")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("marl","mudstone")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("mudatone","mudstone")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("ribs ","ribs")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("rib","ribs")
    df['NATURE OF STRATA'] = df['NATURE OF STRATA'].replace("breccia","conglomerate")
    
    toth = df['Thickness'].sum(axis=0)
    df['Percentage'] = df.apply(lambda row: row.Thickness/toth*100, axis = 1) 
    log[name] = [df['Thickness'].groupby(df['NATURE OF STRATA']).sum(),df['Percentage'].groupby(df['NATURE OF STRATA']).sum()]
    a[name]=df[df['GEOLOGICA CLASSIF'].notnull()]
    
    
    if i == 'ELDON.txt':
       mcms[name]= df['Thickness'].iloc[:58].groupby(df['NATURE OF STRATA']).sum()*100/df['Thickness'].iloc[:58].sum()
       lcms[name]=df['Thickness'].iloc[58:].groupby(df['NATURE OF STRATA']).sum()*100/df['Thickness'].iloc[58:].sum()
       eldon['MCMS']= df['Thickness'].iloc[:58].groupby(df['NATURE OF STRATA']).sum()*100/df['Thickness'].iloc[:58].sum()
       eldon['LCMS']=df['Thickness'].iloc[58:].groupby(df['NATURE OF STRATA']).sum()*100/df['Thickness'].iloc[58:].sum()
    if i == 'HOUGHTON.txt':
       mcms[name]= df['Thickness'].iloc[:53].groupby(df['NATURE OF STRATA']).sum()*100/df['Thickness'].iloc[:53].sum()
       lcms[name]=  df['Thickness'].iloc[53:].groupby(df['NATURE OF STRATA']).sum()*100/df['Thickness'].iloc[:53].sum()  
       houghton['MCMS']= df['Thickness'].iloc[:53].groupby(df['NATURE OF STRATA']).sum()*100/df['Thickness'].iloc[:53].sum()
       houghton['LCMS']=  df['Thickness'].iloc[53:].groupby(df['NATURE OF STRATA']).sum()*100/df['Thickness'].iloc[:53].sum()  
    if i =='LUMLEY6.txt':
       mcms[name]= df['Thickness'].iloc[:31].groupby(df['NATURE OF STRATA']).sum()*100/df['Thickness'].iloc[:31].sum()
       lcms[name]=  df['Thickness'].iloc[31:].groupby(df['NATURE OF STRATA']).sum()*100/df['Thickness'].iloc[:31].sum()
       lumley['MCMS']= df['Thickness'].iloc[:31].groupby(df['NATURE OF STRATA']).sum()*100/df['Thickness'].iloc[:31].sum()
       lumley['LCMS']=  df['Thickness'].iloc[31:].groupby(df['NATURE OF STRATA']).sum()*100/df['Thickness'].iloc[:31].sum()
    if i =='MONKTONHOUSEBORE37.txt':
       cms[name]= df[df['Depth'] < 330]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[df['Depth'] < 330]['Thickness'].sum()
       pgp[name]=  df[(df['Depth'] > 330) & (df['Depth'] < 521)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 330) & (df['Depth'] < 521)]['Thickness'].sum()
       ulcs[name]=  df[(df['Depth'] > 521) & (df['Depth'] < 790)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 521) & (df['Depth'] < 790)]['Thickness'].sum()
       lcs[name]=  df[(df['Depth'] > 790)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 790)]['Thickness'].sum()
       moncktonhouse['CMS']= df[df['Depth'] < 330]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[df['Depth'] < 330]['Thickness'].sum()
       moncktonhouse['PGP']=  df[(df['Depth'] > 330) & (df['Depth'] < 521)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 330) & (df['Depth'] < 521)]['Thickness'].sum()
       moncktonhouse['ULCS']=  df[(df['Depth'] > 521) & (df['Depth'] < 790)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 521) & (df['Depth'] < 790)]['Thickness'].sum()
       moncktonhouse['LCS']=  df[(df['Depth'] > 790)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 790)]['Thickness'].sum()
    if i =='SPILMERSFORD.txt':
       llcs[name]= df[df['Depth'] < 22]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[df['Depth'] < 22]['Thickness'].sum()
       wlo[name]=  df[(df['Depth'] > 22) & (df['Depth'] < 128)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 22) & (df['Depth'] < 128)]['Thickness'].sum()
       gul[name]=  df[(df['Depth'] > 128) & (df['Depth'] < 287)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 128) & (df['Depth'] < 287)]['Thickness'].sum()
       art[name]=  df[(df['Depth'] > 287) & (df['Depth'] < 660)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 287) & (df['Depth'] < 660)]['Thickness'].sum()
       inv[name]=  df[(df['Depth'] > 660)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 660)]['Thickness'].sum()
       spilmersford['LLCS']= df[df['Depth'] < 22]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[df['Depth'] < 22]['Thickness'].sum()
       spilmersford['WLO']=  df[(df['Depth'] > 22) & (df['Depth'] < 128)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 22) & (df['Depth'] < 128)]['Thickness'].sum()
       spilmersford['GUL']=  df[(df['Depth'] > 128) & (df['Depth'] < 287)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 128) & (df['Depth'] < 287)]['Thickness'].sum()
       spilmersford['ART']=  df[(df['Depth'] > 287) & (df['Depth'] < 660)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 287) & (df['Depth'] < 660)]['Thickness'].sum()
       spilmersford['INV']=  df[(df['Depth'] > 660)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 660)]['Thickness'].sum()
    if i =='SALSBURGH.txt':
       pgp[name]= df[df['Depth'] < 12]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[df['Depth'] < 12]['Thickness'].sum()
       ulcs[name]=  df[(df['Depth'] > 12) & (df['Depth'] < 322)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 12) & (df['Depth'] < 322)]['Thickness'].sum()
       lcs[name]=  df[(df['Depth'] > 322) & (df['Depth'] < 526)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 322) & (df['Depth'] < 526)]['Thickness'].sum()
       llcs[name]=  df[(df['Depth'] > 526) & (df['Depth'] < 632)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 526) & (df['Depth'] <632)]['Thickness'].sum()
       wlo[name]=  df[(df['Depth'] > 632) & (df['Depth'] < 1113)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 632) & (df['Depth'] < 1113)]['Thickness'].sum()
       art[name]=  df[(df['Depth'] > 1113) & (df['Depth'] < 1215)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 1113) & (df['Depth'] < 1215)]['Thickness'].sum()
       devi[name]=  df[(df['Depth'] > 1215)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 1215)]['Thickness'].sum()
       salsburgh1a['PGP']= df[df['Depth'] < 12]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[df['Depth'] < 12]['Thickness'].sum()
       salsburgh1a['ULCS']=  df[(df['Depth'] > 12) & (df['Depth'] < 322)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 12) & (df['Depth'] < 322)]['Thickness'].sum()
       salsburgh1a['LCS']=  df[(df['Depth'] > 322) & (df['Depth'] < 526)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 322) & (df['Depth'] < 526)]['Thickness'].sum()
       salsburgh1a['LLCS']=  df[(df['Depth'] > 526) & (df['Depth'] < 632)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 526) & (df['Depth'] <632)]['Thickness'].sum()
       salsburgh1a['WLO']=  df[(df['Depth'] > 632) & (df['Depth'] < 1113)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 632) & (df['Depth'] < 1113)]['Thickness'].sum()
       salsburgh1a['ART']=  df[(df['Depth'] > 1113) & (df['Depth'] < 1215)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 1113) & (df['Depth'] < 1215)]['Thickness'].sum()
       salsburgh1a['DEVI']=  df[(df['Depth'] > 1215)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 1215)]['Thickness'].sum()
    if i =='PUMPHERSTON.txt':
       wlo[name]= df[df['Depth'] < 65]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[df['Depth'] < 65]['Thickness'].sum()
       gul[name]=  df[(df['Depth'] > 65) & (df['Depth'] < 903)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 65) & (df['Depth'] < 903)]['Thickness'].sum()
       inv[name]=  df[(df['Depth'] > 903)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 903)]['Thickness'].sum()
       pumpherston['WLO']= df[df['Depth'] < 65]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[df['Depth'] < 65]['Thickness'].sum()
       pumpherston['GUL']=  df[(df['Depth'] > 65) & (df['Depth'] < 903)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 65) & (df['Depth'] < 903)]['Thickness'].sum()
       pumpherston['INV']=  df[(df['Depth'] > 903)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 903)]['Thickness'].sum()
    if i =='MACKIES_MILL.txt':
       cms[name]= df[df['Depth'] < 150]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[df['Depth'] < 150]['Thickness'].sum()
       pgp[name]=  df[(df['Depth'] > 150) & (df['Depth'] < 430)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 150) & (df['Depth'] < 430)]['Thickness'].sum()
       ulcs[name]=  df[(df['Depth'] > 430) & (df['Depth'] < 746)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 430) & (df['Depth'] < 746)]['Thickness'].sum()
       lcs[name]=  df[(df['Depth'] > 746) & (df['Depth'] < 981)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 746) & (df['Depth'] < 981)]['Thickness'].sum()
       llcs[name]=  df[(df['Depth'] > 981) & (df['Depth'] < 1095)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 981) & (df['Depth'] < 1095)]['Thickness'].sum()
       art[name]=  df[(df['Depth'] > 1095)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 1095)]['Thickness'].sum()     
       mackiesMill['CMS']= df[df['Depth'] < 150]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[df['Depth'] < 150]['Thickness'].sum()
       mackiesMill['PGP']=  df[(df['Depth'] > 150) & (df['Depth'] < 430)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 150) & (df['Depth'] < 430)]['Thickness'].sum()
       mackiesMill['ULCS']=  df[(df['Depth'] > 430) & (df['Depth'] < 746)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 430) & (df['Depth'] < 746)]['Thickness'].sum()
       mackiesMill['LCS']=  df[(df['Depth'] > 746) & (df['Depth'] < 981)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 746) & (df['Depth'] < 981)]['Thickness'].sum()
       mackiesMill['LLCS']=  df[(df['Depth'] > 981) & (df['Depth'] < 1095)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 981) & (df['Depth'] < 1095)]['Thickness'].sum()
       mackiesMill['ART']=  df[(df['Depth'] > 1095)]['Thickness'].groupby(df['NATURE OF STRATA']).sum()*100/df[(df['Depth'] > 1095)]['Thickness'].sum()
       
wells = {'moncktonhouse':moncktonhouse,'spilmersford':spilmersford,'salsburgh':salsburgh1a,'pumpherston':pumpherston,'mackies hill':mackiesMill}
fm = {'cms':cms, 'pgp':pgp,'ulcs':ulcs,'lcs':lcs,'llcs':llcs,'wlo':wlo,'art':art,'gul':gul}
#Lower Coal Measures	Bates	Ladysmith	Houghton	Eldon 	Lumley 6
# Middle Coal Measures	Easington	Chatershaugh	Hawthorn	Houghton	Eldon 	Lumley 6	average
# Limestone Coal formation	Moncktonhall	Lady Victoria
#%%

things = []
for key in wells.keys():
    print(key)
    for key2 in wells[key]:
        print(key2)        
        converted  = pd.DataFrame(wells[key][key2])
        converted['rock']=converted.index
        formation = []
        borehole = []
        for i in range(len(wells[key][key2])):
              formation.append(key2)
              borehole.append(key)
        converted['formation'] = formation
        converted['borehole'] = borehole
        #converted.plot.bar(x='rock', y='Thickness', rot=0)
        things.append(converted)

df_stacked = pd.concat([r for r in things], ignore_index=True)
test = df_stacked['Thickness'].groupby(df_stacked['rock']).mean()
#df_stacked.pivot(index='rock', columns='rock', values='Thickness').plot(kind='bar')
   #%%  
# collect all the rock types
for key in log.keys():
    print(key)
    rock=list(chain(rock,log[key][1].index))
rock = np.unique(rock) # list(map(lambda x:x.lower(), rock))

df1 = pd.DataFrame(index = rock)
for key in log.keys():
    print(key)
    temp=pd.DataFrame(log[key][1])
    temp.rename(columns = {'Percentage': key}, inplace= True)
    df1 = pd.concat([df1, temp], axis=1)

#add conductivities, rhp (W/m3)
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
'seatearth':[2.42,860,2380,1.18233E-06,1.90E-06],
'seatrock':[2.42,860,2680,1.04998E-06,1.90E-06],
'shale':[1.3,390,2600,1.28205E-06,2.90E-06],
'siltstone':[1.84,910,2680,7.54469E-07,1.39E-06],
'soil':[0.77,860,1900,4.71236E-07,0.0000017],
'trachyte':[5.21,840,2440,2.54196E-06,0.0000032],
'tuff':[2.15,200,1500,7.16667E-06,0.0000032]}

 
properties = pd.DataFrame(properties).T
properties.columns=['cond','hc','rho','a','rhp']

#properties = pd.DataFrame(list(properties.items()), columns=['rock','cond','rhp'])
#properties = properties.set_index('rock')
conductivity = df1.mul(properties['cond'], axis='index').sum(axis = 0)/100
rhp = df1.mul(properties['rhp'], axis='index').sum(axis = 0)/100
merged = pd.merge(pd.DataFrame(conductivity), pd.DataFrame(rhp), how ='outer', left_index=True, right_index=True) 
merged.columns=['conductivity', 'rhp']

# plot rock types
df2 = df1.T 
#df2.plot.bar(stacked=True,rot=45, title="Rock percentage for different logs");
#plt.ylabel('%')
#plt.xlabel('LOG')
#plt.legend(rock)
#plt.show()
#%% group per rock type and plot data 
df3 = pd.DataFrame()
df3['volcanic'] = df2[['agglomerate', 'tuff']].sum(axis=1)
df3['igneous'] = df2[['basalt', 'dolerite', 'trachyte']].sum(axis=1)
df3['mud'] = df2[['marl','clay','seatclay','seatearth', 'fireclay']].sum(axis=1)
df3['sand'] = df2[['sand', 'soil']].sum(axis=1)
df3['fine rock'] = df2[['mudstone','shale','fakes','siltstone','clayrock','seatrock']].sum(axis=1)
df3['coarse rock'] = df2[['breccia', 'sandstone', 'blaes','conglomerate']].sum(axis=1)
df3['carbonate'] = df2[['cementstone', 'calcite', 'dolomite', 'limestone','chert']].sum(axis=1)
df3['coal'] = df2[['coal', 'ribs']].sum(axis=1)
df3['ironstone'] = df2[['ironstone', 'haematite']].sum(axis=1)
df3['no core'] = df2[['no core']].sum(axis=1)
rock2 = list(df3.columns)

#plot % rock per location
df3.plot.bar(stacked=True,rot=45, title="Rock type percentage for different logs", color = colormap);
plt.ylabel('%')
plt.xlabel('LOG')
plt.legend(rock2, bbox_to_anchor=(1,0.5))



#%% plot relationships temp vs cond

# import temperatures
temperatures={'AUCHENNIDY':[1459,18,19.6],
              'BILSTON_GLEN':[670,15,8.7],
              'FRANCES':[841,29.0,23.8],
              'HALLSIDE':[350,11.8,6],
              'LADY_VICT':[768,18,10.8],
              'LOCHHEAD':[1167,30.4,17.7],
              'MACKIES_MILL':[960,33.3,24.6],
              'MONKTONHALL':[866,25.5,18.2],
              'SALSBURGH':[874,29,24.1],
              'SPILMERSFORD':[877,27.8,20.9],
              'THORNTON_BRIDGE':[665,28.0,27.5],
              'THORNTON_FARM':[1055,38,26.8],
              'PUMPHERSTON':[1175,36.7,23.3],
              'QUEENSLIE':[691,36,38.4],
              'SEAFIELD':[789,29,25.3],
              'WELLSGREEN':[1485,42.3,22.0]}

temperatures = pd.DataFrame(temperatures).T
temperatures.columns=['depth','temperature','gradient']

data = merged.merge(temperatures, how = 'inner', left_index = True, right_index = True)

plt.figure(figsize=(8,6))
plt.subplot(2,1,1)
plt.scatter(data['conductivity'], data['gradient'], c='b', label=list(temperatures.index))
for label,x,y in zip(list(temperatures.index), data['conductivity'], data['gradient']):
    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center
plt.xlabel('rock conductivity')
plt.ylabel('temperature gradient')

plt.subplot(2,1,2)
plt.scatter(data['rhp'], data['gradient'], c='r', label=list(temperatures.index))
for label,x,y in zip(list(temperatures.index), data['rhp'], data['gradient']):
    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center
plt.xlabel('radiogenic heat production')
plt.ylabel('temperature gradient')
plt.xlim(min(data['rhp']-1e-7), max(data['rhp']+1e-7))
plt.suptitle('relationship between temperature gradient, average rock conductivity, and radiogenic heat production')


#%%
temperatures_central={'HALLSIDE':[350,11.8,6],
              'SALSBURGH':[874,29,24.1],
              'PUMPHERSTON':[1175,36.7,23.3],
              'QUEENSLIE':[691,36,38.4]}#,
temperatures_fife={'FRANCES':[841,29.0,23.8],
              'LOCHHEAD':[1167,30.4,17.7],
              'MACKIES_MILL':[960,33.3,24.6],
              'THORNTON_BRIDGE':[665,28.0,27.5],
              'THORNTON_FARM':[1055,38,26.8],
              'SEAFIELD':[789,29,25.3],
              'WELLSGREEN':[1485,42.3,22.0]}
temperatures_midlothian={'AUCHENNIDY':[1459,18,19.6],
              'BILSTON_GLEN':[670,15,8.7],
              'LADY_VICT':[768,18,10.8],
              'MONKTONHALL':[866,25.5,18.2],
              'SPILMERSFORD':[877,27.8,20.9]}

temperatures_central = pd.DataFrame(temperatures_central).T
temperatures_central.columns=['depth','temperature','gradient']
temperatures_fife = pd.DataFrame(temperatures_fife).T
temperatures_fife.columns=['depth','temperature','gradient']
temperatures_midlothian = pd.DataFrame(temperatures_midlothian).T
temperatures_midlothian.columns=['depth','temperature','gradient']

data_central = merged.merge(temperatures_central, how = 'inner', left_index = True, right_index = True)
data_fife = merged.merge(temperatures_fife, how = 'inner', left_index = True, right_index = True)
data_midlothian = merged.merge(temperatures_midlothian, how = 'inner', left_index = True, right_index = True)

plt.figure(figsize=(8,6))
plt.subplot(2,1,1)
plt.scatter(data_central['conductivity'], data_central['gradient'], s=20, marker='x', c='b', label=list(temperatures_central.index))
plt.scatter(data_fife['conductivity'], data_fife['gradient'], s=20, marker='x', c='r', label=list(temperatures_fife.index))
plt.scatter(data_midlothian['conductivity'], data_midlothian['gradient'],s=20, marker='x',  c='g', label=list(temperatures_midlothian.index))

for label,x,y in zip(list(temperatures.index), data['conductivity'], data['gradient']):
    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(30,3), # distance from text to points (x,y)
                 ha='center',
                 fontsize=8) # horizontal alignment can be left, right or center
plt.xlabel('rock conductivity')
plt.ylabel('temperature gradient')

plt.subplot(2,1,2)
plt.scatter(data_central['rhp'], data_central['gradient'], s=20, marker='x', c='r', label=list(temperatures_central.index))
plt.scatter(data_fife['rhp'], data_fife['gradient'], s=20, marker='x', c='r', label=list(temperatures_fife.index))
plt.scatter(data_midlothian['rhp'], data_midlothian['gradient'], s=20, marker='x', c='g', label=list(temperatures_midlothian.index))
for label,x,y in zip(list(temperatures.index), data['rhp'], data['gradient']):
    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(30,3), # distance from text to points (x,y)
                 ha='center',
                 fontsize=8) # horizontal alignment can be left, right or center
plt.xlabel('radiogenic heat production')
plt.ylabel('temperature gradient')
plt.xlim(min(data['rhp']-1e-7), max(data['rhp']+1e-7))
plt.suptitle('relationship between temperature gradient, average rock conductivity, and radiogenic heat production', fontsize=10)


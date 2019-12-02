# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 23:31:49 2019

@author: mylen
"""
# Importing the matplotlb.pyplot 
import matplotlib.pyplot as plt 
import datetime
import numpy as np

date_time_series = []
date_time = datetime.date(2019, 9, 1)
date_at_end = datetime.date(2023, 9, 1)
step = datetime.timedelta(days=31)
i=0
month=[]


while date_time <= date_at_end:
  date_time_series.append(date_time)
  date_time += step
  i+=1
  month.append(i)
  
# Declaring a figure "gnt" 
  #plt.figure(figsize=(6,4))
fig, gnt = plt.subplots(figsize=(18,10)) 
 
# Setting axis limits 
gnt.set_xlim(date_time, date_at_end) 
gnt.set_ylim(0, 23) 

gnt.set_xlabel('Month since start') 
gnt.set_xticks(date_time_series) 
gnt.xaxis.tick_top()
plt.gca().invert_xaxis()
#plt.xticks(rotation=60)
gnt.set_xticklabels(month[:])
        
gnt.set_ylabel('Task') 
gnt.set_yticks(np.arange(0,24,1)) 
plt.gca().invert_yaxis()
gnt.set_yticklabels(['',
                     'Confirmation panel',
                     'CASE placement',
                     'ECCI placement',
                     'PIP',
                     'PGR Conference',
                     'IMWA Conference',
                     '2D models set-up',
                     'Data collectio \n & analysis',
                     'Conceptual model set-up',
                     '2D models validation',
                     'Paper 1',
                     'Set-up model study area 1',
                     'Set-up model study area 2',
                     '3D Steady-state \n & transient simulation',
                     'Data update \n & Predictive tool validation',
                     'Paper 2',
                     'Sustainable heat scheme \n dimensioning',
                     'Paper 3',
                     'Thesis compilation \n & complementary analysis',
                     'Conclusion',
                     'Thesis review',
                     'Thesis submission']) 
  
# Setting graph attribute 
gnt.grid(True) 
  
# Declaring a bar in schedule 
gnt.broken_barh([], (0, 0.5),
                 facecolors =('tab:red'))
# admin
# Confirmation panel
gnt.broken_barh([(datetime.date(2020, 6, 1), 1)], (0.8, 0.5),
                 facecolors =('black'))
plt.plot(datetime.date(2020,6,1), 1, 'x', color='black' )

# CASE placements 
gnt.broken_barh([(datetime.date(2020,1,6), 30), (datetime.date(2021, 1, 4), 30),(datetime.date(2022, 1, 1), 30)], (1.8, 0.5), 
                 facecolors ='black') 
# ECCI placement 
gnt.broken_barh([(datetime.date(2021, 9, 1), 30)], (2.8,0.5),
                 facecolors =('black')) 
# PIP
gnt.broken_barh([(datetime.date(2023, 2, 1), 90)], (3.8,0.5),
                 facecolors =('black')) 
# conferences
# PGR conference
gnt.broken_barh([(datetime.date(2020, 4, 23), 2)], (4.8,0.5),
                 edgecolors =('black')) 
# IMWA Conference
gnt.broken_barh([(datetime.date(2021, 6, 30), 2)], (5.8,0.5),
                 facecolors =('black'))
# year 1
# 2D numerocal model set up
gnt.broken_barh([(datetime.date(2019,9,1), 90)], (6.8,0.5), 
                 facecolors =('tab:blue')) 
# Data collection and analysis 
gnt.broken_barh([(datetime.date(2020, 2, 3), 90)], (7.8,0.5),
                 facecolors =('tab:blue')) 
# Conceptual model set up
gnt.broken_barh([(datetime.date(2020, 3, 9), 30)], (8.8,0.5),
                 facecolors =('tab:blue')) 
# 2D numerical models validation
gnt.broken_barh([(datetime.date(2020, 4, 6), 120)], (9.8, 0.5),
                 facecolors =('tab:blue')) 
# Paper 1
gnt.broken_barh([(datetime.date(2020, 9, 1), 120)], (10.8, 0.5),
                 facecolors =('tab:blue')) 
# year 2
# Case study 1 & 3D model set-up
gnt.broken_barh([(datetime.date(2021, 2, 1), 30)], (11.8, 0.5),
                 facecolors =('tab:green')) 
# Case study 2 & 3D model set-up
gnt.broken_barh([(datetime.date(2021, 3, 1), 30)], (12.8, 0.5),
                 facecolors =('tab:green')) 
# 3D Stready-state & trasient simulation'
gnt.broken_barh([(datetime.date(2021, 4, 1), 120)], (13.8, 0.5),
                 facecolors =('tab:green')) 
# Year 3
# Data update and predictive tool validation
gnt.broken_barh([(datetime.date(2021, 10, 1), 30)], (14.8, 0.5),
                 facecolors =('tab:green')) 
# Paper 2
gnt.broken_barh([(datetime.date(2021, 11 ,3), 90)], (15.8,0.5),
                 facecolors =('tab:green')) 
#sustainable scheme modeling
gnt.broken_barh([(datetime.date(2022, 2, 1), 90)], (16.8,0.5),
                 facecolors =('tab:red')) 
# Paper 3
gnt.broken_barh([(datetime.date(2022, 5, 1), 90)], (17.8,0.5),
                 facecolors =('tab:red')) 

# Year 4
# Thesis compilation
gnt.broken_barh([(datetime.date(2022, 9, 1), 90)], (18.8,0.5),
                 facecolors =('tab:orange')) 
# Conclusions
gnt.broken_barh([(datetime.date(2023, 1, 1), 30)], (19.8, 0.5),
                 facecolors =('tab:orange')) 
#Thesis review
gnt.broken_barh([(datetime.date(2023, 5, 1), 90)], (20.8, 0.5),
                 facecolors =('tab:orange')) 
# Thesis submission
gnt.broken_barh([(datetime.date(2023, 8, 31), 1)], (21.8,0.5),
                 facecolors =('black')) 
plt.plot(datetime.date(2023,8,31), 22, 'x', color='black' )

plt.axvline(datetime.date(2020,9,1),color='black')  
plt.axvline(datetime.date(2021,9,1),color='black')  
plt.axvline(datetime.date(2022,9,1),color='black')  
plt.text(datetime.date(2020,2,1), -1, 'Year 1', fontsize=12)
plt.text(datetime.date(2021,2,1), -1, 'Year 2', fontsize=12)
plt.text(datetime.date(2022,2,1), -1, 'Year 3', fontsize=12)
plt.text(datetime.date(2023,2,1), -1, 'Year 4', fontsize=12)

plt.axhline(y=4.5, color='k', linestyle='--', linewidth=1)
plt.axhline(y=6.5, color='k', linestyle='--', linewidth=1)
plt.axhline(y=11.5, color='k', linestyle='--', linewidth=1)
plt.axhline(y=16.5, color='k', linestyle='--', linewidth=1)
plt.axhline(y=18.5, color='k', linestyle='--', linewidth=1)


plt.savefig("gantt1.png") 
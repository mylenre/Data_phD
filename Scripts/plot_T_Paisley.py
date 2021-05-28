# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 08:24:11 2020

@author: mylen
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import scipy.optimize

def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * np.cos(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.cos(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}

# Define parameters
datelist=np.arange(2000,2011,1) # years to consider for average
time=np.arange(0,366,1) # time steps in one year
t=30 #total simulation time (years)
tt=np.arange(0,t*366*24*3600,86400) #10980 steps


#%% import model data
os.chdir(r'S:\Modeling\1D_Models\3_Heat_extraction_new_areas\Solar\3_ALTERNATIVE\1_REFERENCE')

#import flux
flux = pd.read_csv('q_surf.txt', delimiter=',', header=0) 

# import model output surface temperature 
surf_temp = pd.read_csv('T_surf.txt', delimiter=',', header=0) 
temp_30cm = pd.read_csv('T_30cm.txt', delimiter=',', header=0) 
temp_100cm = pd.read_csv('T_100cm.txt', delimiter=',', header=0) 

fig = plt.figure(figsize=(8,8))
plt.rcParams['font.size'] = 10 
cx1 = plt.subplot(211)
cx2 = cx1.twinx()
cx1.plot(time[0:366], flux['flux'][0:366], c='r', label="Input flux", linewidth=2)
cx2.plot(time[0:366], surf_temp['temp'][0:366], label="Modelled surface temperature", linewidth=2)
cx1.set_ylabel("Flux (W/m²)")
cx2.set_ylabel("Temperature (°C)")
plt.grid(True, which='both')
plt.title('Comparison temperature data and model at the Paisley station')

#% Import AIR TEMPERATURE data
os.chdir(r'S:\GitHub\Data_phD\Data\Climate_Data\Paisley\AirTemperature')
air_temp={}

with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        print(line)
        date = line.split('.')[0]
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=6)
        data.DATES = pd.to_datetime(pd.Series(data.DATES))
        data.DATES = data.DATES.dt.strftime('%m/%d')
        data = data.sort_values(by=['DATES'])
        air_temp[date] = data
df = pd.DataFrame()
for i in air_temp:
    df[i] = air_temp[i]['Near-Surface Air Temperature (K)'][0:366]
mean_val = df.mean(axis = 1)-273
table=np.stack((time, mean_val), axis=-1)

plt.figure(figsize=(10,5))
#plt.subplot(4,2,1)
#plt.scatter(table[:,0],table[:,1], s=1, c = 'b', label='Air temperature data')
#res = fit_sin(table[:,0],table[:,1])
#ATfit=res["fitfunc"](table[:,0])
#print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
#plt.plot(table[:,0], ATfit, '--', c = 'b', label="Best Fit Air Temperature", linewidth=2)
#plt.grid(True, which='both')
#plt.legend(loc="best")
#plt.ylabel('Air temperature (°C)')

#% SOIL TEMPERATURE
os.chdir(r'S:\GitHub\Data_phD\Data\Climate_Data\Paisley\Soil_Temp_CEDA')
soil_temp={}
a = 1.2

with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        print(line)
        date = line.split('.')[0]
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=85)
        soil_temp[date] = data

df1 = pd.DataFrame()
df2 = pd.DataFrame()
for i in soil_temp:
    df1[i] = soil_temp[i]['q30cm_soil_temp'][0:366]
    df2[i] = soil_temp[i]['q100cm_soil_temp'][0:366]
mean_val1 = df1.mean(axis = 1) - a
mean_val2 = df2.mean(axis = 1) - a
#table=np.stack((time, mean_val1, mean_val2), axis=-1)
table=np.stack((time, list(mean_val1[63:366])+list(mean_val1[0:63]), 
                list(mean_val2[63:366])+list(mean_val2[0:63])), axis=-1)


# plot data
cx1 = plt.subplot(111)
cx2 = cx1.twinx()

cx1.plot(table[:,0],table[:,1], '.', c='darkslategray', label="Measured soil temperature at 30cm depth")
res = fit_sin(table[:,0],table[:,1])
ST1fit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )

cx1.plot(table[:,0],table[:,2], '.', c = 'darkred', label="Measured soil temperature at 1m depth")
res = fit_sin(table[:,0],table[:,2])
ST2fit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )

#plot interpolation
cx1.plot(table[:,0], ST1fit , '--', c='darkslategray',  label="Best Fit Soil Temperature (30cm)", linewidth=2) 
cx1.plot(table[:,0], ST2fit ,  '--', c='darkred', label="Best Fit Soil Temperature (1m)", linewidth=2) 

# plot modelled temperature
i=0
#cx1.plot(time, surf_temp['temp'][i:i+366], c='b', label="Modelled surface temperature", linewidth=2)
p1, = cx1.plot(time, temp_30cm['temp'][i:i+366], c='k', label="Modelled temperature (30cm)", linewidth=2)
p1b = cx1.plot(time, temp_100cm['temp'][i:i+366], c='r', label="Modelled temperature (1m)", linewidth=2)

#plot flux
p2, = cx2.plot(time, flux['flux'][i:i+366], c='b', label="Input flux", linewidth=2)

cx1.set_xlabel('Time (days)')
cx1.set_ylabel('Temperature (°C)')
cx2.set_ylabel("Flux (W/m²)")
cx1.yaxis.get_label().set_color(p1.get_color())
cx2.yaxis.get_label().set_color(p2.get_color())
cx1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
plt.grid(True, which='both')


# np.mean(ATfit) = 9.51
# np.mean(surf_temp['temp'])= 9.16

# np.mean(ST1fit)= 10.37
# np.mean(ST2fit)= 10.832

# np.mean(temp_30cm['temp'][i:i+366]) = 9.18
# np.mean(temp_100cm['temp'][i:i+366]) = 9.20
# increasing the gradient and gradient/cond increases by 0.01°C mean temeprature at 30/100 cm
# decreasing conductivity increases amplitude of temperature change

#(np.max(ATfit)-np.min(ATfit))/2 = 5.34
# ST1 amplitude = 6.72
# ST2 amplitude = 4.77

# Paisley : average temperature at surface: 9.73, at 30/100 cm is 9.75/9.78


#%% QUICK TEST
datelist=np.arange(2000,2011,1) # years to consider for average
time=np.arange(0,366,1) # time steps in one year
t=30 #total simulation time (years)
tt=np.arange(0,t*366*24*3600,86400) #10980 steps

os.chdir(r'C:\Workspace\recover\Users\s1995204\Documents_LOCAL\Modeling\6_BACK_COND_AMP')
# import model output surface temperature 
temp_30cm = pd.read_csv('T_30cm.txt', delimiter=',', header=0) 
temp_100cm = pd.read_csv('T_100cm.txt', delimiter=',', header=0) 

#% SOIL TEMPERATURE
os.chdir(r'S:\GitHub\Data_phD\Data\Climate_Data\Paisley\Soil_Temp_CEDA')
soil_temp={}
a = 1.2 #0.65

with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        print(line)
        date = line.split('.')[0]
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=85)
        soil_temp[date] = data

df1 = pd.DataFrame()
df2 = pd.DataFrame()
for i in soil_temp:
    df1[i] = soil_temp[i]['q30cm_soil_temp'][0:366]
    df2[i] = soil_temp[i]['q100cm_soil_temp'][0:366]
mean_val1 = df1.mean(axis = 1) - a
mean_val2 = df2.mean(axis = 1) - a
table=np.stack((time, list(mean_val1[63:366])+list(mean_val1[0:63]), 
                list(mean_val2[63:366])+list(mean_val2[0:63])), axis=-1)

cx1 = plt.subplot(111)

cx1.scatter(table[:,0],table[:,1], c='darkslategray', s=1, label="Measured soil temperature at 30cm depth")
res = fit_sin(table[:,0],table[:,1])
ST1fit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
cx1.plot(table[:,0], ST1fit , '--', c='darkslategray',  label="Best Fit Soil Temperature (30cm)", linewidth=2) 

cx1.scatter(table[:,0],table[:,2], c = 'darkred', s=1, label="Measured soil temperature at 1m depth")
res = fit_sin(table[:,0],table[:,2])
ST2fit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
cx1.plot(table[:,0], ST2fit ,  '--', c='darkred', label="Best Fit Soil Temperature (1m)", linewidth=2) 

# plot modelled temperature
i=0
p1, = cx1.plot(time, temp_30cm['temp'][i:i+366], c='k', label="Modelled temperature (30cm)", linewidth=2)
p1b = cx1.plot(time, temp_100cm['temp'][i:i+366], c='r', label="Modelled temperature (1m)", linewidth=2)


cx1.set_xlabel('Time (days)')
cx1.set_ylabel('Temperature (°C)')
cx1.yaxis.get_label().set_color(p1.get_color())
cx1.legend(loc="best",frameon=False)
plt.grid(True, which='both')

#%%
os.chdir(r'S:\GitHub\Data_phD\Data\Climate_Data\Paisley')

data = np.loadtxt('Tcomp.txt', skiprows=1,usecols=(2,3))  # all data
time = np.arange(0,366,1)

# Import data
Tair = data[:,0]  
Tair_av = np.mean(Tair)
Tsoil = data[:,1]
Tsoil_av = np.mean(Tsoil)
Tdiff = Tair - Tsoil
hc = 1.2
q = (Tdiff/0.030)*hc
q_av=np.mean(q)
date_time_series = []
date_time = datetime.datetime(2000, 1, 1)
date_at_end = datetime.datetime(2000, 12, 31)
step = datetime.timedelta(days=1)

# set datetime
while date_time <= date_at_end:
  date_time_series.append(date_time)
  date_time += step

# plot data 
fig = plt.figure(figsize=(15,10))
plt.rcParams['font.size'] = 10 
plt.title('2000 daily air and soil temperature at the Paisley station')

cx1 = plt.subplot(211)
cx2 = cx1.twinx()
cx1.plot(date_time_series, Tair, label="Air Temperature", linewidth=2)
cx1.plot(date_time_series, Tsoil, label="Soil Temperature at 30 cm depth", linewidth=2)
cx2.plot(date_time_series, q, color = 'g', ls = '--', label="Flux from air to soil", linewidth=1)
cx2.axhline(y=0,xmin=0,xmax=1, linewidth=1, color='k', ls='--')
cx1.legend(loc='lower left')
cx2.legend(loc='upper right')
plt.legend(fontsize=12) 

# Calculate sinusoidal funtions and plot
cx3 = plt.subplot(212)
cx4 = cx3.twinx()

res = fit_sin(time,Tair)
fit=res["fitfunc"](time)
cx3.plot(time, fit,  linewidth=2)
res = fit_sin(time,Tsoil)
fit=res["fitfunc"](time)
cx3.plot(time, fit,  linewidth=2)
res = fit_sin(time,q)
fit=res["fitfunc"](time)
cx4.plot(time, fit, color = 'g', ls = '--', linewidth=1)
plt.axhline(y=0,xmin=0,xmax=1, linewidth=1, color='k', ls='--')

cx1.set_ylabel("Temperature (°C)")
cx2.set_ylabel("Flux (W/m²)")
cx3.set_ylabel("Temperature (°C)")
cx4.set_ylabel("Flux (W/m²)")
plt.xlabel("Time")

#plt.savefig("Tcomp_Paisley.png") 
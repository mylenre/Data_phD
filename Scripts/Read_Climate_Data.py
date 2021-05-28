# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 09:57:16 2019

@author: mylen
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import numpy, scipy.optimize

# a = os.listdir(path='.')
# filelist=glob.glob('*\*.csv')

def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = numpy.array(tt)
    yy = numpy.array(yy)
    ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(numpy.fft.fft(yy))
    guess_freq = abs(ff[numpy.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = numpy.std(yy) * 2.**0.5
    guess_offset = numpy.mean(yy)
    guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * numpy.cos(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*numpy.pi)
    fitfunc = lambda t: A * numpy.cos(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}


# Define parameters
datelist=np.arange(2000,2011,1) # years to consider for average
time=np.arange(0,366,1) # time steps in one year
t=30 #total simulation time (years)
tt=np.arange(0,t*366*24*3600,86400) #10980 steps

#%% Import data

albedo_sw=0.31
albedo_lw=0.1

#% AIR TEMPERATURE
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

plt.figure(figsize=(20,20))
plt.subplot(4,2,1)
plt.scatter(table[:,0],table[:,1], c = 'royalblue', s=1, label='Air temperature data')
res = fit_sin(table[:,0],table[:,1])
ATfit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
plt.plot(table[:,0], ATfit , c = 'royalblue', label="Fit Air Temperature", linewidth=2)
#plt.grid(True, which='both')
#plt.legend(loc="best")
#plt.ylabel('Air temperature (°C)')


#% SOIL TEMPERATURE
os.chdir(r'S:\GitHub\Data_phD\Data\Climate_Data\Paisley\Soil_Temp_CEDA')
soil_temp={}

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
mean_val1 = df1.mean(axis = 1)
mean_val2 = df2.mean(axis = 1)
table=np.stack((time, mean_val1, mean_val2), axis=-1)

#plt.subplot(4,2,2)
plt.scatter(table[:,0],table[:,1], c='chocolate', s=1, label="Soil temperature data 30 cm")
plt.scatter(table[:,0],table[:,2], c = 'slategray', s=1, label="Soil temperature data 100 cm")

res = fit_sin(table[:,0],table[:,1])
ST1fit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
plt.plot(table[:,0], ST1fit , 'chocolate', label="Fit Soil Temperature 30 cm", linewidth=2) 

res = fit_sin(table[:,0],table[:,2])
ST2fit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
plt.plot(table[:,0], ST2fit , 'slategray', label="Fit Soil Temperature 100 cm", linewidth=2) 

plt.ylabel('Temperature (°C)')
plt.legend(loc="best")
plt.grid(True, which='both')

#% WINDSPEED
os.chdir(r'S:\GitHub\Data_phD\Data\Climate_Data\Paisley\Windspeed')
wind_speed={}

with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        print(line)
        date = line.split('.')[0]
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=6)
        data.DATES = pd.to_datetime(pd.Series(data.DATES))
        data.DATES = data.DATES.dt.strftime('%m/%d')
        data = data.sort_values(by=['DATES'])
        wind_speed[date] = data
df = pd.DataFrame()
for i in wind_speed:
    df[i] = wind_speed[i]['Near-Surface Wind Speed (m s-1)'][0:366]
mean_val = df.mean(axis = 1)
table=np.stack((time, mean_val), axis=-1)

plt.subplot(4,2,2)
plt.scatter(table[:,0],table[:,1], s=1, c = 'teal', label='Wind speed data')
res = fit_sin(table[:,0],table[:,1])
WSfit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
plt.plot(table[:,0], WSfit, '-', c = 'teal', label="Fit Wind Speed", linewidth=2)
plt.ylabel('Wind speed (m/s)')
plt.legend(loc="best")
plt.grid(True, which='both')

# Convective heat flux
h_conv=[] #h—convective heat transfer coefficient (W/(m2K))
for u in WSfit:
    if u < 4.88:
        h = 5.7 + 3.8*u
    else:
        h = 7.2*u**0.78
    h_conv.append(h)
# h_conv = 0.5+ 1.2*WSfit**0.5 # SalahSaadi et al (2017)       
q_conv=h_conv*((ATfit+273)-(ST1fit+273))

#% SHORTWAVE (solar radiations)
os.chdir(r'S:\GitHub\Data_phD\Data\Climate_Data\Paisley\Shortwave')
shortwave= {}

with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        print(line)
        date = line.split('.')[0]
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=6)
        data.DATES = pd.to_datetime(pd.Series(data.DATES))
        data.DATES = data.DATES.dt.strftime('%m/%d')
        data = data.sort_values(by=['DATES'])
        shortwave[date] = data
df = pd.DataFrame()
for i in shortwave:
    df[i] = shortwave[i]['Surface Downwelling Shortwave Radiation (W m-2)'][0:366]
mean_val = (1-albedo_sw)* df.mean(axis = 1) #absorbed radiations
table=np.stack((time, mean_val), axis=-1)

plt.subplot(4,2,3)
plt.scatter(table[:,0],table[:,1], s=1, c = 'orange', label='Downwelling Shortwave Radiation data')
res = fit_sin(table[:,0],table[:,1])
SWfit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
plt.plot(table[:,0], SWfit, '-', c = 'orange', label="Fit Downwelling Shortwave Radiation", linewidth=2)
plt.ylabel('Shortwave (W/m$^2$)')
plt.legend(loc="best")
plt.grid(True, which='both')

If = 0.5 #intensity factor (Qin et al., 2013)
q_abs = SWfit * If

#% Downward LONGWAVE radiations
os.chdir(r'S:\GitHub\Data_phD\Data\Climate_Data\Paisley\Longwave')
longwave= {}

with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        print(line)
        date = line.split('.')[0]
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=6)
        data.DATES = pd.to_datetime(pd.Series(data.DATES))
        data.DATES = data.DATES.dt.strftime('%m/%d')
        data = data.sort_values(by=['DATES'])
        longwave[date] = data
df = pd.DataFrame()
for i in longwave:
    df[i] = longwave[i]['Surface Downwelling Longwave Radiation (W m-2)'][0:366]
#mean_val = df.mean(axis = 1) 
mean_val = (1-albedo_lw)*df.mean(axis = 1) 
table=np.stack((time, mean_val), axis=-1)

plt.subplot(4,2,4)
plt.scatter(table[:,0],table[:,1], s=1, c = 'orange', label='Downwelling Longwave Radiation data')
res = fit_sin(table[:,0],table[:,1])
LWfit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
plt.plot(table[:,0], LWfit, '-',c = 'orange', label="Fit Downwelling Longwave Radiation", linewidth=2)

#Reflected thermal radiations from ground
#plt.subplot(4,2,6)
# Analytical calculations of longwave thermal radiations (Qin et al 2013)
sigma = 5.669e-8 # W/(m2K4) Stefan-Boltzmann constant
Tdp = ATfit- 10 # dew point (Perry and Green, 1997)
emissivity = 0.754 + 0.0044*Tdp # ground surface emissivity (Tang et al., 2004)
Tsky = ATfit*emissivity**0.25
q_irr = sigma * emissivity * ((Tsky+273)**4- (ST1fit+273)**4)
#plt.plot(table[:,0], q_irr, 'k', label="Analytical Longwave (Qin et al., 2013)", linewidth=2)

# Analytical calculations of longwave thermal radiations (larwa, 2018)
Tsky = ATfit*(0.711+0.0056*Tdp+0.000073*Tdp**2)**0.25
LW = sigma * emissivity * ((ST1fit+273)**4 - (Tsky+273)**4)
#plt.plot(table[:,0], LW, 'r', label="Analytical Longwave (Salah Saadi et al., 2017)", linewidth=2)

# Analytical calculations of longwave thermal radiations (Salah Saadi et al 2017)
LR = emissivity * sigma * ((ST1fit+273)**4-(ATfit+273)**4)
#plt.plot(table[:,0], LR, 'r', label="Analytical Longwave (Salah Saadi et al., 2017)", linewidth=2)

# Analytical calculations of longwave thermal radiations (Singh and sharma 2017)
Tsky = ATfit-12
TR = emissivity * sigma * ((ATfit+273)**4-(Tsky+273)**4)
#plt.plot(table[:,0], TR, 'g', label="Analytical Longwave (Singh & sharma, 2017)", linewidth=2)

# from Banks, 2008
emissivity = 0.97
q_back = emissivity * sigma * (ATfit + 273)**4
plt.plot(table[:,0], q_back, c='darkred', label="Reflected Longwave (Banks, 2008)", linewidth=2)
plt.ylabel('Longwave (W/m$^2$)')
plt.legend(loc="best")
plt.grid(True, which='both')


#% Relative Humidity
os.chdir(r'S:\GitHub\Data_phD\Data\Climate_Data\Paisley\RelativeHumidity')
humidity= {}

with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        print(line)
        date = line.split('.')[0]
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=6)
        data.DATES = pd.to_datetime(pd.Series(data.DATES))
        data.DATES = data.DATES.dt.strftime('%m/%d')
        data = data.sort_values(by=['DATES'])
        humidity[date] = data
df = pd.DataFrame()
for i in humidity:
    df[i] = humidity[i]['Near-Surface Specific Humidity (kg kg-1)'][0:366]
mean_val = df.mean(axis = 1) 
table=np.stack((time, mean_val), axis=-1)

#plt.subplot(4,2,6)
#plt.scatter(table[:,0],table[:,1], s=1, label='Relative Humidity data')
res = fit_sin(table[:,0],table[:,1])
RHfit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
#plt.plot(table[:,0], RHfit, '-', label="Fit Relative Humidity", linewidth=2)
#plt.ylabel('m/s')
#plt.legend(loc="best")
#plt.xlabel('Time (days)')
#plt.ylabel('Relative humidity (%)')
#plt.grid(True, which='both')

# latent heat of evaporation # SalahSaadi et al (2017); Larwa (2018)
f = 0.7
hc = 0.5+ 1.2*WSfit**0.5 # SalahSaadi et al (2017)       
LE = 0.0168 * f * hc * (103 * (ST1fit+273) + 609 - RHfit * (103 * (ATfit + 273) + 609))
#plt.plot(table[:,0], LE, label='Latent heat of evaporation')

#% EVAPOTRANSPIRATION
os.chdir(r'S:\GitHub\Data_phD\Data\Climate_Data\Paisley\Evapotranspiration')
evapo= {}

with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        print(line)
        date = line.split('.')[0]
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=6)
        data.DATES = pd.to_datetime(pd.Series(data.DATES))
        data.DATES = data.DATES.dt.strftime('%m/%d')
        data = data.sort_values(by=['DATES'])
        evapo[date] = data
df = pd.DataFrame()
for i in evapo:
    df[i] = evapo[i]['Potential evapotranspiration with interception correction (mm/day)'][0:366]
mean_val = df.mean(axis = 1) 
table=np.stack((time, mean_val), axis=-1)

plt.subplot(4,2,5)
#plt.scatter(table[:,0],table[:,1], s=1, label='Evapo-Transpiration data')
res = fit_sin(table[:,0],table[:,1])
EVfit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
#plt.plot(table[:,0], EVfit, '-', label="Fit Evapo-Transpiration", linewidth=2)
#plt.xlabel('Time (days)')
#plt.ylabel('Evapo-transpiration (mm/day)')

# latent heat of evaporation (Banks, 2008)
q_evap = EVfit * 1000 * 2257 / 86400 #(Banks, 2008) mm/day * 1000 g/m2 *2257 J/g /86400s = W/m2
#https://www.researchgate.net/post/How-to-calculate-evapotranspiration-from-latent-heat-flux
plt.plot(table[:,0], q_evap, c='darkred', label='Latent heat of evaporation')
plt.xlabel('Time (days)')
plt.ylabel('Evapo-transpiration (W/m$^2$)')
plt.legend(loc="best")
plt.grid(True, which='both')

#% plot Convective heat flux
#plt.figure(figsize=(20,20))
plt.subplot(4,2,6)
plt.plot(table[:,0],q_conv, c = 'teal', label='Convective flux')  
plt.ylabel('W/m$^2$')
plt.legend(loc="best")

#% plot Conductive heat flux
#qcond0 = q_conv - LWfit + SWfit - EVfit #ref
qcond0 = q_conv + LR + SWfit #ref
qcond1 = q_conv - LW + SWfit - LE # Larwa, 2018
qcond2 = q_conv + q_irr + q_abs # Qin et al., 2013
qcond3 = q_conv - LR + SWfit - LE #CE (convective energy)- lR (Longwave radiations emitted form ground)+ SR (absobed radiation) - LE (latente heat evaporation) # SalahSaadi et al (2017)
qcond4 = q_conv - TR + SWfit # Singh and Sharma 2017

#plt.plot(table[:,0],qcond0, label='Conductive flux (reference)')
##plt.plot(table[:,0],qcond1, label='Conductive flux Larwa (2018)')
#plt.plot(table[:,0],qcond2, label='Conductive flux Qin et al. (2013)')
##plt.plot(table[:,0],qcond3, label='Conductive flux Salah Saadi et al. (2017)')
##plt.plot(table[:,0],qcond4, label='Conductive flux Singh and Sharma (2017)')

#% plot net incoming radiations (Banks,2008)
rn = SWfit + LWfit - q_back
rn2 = rn - (q_conv + q_evap)
plt.plot(table[:,0],rn, c = 'orange', label='Net incoming radiations (Banks, 2008)')
plt.plot(table[:,0],rn2, c='darkred', label='Thermal input (Banks, 2008)')

plt.legend(loc="best")
plt.xlabel('Time (s)')
plt.ylabel('W/m$^2$')
plt.grid(True, which='both')

os.chdir(r'S:\GitHub\Data_phD\Data\Climate_Data\Paisley')
#plt.savefig('Data_plot_v2.png') 

#%%
tot_irr = np.mean(SWfit)+np.mean(LWfit) # total incoming radiations
    
sw = np.mean(SWfit)# shortwave radiations
lw = np.mean(LWfit) # downwelling LW rad 
th = np.mean(q_back) #emitted rad 
rn_mean = np.mean(rn)
rn2_mean = np.mean(rn2)

#print('assuming shortwave reflectivity of '+ str(albedo_sw) + ' and longwave reflectivity of ' + str(albedo_lw)))
print(sw)
print(lw)
print(th)
print(rn_mean)
print(rn2_mean)

# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 09:57:16 2019

@author: mylen
"""
######################### import packages ############################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import numpy, scipy.optimize

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


#########################define parameters############################
datelist=np.arange(2000,2011,1) # years to consider for average
time=np.arange(0,86400*366,86400) # time steps in one year
t=30 #total simulation time (years)
tt=np.arange(0,t*366*24*3600,86400) #10980 steps

#w=2*np.pi/365 # frequency of annual cyle
#L= (2*a/w) #damping depth

########################### AIR TEMPERATURE##########################
os.chdir(r'R:\GitHub\Data_phD\Data\Climate_Data\Paisley\AirTemperature')
AT={}
alldate=[]
alltemp=[]

with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=6)
        year=data['DATES']
        temperature=data['Near-Surface Air Temperature (K)']
        date=np.array(year)
        temp=np.array(temperature)
        alldate.append(date)
        alltemp.append(temp)
alldate=[x for xs in alldate for x in xs]
alltemp=[x for xs in alltemp for x in xs]  

for i in datelist:
    i=str(i)
    for line in alldate:
        if(i in line):
            id=alldate.index(line)
            if i not in AT:
                AT[i] = []
            AT[i].append(alltemp[id])   
list_AT=[]       
for year in AT:
     if(np.size(AT[year])<366):
        continue
     else:
        temp= AT[year]
        temp=np.array(temp[0:366])
        list_AT.append(temp)
        
averageAT= np.mean(list_AT, axis=0)-273
table=np.stack((time, averageAT), axis=-1)

plt.figure(figsize=(16,20))
plt.subplot(4,1,1)
plt.scatter(table[:,0],table[:,1], s=1, label='Air temperature data')

res = fit_sin(table[:,0],table[:,1])
#ATfit_lt=res["fitfunc"](tt)
ATfit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
plt.plot(table[:,0], ATfit , label="Fit Air Temperature", linewidth=2)


########################### SOIL TEMPERATURE##########################

os.chdir(r'R:\GitHub\Data_phD\Data\Climate_Data\Paisley\Soil_Temp_CEDA')
ST= {}
ST2= {}
with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=85)
        year=data['ob_time']
        temperature=data['q30cm_soil_temp'] 
        temperature2=data['q100cm_soil_temp']
        ST[year[0]]=temperature[0:366]
        ST2[year[0]]=temperature2[0:366]

list_ST=[]
list_ST2=[]
for i in datelist:
    i=str(i)
    for year in ST:
        if i in year:
            temp= ST[year]
            temp=np.array(temp)
            list_ST.append(temp)
            temp2= ST2[year]
            temp2=np.array(temp2)
            list_ST2.append(temp2)
            
#soil temperature at 100 cm
averageST2= np.nanmean(list_ST2, axis=0)
table=np.stack((time, averageST2), axis=-1)
plt.scatter(table[:,0],table[:,1], c="r", s=1, label="Soil temperature data 100 cm")

res = fit_sin(table[:,0],table[:,1])
#STfit_lt=res["fitfunc"](tt)
STfit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
plt.plot(table[:,0], STfit , "r-", label="Fit Soil Temperature 100 cm", linewidth=2) 

#soil temperature at 30 cm
averageST= np.nanmean(list_ST, axis=0)
table=np.stack((time, averageST), axis=-1)
plt.scatter(table[:,0],table[:,1], c="k", s=1, label="Soil temperature data 30 cm")

res = fit_sin(table[:,0],table[:,1])
#STfit_lt=res["fitfunc"](tt)
STfit=res["fitfunc"](table[:,0])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
plt.plot(table[:,0], STfit , "k-", label="Fit Soil Temperature 30 cm", linewidth=2) 

plt.title('Paisley station')
plt.ylabel('°C')
plt.legend(loc="best")

########################### WINDSPEED ##########################


os.chdir(r'R:\GitHub\Data_phD\Data\Climate_Data\Paisley\Windspeed')
WS= {}
alldate=[]
allwind=[]
with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=6)
        year=data['DATES']
        wind=data['Near-Surface Wind Speed (m s-1)']
        date=np.array(year)
        windspeed=np.array(wind)
        alldate.append(date)
        allwind.append(windspeed)
alldate=[x for xs in alldate for x in xs]
allwind=[x for xs in allwind for x in xs]  

for i in datelist:
    i=str(i)
    for line in alldate:
        if(i in line):
            id=alldate.index(line)
            if i not in WS:
                WS[i] = []
            WS[i].append(allwind[id])   
list_WS=[]       
for year in WS:
     if(np.size(WS[year])<366):
        continue
     else:
        windspeed= WS[year]
        windspeed=np.array(windspeed[0:366])
        list_WS.append(windspeed)        
        
averageWS= np.mean(list_WS, axis=0)
table=np.stack((time, averageWS), axis=-1)

plt.subplot(4,1,2)
plt.scatter(table[:,0],table[:,1], c="r", s=1, label='Wind speed data')       
        
res = fit_sin(table[:,0],table[:,1])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
WSfit_lt= res["fitfunc"](tt)
WSfit= res["fitfunc"](table[:,0])
plt.plot(table[:,0],WSfit, "r-", label="Fit Wind Speed", linewidth=2)
plt.ylabel('m/s')
plt.legend(loc="best")

########################### SHORTWAVE (solar radiations) ##########################
 
albedo=0

os.chdir(r'R:\GitHub\Data_phD\Data\Climate_Data\Paisley\Shortwave')
SW= {}
alldate=[]
allSW=[]
with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=6)
        year=data['DATES']
        shWave=data['Surface Downwelling Shortwave Radiation (W m-2)']
        date=np.array(year)
        shortwave=np.array(shWave)
        alldate.append(date)
        allSW.append(shortwave)
alldate=[x for xs in alldate for x in xs]
allSW=[x for xs in allSW for x in xs]  

for i in datelist:
    i=str(i)
    for line in alldate:
        if(i in line):
            id=alldate.index(line)
            if i not in SW:
                SW[i] = []
            SW[i].append(allSW[id])   
list_SW=[]       
for year in SW:
     if(np.size(SW[year])<366):
        continue
     else:
        shortwave= SW[year]
        shortwave=np.array(shortwave[0:366])
        list_SW.append(shortwave)  
        
#absorbed radiations:        
averageSW= (1-albedo)*np.mean(list_SW, axis=0)
table=np.stack((time, averageSW), axis=-1)

plt.subplot(4,1,3)
plt.scatter(table[:,0],table[:,1], s=1, c="g", label='shortwave data')       
     
res = fit_sin(table[:,0],table[:,1])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
SWfit_lt= res["fitfunc"](tt)
SWfit= res["fitfunc"](table[:,0])
plt.plot(table[:,0],SWfit, "g-", label="Fit shortwave", linewidth=2)

########################### LONGWAVE ##########################

os.chdir(r'R:\GitHub\Data_phD\Data\Climate_Data\Paisley\Longwave')
LW= {}
alldate=[]
allLW=[]
with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=6)
        year=data['DATES']
        lgWave=data['Surface Downwelling Longwave Radiation (W m-2)']
        date=np.array(year)
        longwave=np.array(lgWave)
        alldate.append(date)
        allLW.append(longwave)
alldate=[x for xs in alldate for x in xs]
allLW=[x for xs in allLW for x in xs]  

for i in datelist:
    i=str(i)
    for line in alldate:
        if(i in line):
            id=alldate.index(line)
            if i not in LW:
                LW[i] = []
            LW[i].append(allLW[id])   
list_LW=[]       
for year in LW:
     if(np.size(LW[year])<366):
        continue
     else:
        longwave= LW[year]
        longwave=np.array(longwave[0:366])
        list_LW.append(longwave)        
        
averageLW= np.mean(list_LW, axis=0)
table=np.stack((time, averageLW), axis=-1)

plt.scatter(table[:,0],table[:,1], s=1, c="b", label='longwave data')       
     
res = fit_sin(table[:,0],table[:,1])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
LWfit_lt= res["fitfunc"](tt)
LWfit= res["fitfunc"](table[:,0])
plt.plot(table[:,0],LWfit, "b-", label="Fit longwave", linewidth=2)

########################## Longwave Radiation from Earth ##################

a=17.3          # Qin et al., 2013 (q_irr)
b=237.7
c=5.67*10**(-8) # Stefan-Boltzmann constant
e=0.9           # ground surface emissivity
RH= 80 

#gamma=(a*ATfit)/(b+ATfit)+ln(RH/100) # Qin et al., 2013 (q_irr)
#Tdp=(b*gamma)/(a-gamma)
#Esky=0.754+0.0044*Tdp
#Tsky=Esky*ATfit
#LWEarth0=c*e*((Tsky+273.15)**4-(STfit+273.15)**4) 

Td= np.mean(ATfit) - ((100 - RH)/5) 
Tsky = (ATfit+273.15)*(0.711+0.0056*Td+0.000073*Td**2)**(1/4)  # Gwadera et al (2017)
TLWm=0.5*((STfit+273.15)+Tsky)
LWEarth=4*c*TLWm**3*((STfit+273)-Tsky)
#LWEarth=c*((STfit+273)**4-Tsky**4)
#LWEarth=e*c*((STfit+273)**4-Tsky*4)                           # Larwa, 2018 
#LWEarth=e*4.83*((STfit+273)-Tsky) 

plt.plot(table[:,0],LWEarth, label='Average Longwave from Earth') 
plt.legend(loc="best")


############################## Convective Flux #######################

hu=[]
for u in WSfit:
    if u < 4.88:
        h=5.7+3.8*u
    else:
        h=7.2*u**0.78
    hu.append(h)
       
H=hu*(ATfit-STfit)
plt.plot(table[:,0],H, label='Convective flux')  
plt.ylabel('W/m2')
plt.legend(loc="best")


######################### conductive heat flux ##########################
os.chdir(r'R:\GitHub\Data_phD\Data\Climate_Data\Paisley')

plt.subplot(4,1,4)
qcond=H+SWfit-LWEarth      #qconv+qabs+qirr in Qin et al., 2013
plt.plot(table[:,0],qcond, label='Conductive heat flux')
plt.legend(loc="best")
plt.xlabel('Time (s)')
plt.ylabel('W/m2')
plt.grid(True, which='both')
#plt.savefig('Paisley_meteo.png') 

#######"" create AT and qcond output file for 30 years simulation ###########

AT_sim=[]
for i in range(30):
     AT_sim.append(ATfit)
AT_sim=[x for xs in AT_sim for x in xs]
Curve_AT=np.stack((tt, AT_sim), axis=-1)

qcond_sim=[]
for i in range(30):
     qcond_sim.append(qcond)
qcond_sim=[x for xs in qcond_sim for x in xs]
Curve_qcond=np.stack((tt, qcond_sim), axis=-1)

plt.figure(figsize=(16,5))
#plt.plot(tt, AT_sim, label="AT stack")
#plt.plot(tt, ATfit_lt, label="lt interpolation")

def moving_average(y, K=5):
    """
    2K+1 point moving average of array y
    """
    N = np.size(y)      # find the size of y
    s = np.zeros(N)     # make an array of zeros with the same size
    for n in range(N):  # loop for the moving average
        kmin = max(n-K, 0)    # limit to indices within the array
        kmax = min(n+K+1, N)  # i.e. range 0 to N-1
        s[n] = np.mean(y[kmin:kmax])
    return s            # return the smoothed array

# plot smoothed temperatures
AT_smooth = moving_average(AT_sim, K=30)
plt.plot(tt, AT_smooth, color='black', lw=1)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.legend(loc='best')

plt.twinx()
plt.plot(Curve_qcond[:,0],Curve_qcond[:,1],c='r')
plt.ylim(-150,150)
plt.ylabel('Flux (W/m²)',color='r')

#plt.savefig('Paisley_inputs.png') 
#np.savetxt('Curve_AT_Paisley.txt', Curve_AT)
#np.savetxt('Curve_qcond_Paisley.txt', Curve_qcond)



########################################################################
########### Effective surface temperature Singh and Sharma 2017 T########
########################################################################

os.chdir(r'C:\Users\s1995204\Documents_LOCAL\Modeling')
c=5.67*10**(-8)  # Stefan-Boltzmann constant
e=0.9            # ground surface emissivity
absorp=0.5
hr=4*e*c*ATfit**3
hc=2.8+3*WSfit
Tsky=ATfit-12
h=hr+hc
S=SWfit
DR=c*((ATfit+273.15)**4-(Tsky+273.15)**4)

#calculate effetcive air temperature
Te=ATfit+absorp*S/h-e*DR/h
meanSoilTemp=np.mean(STfit)
meanTe=np.mean(Te)

# calculate ground temperature
Tg0=[]
Dy=2
k=3.14
for i in np.arange(366):
    temp=(STfit[i]+(h[i]*Dy/k)*Te[i])/(1+(h[i]*Dy/k))
    Tg0.append(temp)

# plot Teff
plt.figure(figsize=(16,10))
plt.subplot(2,1,1)
plt.plot(table[:,0], STfit , "k-", label="Fit Soil Temperature 30 cm", linewidth=2) 
plt.plot(table[:,0], Te, color='blue', label="Effective temperature", linewidth=2)
plt.plot(table[:,0], Tg0, color='r', label="Calculated ground temperature", linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.legend(loc='best')


#plot flux
plt.subplot(2,1,2)
qsurf= 1.2 *(Tg0-STfit)/0.3 # Soil conductivity and temperature at 30 cm              #v3 (deleted)
averageq = np.mean(qsurf)
minq= np.min(qsurf) 
maxq= np.max(qsurf) 

plt.plot(table[:,0], qsurf , "k-", linewidth=2) 
plt.xlabel('Time (s)')
plt.ylabel('Flux (W/m2)')
#plt.savefig('Surface_Temperature.png') 

###################### R:\Modeling\2D_Models\M1 ######################
dt_d = 1 
dt_s=3600*24 # 1 day
t_y= 1000 # year
t_d=dt_d*365.25*t_y
t_s=dt_s*365.25*t_y

time = np.arange(0, t_d, dt_d)
time_s= np.arange(0, t_s, dt_s)
#surflux = 4*np.cos(2*np.pi*(time/t_d*t_y)+1.571) -0.026                                #BEMCHMARK        
surflux = 4*np.cos(2*np.pi*(time/t_d*t_y)+1.5708) -0.068                                #M1    

plt.figure(figsize=(16,5))
plt.plot(time, surflux)
plt.title('Average daily surface flux for 30 years')
plt.xlabel('Time (days)')
plt.ylabel('Amplitude = flux')
plt.grid(True, which='both')
plt.axhline(y=0, color='k')

#plt.savefig('q_surface_4.png') 

qsurfaceinput=np.stack((time_s, surflux), axis=-1)

#np.savetxt('qsurf_4.txt', qsurfaceinput)

########################### SHORTWAVE (solar radiations) ##########################
 
os.chdir(r'R:\GitHub\Data_phD\Data\Climate_Data\Paisley\RelativeHumidity')
RH= {}
alldate=[]
allRH=[]
with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=6)
        year=data['DATES']
        srh=data['Near-Surface Specific Humidity (kg kg-1)']
        date=np.array(year)
        relhumidity=np.array(srh)
        alldate.append(date)
        allRH.append(relhumidity)
alldate=[x for xs in alldate for x in xs]
allRH=[x for xs in allRH for x in xs]  

for i in datelist:
    i=str(i)
    for line in alldate:
        if(i in line):
            id=alldate.index(line)
            if i not in RH:
                RH[i] = []
            RH[i].append(allRH[id])   
list_RH=[]       
for year in RH:
     if(np.size(RH[year])<366):
        continue
     else:
        relhumidity= RH[year]
        relhumidity=np.array(relhumidity[0:366])
        list_RH.append(relhumidity)  
      
averageRH= np.mean(list_RH, axis=0)
table=np.stack((time, averageRH), axis=-1)


plt.figure(figsize=(16,5))
plt.scatter(table[:,0],table[:,1], s=1, c="g", label='relative humidity data')       
     
res = fit_sin(table[:,0],table[:,1])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
RHfit_lt= res["fitfunc"](tt)
RHfit= res["fitfunc"](table[:,0])
plt.plot(table[:,0],RHfit, "g-", label="Fit relative humidity", linewidth=2)

plt.title('Average daily relative humidity')
plt.xlabel('Time (days)')
plt.ylabel('Relative humidity')
plt.grid(True, which='both')
plt.axhline(y=0, color='k')



########################################################################
########### sALAHsAADIeTaL 2017 T########
########################################################################
f=0.7
alb=0.1
sigma=5.67e-8
HTC = 0.5+1.2*WSfit**(0.5)
CE = HTC * (ATfit - STfit) #Convective energy
LR = e  * sigma * ((STfit+273)**4  - (ATfit+273)**4)# longwave radiation emitted from the ground, T in Kelvin
SR = (1 - alb) * SWfit #absorbed solar radiations
LE = 0.0168*f* HTC*(103*STfit+609-RHfit*(103*ATfit+609))# latent heat due to evaporation

q = CE - LR + DR - LE
plt.figure(figsize=(16,5))
plt.scatter(table[:,0],q)    
plt.title('surface heat flux')
plt.xlabel('Time (days)')
plt.ylabel('Relative humidity')
plt.grid(True, which='both')
plt.axhline(y=0, color='k')

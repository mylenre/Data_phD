# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 00:39:31 2019

@author: mylen
"""
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

    def sinfunc(t, A, w, p, c):  return A * numpy.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*numpy.pi)
    fitfunc = lambda t: A * numpy.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#datelist=np.arange(2000,2011,1)
datelist=np.arange(2000,2001,1)

########################### EVAPOTRANSPIRATION ##########################


os.chdir(r'D:\mylen\Documents\phD\Data_phD\Data\Paisley\Evapotranspiration')
EV= {}
alldate=[]
allEV=[]
with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        line = line[:-1]
        data = pd.read_csv(line, delimiter=',', header=6)
        year=data['DATES']
        evap=data['Potential evapotranspiration with interception correction (mm/day)']
        date=np.array(year)
        evapotranspiration=np.array(evap)
        alldate.append(date)
        allEV.append(evapotranspiration)
alldate2=[x for xs in alldate for x in xs]
allEV2=[x for xs in allEV for x in xs]

for i in datelist:
    i=str(i)
    for line in alldate:
        if(i in line):
            id=alldate.index(line)
            if i not in EV:
                EV[i] = []
            EV[i].append(allEV[id])   
list_EV=[]       
for year in EV:
     if(np.size(EV[year])<366):
        continue
     else:
        evapotranspiration= EV[year]
        evapotranspiration=np.array(evapotranspiration[0:366])
        list_EV.append(evapotranspiration)        

averageEV= np.mean(list_EV, axis=0)
table=np.stack((time, averageEV), axis=-1)

plt.figure(figsize=(16,4))
plt.scatter(table[:,0],table[:,1], s=1, label='evapotranspiration data')       

res = fit_sin(table[:,0],table[:,1])
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )
EVfit= res["fitfunc"](table[:,0])
plt.plot(table[:,0],EVfit, label="Fit evapotranspiration", linewidth=2)
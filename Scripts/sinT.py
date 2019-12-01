# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 01:12:49 2019

@author: mylen
"""

import numpy as np
import matplotlib.pyplot as plt

dt_d=1
dt_s=3600*24

t_y=30
t_d=dt_d*365.25*t_y
t_s=dt_s*365.25*t_y

qmax=0.1
ref=0.11
#name=ref=qmax-1/2*qmax


time = np.arange(0, t_d, dt_d)
time_s= np.arange(0, t_s, dt_s)
amplitude   = ref-qmax*np.cos(2*np.pi*(time/t_d*t_y))

plt.plot(time, amplitude)
plt.title('Sine wave')
plt.xlabel('Time (days)')
plt.ylabel('Amplitude = flux')
plt.grid(True, which='both')
plt.axhline(y=0, color='k')
plt.show()

data=np.stack((time_s, amplitude), axis=-1)
np.savetxt('sinT_'+str(ref)+'_'+str(qmax)+'.txt', data)

